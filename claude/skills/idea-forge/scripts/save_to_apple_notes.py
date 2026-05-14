#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


APPLESCRIPT = r'''
on run argv
    set folderName to item 1 of argv
    set noteTitle to item 2 of argv
    set bodyFilePath to POSIX file (item 3 of argv)
    set accountName to ""
    if (count of argv) is greater than 3 then
        set accountName to item 4 of argv
    end if

    set noteBody to read bodyFilePath as «class utf8»
    set htmlBody to my markdownToHtml(noteTitle, noteBody)

    tell application "Notes"
        set targetAccount to my resolveAccount(accountName)
        set targetFolder to my resolveFolder(targetAccount, folderName)
        make new note at targetFolder with properties {body:htmlBody}
    end tell
end run

on resolveAccount(accountName)
    tell application "Notes"
        if accountName is not "" then
            repeat with currentAccount in accounts
                if (name of currentAccount as text) is accountName then
                    return currentAccount
                end if
            end repeat
            error "Apple Notes account not found: " & accountName
        end if

        if (count of accounts) is 0 then
            error "No Apple Notes accounts are available."
        end if

        return first account
    end tell
end resolveAccount

on resolveFolder(targetAccount, folderName)
    tell application "Notes"
        repeat with existingFolder in folders of targetAccount
            if (name of existingFolder as text) is folderName then
                return existingFolder
            end if
        end repeat

        return make new folder at targetAccount with properties {name:folderName}
    end tell
end resolveFolder

on markdownToHtml(noteTitle, noteBody)
    set escapedTitle to my escapeHtml(noteTitle)
    set escapedBody to my escapeHtml(noteBody)
    set normalizedBody to my replaceText(linefeed, "<br>", escapedBody)
    return "<h1>" & escapedTitle & "</h1><div>" & normalizedBody & "</div>"
end markdownToHtml

on escapeHtml(inputText)
    set outputText to my replaceText("&", "&amp;", inputText)
    set outputText to my replaceText("<", "&lt;", outputText)
    set outputText to my replaceText(">", "&gt;", outputText)
    return outputText
end escapeHtml

on replaceText(findText, replaceText, sourceText)
    set AppleScript's text item delimiters to findText
    set textItems to every text item of sourceText
    set AppleScript's text item delimiters to replaceText
    set newText to textItems as text
    set AppleScript's text item delimiters to ""
    return newText
end replaceText
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save IdeaForge output to Apple Notes on macOS.")
    parser.add_argument("--folder", default="Ideas", help="Target Apple Notes folder name.")
    parser.add_argument("--title", required=True, help="Note title.")
    parser.add_argument("--body-file", required=True, help="Path to a UTF-8 text file containing the note body.")
    parser.add_argument("--account", help="Optional Apple Notes account name, such as iCloud.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if sys.platform != "darwin":
        print("Apple Notes save only works on macOS.", file=sys.stderr)
        return 1

    body_path = Path(args.body_file).expanduser().resolve()
    if not body_path.exists():
        print(f"Body file not found: {body_path}", file=sys.stderr)
        return 1

    with tempfile.NamedTemporaryFile("w", suffix=".applescript", delete=False, encoding="utf-8") as handle:
        handle.write(APPLESCRIPT)
        script_path = Path(handle.name)

    command = ["osascript", str(script_path), args.folder, args.title, str(body_path)]
    if args.account:
        command.append(args.account)

    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        if exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        return exc.returncode
    finally:
        script_path.unlink(missing_ok=True)

    if completed.stdout.strip():
        print(completed.stdout.strip())

    print(f"Saved note '{args.title}' to Apple Notes folder '{args.folder}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

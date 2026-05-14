#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save IdeaForge output to an Obsidian vault folder.")
    parser.add_argument("--vault-path", required=True, help="Path to the Obsidian vault root.")
    parser.add_argument("--folder", default="Ideas", help="Target folder inside the vault.")
    parser.add_argument("--title", required=True, help="Note title.")
    parser.add_argument("--body-file", required=True, help="Path to a UTF-8 text file containing the note body.")
    return parser.parse_args()


def slugify_file_name(title: str) -> str:
    safe = re.sub(r'[<>:"/\\\\|?*]+', "", title).strip()
    return safe or "IdeaForge Note"


def main() -> int:
    args = parse_args()

    vault_root = Path(args.vault_path).expanduser().resolve()
    if not vault_root.exists():
        raise SystemExit(f"Vault path not found: {vault_root}")

    body_path = Path(args.body_file).expanduser().resolve()
    if not body_path.exists():
        raise SystemExit(f"Body file not found: {body_path}")

    note_body = body_path.read_text(encoding="utf-8")
    target_folder = vault_root / args.folder
    target_folder.mkdir(parents=True, exist_ok=True)

    note_path = target_folder / f"{slugify_file_name(args.title)}.md"
    note_path.write_text(f"# {args.title}\n\n{note_body.rstrip()}\n", encoding="utf-8")

    print(f"Saved note to {note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

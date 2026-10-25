import argparse
from pathlib import Path
import re
import sys


def validate(text, max_words=1200, max_draft_words=300):
    if max_words < 1 or max_draft_words < 1:
        raise ValueError('Word limits must be positive')
    headings = list(re.finditer(r'^## (\d+)\. [^\r\n]+', text, re.MULTILINE))
    if [int(match[1]) for match in headings] != list(range(1, 15)):
        raise ValueError('Include sections 1 through 14 exactly once, in order')
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        if not text[heading.end():end].strip():
            raise ValueError(f'Section {heading[1]} has no content')
    total = len(text.split())
    draft = len(text[headings[9].start():headings[10].start()].split())
    if total > max_words or draft > max_draft_words:
        raise ValueError(f'Word limits exceeded: package {total}/{max_words}; section 10 {draft}/{max_draft_words}')
    return total, draft


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package', type=Path)
    parser.add_argument('--max-words', type=int, default=1200)
    parser.add_argument('--max-draft-words', type=int, default=300)
    args = parser.parse_args()
    try:
        total, draft = validate(args.package.read_text(encoding='utf-8'), args.max_words, args.max_draft_words)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(f'Package {total} words; section 10 {draft} words; sections 1 through 14 populated')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

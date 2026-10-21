import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys


def minutes(value):
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError):
        raise ValueError('Duration must be a literal number of minutes') from None
    if not result.is_finite() or result < 0:
        raise ValueError('Duration must be finite and nonnegative')
    return result


def validate(data, logged_total_minutes=None):
    if not data.startswith((b'---\n', b'---\r\n')):
        raise ValueError('Frontmatter delimiter must start at byte zero, without BOM, blank line or fence')
    lines = data.decode('utf-8').splitlines()
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise ValueError('Closing frontmatter delimiter is missing') from None
    if not any(line.strip() for line in lines[end + 1:]):
        raise ValueError('Workout note body is missing')
    fields = {}
    for line in lines[1:end]:
        match = re.match(r'^(type|duration):\s*(.*?)\s*$', line)
        if match:
            if match[1] in fields:
                raise ValueError(f'Duplicate {match[1]} property')
            fields[match[1]] = match[2]
    kind = fields.get('type', '').strip('\'"')
    if kind not in ('strength', 'ride', 'run', 'combined'):
        raise ValueError('Use a literal strength, ride, run or combined type property')
    if 'duration' in fields:
        duration = minutes(fields['duration'])
        if kind == 'combined':
            if logged_total_minutes is None:
                raise ValueError('Combined duration requires an explicitly logged whole-session total; keep partial durations per activity')
            if duration != minutes(logged_total_minutes):
                raise ValueError('Combined duration differs from the supplied whole-session total')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('note', type=Path)
    parser.add_argument('--logged-total-minutes')
    args = parser.parse_args()
    try:
        validate(args.note.read_bytes(), args.logged_total_minutes)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(f'Validated frontmatter boundary and duration scope: {args.note.name}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

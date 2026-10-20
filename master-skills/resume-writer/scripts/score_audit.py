import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'Positioning and Narrative': 'positioning_and_narrative',
    'Evidence and Bullet Strength': 'evidence_and_bullet_strength',
    'ATS and Structural Reliability': 'ats_and_structural_reliability',
    'Relevance and Targeting': 'relevance_and_targeting',
    'Professionalism and Trust': 'professionalism_and_trust',
}
PROFILES = {'generic': (25, 35, 20, 10, 10), 'targeted': (25, 30, 20, 15, 10)}
VERDICTS = ('High risk', 'Weak', 'Good but inconsistent', 'Strong', 'Excellent')


def number(value):
    if type(value) not in (int, float, Decimal):
        raise ValueError('Scores and weights must be numbers')
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError('Scores and weights must be finite')
    return result


def rounded(value):
    return value.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)


def sources(root):
    library = set(re.findall(r'^## (.+)$', (root / 'insights/principles.md').read_text(encoding='utf-8'), re.M))
    patterns = set(re.findall(r'^#{2,3} (.+)$', (root / 'references/common-patterns.md').read_text(encoding='utf-8'), re.M))
    mapping = {}
    for line in (root / 'scoring-model.md').read_text(encoding='utf-8').splitlines():
        cells = [part.strip() for part in line.strip().strip('|').split('|')]
        if len(cells) == 4 and cells[0] in library and cells[1] in CATEGORIES:
            mapping[cells[0]] = (cells[1], Decimal(cells[2]))
    return mapping, patterns


def calculate(audit, root=ROOT):
    if not isinstance(audit, dict) or audit.get('review_context') not in PROFILES:
        raise ValueError('review_context must be generic or targeted')
    entries = audit.get('principle_scores')
    if not isinstance(entries, list) or not entries:
        raise ValueError('A complete principle_scores ledger is required')
    library, patterns = sources(root)
    groups = {category: [] for category in CATEGORIES}
    counts = dict.fromkeys(('CRITICAL', 'MAJOR', 'MINOR', 'INFO'), 0)
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Each ledger entry must be an object')
        name, kind, category = (entry.get(key) for key in ('source_name', 'source_type', 'category'))
        if not isinstance(name, str) or not isinstance(category, str) or category not in groups:
            raise ValueError('Each entry needs a valid source_name and category')
        if kind not in ('library_principle', 'common_pattern'):
            raise ValueError('source_type must be library_principle or common_pattern')
        if (kind, name) in seen:
            raise ValueError('Score each source once; group its findings in one entry')
        seen.add((kind, name))
        weight = number(entry.get('weight'))
        if kind == 'library_principle':
            if name not in library or entry.get('principle') != name:
                raise ValueError(f'Not an authoritative library principle: {name}')
            if (category, weight) != library[name]:
                raise ValueError(f'Wrong category or weight for library principle: {name}')
        elif kind == 'common_pattern':
            if not name.startswith('common-patterns § ') or name.removeprefix('common-patterns § ') not in patterns:
                raise ValueError(f'Not a supplied common-pattern heading: {name}')
            if weight != 1:
                raise ValueError('Common patterns use weight 1.0')
        score = entry.get('score')
        if type(score) is not int or score not in range(4):
            raise ValueError('Principle scores must be integers from 0 through 3')
        severity = entry.get('severity')
        if severity not in counts:
            raise ValueError('Unknown severity')
        counts[severity] += 1
        groups[category].append((Decimal(score), weight))
    if any(not entries for entries in groups.values()):
        raise ValueError('Include supported scoring evidence for all five categories before reporting a total')
    categories = {CATEGORIES[name]: rounded(sum(score / 3 * weight for score, weight in items) / sum(weight for _, weight in items) * 100) for name, items in groups.items()}
    final = rounded(sum(value * Decimal(weight) / 100 for value, weight in zip(categories.values(), PROFILES[audit['review_context']])))
    rank = 4 if final >= 90 else 3 if final >= 80 else 2 if final >= 70 else 1 if final >= 60 else 0
    critical = counts['CRITICAL']
    cap = 1 if critical >= 3 else 2 if critical == 2 else 3 if critical == 1 else 4
    if audit.get('confidence') == 'low':
        cap = min(cap, 3)
    result = dict(audit)
    result.update(category_scores={name: float(value) for name, value in categories.items()}, final_score=float(final), verdict=VERDICTS[min(rank, cap)], critical_issue_count=critical, major_issue_count=counts['MAJOR'], minor_issue_count=counts['MINOR'])
    return result


def reject_constant(value):
    raise ValueError(f'Invalid JSON number: {value}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audit', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        audit = json.loads(args.audit.read_text(encoding='utf-8-sig'), parse_constant=reject_constant)
        result = calculate(audit)
        if args.check:
            for key in ('final_score', 'critical_issue_count', 'major_issue_count', 'minor_issue_count'):
                number(audit.get(key))
            if not isinstance(audit.get('category_scores'), dict):
                raise ValueError('category_scores must be an object')
            for value in audit['category_scores'].values():
                number(value)
            for key in ('category_scores', 'final_score', 'verdict', 'critical_issue_count', 'major_issue_count', 'minor_issue_count'):
                if audit.get(key) != result[key]:
                    raise ValueError(f'Reported {key} does not match the ledger')
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, InvalidOperation, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

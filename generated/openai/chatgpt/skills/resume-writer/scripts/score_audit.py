import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'fixed-evidence-v1'
CATEGORIES = ('Positioning and Narrative', 'Evidence and Bullet Strength', 'ATS and Structural Reliability', 'Relevance and Targeting', 'Professionalism and Trust')
PROFILES = {'generic': (25, 35, 20, 10, 10), 'targeted': (25, 30, 20, 15, 10)}
VERDICTS = ('High risk', 'Weak', 'Good but inconsistent', 'Strong', 'Excellent')
SLOTS = (
    ('positioning', 'Make the target role obvious in the top third', 0, 1.5),
    ('specificity', 'Every bullet must name the thing', 1, 1.5),
    ('measurements', 'Numbers, everywhere, or you get an interview with nobody', 1, 1.5),
    ('structure', 'Standard section headings beat clever branding', 2, 1.25),
    ('chronology', 'Chronology should be easy to follow', 2, 1.25),
    ('alignment', "Mirror the job description's language naturally", 3, 1.5),
    ('privacy', 'No photos, no headshots, no personal data', 4, 1.0),
)
STATES = {
    'positioning': {'role_and_evidence': (3, 'INFO'), 'role_only': (2, 'MINOR'), 'inferred': (1, 'MAJOR'), 'absent': (0, 'CRITICAL')},
    'structure': {'standard': (3, 'INFO'), 'mixed': (2, 'MINOR'), 'unclear': (1, 'MAJOR'), 'unreadable': (0, 'CRITICAL')},
    'chronology': {'clear': (3, 'INFO'), 'coarse': (2, 'MINOR'), 'missing_dates': (1, 'MAJOR'), 'contradictory': (0, 'CRITICAL')},
    'privacy': {'safe': (3, 'INFO'), 'unsafe': (0, 'CRITICAL')},
}


def rounded(value):
    return value.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def items(value, label, boolean_fields):
    if not isinstance(value, list) or not value:
        raise ValueError(f'{label} requires a nonempty inventory; otherwise use qualitative review')
    seen = set()
    for item in value:
        if not isinstance(item, dict) or not nonempty(item.get('text')):
            raise ValueError(f'{label} needs quoted source text for every item')
        key = ' '.join(item['text'].casefold().split())
        if key in seen:
            raise ValueError(f'Duplicate {label} item')
        seen.add(key)
        if any(type(item.get(field)) is not bool for field in boolean_fields):
            raise ValueError(f'{label} observations must be booleans')
        if not nonempty(item.get('evidence')):
            raise ValueError(f'{label} needs evidence or an explicit absence explanation')
    return value


def calculate(audit, root=ROOT):
    if not isinstance(audit, dict) or not isinstance(audit.get('review_context'), str) or audit['review_context'] not in PROFILES:
        raise ValueError('review_context must be generic or targeted')
    if audit.get('rubric_version') != VERSION:
        raise ValueError(f'Numeric audits require rubric_version {VERSION}')
    evidence = audit.get('scoring_evidence')
    if not isinstance(evidence, dict):
        raise ValueError('A complete scoring_evidence inventory is required')
    statements = items(evidence.get('experience_statements'), 'experience_statements', ('names_specific_object', 'has_supplied_measure'))
    requirements = items(evidence.get('requirements'), 'requirements', ('supported',))
    states = {}
    for key, choices in STATES.items():
        observation = evidence.get(key)
        if not isinstance(observation, dict) or not isinstance(observation.get('state'), str) or observation['state'] not in choices or not nonempty(observation.get('evidence')):
            raise ValueError(f'Invalid or unobservable {key}; use qualitative review')
        states[key] = choices[observation['state']]
    specific = sum(item['names_specific_object'] for item in statements)
    measured = sum(item['has_supplied_measure'] for item in statements)
    matched = sum(item['supported'] for item in requirements)
    states['specificity'] = (3, 'INFO') if specific == len(statements) else (1, 'MAJOR') if specific else (0, 'CRITICAL')
    states['measurements'] = (3, 'INFO') if measured == len(statements) else (2, 'MINOR') if measured else (0, 'MAJOR')
    states['alignment'] = (3, 'INFO') if matched == len(requirements) else (1, 'MAJOR') if matched else (0, 'MAJOR')
    library = set(re.findall(r'^## (.+)$', (root / 'insights/principles.md').read_text(encoding='utf-8'), re.M))
    patterns = set(re.findall(r'^#{2,3} (.+)$', (root / 'references/common-patterns.md').read_text(encoding='utf-8'), re.M))
    entries = []
    for criterion, name, category, weight in SLOTS:
        kind = 'library_principle'
        if criterion == 'privacy' or criterion == 'alignment' and audit['review_context'] == 'generic':
            kind = 'common_pattern'
            name = 'Skills keyword dumps' if criterion == 'alignment' else name
            weight = 1.0
        if name not in (library if kind == 'library_principle' else patterns):
            raise ValueError(f'Authoritative source heading missing: {name}')
        score, severity = states[criterion]
        if criterion in STATES:
            reason = evidence[criterion]['evidence']
        elif criterion == 'alignment':
            reason = f'{matched}/{len(requirements)} supplied requirements supported; see scoring_evidence.requirements'
        else:
            numerator = specific if criterion == 'specificity' else measured
            reason = f'{numerator}/{len(statements)} experience statements meet {criterion}; see scoring_evidence.experience_statements'
        entries.append(dict(criterion_id=criterion, principle=name, source_type=kind, source_name=name if kind == 'library_principle' else 'common-patterns § ' + name, category=CATEGORIES[category], score=score, weight=weight, severity=severity, reason=reason, before=None, after=None, fix=None if severity == 'INFO' else f'Review {criterion} using the supplied evidence; request missing facts without invention.'))
    supplied = audit.get('principle_scores')
    if supplied is not None:
        if not isinstance(supplied, list) or len(supplied) != len(entries):
            raise ValueError('Use exactly the seven fixed scoring criteria; no added or omitted principles')
        actual = {entry.get('criterion_id'): entry for entry in supplied if isinstance(entry, dict) and isinstance(entry.get('criterion_id'), str)}
        if len(actual) != len(entries):
            raise ValueError('Score each fixed criterion once')
        for entry in entries:
            prior = actual.get(entry['criterion_id'], {})
            for key in ('principle', 'source_type', 'source_name', 'category', 'weight'):
                if prior.get(key) != entry[key] or key == 'weight' and type(prior.get(key)) not in (int, float):
                    raise ValueError(f'Fixed source/category/weight mismatch for {entry["criterion_id"]}')
    counts = {severity: sum(entry['severity'] == severity for entry in entries) for severity in ('CRITICAL','MAJOR','MINOR')}
    categories = {}
    for category in CATEGORIES:
        group = [entry for entry in entries if entry['category'] == category]
        numerator = sum(Decimal(entry['score']) * Decimal(str(entry['weight'])) for entry in group)
        denominator = 3 * sum(Decimal(str(entry['weight'])) for entry in group)
        categories[category.lower().replace(' ', '_')] = rounded(numerator / denominator * 100)
    final = rounded(sum(value * weight / 100 for value, weight in zip(categories.values(), PROFILES[audit['review_context']])))
    rank = 4 if final >= 90 else 3 if final >= 80 else 2 if final >= 70 else 1 if final >= 60 else 0
    critical = counts['CRITICAL']
    cap = 1 if critical >= 3 else 2 if critical == 2 else 3 if critical == 1 else 4
    if audit.get('confidence') == 'low':
        cap = min(cap, 3)
    result = dict(audit)
    result.update(principle_scores=entries, category_scores={name: float(value) for name, value in categories.items()}, final_score=float(final), verdict=VERDICTS[min(rank, cap)], critical_issue_count=critical, major_issue_count=counts['MAJOR'], minor_issue_count=counts['MINOR'])
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
            if any(type(entry.get('score')) is not int for entry in audit.get('principle_scores', [])):
                raise ValueError('Criterion scores must be integers, not booleans')
            for key in ('principle_scores', 'category_scores', 'final_score', 'verdict', 'critical_issue_count', 'major_issue_count', 'minor_issue_count'):
                if audit.get(key) != result[key]:
                    raise ValueError(f'Reported {key} does not match fixed evidence scoring')
            for key in ('final_score', 'critical_issue_count', 'major_issue_count', 'minor_issue_count'):
                if type(audit.get(key)) not in (int, float):
                    raise ValueError(f'{key} must be numeric, not boolean')
            if any(type(value) not in (int, float) for value in audit['category_scores'].values()):
                raise ValueError('Category scores must be numeric')
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

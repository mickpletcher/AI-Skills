#!/usr/bin/env python3
"""Bounded deterministic fictional fixtures; no network, eval or target execution."""
import argparse
import copy
import csv
import hashlib
import io
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

VERSION = '0.1.0'
MAX_INPUT = 1024 * 1024
MAX_OUTPUT = 20 * 1024 * 1024
IDENT = re.compile(r'[a-z][a-z0-9_]{0,47}\Z')
CASE_ID = re.compile(r'[a-z][a-z0-9-]{0,63}\Z')
EMAIL = re.compile(r'[^\s@]+@[^\s@]+\.[^\s@]+\Z')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}\Z')
EXTRA = {'id': set(), 'text': {'min_length', 'max_length'}, 'email': set(),
         'integer': {'min', 'max'}, 'boolean': set(), 'enum': {'values'},
         'date': {'min', 'max'}, 'ref': {'table', 'field'}}
CATEGORIES = {'normal', 'boundary', 'missing', 'malformed', 'duplicate', 'relationship'}
RULES = {'required', 'null', 'type', 'range', 'length', 'format', 'enum', 'unique', 'reference'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def keys(value, required, optional=()):
    require(isinstance(value, dict), 'Expected an object')
    require(set(required) <= set(value) <= set(required) | set(optional),
            f'Expected keys {sorted(required)} plus {sorted(optional)}; got {sorted(value)}')


def integer(value):
    return type(value) is int


def iso_date(value):
    require(isinstance(value, str) and DATE.fullmatch(value), 'Expected YYYY-MM-DD')
    return date.fromisoformat(value)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':'))


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2) + '\n').encode('utf-8')


def scalar(value):
    return type(value) in (str, int, bool)


def validate_spec(spec):
    keys(spec, {'schema_version', 'seed', 'tables'}, {'cases', 'malformed_json', 'source_evidence'})
    require(type(spec['schema_version']) is int and spec['schema_version'] == 1, 'Unsupported schema_version')
    require(integer(spec['seed']) and -(2**63) <= spec['seed'] < 2**63, 'seed must be a signed 64-bit integer')
    require(type(spec.get('malformed_json', False)) is bool, 'malformed_json must be boolean')
    require(isinstance(spec['tables'], list) and 1 <= len(spec['tables']) <= 50, 'Expected 1–50 tables')
    tables = {}
    total = 0
    for table in spec['tables']:
        keys(table, {'name', 'rows', 'fields'})
        name = table['name']
        require(isinstance(name, str) and IDENT.fullmatch(name) and name not in tables, 'Invalid or duplicate table name')
        require(integer(table['rows']) and 1 <= table['rows'] <= 1000, 'rows must be 1–1000')
        total += table['rows']
        require(total <= 1000, 'At most 1000 total rows')
        require(isinstance(table['fields'], dict) and 1 <= len(table['fields']) <= 50, 'Expected 1–50 fields')
        for field, rule in table['fields'].items():
            require(isinstance(field, str) and IDENT.fullmatch(field), 'Invalid field name')
            require(isinstance(rule, dict) and isinstance(rule.get('type'), str) and rule['type'] in EXTRA, 'Unsupported field type')
            kind = rule['type']
            keys(rule, {'type'}, {'required', 'nullable'} | EXTRA[kind])
            require(all(type(rule[k]) is bool for k in ('required', 'nullable') if k in rule), 'required/nullable must be boolean')
            if kind in ('integer', 'text'):
                lo, hi = (rule.get('min', 0), rule.get('max', 100)) if kind == 'integer' else (rule.get('min_length', 0), rule.get('max_length', 80))
                limit_lo, limit_hi = (-10**12, 10**12) if kind == 'integer' else (0, 1000)
                require(integer(lo) and integer(hi) and limit_lo <= lo <= hi <= limit_hi, 'Invalid bounds')
            elif kind == 'date':
                require(iso_date(rule.get('min', '2000-01-01')) <= iso_date(rule.get('max', '2030-12-31')), 'Invalid date bounds')
            elif kind == 'enum':
                values = rule.get('values')
                require(isinstance(values, list) and 1 <= len(values) <= 100, 'enum needs 1–100 values')
                require(all(scalar(v) and (not isinstance(v, str) or len(v) <= 1000) and (type(v) is not int or abs(v) <= 10**12) for v in values), 'Unsupported enum value')
                require(len({canonical(v) for v in values}) == len(values), 'Duplicate enum values')
            elif kind == 'ref':
                target, target_field = rule.get('table'), rule.get('field')
                require(isinstance(target, str) and isinstance(target_field, str) and target in tables and
                        target_field in tables[target]['fields'] and tables[target]['fields'][target_field]['type'] == 'id',
                        'References need an id field in an earlier table')
        tables[name] = table
    cases = spec.get('cases', [])
    require(isinstance(cases, list) and len(cases) <= 100, 'At most 100 cases')
    ids = {'baseline', 'malformed-json'}
    for case in cases:
        keys(case, {'id', 'category', 'description', 'mutations', 'expected_violations'})
        require(isinstance(case['id'], str) and CASE_ID.fullmatch(case['id']) and case['id'] not in ids, 'Invalid or duplicate case ID')
        ids.add(case['id'])
        require(isinstance(case['category'], str) and case['category'] in CATEGORIES, 'Invalid case category')
        require(isinstance(case['description'], str) and 0 < len(case['description']) <= 1000, 'Case needs a bounded description')
        require(isinstance(case['mutations'], list) and 1 <= len(case['mutations']) <= 100, 'Expected 1–100 mutations')
        for mutation in case['mutations']:
            require(isinstance(mutation, dict) and mutation.get('operation') in ('set', 'omit'), 'Unsupported mutation')
            keys(mutation, {'table', 'row', 'field', 'operation'} | ({'value'} if mutation['operation'] == 'set' else set()))
            check_location(mutation, tables)
        require(isinstance(case['expected_violations'], list), 'expected_violations must be an array')
        for violation in case['expected_violations']:
            keys(violation, {'table', 'row', 'field', 'rule'})
            check_location(violation, tables)
            require(isinstance(violation['rule'], str) and violation['rule'] in RULES, 'Unknown violation rule')
        require(len({canonical(v) for v in case['expected_violations']}) == len(case['expected_violations']), 'Duplicate expected violations')
    evidence = spec.get('source_evidence', [])
    require(isinstance(evidence, list) and len(evidence) <= 100, 'source_evidence must be a bounded array')
    for source in evidence:
        keys(source, {'path', 'sha256', 'revision', 'requirements'})
        require(isinstance(source['path'], str) and 0 < len(source['path']) <= 1000, 'Source needs a descriptive path')
        require(isinstance(source['sha256'], str) and re.fullmatch('[0-9a-f]{64}', source['sha256']), 'Source needs SHA-256')
        require(source['revision'] is None or (isinstance(source['revision'], str) and 0 < len(source['revision']) <= 200), 'Invalid revision')
        require(isinstance(source['requirements'], list) and all(isinstance(v, str) and 0 < len(v) <= 1000 for v in source['requirements']), 'Invalid requirement references')
    # Also rejects non-JSON and non-finite values in programmatic calls.
    require(len(encode(spec)) <= MAX_INPUT, 'Configuration exceeds input limit')
    return tables


def check_location(item, tables):
    name, row, field = item.get('table'), item.get('row'), item.get('field')
    require(isinstance(name, str) and name in tables and integer(row) and 0 <= row < tables[name]['rows'] and
            isinstance(field, str) and field in tables[name]['fields'], 'Mutation/violation location outside schema')


def generate_rows(spec):
    result = {}
    for table in spec['tables']:
        name = table['name']
        rows = []
        for index in range(table['rows']):
            row = {}
            for field, rule in table['fields'].items():
                digest = hashlib.sha256(canonical([spec['seed'], name, index, field]).encode()).hexdigest()
                number = int(digest, 16)
                kind = rule['type']
                if kind == 'id':
                    value = f'synthetic-{name}-{field}-{index + 1:06d}'
                elif kind == 'text':
                    lo, hi = rule.get('min_length', 0), rule.get('max_length', 80)
                    value = ('synthetic-' + digest)[:hi].ljust(lo, 'x')
                elif kind == 'email':
                    value = f'synthetic-{digest[:12]}@example.invalid'
                elif kind == 'integer':
                    lo, hi = rule.get('min', 0), rule.get('max', 100)
                    value = lo + number % (hi - lo + 1)
                elif kind == 'boolean':
                    value = bool(number % 2)
                elif kind == 'enum':
                    value = rule['values'][number % len(rule['values'])]
                elif kind == 'date':
                    lo, hi = iso_date(rule.get('min', '2000-01-01')), iso_date(rule.get('max', '2030-12-31'))
                    value = (lo + timedelta(days=number % ((hi - lo).days + 1))).isoformat()
                else:
                    targets = result[rule['table']]
                    value = targets[number % len(targets)][rule['field']]
                row[field] = value
            rows.append(row)
        result[name] = rows
    return result


def sorted_violations(items):
    return sorted(items, key=lambda v: (v['table'], v['row'], v['field'], v['rule']))


def validate_payload(payload, spec):
    """Return exact rule violations; never equate these with application outcomes."""
    errors = []
    for table in spec['tables']:
        name = table['name']
        for index, row in enumerate(payload[name]):
            for field, rule in table['fields'].items():
                def add(reason):
                    errors.append({'table': name, 'row': index, 'field': field, 'rule': reason})
                if field not in row:
                    if rule.get('required', True):
                        add('required')
                    continue
                value = row[field]
                if value is None:
                    if not rule.get('nullable', False):
                        add('null')
                    continue
                kind = rule['type']
                if kind == 'enum':
                    if not any(type(value) is type(v) for v in rule['values']):
                        add('type')
                    elif not any(type(value) is type(v) and value == v for v in rule['values']):
                        add('enum')
                    continue
                valid_type = integer(value) if kind == 'integer' else type(value) is bool if kind == 'boolean' else isinstance(value, str)
                if not valid_type:
                    add('type')
                    continue
                if kind == 'integer' and not rule.get('min', 0) <= value <= rule.get('max', 100):
                    add('range')
                elif kind == 'text' and not rule.get('min_length', 0) <= len(value) <= rule.get('max_length', 80):
                    add('length')
                elif kind == 'email' and not EMAIL.fullmatch(value):
                    add('format')
                elif kind == 'date':
                    try:
                        actual = iso_date(value)
                    except ValueError:
                        add('format')
                    else:
                        if not iso_date(rule.get('min', '2000-01-01')) <= actual <= iso_date(rule.get('max', '2030-12-31')):
                            add('range')
                elif kind == 'id':
                    if sum(type(other.get(field)) is str and other[field] == value for other in payload[name]) > 1:
                        add('unique')
                elif kind == 'ref':
                    if not any(type(other.get(rule['field'])) is str and other[rule['field']] == value for other in payload[rule['table']]):
                        add('reference')
    return sorted_violations(errors)


def build(spec):
    validate_spec(spec)
    baseline = generate_rows(spec)
    require(not validate_payload(baseline, spec), 'Generated baseline violates contract')
    records = [{'id': 'baseline', 'category': 'normal', 'description': 'Fictional valid baseline',
                'payload': baseline, 'expected_contract_result': 'valid', 'expected_violations': []}]
    running_size = len(encode(spec)) + len(encode(records[0]))
    require(running_size <= MAX_OUTPUT, 'Output exceeds 20 MiB limit; reduce rows/cases')
    for case in spec.get('cases', []):
        payload = copy.deepcopy(baseline)
        for mutation in case['mutations']:
            row = payload[mutation['table']][mutation['row']]
            if mutation['operation'] == 'omit':
                row.pop(mutation['field'], None)
            else:
                row[mutation['field']] = copy.deepcopy(mutation['value'])
        observed = validate_payload(payload, spec)
        require(observed == sorted_violations(case['expected_violations']),
                f"Case {case['id']} expected {sorted_violations(case['expected_violations'])}, observed {observed}")
        record = {'id': case['id'], 'category': case['category'], 'description': case['description'],
                  'payload': payload, 'expected_contract_result': 'invalid' if observed else 'valid',
                  'expected_violations': observed}
        running_size += len(encode(record))
        require(running_size <= MAX_OUTPUT, 'Output exceeds 20 MiB limit; reduce rows/cases')
        records.append(record)
    wire = []
    if spec.get('malformed_json', False):
        raw = '{"synthetic_records": ['
        try:
            json.loads(raw)
        except json.JSONDecodeError:
            wire.append({'id': 'malformed-json', 'format': 'json', 'raw': raw,
                         'expected_contract_result': 'invalid', 'expected_result': 'json_parse_error'})
        else:
            raise ValueError('Malformed JSON fixture unexpectedly parsed')
    bundle = {'synthetic': True, 'generator_version': VERSION,
              'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'configuration_sha256': hashlib.sha256(canonical(spec).encode()).hexdigest(),
              'seed': spec['seed'], 'configuration': spec, 'cases': records, 'wire_cases': wire,
              'oracle_scope': 'Helper data contract only; application outcomes are unspecified.',
              'source_verification': 'Source evidence is supplied metadata; helper does not read or verify target skill files.'}
    require(len(encode(bundle)) <= MAX_OUTPUT, 'Output exceeds 20 MiB limit; reduce rows/cases')
    return bundle


def csv_artifacts(bundle):
    """CSV plus explicit null/missing/type sidecar; refuse executable-looking text."""
    manifest = copy.deepcopy(bundle)
    manifest['format'] = 'csv-with-sidecar-v1'
    manifest['csv_semantics'] = 'UTF-8, comma delimiter, quoted as needed, LF, sorted field-name order; empty cells need sidecar to distinguish missing/null/empty. Not an application import contract.'
    artifacts = {}
    running_size = len(encode(bundle['configuration']))
    for case in manifest['cases']:
        payload = case.pop('payload')
        case['tables'] = {}
        for table in bundle['configuration']['tables']:
            name = table['name']
            fields = sorted(table['fields'])
            text = io.StringIO(newline='')
            writer = csv.writer(text, lineterminator='\n')
            writer.writerow(fields)
            states = []
            expected_rows = []
            for index, row in enumerate(payload[name]):
                cells = []
                for field in fields:
                    value = row.get(field)
                    state = 'missing' if field not in row else 'null' if value is None else type(value).__name__
                    require(value is None or scalar(value) or type(value) is float, 'CSV helper supports scalar cells only; use JSON for nested wrong-type cases')
                    if isinstance(value, str):
                        require(not value.lstrip().startswith(('=', '+', '-', '@')), 'CSV refuses formula-like text; keep adversarial strings in a labeled JSON fixture')
                    cell = '' if value is None else value if isinstance(value, str) else canonical(value)
                    cells.append(cell)
                    states.append({'row': index, 'field': field, 'state': state})
                writer.writerow(cells)
                expected_rows.append(cells)
            contents = text.getvalue()
            require(list(csv.reader(io.StringIO(contents, newline=''))) == [fields] + expected_rows, 'CSV round trip failed')
            filename = f"{case['id']}__{name}.csv"
            running_size += len(contents.encode('utf-8')) + len(encode(states))
            require(running_size <= MAX_OUTPUT, 'CSV output exceeds 20 MiB limit')
            artifacts[filename] = contents.encode('utf-8')
            case['tables'][name] = {'file': filename, 'rows': len(payload[name]), 'fields': fields, 'cell_states': states}
    artifacts['manifest.json'] = encode(manifest)
    require(sum(map(len, artifacts.values())) <= MAX_OUTPUT, 'CSV output exceeds 20 MiB limit')
    return artifacts


def read_spec(path):
    with path.open('rb') as stream:
        raw = stream.read(MAX_INPUT + 1)
    require(len(raw) <= MAX_INPUT, 'Input exceeds 1 MiB limit')
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError(f'Nonstandard JSON constant: {value}')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=reject_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--format', choices=('json', 'csv'), default='json')
    args = parser.parse_args()
    try:
        bundle = build(read_spec(args.spec))
        if args.format == 'json':
            with args.output.open('xb') as stream:
                stream.write(encode(bundle))
        else:
            artifacts = csv_artifacts(bundle)
            args.output.mkdir()  # Refuse existing directories and symlinks.
            for filename, contents in artifacts.items():
                with (args.output / filename).open('xb') as stream:
                    stream.write(contents)
        print(f'Created synthetic {args.format} fixtures: {args.output}')
    except (OSError, ValueError, TypeError, RecursionError) as error:
        parser.exit(2, f'error: {error}\n')


if __name__ == '__main__':
    main()

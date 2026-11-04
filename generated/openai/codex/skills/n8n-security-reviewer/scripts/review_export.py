#!/usr/bin/env python3
"""Bounded, value-free static triage. Never executes n8n or supplied content."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 10 * 1024 * 1024
MAX_DEPTH = 80
MAX_ITEMS = 100000
MAX_NODES = 5000
EMBEDDED_MAX_BYTES = 64 * 1024
EMBEDDED_TOTAL_BYTES = 256 * 1024
EMBEDDED_MAX_DEPTH = 32
EMBEDDED_MAX_VALUES = 4096
EMBEDDED_TOTAL_VALUES = 16384
EMBEDDED_MAX_FIELDS = 128
EMBEDDED_MAX_FINDINGS = 100
EMBEDDED_MAX_COVERAGE = 100
EMBEDDED_FIELDS = ('jsonHeaders', 'jsonBody')
HTTP_TYPES = {'n8n-nodes-base.httpRequest', 'n8n-nodes-base.httpRequestTool'}
AUTH_KEYS = {'authorization', 'proxy-authorization'}
AUTH_SCHEME = re.compile(r'^(?:Bearer|Basic)\s+(.+)$', re.I | re.S)
SECRET_KEY = re.compile(r'^(authorization|proxy-authorization|x-api-key|api[-_]?key|access[-_]?token|refresh[-_]?token|client[-_]?secret|password|secret|token|cookie|apca-api-secret-key)$', re.I)
TOKEN = re.compile(r'(?:\b(?:sk-(?:ant-)?|ghp_|github_pat_)[A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
EXPRESSION = re.compile(r'\{\{|\$\{')
PLACEHOLDERS = {'', '[redacted]', '<redacted>', 'redacted', 'placeholder', 'changeme', 'your-api-key', 'your-token', '***'}
LIMITS = [
    'Static triage only; no workflow or expression was executed and no endpoint was contacted.',
    'Candidates are not validated vulnerabilities. Empty candidates do not mean secure.',
    'No dataflow, authentication effectiveness, published state, secret validity, or credential scopes are verified.',
    'Only documented helper rules are checked; one bounded JSON layer in selected HTTP fields is inspected, not arbitrary encoded secrets or code.',
    'Expressions are never evaluated. Coverage unknowns, truncation, unknown/custom nodes and version schemas require contextual review.',
    'Marker counts may overlap raw and decoded scans; they are not counts of distinct credentials.',
    'Deployment, network controls, runtime defaults, dependencies, access rights, and data retention require separate evidence.',
]


class InputError(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError('Duplicate JSON keys are not supported.')
        result[key] = value
    return result


def reject_constant(_):
    raise InputError('Non-finite JSON numbers are not supported.')


def validate_bounds(data):
    queue = [(data, 0)]
    seen = 0
    while queue:
        value, depth = queue.pop()
        seen += 1
        if seen > MAX_ITEMS or depth > MAX_DEPTH:
            raise InputError('JSON exceeds structural limits.')
        if isinstance(value, float) and not math.isfinite(value):
            raise InputError('Non-finite JSON numbers are not supported.')
        if isinstance(value, dict):
            queue.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, list):
            queue.extend((child, depth + 1) for child in value)


def read_json(path):
    """Use an explicit regular file; reject links and devices before reading."""
    path = Path(path).absolute()
    try:
        for part in (path, *path.parents):
            if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
                raise InputError('Linked input paths are not supported.')
        if not stat.S_ISREG(path.stat().st_mode):
            raise InputError('Input must be a regular file.')
        # NOFOLLOW and descriptor checks reduce common link/special-file races on POSIX.
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise InputError('Input must be a regular JSON file within the size limit.')
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise InputError('Input exceeds the size limit.')
        data = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique_object,
                          parse_constant=reject_constant)
        validate_bounds(data)
        return data, hashlib.sha256(raw).hexdigest()
    except InputError:
        raise
    except (OSError, UnicodeError, ValueError, RecursionError):
        # Never print parser exceptions: they may contain input values or private paths.
        raise InputError('Input could not be read as bounded UTF-8 JSON.') from None


def normalize_workflows(data):
    if isinstance(data, dict) and 'nodes' in data and 'data' in data:
        raise InputError('Ambiguous workflow and data-wrapper fields are not supported.')
    if isinstance(data, dict) and 'nodes' in data:
        workflows = [data]
    elif isinstance(data, list):
        workflows = data
    elif isinstance(data, dict) and isinstance(data.get('data'), list):
        workflows = data['data']
    else:
        raise InputError('Expected a workflow, workflow list, or data-list wrapper.')
    if not workflows:
        raise InputError('No workflows were supplied.')
    count = 0
    for workflow in workflows:
        if not isinstance(workflow, dict) or not isinstance(workflow.get('nodes'), list):
            raise InputError('Every workflow must contain a nodes list.')
        count += len(workflow['nodes'])
        if count > MAX_NODES:
            raise InputError('Too many nodes for bounded triage.')
        for node in workflow['nodes']:
            if not isinstance(node, dict) or not isinstance(node.get('type'), str):
                raise InputError('Every node must have a string type.')
            if 'parameters' in node and not isinstance(node['parameters'], dict):
                raise InputError('Node parameters must be an object.')
        if 'settings' in workflow and not isinstance(workflow['settings'], dict):
            raise InputError('Workflow settings must be an object.')
    return workflows


def literal(value):
    if not isinstance(value, str):
        return False
    clean = value.strip()
    if clean.casefold() in PLACEHOLDERS or EXPRESSION.search(clean):
        return False
    if re.fullmatch(r'<[^<>]+>', clean) or re.fullmatch(r'\*+', clean):
        return False
    return bool(clean)


def secret_markers(parameters):
    """Return counts only: do not leak user-defined keys, values, names or paths."""
    named, tokens = 0, 0
    stack = [parameters]
    while stack:
        obj = stack.pop()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if SECRET_KEY.fullmatch(key) and literal(value):
                    named += 1
                if isinstance(value, (dict, list)):
                    stack.append(value)
                elif isinstance(value, str) and TOKEN.search(value):
                    tokens += 1
            if isinstance(obj.get('name'), str) and SECRET_KEY.fullmatch(obj['name']) and literal(obj.get('value')):
                named += 1
        elif isinstance(obj, list):
            stack.extend(obj)
        elif isinstance(obj, str) and TOKEN.search(obj):
            tokens += 1
    return named, tokens


class EmbeddedInputError(ValueError):
    """A fixed reason code only, never a decoder exception or source excerpt."""


def embedded_secret_value(value, auth=False):
    """Classify literal markers without mistaking references for credentials."""
    if not isinstance(value, str):
        return 'none'
    # Delimiters inside an angle-bracket wrapper still limit coverage. Do not
    # let a placeholder-shaped string hide environment/credential references.
    if EXPRESSION.search(value):
        return 'dynamic'
    clean = value.strip()
    if auth:
        match = AUTH_SCHEME.fullmatch(clean)
        if match:
            clean = match.group(1).strip()
    if clean.casefold() in PLACEHOLDERS or re.fullmatch(r'<[^<>]+>|\*+', clean):
        return 'none'
    return 'literal'


def has_secret_expression(parameters):
    """At most one coverage notice per ordinary parameter scope."""
    stack = [parameters]
    while stack:
        obj = stack.pop()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if (SECRET_KEY.fullmatch(key) and
                        embedded_secret_value(value, key.casefold() in AUTH_KEYS) == 'dynamic'):
                    return True
                if isinstance(value, (dict, list)):
                    stack.append(value)
            name = obj.get('name')
            if (isinstance(name, str) and SECRET_KEY.fullmatch(name) and
                    embedded_secret_value(obj.get('value'), name.casefold() in AUTH_KEYS) == 'dynamic'):
                return True
        elif isinstance(obj, list):
            stack.extend(obj)
    return False


def read_embedded_json(value, budget):
    """Parse data once within per-field and shared limits; never evaluate code."""
    # Bound before allocating a second UTF-8 representation or a decoded tree.
    if len(value) > EMBEDDED_MAX_BYTES:
        raise EmbeddedInputError('field_size_limit')
    try:
        size = len(value.encode('utf-8'))
    except UnicodeError:
        raise EmbeddedInputError('unsupported_unicode') from None
    if size > EMBEDDED_MAX_BYTES:
        raise EmbeddedInputError('field_size_limit')
    if size > budget['bytes']:
        raise EmbeddedInputError('total_parse_budget')
    if budget['values'] <= 0:
        raise EmbeddedInputError('total_value_budget')
    if budget['fields'] <= 0:
        raise EmbeddedInputError('total_field_budget')
    # Failed parses also consume the attempt and byte budgets.
    budget['bytes'] -= size
    budget['fields'] -= 1
    try:
        data = json.loads(value, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, RecursionError):
        raise EmbeddedInputError('not_strict_json') from None
    stack = [(data, 0)]
    seen = 0
    while stack:
        obj, depth = stack.pop()
        seen += 1
        if budget['values'] <= 0:
            raise EmbeddedInputError('total_value_budget')
        budget['values'] -= 1
        if depth > EMBEDDED_MAX_DEPTH or seen > EMBEDDED_MAX_VALUES:
            raise EmbeddedInputError('structure_limit')
        if isinstance(obj, float) and not math.isfinite(obj):
            raise EmbeddedInputError('nonfinite_number')
        try:
            if isinstance(obj, str):
                obj.encode('utf-8')
            elif isinstance(obj, dict):
                for key in obj:
                    key.encode('utf-8')
        except UnicodeError:
            raise EmbeddedInputError('unsupported_unicode') from None
        if isinstance(obj, dict):
            stack.extend((child, depth + 1) for child in obj.values())
        elif isinstance(obj, list):
            stack.extend((child, depth + 1) for child in obj)
    return data


def embedded_markers(data):
    """Return counts; never expose decoded keys, values or secret fingerprints."""
    named, tokens, dynamic = 0, 0, 0
    stack = [data]
    while stack:
        obj = stack.pop()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if SECRET_KEY.fullmatch(key):
                    named += embedded_secret_value(value, key.casefold() in AUTH_KEYS) == 'literal'
                dynamic += bool(EXPRESSION.search(key))
                if isinstance(value, (dict, list)):
                    stack.append(value)
                elif isinstance(value, str):
                    tokens += bool(TOKEN.search(value))
                    dynamic += bool(EXPRESSION.search(value))
            name = obj.get('name')
            if isinstance(name, str) and SECRET_KEY.fullmatch(name):
                named += embedded_secret_value(obj.get('value'), name.casefold() in AUTH_KEYS) == 'literal'
        elif isinstance(obj, list):
            stack.extend(obj)
        elif isinstance(obj, str):
            tokens += bool(TOKEN.search(obj))
            dynamic += bool(EXPRESSION.search(obj))
    return named, tokens, dynamic


def inspect_embedded(workflows):
    """Supplement raw triage with bounded JSON and explicit coverage gaps."""
    budget = {'bytes': EMBEDDED_TOTAL_BYTES, 'values': EMBEDDED_TOTAL_VALUES,
              'fields': EMBEDDED_MAX_FIELDS}
    findings, coverage = [], []
    counts = dict(decoded_fields=0, literal_markers=0, known_token_markers=0,
                  dynamic_scopes=0, unreviewed_scopes=0,
                  suppressed_findings=0, suppressed_coverage=0)

    def record(destination, item):
        limit = EMBEDDED_MAX_FINDINGS if destination is findings else EMBEDDED_MAX_COVERAGE
        if len(destination) < limit:
            destination.append(item)
        else:
            key = 'suppressed_findings' if destination is findings else 'suppressed_coverage'
            counts[key] += 1

    def gap(location, reason):
        counts['unreviewed_scopes'] += 1
        record(coverage, dict(location=location, status='unknown', reason=reason,
                              message='This scope needs contextual review; no expression was evaluated and no secret absence is established.'))

    for wi, workflow in enumerate(workflows):
        for ni, node in enumerate(workflow['nodes']):
            location = f'workflows[{wi}].nodes[{ni}].parameters'
            params = node.get('parameters', {})
            if has_secret_expression(params):
                counts['dynamic_scopes'] += 1
                gap(location, 'expression_like_secret_value')
            if node['type'] not in HTTP_TYPES:
                continue
            for field in EMBEDDED_FIELDS:
                if field not in params:
                    continue
                loc = location + '.' + field  # Only fixed allowlisted names.
                value = params[field]
                if not isinstance(value, str):
                    gap(loc, 'unsupported_field_shape')
                    continue
                stripped = value.lstrip()
                if not stripped:
                    continue
                # These prefixes cannot begin strict JSON. Other strings are
                # parsed first so literal siblings survive expression markers.
                if stripped.startswith(('=', '{{')):
                    counts['dynamic_scopes'] += 1
                    gap(loc, 'unevaluated_expression')
                    continue
                try:
                    decoded = read_embedded_json(value, budget)
                except EmbeddedInputError as exc:
                    reason = str(exc)
                    if reason == 'not_strict_json' and EXPRESSION.search(value):
                        reason = 'unevaluated_expression'
                        counts['dynamic_scopes'] += 1
                    gap(loc, reason)
                    continue
                if field == 'jsonHeaders' and not isinstance(decoded, dict):
                    gap(loc, 'unsupported_header_shape')
                    continue
                counts['decoded_fields'] += 1
                named, tokens, dynamic = embedded_markers(decoded)
                counts['literal_markers'] += named
                counts['known_token_markers'] += tokens
                if named or tokens:
                    priority = 'low' if field == 'jsonBody' and not tokens else 'medium'
                    record(findings, candidate('NSR-EMBEDDED-SECRET', loc,
                                              'Potential secret material in embedded JSON',
                                              'Strict JSON contains secret-named literal fields or known token markers. Values withheld; validity and runtime use untested.',
                                              priority, marker_count=named + tokens,
                                              named_literal_marker_count=named, known_token_marker_count=tokens,
                                              disabled=node.get('disabled') is True, reachability='not analyzed'))
                if dynamic:
                    counts['dynamic_scopes'] += 1
                    gap(loc, 'dynamic_embedded_value')
    truncated = bool(counts['suppressed_findings'] or counts['suppressed_coverage'])
    metadata = {
        'status': 'partial' if counts['unreviewed_scopes'] or truncated else 'completed_within_scope',
        'scope': 'One strict JSON layer in allowlisted HTTP fields; expression-like secret-field coverage notices. Not complete secret detection.',
        'counts': counts,
        'budgets': {'bytes_consumed': EMBEDDED_TOTAL_BYTES - budget['bytes'],
                    'values_consumed': EMBEDDED_TOTAL_VALUES - budget['values'],
                    'fields_consumed': EMBEDDED_MAX_FIELDS - budget['fields']},
        'output_truncated': truncated,
    }
    return findings, coverage, metadata


def candidate(code, location, title, detail, priority='medium', **extra):
    return dict(rule=code, location=location, title=title, classification='conditional risk',
                priority=priority, evidence=detail, **extra)


def inspect_workflows(workflows):
    findings = []
    credential_references = 0
    for wi, workflow in enumerate(workflows):
        prefix = f'workflows[{wi}]'
        if workflow.get('pinData'):
            findings.append(candidate('NSR-PIN', prefix + '.pinData', 'Pinned data is included',
                                      'Non-empty pinned data exists; sensitivity is not determined.', 'low'))
        for field in ('saveDataErrorExecution', 'saveDataSuccessExecution'):
            if workflow.get('settings', {}).get(field) == 'all':
                findings.append(candidate('NSR-LOG', prefix + '.settings.' + field, 'Execution payload saving is explicit',
                                          'Setting explicitly saves all data for this execution category; inspect actual data and access.', 'low'))
        for ni, node in enumerate(workflow['nodes']):
            loc = f'{prefix}.nodes[{ni}]'
            params = node.get('parameters', {})
            kind = node['type']
            common = {'disabled': node.get('disabled') is True, 'reachability': 'not analyzed'}
            if isinstance(node.get('credentials'), dict):
                credential_references += len(node['credentials'])
            named, tokens = secret_markers(params)
            if named or tokens:
                findings.append(candidate('NSR-SECRET', loc + '.parameters', 'Potential inline secret material',
                                          'Secret-named literal fields or known token markers exist; values withheld. Validity is untested.',
                                          'high', marker_count=named + tokens, **common))
            if kind == 'n8n-nodes-base.webhook':
                auth = params.get('authentication')
                if auth == 'none':
                    findings.append(candidate('NSR-AUTH', loc + '.parameters.authentication', 'No built-in webhook authentication selected',
                                              'Explicit none; external controls, intended public use and downstream verification are unverified.', **common))
                elif auth is None:
                    findings.append(dict(candidate('NSR-AUTH-UNKNOWN', loc + '.parameters', 'Webhook authentication is unspecified',
                                                   'Field absent; do not infer a default without matching node-version evidence.', 'low', **common), classification='unknown'))
                else:
                    findings.append(dict(candidate('NSR-AUTH-REVIEW', loc + '.parameters.authentication', 'Authentication configuration needs context',
                                                   'An auth selection exists; supported schema, credential resolution and actual enforcement are not verified.', 'low', **common), classification='unknown'))
            if kind in ('n8n-nodes-base.httpRequest', 'n8n-nodes-base.httpRequestTool'):
                url = params.get('url')
                if isinstance(url, str) and EXPRESSION.search(url):
                    findings.append(candidate('NSR-URL', loc + '.parameters.url', 'Expression controls part of an outbound URL',
                                              'Trace input provenance, destination allowlisting, redirects and egress controls manually.', **common))
                elif isinstance(url, str) and url.lower().startswith('http://'):
                    findings.append(candidate('NSR-HTTP', loc + '.parameters.url', 'Plain HTTP is configured',
                                              'Transport is unencrypted at this hop; endpoint, payload and network context are unverified.', **common))
                if isinstance(url, str) and re.search(r'^[a-z]+://[^/]*@|[?&](?:token|api_key|api-key|access_token|password|secret)=', url, re.I):
                    findings.append(candidate('NSR-URL-SECRET', loc + '.parameters.url', 'URL may carry authentication material',
                                              'Userinfo or a secret-like query parameter exists; values withheld and validity untested.', 'high', **common))
                options = params.get('options', {})
                if isinstance(options, dict) and options.get('allowUnauthorizedCerts') is True:
                    findings.append(candidate('NSR-TLS', loc + '.parameters.options.allowUnauthorizedCerts', 'TLS validation bypass is selected',
                                              'Known HTTP Request option is explicitly true; verify schema compatibility and trust context.', **common))
            if kind in ('n8n-nodes-base.code', 'n8n-nodes-base.function', 'n8n-nodes-base.functionItem',
                        'n8n-nodes-base.executeCommand', 'n8n-nodes-base.readWriteFile',
                        'n8n-nodes-base.readBinaryFile', 'n8n-nodes-base.writeBinaryFile'):
                findings.append(dict(candidate('NSR-CODE', loc, 'Code, command or filesystem boundary needs manual review',
                                               'Node type can process code or files; presence alone is not a vulnerability and code was not executed.', 'low', **common), classification='hardening option'))
    return findings, credential_references


def inspect_config(config):
    if not isinstance(config, dict) or not isinstance(config.get('environment'), dict):
        raise InputError('Config requires an environment object containing redacted configuration evidence.')
    env = config['environment']
    findings = []
    risky = {
        'N8N_RUNNERS_INSECURE_MODE': ('true', 'Runner insecure mode is explicitly selected'),
        'N8N_BLOCK_ENV_ACCESS_IN_NODE': ('false', 'Environment-access block is explicitly disabled'),
        'N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES': ('false', 'n8n file-access protection is explicitly disabled'),
        'N8N_SECURE_COOKIE': ('false', 'Secure-cookie setting is explicitly disabled'),
        'N8N_SSRF_PROTECTION_ENABLED': ('false', 'Application SSRF protection is explicitly disabled'),
        'EXECUTIONS_DATA_PRUNE': ('false', 'Execution pruning is explicitly disabled'),
    }
    for name, (value, title) in risky.items():
        current = env.get(name)
        normalized = str(current).lower() if isinstance(current, (str, bool)) else None
        if normalized == value:
            findings.append(candidate('NSR-CONFIG', 'config.environment.' + name, title,
                                      'Explicit configuration evidence only; installed-version support, effective runtime and compensating controls are unverified.'))
    for name in ('NODE_FUNCTION_ALLOW_BUILTIN', 'NODE_FUNCTION_ALLOW_EXTERNAL', 'N8N_SSRF_ALLOWED_HOSTNAMES'):
        if env.get(name) == '*':
            findings.append(candidate('NSR-WILDCARD', 'config.environment.' + name, 'Broad wildcard permission configured',
                                      'Explicit wildcard; verify version support, necessity, deployed scope and possible narrowing.'))
    return findings


def review(data, config=None):
    validate_bounds(data)
    workflows = normalize_workflows(data)
    findings, credentials = inspect_workflows(workflows)
    embedded_findings, coverage, embedded_review = inspect_embedded(workflows)
    findings.extend(embedded_findings)
    if config is not None:
        validate_bounds(config)
        findings.extend(inspect_config(config))
    return {
        'schema_version': 2,
        'review_kind': 'offline static triage; contextual review required',
        'workflow_count': len(workflows),
        'node_count': sum(len(w['nodes']) for w in workflows),
        'credential_reference_count': credentials,
        'candidates': findings,
        'coverage': coverage,
        'embedded_review': embedded_review,
        'limits': LIMITS,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', help='Existing local JSON export, never a URL')
    parser.add_argument('--config', help='Optional redacted JSON evidence with an environment object')
    args = parser.parse_args(argv)
    try:
        data, sha = read_json(args.workflow)
        config, config_sha = read_json(args.config) if args.config else (None, None)
        if args.config and not isinstance(config, dict):
            raise InputError('Supplied config must be an object with an environment object.')
        report = review(data, config)
        report['input_sha256'] = sha
        if config_sha:
            report['config_sha256'] = config_sha
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except InputError as exc:
        print(json.dumps({'status': 'input_error', 'message': str(exc), 'review_completed': False}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

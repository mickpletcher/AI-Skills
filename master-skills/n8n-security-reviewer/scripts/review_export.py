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
SECRET_KEY = re.compile(r'^(authorization|proxy-authorization|x-api-key|api[-_]?key|access[-_]?token|refresh[-_]?token|client[-_]?secret|password|secret|token|cookie|apca-api-secret-key)$', re.I)
TOKEN = re.compile(r'(?:\b(?:sk-(?:ant-)?|ghp_|github_pat_)[A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
EXPRESSION = re.compile(r'\{\{|\$\{')
PLACEHOLDERS = {'', '[redacted]', '<redacted>', 'redacted', 'placeholder', 'changeme', 'your-api-key', 'your-token', '***'}
LIMITS = [
    'Static triage only; no workflow or expression was executed and no endpoint was contacted.',
    'Candidates are not validated vulnerabilities. Empty candidates do not mean secure.',
    'No dataflow, authentication effectiveness, published state, secret validity, or credential scopes are verified.',
    'Only documented helper rules are checked; unknown/custom nodes, version schemas, encoded secrets, and obfuscated code need manual review.',
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
    if config is not None:
        validate_bounds(config)
        findings.extend(inspect_config(config))
    return {
        'schema_version': 1,
        'review_kind': 'offline static triage; contextual review required',
        'workflow_count': len(workflows),
        'node_count': sum(len(w['nodes']) for w in workflows),
        'credential_reference_count': credentials,
        'candidates': findings,
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

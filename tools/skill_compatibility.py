#!/usr/bin/env python3
"""Generate evidence-bounded maintenance maps; never certify native support."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from ecosystem_paths import PLATFORM_PATHS
from generate_master_skills import TARGETS
from model_profiles import load_ecosystems, local_tree

ROOT = Path(__file__).resolve().parents[1]
LABELS = {'claude': 'Claude', 'chatgpt': 'OpenAI ChatGPT', 'codex': 'OpenAI Codex',
          'cursor': 'Cursor', 'copilot': 'GitHub Copilot', 'gemini': 'Gemini', 'perplexity': 'Perplexity'}
STATUS_ECOSYSTEMS = {
    **LABELS,
    'microsoft-copilot': 'Microsoft Copilot (consumer)',
    'microsoft-365-copilot': 'Microsoft 365 Copilot',
    'copilot-studio': 'Microsoft Copilot Studio',
    'amazon-q': 'Amazon Q Developer',
    'grok': 'Grok',
}
STATUS_PATHS = {**PLATFORM_PATHS, 'copilot-studio': 'microsoft/copilot-studio', 'amazon-q': 'amazon-q', 'grok': 'grok'}


def implementation_status(root, name, target, placement):
    # Consumer/M365 paths are deliberately not inferred: the repo has no variants for them.
    if target in ('microsoft-copilot', 'microsoft-365-copilot'):
        return 'Not targeted'
    relative = STATUS_PATHS[target]
    exists = any((root / prefix / relative / 'skills' / name / filename).is_file()
                 for prefix in ('', 'generated') for filename in ('SKILL.md', 'instructions.md'))
    return 'Implemented' if exists else 'Planned' if target in placement['allowed'] else 'Not targeted'


# Reviewed native-host metadata paths, not arbitrary mentions of a product in prompts.
CHATGPT_HOST_FIELDS = {
    'native-writing.json': ('rounds', 0, 'host'),
    'photo-native.json': ('native_retry', 'host'),
    'native-batch2-repairs.json': ('host',),
    'native-batch4.json': ('scope',),
    'native-batch8.json': ('host',),
    'native-batch9.json': ('host',),
    'native-batch10.json': ('host',),
    'native-batch10-repairs.json': ('host_limits',),
}


def passed_skill_case(value, skill, instruction_hash):
    if isinstance(value, dict):
        outcome = value.get('assessment', {}).get('outcome', value.get('status', ''))
        if (value.get('skill') == skill
                and value.get('resources_sha256', {}).get('instructions.md') == instruction_hash
                and re.fullmatch(r'bounded_(?:[a-z_]*_)?pass(?:_[a-z_]+)?', outcome)):
            return True
        return any(passed_skill_case(v, skill, instruction_hash) for v in value.values())
    if isinstance(value, list):
        return any(passed_skill_case(v, skill, instruction_hash) for v in value)
    return False


def native_chatgpt_evidence(path, instruction_hash, skill):
    fields = CHATGPT_HOST_FIELDS.get(path.name)
    if fields is None or not path.is_file():
        return False
    text = path.read_text()
    record = json.loads(text)
    value = record
    try:
        for key in fields:
            value = value[key]
    except (KeyError, IndexError, TypeError):
        return False
    passing = passed_skill_case(record, skill, instruction_hash)
    if path.name == 'photo-native.json' and skill == 'photo-rename':
        passing = (record.get('candidate_target') == 'chatgpt'
                   and record.get('candidate_sha256') == instruction_hash
                   and record.get('native_retry', {}).get('copy', {}).get('status') == 'passed')
    return (isinstance(value, str) and passing
            and ('ChatGPT native' in value or 'native ChatGPT' in value))


def verified_scopes(root, name, evidence):
    scopes = {}
    if not evidence:
        return scopes
    path = root / 'generated/openai/chatgpt/skills' / name / 'instructions.md'
    expected = evidence.get('current_chatgpt_instruction_sha256')
    if (path.is_file() and expected and hashlib.sha256(path.read_bytes()).hexdigest() == expected
            and evidence.get('current_instruction_hash_present_in_selected_evidence') is True
            and evidence.get('bounded_native_acceptance', '').lower().startswith('accepted')
            and any(native_chatgpt_evidence(root / p, expected, name) for p in evidence['evidence'])):
        scopes['chatgpt'] = ('Yes for the recorded passing bounded ChatGPT instruction-packet cases only, with explicit native-host metadata. '
                            'Current instruction bytes match a recorded passing case for this skill; installed routing, full workflow coverage, '
                            'all resources and broader models remain unverified. See per-skill evidence below.')
    host = evidence.get('codex_host18', {})
    if host.get('status') == 'BOUNDED_LOAD_OBSERVED' and (root / host['evidence']).is_file():
        fixture = json.loads((root / host['evidence']).read_text())
        expected = fixture.get('candidate_bundles', {}).get(name, {}).get('skill_sha256')
        path = root / 'generated/openai/codex/skills' / name / 'SKILL.md'
        if path.is_file() and expected and hashlib.sha256(path.read_bytes()).hexdigest() == expected:
            scopes['codex'] = ('Yes for the recorded bounded Codex CLI loading observation only, not full task execution. '
                               'Current instruction bytes match that fixture. ' + host['limits'] + ' Evidence: ' + link(host['evidence']) + '.')
    return scopes


def status_table(root, name, placement, evidence):
    scopes = verified_scopes(root, name, evidence)
    lines = ['## Ecosystem status at a glance', '',
             '| Ecosystem | Compatibility | Implementation status |',
             '| --- | --- | --- |']
    for target, label in STATUS_ECOSYSTEMS.items():
        compatibility = 'Yes' if target in scopes else 'Unknown'
        lines.append(f'| {label} | {compatibility} | {implementation_status(root, name, target, placement)} |')
    lines += ['', '### Scope of Yes ratings', '']
    lines += [f'- **{STATUS_ECOSYSTEMS[target]}:** {scope}' for target, scope in scopes.items()] or ['No affirmative rating is established for this master.']
    return lines + ['',
        '**Compatibility:** Yes requires actual evidence for an explicitly defined support scope; '
        'No requires a demonstrated incompatibility and a documented blocker. Unknown means affirmative scoped compatibility '
        'has not been established. A Yes applies only to its scope immediately above, never whole-skill or ecosystem-wide certification. '
        'Unknown also covers evidence needing additional host/case tracing; historical results remain below. Unknown does not mean incompatible, and skipped placement is not a technical blocker. No demonstrated host incompatibility is established here, so no No rating is assigned.', '',
        '**Implementation status:** Implemented means an existing same-name repository variant (candidate, shipped source '
        'or scaffold), not installed, activated or natively verified. The detailed paths below identify which kind. '
        'Planned means explicit intent for this master but no variant yet. Not targeted means no existing variant or '
        'per-master target intent. Reserved product folders alone do not make every skill Planned.', '',
        'The first seven rows are the existing repository target IDs. The additional five rows cover explicitly distinguished Microsoft products and reserved product guides, not new target approval or every AI product in existence. '
        'Amazon Q Developer is not Amazon Bedrock Agents; Grok consumer and Grok Build support are not assumed equivalent. '
        'Update the ecosystem list and evidence deliberately when repository targets change.', '']


COVERAGE = 'evaluations/native-coverage-2026-10-22.json'
URL = 'https://github.com/mickpletcher/AI-Skills/blob/main/'


def link(path):
    # Root URLs remain valid when this document is copied into candidate bundles.
    return f'[`{path}`]({URL}{path})'


def render(root, source):
    if set(TARGETS) != {'claude', 'chatgpt', 'codex', 'cursor'}:
        raise ValueError('Generator targets changed; review map labels and support wording')
    name = source.parent.name
    placement = load_ecosystems(source, TARGETS)
    contract = json.loads(source.with_name('capabilities.json').read_text())
    shipped = {s['source'] for s in json.loads((root / 'catalog.json').read_text())['skills']}
    evidence = next((r for r in json.loads((root / COVERAGE).read_text())['rows'] if r['skill'] == name), None)
    lines = [f'# Compatibility and update map: {name}', '',
             '<!-- Generated by tools/skill_compatibility.py; refresh declarations/evidence, then regenerate. -->', '',
             '## Meaning of support', '',
             'Allowed means an intended review candidate in `ecosystems.json`, not verified compatibility with every host/model. '
             'Skipped means no approved candidate placement. Shipped platform sources remain independently maintained. '
             'File existence and deterministic generation verify repository structure only, not installation or native behavior.', '',
             f'Declarations: {link(f"master-skills/{name}/ecosystems.json")}; '
             f'capabilities: {link(f"master-skills/{name}/capabilities.json")}.', '',
             *status_table(root, name, placement, evidence),
             '## Ecosystems and existing copies', '',
             '| Ecosystem | Intended placement / limits | Generated candidate entry point | Existing platform source (review separately) |',
             '| --- | --- | --- | --- |']
    adapters = []
    for target, label in LABELS.items():
        candidate = 'None'
        if target in placement['allowed']:
            decision = 'Allowed candidate: ' + placement['allowed'][target]
            path = f'generated/{PLATFORM_PATHS[target]}/skills/{name}/{TARGETS[target]}'
            if not (root / path).is_file():
                raise ValueError(f'Missing allowed candidate: {path}; generate it first')
            candidate = link(path)
        elif target in placement['skipped']:
            decision = 'Skipped: ' + placement['skipped'][target]
        else:
            decision = 'No canonical generator support or approved placement for this master.'
        copies = []
        for filename in ('SKILL.md', 'instructions.md'):
            path = f'{PLATFORM_PATHS[target]}/skills/{name}/{filename}'
            if (root / path).is_file():
                status = 'shipped' if path in shipped else 'scaffold; not shipped' if name == 'example-skill' else 'not in shipped catalog'
                copies.append(f'{link(path)} ({status})')
        decision = decision.replace('|', '\\|').replace('\n', ' ')
        lines.append(f'| {label} | {decision} | {candidate} | ' + ('<br>'.join(copies) or 'None') + ' |')
        path = f'adapters/{PLATFORM_PATHS[target]}/{name}/append.md'
        if (root / path).is_file():
            adapters.append(link(path))
    lines += ['', 'Microsoft Copilot / Microsoft 365 Copilot is not established by GitHub Copilot paths. '
              'Copilot Studio, Amazon Q and Grok are reserved with no generator/deployment support. '
              'Gemini and Perplexity have no generated candidates for this master. '
              'Related workflows with different names are not assumed to be equivalent copies.', '',
              'Adapters to review: ' + (', '.join(adapters) or 'None for this master') + '.', '',
              '## Verified evidence versus intended support', '']
    if evidence:
        lines += [f'Recorded bounded native outcome: {evidence["native_outcome"]}', '',
                  f'Acceptance: {evidence["bounded_native_acceptance"]}. This is not whole-skill or cross-ecosystem certification.', '',
                  'Evidence: ' + ', '.join(link(p) for p in evidence['evidence']) + '.', '',
                  'Remaining skill-specific limits: ' + ('; '.join(evidence['open_verification']) or
                  'Broader host/model behavior, integrations and repeatability remain unverified').rstrip('.') + '.', '']
        if 'codex_host18' in evidence:
            host = evidence['codex_host18']
            lines += [f'Historical Codex host observation: `{host["status"]}`. {host["limits"]} '
                      f'Evidence: {link(host["evidence"])}.', '']
    else:
        lines += ['No bounded native evidence row is indexed; support remains intended/unverified.', '']
    lines += [f'See {link(COVERAGE)} and {link("evaluations/native-coverage-2026-10-22.md")} for exact scopes, revisions '
              'and host/model limits. Historical results do not certify current bytes or every ecosystem row. '
              'Consult any master `model-history.json` for additional recorded runs. '
              'No blanket native verification is claimed for Claude, ChatGPT, Codex, Cursor or Copilot.', '',
              '## Capability and runtime limitations', '',
              '- Required: ' + ', '.join(f'`{c}`' for c in contract['required']) + '.']
    lines += [f'- Conditional `{key}`: {value}' for key, value in contract['conditional'].items()]
    lines += [f'- Fallback: {contract["fallback"]}', f'- Safeguards: {contract["safeguards"]}', '',
              f'Helpers require actual dependencies, permissions and runtime access. See {link("docs/installation.md")} '
              f'and {link("docs/dependencies.md")}.', '',
              '## When this master changes', '',
              '1. Review source, resources, capability/ecosystem declarations and adapters above. Do not widen support just because a model can read Markdown.',
              '2. Run `python tools/skill_compatibility.py`, then `python tools/generate_master_skills.py`. '
              'Synchronize all listed candidate entry points, supporting resources and provenance. '
              'For a newly allowed target, first generate its candidate, refresh this map, then regenerate candidates again.',
              '3. Review each listed existing platform source for an explicitly approved equivalent change. '
              'Do not overwrite shipped variants or promote/rebuild their packages automatically from a master update. '
              'Review named-model builds separately; profiles cannot widen the allowlist.',
              '4. Run `python tools/skill_compatibility.py --check`, `python tools/generate_master_skills.py --check`, '
              '`python tools/skill_repository.py validate` and `python -m unittest discover -s tools/tests -v`. '
              'Record actual host/model tests separately before claiming runtime compatibility.', '']
    return '\n'.join(lines)


def generate(root=ROOT, check=False):
    local_tree(root, root / 'master-skills')
    planned = {p.with_name('COMPATIBILITY.md'): render(root, p)
               for p in sorted((root / 'master-skills').glob('*/SKILL.md'))}
    drift = [p for p, text in planned.items() if not p.is_file() or p.read_text(encoding='utf-8') != text]
    if check and drift:
        raise ValueError('Missing or drifted maps: ' + ', '.join(str(p.relative_to(root)) for p in drift))
    if not check:
        for path, text in planned.items():
            path.write_text(text, encoding='utf-8', newline='\n')
    return len(planned)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(f'{generate(check=args.check)} compatibility maps ' + ('checked' if args.check else 'generated'))

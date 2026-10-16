"""Declarative model selection and capability contracts; never calls a model."""
import hashlib
import json
import re

CAPABILITIES = {'text_reasoning', 'web_retrieval', 'file_access', 'code_execution', 'image_understanding', 'persistent_storage'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_profile(root, name):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid model profile name')
    path = root/'model-profiles'/f'{name}.json'
    if path.is_symlink():
        raise ValueError('Profile symlinks are not supported')
    data = json.loads(path.read_text(encoding='utf-8'))
    keys = {'schema_version', 'id', 'provider', 'model_id', 'capabilities', 'overlay', 'evidence'}
    if set(data) != keys or data['schema_version'] != 1 or data['id'] != name:
        raise ValueError('Invalid model profile fields')
    if name != 'baseline' and any(not isinstance(data[k], str) or not data[k].strip() for k in ('provider', 'model_id')):
        raise ValueError('A non-baseline profile requires an exact provider and model ID')
    if name == 'baseline' and (data['provider'] is not None or data['model_id'] is not None):
        raise ValueError('The baseline must remain model-unconfigured')
    if not isinstance(data['capabilities'], dict) or set(data['capabilities']) != CAPABILITIES or any(
            value not in ('supported', 'unsupported', 'unknown') for value in data['capabilities'].values()):
        raise ValueError('Declare each capability as supported, unsupported, or unknown')
    if not isinstance(data['overlay'], str) or not isinstance(data['evidence'], list) or not all(isinstance(e, str) for e in data['evidence']):
        raise ValueError('Invalid overlay or evidence references')
    return data, digest(path.read_bytes())


def load_contract(source):
    path = source.parent/'capabilities.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    if set(data) != {'schema_version', 'required', 'conditional', 'fallback', 'safeguards'} or data['schema_version'] != 1:
        raise ValueError('Invalid capability contract')
    if not isinstance(data['required'], list) or not all(isinstance(c, str) for c in data['required']) or not set(data['required']) <= CAPABILITIES:
        raise ValueError('Invalid required capabilities')
    if not isinstance(data['conditional'], dict) or not set(data['conditional']) <= CAPABILITIES or set(data['required']) & set(data['conditional']):
        raise ValueError('Invalid conditional capabilities')
    if any(not isinstance(v, str) or not v.strip() for v in [data['fallback'], data['safeguards'], *data['conditional'].values()]):
        raise ValueError('Capability fallback guidance must be explicit')
    return data


def model_guidance(profile, contract):
    lines = ['## Target model and capability overlay', '',
             f"Profile: {profile['id']}; provider: {profile['provider'] or 'unconfigured'}; model: {profile['model_id'] or 'unconfigured'}.",
             'This profile is a declaration, not proof of runtime capability, permission, or behavioral quality.', '',
             contract['fallback'], contract['safeguards'], '', 'Required capabilities:']
    for capability in contract['required']:
        lines.append(f"- {capability}: {profile['capabilities'][capability]}. Verify actual availability before the dependent operation.")
    for capability, condition in contract['conditional'].items():
        lines.append(f"- Conditional {capability}: {profile['capabilities'][capability]}. {condition}")
    lines += ['', 'Model-specific guidance (subordinate to the master safeguards):', profile['overlay'], '',
              'Promotion blocked pending recorded structural regression, domain review, and target-host/model behavioral comparisons. No future model compatibility is inferred.']
    return '\n'.join(lines)


def load_ecosystems(source, targets):
    data = json.loads((source.parent/'ecosystems.json').read_text(encoding='utf-8'))
    if set(data) != {'schema_version', 'allowed', 'skipped', 'review_status', 'adaptation_review'} or data['schema_version'] != 1:
        raise ValueError('Invalid ecosystem mapping')
    if not isinstance(data['allowed'], dict) or not isinstance(data['skipped'], dict):
        raise ValueError('Ecosystem decisions must be explicit mappings')
    if set(data['allowed']) & set(data['skipped']) or set(data['allowed']) | set(data['skipped']) != set(targets):
        raise ValueError('Every ecosystem needs exactly one allowed/skipped decision')
    if not data['allowed'] or any(not isinstance(reason, str) or not reason.strip() for reason in [*data['allowed'].values(), *data['skipped'].values(), data['adaptation_review']]):
        raise ValueError('Ecosystem decisions need reasons')
    if data['review_status'] != 'proposed':
        raise ValueError('Generation does not approve ecosystem suitability')
    return data

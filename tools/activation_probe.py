import re
from pathlib import Path


def resource_boundary(workspace, skill_files):
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir() or not skill_files:
        raise ValueError('An existing workspace and a nonempty skill catalog are required')
    roots = []
    names = set()
    for value in skill_files:
        path = Path(value).resolve(strict=True)
        name = path.parent.name
        if path.name != 'SKILL.md' or not path.is_file() or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError('Catalog entries must identify named SKILL.md files')
        if name.casefold() in names or any(c in path.as_posix() for c in '\r\n'):
            raise ValueError('Duplicate or invalid skill resource path')
        names.add(name.casefold())
        roots.append(path.parent.as_posix())
    lines = '\n'.join('- ' + path for path in sorted(roots))
    return (
        'All task inputs are synthetic. For task data, read only the synthetic repository at '
        + workspace.as_posix() + '. Modify it only as the user task permits. '
        'Separately, you may read the selected skill instructions and supporting resources '
        'only beneath these exact catalog skill directories:\n' + lines + '\n'
        'This permission does not extend to parent profiles, other repositories or credentials. '
        'Do not browse, use connected apps, install dependencies, access credentials, change '
        'settings, delegate or modify real systems. Use the supplied runtime for permitted '
        'synthetic checks and disclose unavailable capabilities.'
    )


def observed_reads(events, skill_contents):
    outputs = [(event.get('item', {}).get('aggregated_output') or '').replace('\r\n', '\n')
               for event in events
               if event.get('type') == 'item.completed'
               and event.get('item', {}).get('type') == 'command_execution'
               and isinstance(event['item'].get('exit_code'), int)]
    return {name: any(content.decode('utf-8').replace('\r\n', '\n') in output for output in outputs)
            for name, content in skill_contents.items() if content}


def observed_injections(messages, skill_contents):
    texts = [part.get('text', '').replace('\r\n', '\n')
             for message in messages if message.get('type') == 'message' and message.get('role') == 'user'
             for part in message.get('content', []) if part.get('type') == 'input_text']
    return {name: any(text.startswith('<skill>\n') and '<name>' + name + '</name>' in text
                     and content.decode('utf-8').replace('\r\n', '\n') in text for text in texts)
            for name, content in skill_contents.items() if content}


def activation_evidence(events, messages, skill_contents):
    if not skill_contents or any(not isinstance(content, bytes) or not content for content in skill_contents.values()):
        raise ValueError('Nonempty pinned skill bodies are required')
    reads = observed_reads(events, skill_contents)
    injections = observed_injections(messages, skill_contents)
    return {name: {'tool_output': reads[name], 'input_injection': injections[name],
                   'loaded': reads[name] or injections[name]} for name in skill_contents}


def nested_write_roots(workspace, cwd, writable):
    workspace = Path(workspace).resolve(strict=True)
    cwd = Path(cwd).resolve(strict=True)
    if not workspace.is_dir() or not cwd.is_dir() or not cwd.is_relative_to(workspace):
        raise ValueError('Probe cwd must be inside its synthetic repository')
    return [workspace.as_posix()] if writable and cwd != workspace else []

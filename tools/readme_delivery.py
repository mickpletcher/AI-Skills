import re


def readme_body(response):
    lines = response.splitlines(keepends=True)
    blocks = []
    i = 0
    while i < len(lines):
        opening = re.fullmatch(r' {0,3}(`{3,}|~{3,})([^`~]*)', lines[i].rstrip())
        if not opening:
            i += 1
            continue
        fence, info = opening.groups()
        closing = re.compile(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*')
        end = next((j for j in range(i + 1, len(lines)) if closing.fullmatch(lines[j].rstrip())), None)
        if end is None:
            raise ValueError('Unclosed delivery fence')
        body = ''.join(lines[i + 1:end])
        if info.strip().casefold() in ('', 'markdown', 'md') and body.lstrip().startswith('# '):
            blocks.append((i, end, body))
        i = end + 1
    if not blocks:
        raise ValueError('Missing fenced Markdown README')
    if len(blocks) != 1:
        raise ValueError('Multiple Markdown artifacts')
    start, end, body = blocks[0]
    outside = ''.join(lines[:start] + lines[end + 1:])
    if outside.strip() and 'Review notes (not part of README)' not in outside:
        raise ValueError('Unlabeled text outside README')
    validate_readme(body)
    return body


def validate_readme(body):
    headings = []
    fence = None
    for line in body.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if match:
            marker, info = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not info.strip():
                fence = None
            continue
        if fence is None:
            heading = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
            if heading:
                headings.append(heading.group(1).strip())
    if fence:
        raise ValueError('Unclosed example fence')
    if not headings or headings[-1].casefold() != 'license':
        raise ValueError('License must be the final README heading')

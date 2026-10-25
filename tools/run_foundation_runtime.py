import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import tempfile
import tomllib
import venv

ROOT = Path(__file__).resolve().parents[1]


def materialize(project, files):
    for name, entry in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or ':' in name or '\\' in name:
            raise ValueError('Unsafe fixture path')
        data = entry['text'].encode('utf-8')
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('Fixture hash mismatch: ' + name)
        target = project / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (project / 'README.md').write_text('# Synthetic runtime input\n\nExample text.\n', encoding='utf-8')


def environment(project, python):
    home = project.parent / 'home'
    home.mkdir()
    env = {key: os.environ[key] for key in ('SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT') if key in os.environ}
    env.update(PATH=str(python.parent) + os.pathsep + os.defpath, HOME=str(home),
               TEMP=str(home), TMP=str(home), TMPDIR=str(home), PYTHONUTF8='1',
               PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
               PIP_NO_INDEX='1', PIP_CONFIG_FILE=os.devnull, PIP_NO_CACHE_DIR='1',
               PIP_DISABLE_PIP_VERSION_CHECK='1')
    return env


def execute(record, project, env, label, argv, stdin=None, expected=None):
    result = subprocess.run(list(map(str, argv)), cwd=project, env=env, input=stdin,
                            capture_output=True, timeout=120)
    valid = result.returncode == 0 if expected is None else expected(result)
    record['checks'].append({'label': label, 'exit_code': result.returncode,
                             'passed': bool(valid), 'stdout': result.stdout.decode('utf-8', errors='replace'),
                             'stderr': result.stderr.decode('utf-8', errors='replace')})
    print(record['id'], label, 'PASS' if valid else 'FAIL', flush=True)
    if not valid:
        raise RuntimeError(record['id'] + ': ' + label + '\n' + result.stderr.decode('utf-8', errors='replace'))
    return result


def run_project(item, workspace, cases, delivery_root):
    project = workspace / item['id'] / 'project'
    project.mkdir(parents=True)
    materialize(project, item['files'])
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(project.parent / 'venv')
    bin_dir = project.parent / 'venv' / ('Scripts' if os.name == 'nt' else 'bin')
    python = bin_dir / ('python.exe' if os.name == 'nt' else 'python')
    env = environment(project, python)
    record = {'id': item['id'], 'capture_sha256': item['capture_sha256'], 'checks': []}
    run = lambda label, args, **kw: execute(record, project, env, label, args, **kw)
    full = item['id'].startswith('architect')
    readme = item['id'].startswith('readme')
    if full or readme:
        config = tomllib.loads((project / 'pyproject.toml').read_text(encoding='utf-8'))
        if config['build-system']['build-backend'] != 'setuptools.build_meta' or config['project']['dependencies']:
            raise ValueError('Unreviewed build configuration')
        run('offline install', [python, '-m', 'pip', 'install', '--no-index', '--no-build-isolation', '--no-deps', *(['-e'] if full else []), '.'])
    else:
        env['PYTHONPATH'] = str(project / 'src')
    if readme:
        executable = bin_dir / ('log-summary-demo.exe' if os.name == 'nt' else 'log-summary-demo')
        (project / 'example.log').write_bytes('alpha\n\nβeta'.encode('utf-8'))
        source = 'example.log' if item['id'].endswith('r1') else 'README.md'
        count = len((project / source).read_text(encoding='utf-8').splitlines())
        run('documented text example', [executable, '--input', source],
            expected=lambda c: c.returncode == 0 and c.stdout.decode().strip() == f'Lines: {count}')
        run('documented JSON example', [executable, '--input', source, '--format', 'json'],
            expected=lambda c: c.returncode == 0 and json.loads(c.stdout) == {'lines': count})
        run('documented help', [executable, '--help'])
        run('documented unittest discovery', [python, '-m', 'unittest', 'discover', '-s', 'tests'])
        return record
    before = {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob('*.py')}
    run('original formatting gate', [python, '-m', 'ruff', 'format', '--check', '.'],
        expected=lambda c: c.returncode == (1 if item['id'] == 'architect-r2' else 0))
    run('apply configured formatter', [python, '-m', 'ruff', 'format', '.'])
    changed = [name for name, data in before.items() if (project / name).read_bytes() != data]
    if changed != (['tests/test_cli.py'] if item['id'] == 'architect-r2' else []):
        raise AssertionError('Unexpected formatting scope: ' + repr(changed))
    for name in changed:
        if ast.dump(ast.parse(before[name])) != ast.dump(ast.parse((project / name).read_bytes())):
            raise AssertionError('Formatter changed Python AST')
    run('final formatting gate', [python, '-m', 'ruff', 'format', '--check', '.'])
    run('final lint gate', [python, '-m', 'ruff', 'check', '.'])
    run('final pytest gate', [python, '-m', 'pytest', '-q'])
    record['formatted_files'] = changed
    record['final_python_sha256'] = {name: hashlib.sha256((project / name).read_bytes()).hexdigest() for name in before}
    if full:
        executable = bin_dir / ('sample-count.exe' if os.name == 'nt' else 'sample-count')
        run('installed entry point', [executable, '--help'])
        for case in cases:
            payload = case['input'].encode('utf-8')
            path = project / 'runtime-input.txt'
            path.write_bytes(payload)
            for mode, args, stdin in [('file', [path], None), ('stdin', [], payload), ('dash', ['-'], payload)]:
                count = case['expected_count']
                run(case['id'] + '/' + mode, [executable, *args], stdin=stdin,
                    expected=lambda c, n=count: c.returncode == 0 and c.stdout.decode().strip() == str(n) and not c.stderr)
        for label, args, stdin, code in [('invalid UTF-8', ['-'], b'valid\n\xff\n', 1),
                                        ('missing file', ['missing.txt'], None, 1),
                                        ('invalid argument', ['--not-real'], None, 2)]:
            run(label, [executable, *args], stdin=stdin,
                expected=lambda c, n=code: c.returncode == n and not c.stdout and bool(c.stderr))
    else:
        (project / 'oracle.json').write_text(json.dumps(cases), encoding='utf-8')
        run('six independent whitespace oracles', [python, '-c',
            "import io,json;from sample_count.core import count_nonempty;cases=json.load(open('oracle.json',encoding='utf-8'));assert all(count_nonempty(io.StringIO(c['input'],newline=None))==c['expected_count'] for c in cases)"])
    delivery = delivery_root / item['id']
    for name in item['files']:
        target = delivery / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((project / name).read_bytes())
    for name, digest in record['final_python_sha256'].items():
        if hashlib.sha256((delivery / name).read_bytes()).hexdigest() != digest:
            raise AssertionError('Delivered stale content')
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve prior runtime evidence')
    delivery_root = args.output.with_suffix('')
    if delivery_root.exists():
        raise FileExistsError('Preserve prior delivered files')
    fixture_path = ROOT / 'evaluations/fixtures/foundation-runtime/projects.json'
    fixture = json.loads(fixture_path.read_text(encoding='utf-8'))
    pilot = json.loads((ROOT / 'evaluations/fixtures/foundation-pilot.json').read_text(encoding='utf-8'))
    cases = next(c for c in pilot['cases'] if c['id'] == 'architect-whitespace-regression')['runtime_cases']
    report = {'platform': platform.platform(), 'python': sys.version, 'status': 'running',
              'fixture_sha256': hashlib.sha256(fixture_path.read_bytes()).hexdigest(), 'projects': []}
    try:
        with tempfile.TemporaryDirectory(prefix='foundation-runtime-') as directory:
            for item in fixture['projects']:
                report['projects'].append(run_project(item, Path(directory), cases, delivery_root))
        report['status'] = 'passed'
    except Exception:
        report['status'] = 'failed'
        raise
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()

"""What the three repos hold: every tracked file, what it says it is, when it last changed, and who points to it.

    ~/.venvs/gidi/bin/python scripts/inventory.py [--out docs/inventory]

Reads the git-tracked files of ~/gidi, ~/gidi-game and ~/gidi-data (the study store: only its notes and scripts are
tracked; nothing untracked, nothing generated) and writes:
  inventory.json   one row per file: repo, path, kind, lines, last change, summary, the files that point to it
  INVENTORY.md     the same per folder, readable; binary files (art, models) counted per folder, not listed
  SUSPECTS.md      what to look at first: code and documents nothing points to, and paths that documents and code name
                   but that no longer exist

"Points to" is read from text, so it covers documents too: a Python or TypeScript import, a script's name in a shell
line, a markdown link, or a plain mention of the file's name or path anywhere in the three repos. A file can be alive
and still unpointed (a tool run by hand), so SUSPECTS is a list to read, not a list to delete.
"""
import argparse
import ast
import collections
import json
import os
import re
import subprocess

REPOS = {'gidi': os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gidi-game': os.path.expanduser('~/gidi-game'),
         'gidi-data': os.path.expanduser('~/gidi-data')}
TEXT = {'.py', '.sh', '.js', '.mjs', '.ts', '.mts', '.tsx', '.md', '.html', '.css', '.json', '.ini', '.txt', '.toml',
        '.yml', '.yaml', '.csv', '.tsv', '.geojson', '.cfg', ''}
CODE = {'.py', '.sh', '.js', '.mjs', '.ts', '.mts', '.tsx', '.html', '.css'}
BIG = 2_000_000      # text files bigger than this (data dumps) are counted, not read
WORD = re.compile(r'[\w.\-/~]+')
PATHY = re.compile(r'(?<![\w/.~-])((?:[\w.-]+/)*[\w.-]+\.(?:py|sh|md|js|mjs|ts|mts|html|json|ini|css|blend))\b')
IMPORT_PY = re.compile(r'^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w., ]+))', re.M)
IMPORT_JS = re.compile(r'''(?:from\s+|require\(\s*|import\(\s*|import\s+)['"]([^'"]+)['"]''')
# Paths the code makes or reads outside git (outputs, caches, other machines' folders): not counted as broken.
OUTSIDE = ('Saved/', 'Intermediate/', 'DerivedDataCache/', 'node_modules/', 'dist/', '/tmp', 'scratchpad', '~/',
           'Generated/', 'out/', 'build/', '.venv', 'http', 'Engine/', 'site-packages')


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=True).stdout


def last_changes(repo):
    when, day = {}, None
    for line in git(repo, 'log', '--format=@%cs', '--name-only').splitlines():
        if line.startswith('@'):
            day = line[1:]
        elif line and line not in when:
            when[line] = day
    return when


def first_text(lines):
    out = []
    for l in lines:
        l = l.strip()
        if not l:
            if out:
                break
            continue
        out.append(l)
        if len(' '.join(out)) > 240:
            break
    return ' '.join(out)


def summary(path, ext, text):
    try:
        if ext == '.py':
            doc = ast.get_docstring(ast.parse(text))
            if doc:
                return first_text(doc.splitlines())
        if ext in ('.py', '.sh'):
            return first_text([l.lstrip('#') for l in text.splitlines() if l.startswith('#') and not l.startswith('#!')][:6])
        if ext in ('.js', '.mjs', '.ts', '.mts', '.tsx', '.css'):
            m = re.match(r'\s*(?:/\*+(.*?)\*/|((?:\s*//[^\n]*\n)+))', text, re.S)
            if m:
                body = m.group(1) or m.group(2)
                return first_text([l.strip().lstrip('/*').strip() for l in body.splitlines()])
        if ext == '.md':
            lines = text.splitlines()
            head = next((l.lstrip('# ').strip() for l in lines if l.startswith('#')), '')
            body = first_text([l for l in lines if not l.startswith('#')])
            return (head + ': ' if head else '') + body
        if ext == '.html':
            m = re.search(r'<title>(.*?)</title>', text, re.S | re.I)
            return m.group(1).strip() if m else ''
        if ext in ('.json', '.geojson'):
            d = json.loads(text)
            if isinstance(d, dict):
                return 'keys: ' + ', '.join(list(d)[:12])
            if isinstance(d, list):
                return f'a list of {len(d)}'
        if ext == '.ini':
            return 'sections: ' + ', '.join(re.findall(r'^\[([^\]]+)\]', text, re.M)[:8])
    except Exception:
        return ''
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(REPOS['gidi'], 'docs', 'inventory'))
    ap.add_argument('--untracked', action='store_true',
                    help="also read gidi's new files not yet added (the commit hook: a commit's new files count too)")
    a = ap.parse_args()

    files = []          # rows
    texts = {}          # (repo, path) -> text, for reading references
    for name, repo in REPOS.items():
        when = last_changes(repo)
        listed = git(repo, 'ls-files', *(['--cached', '--others', '--exclude-standard'] if a.untracked and name == 'gidi' else []))
        for path in listed.splitlines():
            full = os.path.join(repo, path)
            if not os.path.isfile(full):
                continue
            ext = os.path.splitext(path)[1].lower()
            size = os.path.getsize(full)
            row = {'repo': name, 'path': path, 'ext': ext, 'bytes': size, 'changed': when.get(path, ''),
                   'lines': None, 'summary': '', 'text': ext in TEXT}
            # this script's own output names every file: reading it would make everything look pointed to
            if row['text'] and size <= BIG and not (name == 'gidi' and path.startswith('docs/inventory/')):
                try:
                    t = open(full, encoding='utf-8').read()
                except (UnicodeDecodeError, OSError):
                    row['text'] = False
                else:
                    texts[(name, path)] = t
                    row['lines'] = t.count('\n') + 1
                    row['summary'] = summary(path, ext, t)
            files.append(row)

    # every word in every text file, and the imports in the code
    words, imports = {}, collections.defaultdict(set)
    for key, t in texts.items():
        ws = set(WORD.findall(t))
        ws |= {w.rsplit('/', 1)[-1] for w in ws if '/' in w}
        words[key] = ws
        ext = os.path.splitext(key[1])[1]
        if ext == '.py':
            for m in IMPORT_PY.finditer(t):
                for mod in (m.group(1) or m.group(2) or '').split(','):
                    mod = mod.strip().split(' ')[0]
                    if mod:
                        imports[key].add(mod.split('.')[-1])
                        imports[key].add(mod.split('.')[0])
        elif ext in ('.js', '.mjs', '.ts', '.mts', '.tsx', '.html'):
            for m in IMPORT_JS.finditer(t):
                imports[key].add(os.path.splitext(m.group(1).rsplit('/', 1)[-1])[0])
            for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)', t):
                imports[key].add(os.path.splitext(m.group(1).rsplit('/', 1)[-1])[0])

    by_base = collections.defaultdict(list)
    for r in files:
        by_base[os.path.basename(r['path'])].append(r)
    for r in files:
        key = (r['repo'], r['path'])
        base = os.path.basename(r['path'])
        stem = os.path.splitext(base)[0]
        ins = set()
        for k, ws in words.items():
            if k == key:
                continue
            if base in ws or r['path'] in ws:
                ins.add(k)
            elif r['ext'] in CODE and stem in imports.get(k, ()):
                ins.add(k)
        r['refs_in'] = sorted(f'{k[0]}:{k[1]}' for k in ins)

    # paths of ours that do not exist: a name under one of our repos' top folders (scripts/<name>.py, tools/<name>.sh) that is
    # neither tracked nor on disk there, or a bare script name (<name>.py) that exists in none of the repos. Research
    # write-ups about other people's projects name their files, so bare names are only checked outside research/.
    tops, on_disk, have = {}, set(), set()
    for name, repo in REPOS.items():
        tops[name] = {e for e in os.listdir(repo) if os.path.isdir(os.path.join(repo, e)) and not e.startswith('.')}
        for root, dirs, fs in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'DerivedDataCache', 'Intermediate')]
            on_disk.update(fs)
            rel = os.path.relpath(root, repo)
            have.update(os.path.normpath(os.path.join(rel, f)) for f in fs)
    all_tops = set().union(*tops.values()) - {'Saved', 'dist', 'node_modules', 'out', 'build'}
    broken, pathy = collections.defaultdict(set), set()
    for key, t in texts.items():
        if os.path.splitext(key[1])[1] in ('.json', '.csv', '.tsv', '.geojson'):
            continue
        research = key[1].startswith(('research/', 'reference/'))
        for m in PATHY.finditer(t):
            p = m.group(1)
            around = t[max(0, m.start() - 40):m.end() + 2]
            if any(o in around for o in OUTSIDE) or '*' in p or '<' in p or '{' in around[-45:]:
                continue
            if '/' in p:
                if p.split('/')[0] in all_tops and p not in have and os.path.basename(p) not in on_disk:
                    broken[f'{key[0]}:{key[1]}'].add(p)
                    pathy.add(p)
            elif not research and p.endswith(('.py', '.sh', '.md')) and p not in on_disk and not p.startswith('_'):
                broken[f'{key[0]}:{key[1]}'].add(p)

    # A path a repo's .gitignore covers is made by a script (web/frame-study.js, web/city/...), so it is missing from a
    # fresh checkout by design: not a broken name. Asked of git itself, so the answer follows the real ignore rules.
    made = set()
    for repo in REPOS.values():
        out = subprocess.run(['git', '-C', repo, 'check-ignore', '--no-index', '--stdin'], input='\n'.join(sorted(pathy)),
                             capture_output=True, text=True).stdout
        made.update(out.split())
    for k in list(broken):
        broken[k] -= made
        if not broken[k]:
            del broken[k]

    os.makedirs(a.out, exist_ok=True)
    for r in files:
        r.pop('text')
    json.dump({'files': files, 'broken': {k: sorted(v) for k, v in sorted(broken.items())}},
              open(os.path.join(a.out, 'inventory.json'), 'w'), indent=1)
    write_md(files, a.out)
    write_suspects(files, broken, a.out)
    print(f'{len(files)} files, {len(texts)} read, {sum(1 for r in files if not r["refs_in"])} pointed to by nothing, '
          f'{sum(len(v) for v in broken.values())} missing names in {len(broken)} files -> {a.out}')


def folder(path):
    parts = path.split('/')
    return '/'.join(parts[:2]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else '.')


def cell(s, n=160):
    s = (s or '').replace('|', '/').replace('\n', ' ')
    return s if len(s) <= n else s[:n - 1] + '…'


def write_md(files, out):
    lines = ['# Inventory of the three repos', '',
             'Made by `scripts/inventory.py` (gidi): every git-tracked file in gidi, gidi-game and gidi-data. "Refs" is '
             'how many other files name it (imports, links, mentions). Binary files are counted per folder. Run it again '
             'to refresh; do not edit by hand.', '']
    for repo in REPOS:
        rows = [r for r in files if r['repo'] == repo]
        lines += [f'## {repo}', '', f'{len(rows)} files.', '']
        groups = collections.defaultdict(list)
        for r in rows:
            groups[folder(r['path'])].append(r)
        for g in sorted(groups):
            rs = groups[g]
            text = [r for r in rs if r['lines'] is not None and r['ext'] not in ('.json', '.csv', '.tsv', '.geojson')]
            data = [r for r in rs if r['lines'] is not None and r not in text]
            other = [r for r in rs if r['lines'] is None]
            lines += [f'### {repo}/{g}', '']
            if text:
                lines += ['| file | lines | changed | refs | what it says it is |', '|---|---|---|---|---|']
                for r in sorted(text, key=lambda r: r['path']):
                    lines.append(f"| `{r['path'][len(g) + 1:] if g != '.' else r['path']}` | {r['lines']} | {r['changed']} | "
                                 f"{len(r['refs_in'])} | {cell(r['summary'])} |")
                lines.append('')
            if data:
                lines.append(f"Data: {len(data)} files, {sum(r['bytes'] for r in data) / 1e6:.1f} MB "
                             f"({', '.join(sorted({r['ext'] for r in data}))}); unpointed: "
                             f"{sum(1 for r in data if not r['refs_in'])}.")
                lines.append('')
            if other:
                exts = collections.Counter(r['ext'] or '(none)' for r in other)
                lines.append(f"Binary: {len(other)} files, {sum(r['bytes'] for r in other) / 1e6:.1f} MB "
                             f"({', '.join(f'{n} {e}' for e, n in exts.most_common())}).")
                lines.append('')
    open(os.path.join(out, 'INVENTORY.md'), 'w').write('\n'.join(lines))


def write_suspects(files, broken, out):
    lines = ['# Suspects', '', 'Made by `scripts/inventory.py`. A list to read, not to delete: a tool run by hand can be '
             'alive with nothing pointing to it.', '', '## Code and documents nothing points to', '']
    for repo in REPOS:
        rs = [r for r in files if r['repo'] == repo and not r['refs_in'] and r['lines'] is not None
              and r['ext'] in CODE | {'.md'}]
        lines += [f'### {repo} ({len(rs)})', '', '| file | lines | changed | what it says it is |', '|---|---|---|---|']
        for r in sorted(rs, key=lambda r: (r['changed'], r['path'])):
            lines.append(f"| `{r['path']}` | {r['lines']} | {r['changed']} | {cell(r['summary'], 120)} |")
        lines.append('')
    lines += ['## Names of files that exist nowhere', '',
              'Paths named in a document or in code that match no file in any repo (outputs and caches skipped).', '']
    for k, v in sorted(broken.items()):
        lines.append(f"- `{k}`: {', '.join(f'`{p}`' for p in sorted(v))}")
    open(os.path.join(out, 'SUSPECTS.md'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()

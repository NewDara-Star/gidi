"""The code graph, for scripts/inventory.py (owner, 24 Oct: "use the compiler to know what every single piece of code,
every line, is connected to, and that every comment is correct"). Read by the languages' own parsers, not by guessing:
Python by `ast`, JavaScript (the .js files and the inline scripts of the .html pages) by the TypeScript compiler's parser
(scripts/js_symbols.mjs; the compiler is found in $GIDI_TS or an installed copy, and its absence is said, never skipped
in silence). Shell has no parser here: its links to other files come from the inventory's text references.

For every piece of code (a function, class, method or top-level constant):
  used      where it is used: in its own file outside its own body, or in a file that imports its file (Python), or in
            another script of the same page set (JavaScript in the browser shares one global scope)
  maybe     used only by name somewhere that doesn't import it (a call by string, getattr, Blender's operator lookup):
            word matching, so a hint, not proof
  unused    nothing names it anywhere: dead code, or run some way no file says
Every comment and docstring is read for the code names it mentions (`backticked` words, snake_case, camelCase, name()),
and each must exist: as a name in the code of the three repos, a file, a map schema field or a record key. A name that
exists nowhere is a comment that no longer tells the truth (or a typo); the list is in COMMENTS.md.
"""
import ast
import collections
import io
import json
import os
import re
import subprocess
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
TS_PLACES = [os.environ.get('GIDI_TS', ''), os.path.expanduser('~/stride-web/node_modules/typescript'),
             os.path.expanduser('~/Real-world/game/node_modules/typescript')]
# run by a framework or by name, never called in the code: not dead for having no caller
FRAMEWORK = {'main', 'register', 'unregister', 'execute', 'invoke', 'poll', 'draw', 'modal', 'setUp', 'tearDown',
             'do_GET', 'do_POST', 'do_PUT', 'do_OPTIONS', 'log_message', 'end_headers', 'handle', 'run'}
# a name followed by .ext is a file name (map_first.json), checked as a file, not as code
CODE_WORD = re.compile(r'`([^`\n]{1,80})`|\b([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\b(?![.-]\w)|\b([a-z]+[A-Z][A-Za-z0-9]*)\b(?![.-]\w)|\b([A-Za-z_]\w*)\(\)')
IDENT = re.compile(r'[A-Za-z_][\w]*')


# ------------------------------------------------------------------ Python
class PyFile:
    def __init__(self, key, text):
        self.key, self.decls, self.uses, self.imports, self.comments, self.error = key, [], collections.defaultdict(list), [], [], None
        self.strings, self.prefixes = set(), set()
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            self.error = f'does not parse: {e.msg} (line {e.lineno})'
            return
        for n in tree.body:
            self._decl(n, '')
        for n in ast.walk(tree):
            if isinstance(n, ast.Name):
                self.uses[n.id].append(n.lineno)
            elif isinstance(n, ast.Attribute):
                self.uses[n.attr].append(n.lineno)
            elif isinstance(n, ast.keyword) and n.arg:
                self.uses[n.arg].append(n.value.lineno)
            elif isinstance(n, ast.JoinedStr):              # f'glass_{name}': names are built from this prefix
                for v in n.values:
                    if isinstance(v, ast.Constant) and isinstance(v.value, str) and re.fullmatch(r'[a-z]\w*_', v.value):
                        self.prefixes.add(v.value)
            elif isinstance(n, ast.arg):
                self.strings.add(n.arg)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str):
                if IDENT.fullmatch(n.value):
                    self.uses[n.value].append(n.lineno)     # getattr(x, 'name'), a registry key, an operator id
                for w in re.findall(r'(?:^|\s)--([a-z][\w-]*)', n.value):     # a command-line flag the code reads
                    self.strings.add(w.replace('-', '_'))
                # (other words inside strings are prose, a docstring above all: a comment can't vouch for itself)
            elif isinstance(n, ast.Import):
                self.imports += [(a.name, None, n.lineno) for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                self.imports += [(n.module or '', a.name, n.lineno) for a in n.names]
                for a in n.names:
                    self.uses[a.name].append(n.lineno)
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                d = ast.get_docstring(n, clean=False)
                if d and n.body and isinstance(n.body[0], ast.Expr):
                    self.comments.append((n.body[0].lineno, d))
        try:
            for t in tokenize.generate_tokens(io.StringIO(text).readline):
                if t.type == tokenize.COMMENT:
                    self.comments.append((t.start[0], t.string))
        except (tokenize.TokenError, IndentationError):
            pass

    def _decl(self, n, owner):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.decls.append({'name': n.name, 'kind': 'method' if owner else 'function', 'owner': owner,
                               'line': n.lineno, 'end': n.end_lineno})
        elif isinstance(n, ast.ClassDef):
            self.decls.append({'name': n.name, 'kind': 'class', 'owner': owner, 'line': n.lineno, 'end': n.end_lineno,
                               'bases': [ast.unparse(b).split('.')[-1] for b in n.bases]})
            for b in n.body:
                self._decl(b, n.name)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)) and not owner:
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                for x in ast.walk(t):
                    if isinstance(x, ast.Name):
                        self.decls.append({'name': x.id, 'kind': 'const', 'owner': '', 'line': n.lineno, 'end': n.end_lineno})
        elif isinstance(n, (ast.If, ast.Try)) and not owner:
            for b in n.body + getattr(n, 'orelse', []) + [x for h in getattr(n, 'handlers', []) for x in h.body]:
                self._decl(b, owner)


def resolve_import(module, repo, key, by_stem):
    """The repo file a Python import names: by its last dotted part, the same repo first, the same folder before others."""
    stem = module.split('.')[-1] if module else ''
    cands = by_stem.get(stem, [])
    if not cands:
        return None
    here = os.path.dirname(key.split(':', 1)[1])
    cands = sorted(cands, key=lambda k: (k.split(':')[0] != repo, os.path.dirname(k.split(':', 1)[1]) != here, k))
    return cands[0]


# ------------------------------------------------------------------ JavaScript
def find_ts():
    for p in TS_PLACES:
        if p and os.path.isfile(os.path.join(p, 'package.json')):
            return p
    return None


def js_files(texts):
    """Every .js file and every inline <script> of an .html page, as [{key, text, line0}]."""
    out = []
    for (repo, path), t in texts.items():
        if path.endswith(('.js', '.mjs')) and not path.startswith('docs/inventory/'):
            out.append({'key': f'{repo}:{path}', 'text': t, 'line0': 0})
        elif path.endswith('.html'):
            for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', t, re.S):
                out.append({'key': f'{repo}:{path}#{t.count(chr(10), 0, m.start(1)) + 1}', 'text': m.group(1),
                            'line0': t.count('\n', 0, m.start(1))})
    return out


def read_js(files):
    ts = find_ts()
    if not ts:
        return None, 'no TypeScript compiler found (set GIDI_TS to a node_modules/typescript folder): JavaScript not read'
    big = [f for f in files if len(f['text']) < 3_000_000]
    run = subprocess.run(['node', os.path.join(HERE, 'js_symbols.mjs'), ts], input=json.dumps(big),
                         capture_output=True, text=True)
    if run.returncode:
        return None, 'js_symbols.mjs failed: ' + run.stderr.strip()[-300:]
    return json.loads(run.stdout), f'JavaScript read by the TypeScript compiler at {ts}'


def json_keys(o, out=None):
    out = set() if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            out.add(k)
            json_keys(v, out)
    elif isinstance(o, list):
        for v in o[:2000]:
            json_keys(v, out)
    return out


# ------------------------------------------------------------------ the graph
def build(repos, texts, schema_words, on_disk=()):
    """texts: {(repo, path): text}; on_disk: the names of every file in the repos' folders, tracked or not (a texture,
    a test's output), which a comment may name too. Returns {'files': {key: {...}}, 'symbols': [...], 'comments': [...], 'note': str}."""
    py = {}
    for (repo, path), t in texts.items():
        if path.endswith('.py') and not path.startswith('docs/inventory/'):
            py[f'{repo}:{path}'] = PyFile(f'{repo}:{path}', t)
    by_stem = collections.defaultdict(list)
    for k in py:
        by_stem[os.path.splitext(os.path.basename(k))[0]].append(k)

    js_in = js_files(texts)
    js, note = read_js(js_in)
    js = js or {}

    files = {}
    for k, f in py.items():
        imps = []
        for mod, name, line in f.imports:
            tgt = resolve_import(mod, k.split(':')[0], k, by_stem)
            if tgt is None and name:                     # from scripts import check_map
                tgt = resolve_import(name, k.split(':')[0], k, by_stem)
            if tgt and tgt != k:
                imps.append((tgt, name, line))
        files[k] = {'lang': 'python', 'error': f.error, 'imports': sorted({i[0] for i in imps}), 'imported_by': [],
                    'decls': f.decls, 'uses': f.uses, '_imps': imps}
    for k, r in js.items():
        files[k] = {'lang': 'javascript', 'error': r['error'], 'imports': [], 'imported_by': [], 'decls': r['decls'],
                    'uses': {n: ls for n, ls in r['uses'].items()}, '_imps': []}
    for k, f in files.items():
        for t in f['imports']:
            files[t]['imported_by'].append(k)

    # a page's scripts share one global scope: a .js file's names are seen by the pages that load it and their scripts
    page_of = collections.defaultdict(set)
    for (repo, path), t in texts.items():
        if path.endswith('.html'):
            page = {f'{repo}:{path}#{n}' for n in [x['key'].split('#')[1] for x in js_in if x['key'].startswith(f'{repo}:{path}#')]}
            for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)', t):
                src = os.path.normpath(os.path.join(os.path.dirname(path), m.group(1).split('?')[0]))
                page.add(f'{repo}:{src}')
            for k in page:
                page_of[k] |= page

    all_uses = collections.defaultdict(set)          # name -> files using it
    for k, f in files.items():
        for n in f['uses']:
            all_uses[n].add(k)
    text_names = collections.defaultdict(set)        # name -> non-code files naming it (docs, shell, json)
    for (repo, path), t in texts.items():
        k = f'{repo}:{path}'
        if k in files or path.startswith('docs/inventory/'):
            continue
        for w in set(IDENT.findall(t)):
            text_names[w].add(k)

    ours = {d['name'] for f in files.values() for d in f['decls'] if d['kind'] == 'class'}
    symbols = []
    for k, f in files.items():
        outside = {d['name'] for d in f['decls'] if d['kind'] == 'class' and any(b not in ours for b in d.get('bases', []))}
        for d in f['decls']:
            n = d['name']
            inside = [l for l in f['uses'].get(n, []) if not d['line'] <= l <= d['end']]
            used = [k] if inside else []
            if f['lang'] == 'python':
                for g in f['imported_by']:
                    gi = files[g]
                    if n in gi['uses'] or d['kind'] == 'method' and n in gi['uses']:
                        used.append(g)
            else:
                for g in page_of.get(k, ()):
                    if g != k and g in files and n in files[g]['uses']:
                        used.append(g)
            maybe = sorted(all_uses.get(n, set()) - set(used) - {k})
            if d['kind'] == 'method' and maybe and not used:
                used, maybe = maybe, []                  # a method is called on an object: any file calling the name
            state = 'used' if used else 'maybe' if maybe or text_names.get(n) else 'unused'
            if state != 'used' and (n in FRAMEWORK or n.startswith(('__', 'test_')) or n == '_'):
                state = 'used'
            elif state != 'used' and d['kind'] == 'method' and d.get('owner') in outside:
                state = 'maybe'                          # overrides a method of a library's class, which calls it
            symbols.append({'file': k, 'name': n, 'kind': d['kind'], 'owner': d.get('owner', ''), 'line': d['line'],
                            'end': d['end'], 'state': state, 'used_in': sorted(set(used) - {k}), 'self': bool(inside),
                            'maybe': maybe[:8], 'text': sorted(text_names.get(n, ()))[:8]})

    # comments: every code name they mention must exist somewhere
    known = set(schema_words) | {os.path.splitext(x)[0] for x in on_disk} | set(on_disk)
    for f in py.values():
        known |= set(f.uses) | f.strings | {d['name'] for d in f.decls}
    for r in js.values():
        known |= set(r['uses']) | {d['name'] for d in r['decls']}
    for (repo, path) in texts:
        base = os.path.basename(path)
        known |= {base, os.path.splitext(base)[0], path}
        known |= set(re.split(r'[/.]', path))
    for (repo, path), t in texts.items():
        # the names other files give: JSON keys (not values), shell variables and functions, settings keys
        if path.endswith(('.json', '.geojson')):
            try:
                known |= json_keys(json.loads(t))
            except ValueError:
                pass
        elif path.endswith('.sh'):
            known |= set(re.findall(r'\b([A-Za-z_]\w*)=', t)) | set(re.findall(r'\$\{?([A-Za-z_]\w*)', t))
            known |= set(re.findall(r'^\s*([A-Za-z_]\w*)\s*\(\)', t, re.M)) | set(re.findall(r'--([a-z][\w-]*)', t))
        elif path.endswith(('.ini', '.toml', '.cfg', '.yml', '.yaml')):
            known |= set(re.findall(r'^\s*\+?([A-Za-z_][\w.]*)\s*[=:]', t, re.M)) | set(re.findall(r'^\[([^\]]+)\]', t, re.M))
    prefixes = set().union(*(f.prefixes for f in py.values())) if py else set()

    def exists(w):
        return w in known or w.lower() in known or any(w.startswith(p) and w[len(p):] in known for p in prefixes)
    comments = []
    sources = [(k, f.comments) for k, f in py.items()] + [(k, [(c['line'], c['text']) for c in r['comments']]) for k, r in js.items()]
    for k, cs in sources:
        for line, text in cs:
            if re.match(r'#!|# -\*-|#\s*(noqa|type:|pragma)', text):
                continue
            bad = []
            for m in CODE_WORD.finditer(text):
                if m.group(1):                            # `backticked`: each name in it
                    words = [w for w in re.findall(r'[A-Za-z_][\w]*', m.group(1)) if len(w) > 2]
                    if re.search(r'\s', m.group(1).strip()) and not re.search(r'[_.()/]', m.group(1)):
                        continue                          # a quoted phrase, not code
                else:
                    words = [m.group(2) or m.group(3) or m.group(4)]
                for w in words:
                    if not exists(w) and w not in bad:
                        bad.append(w)
            if bad:
                first = text.strip().splitlines()[0][:140]
                comments.append({'file': k, 'line': line, 'names': bad, 'text': first})
    for f in files.values():
        f.pop('_imps')
        f['uses'] = len(f['uses'])
    return {'files': files, 'symbols': symbols, 'comments': comments, 'note': note}


def write(graph, out):
    """CODEMAP.md (each code file: what it defines, imports, is imported by, and what nothing uses) and COMMENTS.md."""
    syms = collections.defaultdict(list)
    for s in graph['symbols']:
        syms[s['file']].append(s)
    n_un = sum(1 for s in graph['symbols'] if s['state'] == 'unused')
    n_maybe = sum(1 for s in graph['symbols'] if s['state'] == 'maybe')
    L = ['# Code map', '',
         f'Made by `scripts/inventory.py` with `scripts/code_graph.py`: every function, class, method and top-level constant in '
         f'gidi, gidi-game and gidi-data, read by the parsers ({graph["note"]}). '
         f'{len(graph["symbols"])} pieces of code in {len(graph["files"])} files: {n_un} used nowhere, {n_maybe} used only by '
         'name where their file is not imported (a hint: a call by string, or dead). "Imported by" is Python imports; a '
         "page's scripts share its names. A file run as a script (by a shell line, Blender, the board) shows in "
         'INVENTORY.md\'s "Refs", not here.', '']
    bad = [k for k, f in graph['files'].items() if f['error']]
    if bad:
        L += ['## Files the parser could not read', ''] + [f'- `{k}`: {graph["files"][k]["error"]}' for k in sorted(bad)] + ['']
    L += ['## Used nowhere (by file)', '']
    for k in sorted(syms):
        un = [s for s in syms[k] if s['state'] == 'unused']
        if un:
            L.append(f'- `{k}`: ' + ', '.join(f'`{s["owner"] + "." if s["owner"] else ""}{s["name"]}` ({s["kind"]}, line {s["line"]})' for s in un))
    L += ['', '## Every code file', '']
    for k in sorted(graph['files']):
        f = graph['files'][k]
        ss = syms.get(k, [])
        L.append(f'### `{k}`')
        L.append(f'{len(ss)} defined ({sum(1 for s in ss if s["state"] == "used")} used, '
                 f'{sum(1 for s in ss if s["state"] == "maybe")} maybe, {sum(1 for s in ss if s["state"] == "unused")} unused). '
                 f'Imports: {", ".join(f"`{i}`" for i in f["imports"]) or "none of ours"}. '
                 f'Imported by: {", ".join(f"`{i}`" for i in sorted(f["imported_by"])) or "nothing"}.')
        out_used = [s for s in ss if s['used_in']]
        if out_used:
            L.append('Used elsewhere: ' + '; '.join(f'`{s["name"]}` in ' + ', '.join(f'`{u}`' for u in s['used_in'][:4]) for s in out_used[:30]))
        L.append('')
    open(os.path.join(out, 'CODEMAP.md'), 'w').write('\n'.join(L) + '\n')

    by = collections.defaultdict(list)
    for c in graph['comments']:
        by[c['file']].append(c)
    C = ['# Comments that name what does not exist', '',
         'Made by `scripts/inventory.py` with `scripts/code_graph.py`. Every comment and docstring in the three repos is read '
         'for the code names it mentions (`backticked` words, snake_case, camelCase, name()); each must exist as a name in '
         'the code, a file, a map schema field or a record key. These do not: the comment is out of date, has a typo, or '
         'names something outside the repos (a Blender or Unreal API, a library), which is fine and can be read past. '
         f'{len(graph["comments"])} comments in {len(by)} files.', '']
    for k in sorted(by):
        C.append(f'## `{k}`')
        for c in sorted(by[k], key=lambda c: c['line']):
            C.append(f'- line {c["line"]}: {", ".join(f"`{n}`" for n in c["names"])}. "{c["text"]}"')
        C.append('')
    open(os.path.join(out, 'COMMENTS.md'), 'w').write('\n'.join(C) + '\n')

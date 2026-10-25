"""The documents as a vault, for scripts/inventory.py (owner, 24 Oct: "use word matching to know what every document is
meant for, like an Obsidian vault; if a document is sort of an orphan, look into it and see its use").

For every markdown document in gidi, gidi-game and gidi-data:
  links     the files it points to: markdown links, [[wiki links]], and every path or file name it mentions
  backlinks the files that point to it (the inventory's "Refs": any mention of its name or path), split into documents
            and code
  for       what it is for, from its own words: its title, its first line, and the words that mark it out from the
            other documents (tf-idf: frequent in it, rare in the rest)
  related   the three documents whose words are closest to its own (cosine of the tf-idf vectors)
An orphan is a document nothing points to; a near-orphan is one only the inventory's own pages (CODEBASE.md) point to.
Both are listed first in VAULT.md with what they are for and their nearest documents, so each can be read and either
linked from where it belongs, moved to history, or deleted. vault.json holds the graph (nodes and links) for a viewer.
"""
import collections
import json
import math
import os
import re

WORD = re.compile(r"[a-z][a-z'-]{3,}")
STOP = set('''this that with from have will they them their there then than what when where which while were been being
also into onto over under only just each every some more most much many such other others these those your ours here
about after before again because both does doing done down during few further hers himself itself myself same should
very would could can't cannot into it's let's isn't aren't wasn't didn't doesn't don't shan't won't the and for are but
not you all any can had her was one our out day get has him his how man new now old see two way who boy did its let put
say she too use like make made first last next owner needs need used uses using file files line lines read reads
keep kept still back away want wants call calls called says said take takes even well know shows show seen look
looks part parts thing things same give gives open runs time times'''.split())
LINK = re.compile(r'\[[^\]]*\]\(([^)\s#]+)[^)]*\)|\[\[([^\]|#]+)')
PATH = re.compile(r'(?<![\w/.~-])((?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|js|mjs|html|json|ini|blend|csv|tsv))\b')


def tokens(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'`[^`]*`|https?://\S+|\(([^)]*\.\w+)\)', ' ', t)
    return [w.strip("'-") for w in WORD.findall(t.lower()) if w.strip("'-") not in STOP]


def build(rows, texts):
    """rows: the inventory's file rows (with refs_in); texts: {(repo, path): text}."""
    docs = {f'{r["repo"]}:{r["path"]}': r for r in rows
            if r['path'].endswith('.md') and (r['repo'], r['path']) in texts and not r['path'].startswith('docs/inventory/')}
    keys = set(f'{r["repo"]}:{r["path"]}' for r in rows)
    by_base = collections.defaultdict(list)
    for k in keys:
        by_base[os.path.basename(k.split(':', 1)[1])].append(k)

    def resolve(repo, here, p):
        p = p.strip().strip('<>')
        if p.startswith(('http', 'mailto')):
            return None
        for cand in (os.path.normpath(os.path.join(os.path.dirname(here), p)), os.path.normpath(p.lstrip('/'))):
            if f'{repo}:{cand}' in keys:
                return f'{repo}:{cand}'
        base = os.path.basename(p if '.' in os.path.basename(p) else p + '.md')
        c = sorted(by_base.get(base, []), key=lambda k: (k.split(':')[0] != repo, k))
        return c[0] if c else None

    # words: tf-idf over the documents
    toks = {k: tokens(texts[(r['repo'], r['path'])]) for k, r in docs.items()}
    df = collections.Counter(w for ts in toks.values() for w in set(ts))
    n = len(docs)
    vec = {}
    for k, ts in toks.items():
        tf = collections.Counter(ts)
        v = {w: (c / max(1, len(ts))) * math.log((1 + n) / (1 + df[w])) for w, c in tf.items() if df[w] < n * 0.5}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vec[k] = {w: x / norm for w, x in v.items()}

    def cos(a, b):
        if len(a) > len(b):
            a, b = b, a
        return sum(x * b.get(w, 0) for w, x in a.items())

    out = {}
    for k, r in docs.items():
        repo, path = k.split(':', 1)
        t = texts[(repo, path)]
        links = set()
        for m in LINK.finditer(t):
            tgt = resolve(repo, path, m.group(1) or m.group(2))
            if tgt and tgt != k:
                links.add(tgt)
        for m in PATH.finditer(t):
            tgt = resolve(repo, path, m.group(1))
            if tgt and tgt != k:
                links.add(tgt)
        refs = [x for x in r.get('refs_in', []) if not x.split(':', 1)[1].startswith('docs/inventory/')]
        from_docs = sorted(x for x in refs if x.endswith('.md'))
        from_code = sorted(x for x in refs if not x.endswith('.md'))
        title = next((l.lstrip('#').strip() for l in t.splitlines() if l.startswith('#')), '')
        top = sorted(vec[k].items(), key=lambda kv: -kv[1])[:8]
        related = sorted(((cos(vec[k], vec[j]), j) for j in docs if j != k), reverse=True)[:3]
        state = 'orphan' if not refs else 'near-orphan' if all(x.endswith('decisions/CODEBASE.md') for x in refs) else 'linked'
        out[k] = {'title': title, 'summary': r.get('summary', ''), 'changed': r.get('changed', ''), 'lines': r.get('lines'),
                  'words': [w for w, _ in top], 'links': sorted(links), 'from_docs': from_docs, 'from_code': from_code,
                  'related': [(round(s, 2), j) for s, j in related if s > 0], 'state': state}
    return out


def write(vault, out):
    orph = [k for k, d in vault.items() if d['state'] == 'orphan']
    near = [k for k, d in vault.items() if d['state'] == 'near-orphan']

    def entry(k, d):
        rel = '; '.join(f'`{j}` ({s})' for s, j in d['related'])
        return [f'### `{k}`',
                f'**{d["title"] or "(no title)"}**. {d["summary"]}',
                f'For: {", ".join(d["words"])}. Last changed {d["changed"] or "?"}, {d["lines"]} lines.',
                f'Links to {len(d["links"])}: {", ".join(f"`{x}`" for x in d["links"][:12])}{" ..." if len(d["links"]) > 12 else ""}',
                f'Backlinks: {len(d["from_docs"])} documents ({", ".join(f"`{x}`" for x in d["from_docs"][:8])}{" ..." if len(d["from_docs"]) > 8 else ""}), '
                f'{len(d["from_code"])} code files ({", ".join(f"`{x}`" for x in d["from_code"][:5])}).',
                f'Nearest in words: {rel or "none"}.', '']

    L = ['# The documents, as a vault', '',
         'Made by `scripts/inventory.py` with `scripts/doc_vault.py`: every markdown document in gidi, gidi-game and gidi-data, '
         'what it is for (its title, first line and the words that mark it out), what it links to, what points to it, and '
         'the documents nearest it in words. The repo folders open as a vault in Obsidian as they are; `vault.json` holds '
         'the same graph.', '',
         f'{len(vault)} documents: {len(orph)} orphans (nothing points to them), {len(near)} near-orphans (only '
         'CODEBASE.md or OLD-MAP.md do).', '', '## Orphans', '']
    for k in sorted(orph):
        L += entry(k, vault[k])
    L += ['## Near-orphans', '']
    for k in sorted(near):
        L += entry(k, vault[k])
    L += ['## Every document, by folder', '']
    folder = None
    for k in sorted(vault):
        f = os.path.dirname(k)
        if f != folder:
            L.append(f'## {f or "(top)"}')
            folder = f
        L += entry(k, vault[k])
    open(os.path.join(out, 'VAULT.md'), 'w').write('\n'.join(L) + '\n')
    nodes = [{'id': k, 'title': d['title'], 'state': d['state'], 'words': d['words']} for k, d in vault.items()]
    links = [{'from': k, 'to': x} for k, d in vault.items() for x in d['links']]
    json.dump({'nodes': nodes, 'links': links}, open(os.path.join(out, 'vault.json'), 'w'), indent=1)

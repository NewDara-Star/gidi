"""Have we done this already? python3 scripts/find.py <word> [<word> ...] [--map] [--all]

CLAUDE.md, "Search before saying or building" (owner, 31 Oct): before telling the owner how something in Gidi works,
proposing an idea, or writing a new tool, builder, material or check, search what exists. This searches the three
repos (gidi, gidi-game, gidi-data): every tracked text file's lines, and the commit messages on every branch. Each
word brings in the words listed with it in decisions/WORDS.md (the same idea under other names). A word matches as a
word start, case aside (`rust` finds rusty).

Files are ranked by how many of the query's words they hit (each word with its synonyms counts once), then by hits.
The map's records (gidi map/, map-stamps/) are left out unless --map: they name every street and would bury the rest.
Code is listed apart from the rest, 15 files each. --all prints every matching line, not the first three per file.
A repo that can't be read stops the search with an error: a search that quietly skipped a repo would say "nothing
found" when it hadn't looked."""
import os
import re
import subprocess
import sys

GIDI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS = {'gidi': GIDI, 'gidi-game': os.path.expanduser('~/gidi-game'), 'gidi-data': os.path.expanduser('~/gidi-data')}
WORDS = os.path.join(GIDI, 'decisions', 'WORDS.md')
SKIP_MAP = (':(exclude)map/', ':(exclude)map-stamps/')
SKIP = (':(exclude)docs/inventory/', ':(exclude)docs/hand/realnames.txt')   # made by scripts (inventory.py, realnames.py)
CODE = ('.py', '.sh', '.js', '.mjs', '.html', '.ush', '.usf', '.cpp', '.h')


def groups():
    """The synonym groups: each bullet line of WORDS.md, its words lower-cased."""
    out = []
    for line in open(WORDS, encoding='utf-8'):
        if line.startswith('- '):
            out.append([w.strip().lower() for w in line[2:].split(',') if w.strip()])
    return out


def expand(word, gs):
    """The word and every word grouped with it."""
    w = word.lower()
    found = {w}
    for g in gs:
        if w in g:
            found.update(g)
    return sorted(found)


def pattern(words):
    """A word start, in the POSIX form git grep and git log read (their -E has no \\b: it matches nothing, silently)."""
    return r'(^|[^[:alnum:]_])(' + '|'.join(re.escape(w).replace(r'\ ', '[ _-]?') for w in words) + ')'


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
    if r.returncode not in (0, 1):   # git grep: 1 is "no match"
        sys.exit(f'find.py: git {args[0]} failed in {repo}: {r.stderr.strip()}')
    return r.stdout


def search(query, with_map=False):
    """{(repo, file): {qi: [(line no, text)]}} for the lines, and [(repo, commit line, {qi})] for the commits."""
    gs = groups()
    pats = [pattern(expand(q, gs)) for q in query]
    lines, commits = {}, []
    for name, repo in REPOS.items():
        if not os.path.isdir(os.path.join(repo, '.git')) and not os.path.isfile(os.path.join(repo, '.git')):
            sys.exit(f'find.py: {name} is not at {repo}; nothing was searched')
        spec = ['--', '.'] + (list(SKIP) + ([] if with_map else list(SKIP_MAP)) if name == 'gidi' else [])
        for qi, p in enumerate(pats):
            for row in git(repo, 'grep', '-I', '-n', '-i', '-E', p, *spec).splitlines():
                f, n, text = row.split(':', 2)
                lines.setdefault((name, f), {}).setdefault(qi, []).append((int(n), text.strip()[:160]))
        log = {}
        for qi, p in enumerate(pats):
            for row in git(repo, 'log', '--all', '--oneline', '-i', '-E', f'--grep={p}').splitlines():
                log.setdefault(row, set()).add(qi)
        commits += [(name, row, qs) for row, qs in log.items()]
    return pats, lines, commits


def main(argv):
    with_map, every = '--map' in argv, '--all' in argv
    query = [a for a in argv if not a.startswith('--')]
    if not query:
        sys.exit(__doc__)
    pats, lines, commits = search(query, with_map)
    gs = groups()
    for q in query:
        print(f'{q}: {", ".join(expand(q, gs))}')
    ranked = sorted(lines.items(), key=lambda kv: (-len(kv[1]), -sum(len(v) for v in kv[1].values()), kv[0]))
    for title, part in (('code', [r for r in ranked if r[0][1].endswith(CODE)]),
                        ('notes, decisions, recipes and the rest', [r for r in ranked if not r[0][1].endswith(CODE)])):
        print(f'\n{len(part)} files: {title}')
        for (repo, f), hits in part[:15]:
            rows = sorted({r for v in hits.values() for r in v})
            print(f'  {repo}/{f}  ({len(hits)}/{len(query)} words, {len(rows)} lines)')
            for n, text in rows if every else rows[:3]:
                print(f'      {n}: {text}')
        if len(part) > 15:
            print(f'  ... {len(part) - 15} more')
    commits.sort(key=lambda c: -len(c[2]))
    print(f'\n{len(commits)} commits')
    for repo, row, qs in commits[:20]:
        print(f'  {repo} {row[:150]}  ({len(qs)}/{len(query)})')
    if not ranked and not commits:
        print('\nNothing found. Before calling it new, try other words; add any that should have matched to decisions/WORDS.md.')


if __name__ == '__main__':
    main(sys.argv[1:])

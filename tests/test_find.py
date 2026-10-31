"""scripts/find.py, down the ways it could lie: python3 tests/test_find.py (exit 1 on a failure).
Each case is a way the search could say "nothing found" when something was there, or say it looked when it didn't."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import find as F  # noqa: E402

fails = []


def check(what, got, want):
    if got != want:
        fails.append(f'{what}: got {got!r}, want {want!r}')


# the pattern is one git really reads: a regex form git's -E doesn't know (\b) matched nothing, silently (31 Oct)
pat = F.pattern(['rust'])
for text, want in (('rusty panel', True), ('the rust', True), ('trust me', False), ('in_rust', False)):
    # through grep -E, the POSIX form git's -E follows (git grep can't read stdin)
    r = subprocess.run(['grep', '-q', '-i', '-E', pat], input=text, text=True)
    check(f'word start: rust in {text!r}', r.returncode == 0, want)

# the words: a search for "slider" also searches "dial" (the 31 Oct miss: the Wear dial, called a slider)
check('slider brings in dial', 'dial' in F.expand('slider', F.groups()), True)
check('an unlisted word stays itself', F.expand('zzqx', F.groups()), ['zzqx'])

# end to end: the 31 Oct question finds the paint material that answers it
pats, lines, commits = F.search(['slider', 'bus'])
check('slider + bus finds gidi_paint.py', ('gidi-game', 'Content/Python/gidi_paint.py') in lines, True)
check('a common word finds many files (the search reads, not zero)', len(F.search(['danfo'])[1]) > 20, True)

# a repo that isn't there stops the search, never a quiet "nothing found"
saved = dict(F.REPOS)
F.REPOS['gidi-data'] = '/nonexistent/gidi-data'
try:
    F.search(['danfo'])
    check('a missing repo stops the search', 'carried on', 'stopped')
except SystemExit as e:
    check('a missing repo stops the search', 'not at' in str(e), True)
F.REPOS.clear(); F.REPOS.update(saved)

# the map's records are left out unless asked for
check('map/ left out by default', any(f.startswith('map/') for (r, f) in F.search(['danfo'])[1] if r == 'gidi'), False)

if fails:
    print('\n'.join(fails))
    sys.exit(1)
print('find.py: all cases pass')

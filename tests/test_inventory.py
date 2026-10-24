"""The inventory's code graph and comment check, down the four paths: python3 tests/test_inventory.py (exit 1 on a failure).
Each case is a way the checker could lie: calling dead code used, letting a comment vouch for itself, missing a name
built in an f-string, or reading nothing and passing."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import code_graph as C  # noqa: E402

fails = []


def check(what, got, want):
    if got != want:
        fails.append(f'{what}: got {got!r}, want {want!r}')


def states(texts):
    return {s['name']: s['state'] for s in C.build({}, texts, set())['symbols']}


# happy: a helper called, a module's function called through its import
a = 'import b\ndef helper(): return 1\ndef dead(): return helper()\nX = 3\nprint(b.used_by_a(), X)\n'
b = 'def used_by_a(): return 2\ndef never(): return 3\n'
s = states({('gidi', 'scripts/a.py'): a, ('gidi', 'scripts/b.py'): b})
check('helper called in its file', s['helper'], 'used')
check('function called through an import', s['used_by_a'], 'used')
# sad: nothing calls it
check('a function nothing calls', s['dead'], 'unused')
check('a module function nothing imports', s['never'], 'unused')
# idiot-proof: a function that only calls itself is not used
s = states({('gidi', 'scripts/r.py'): 'def loop(n):\n    return loop(n - 1)\n'})
check('recursion is not a use', s['loop'], 'unused')

# comments: a name that exists nowhere is caught, also inside a docstring (a docstring can't vouch for itself)
t = '# uses `frobnicate_widget` and grab_tiles()\ndef f():\n    """Calls draw_roofs and camelThing."""\n    return 1\n'
names = sorted(n for c in C.build({}, {('gidi', 'scripts/z.py'): t}, set())['comments'] for n in c['names'])
check('comment names that exist nowhere', names, ['camelThing', 'draw_roofs', 'frobnicate_widget', 'grab_tiles'])
# a name the code really has, and one built from an f-string prefix, pass
t = "def draw_roofs(): pass\n# draw_roofs() then glass_rear\nx = f'glass_{n}'\nrear = 1\n"
check('real names pass', C.build({}, {('gidi', 'scripts/y.py'): t}, set())['comments'], [])
# a file name is checked as a file, not as code
t = '# reads map_first.json\nx = 1\n'
check('a file name is not a code name', C.build({}, {('gidi', 'scripts/w.py'): t}, set())['comments'], [])
# tragedy: a file that doesn't parse is said, not skipped
g = C.build({}, {('gidi', 'scripts/bad.py'): 'def (:\n'}, set())
check('a broken file is reported', bool(g['files']['gidi:scripts/bad.py']['error']), True)

# JavaScript, by the TypeScript parser: a function only another script on the page calls is used
if C.find_ts():
    page = '<script src="lib.js"></script><script>go()</script>'
    g = C.build({}, {('gidi', 'web/p.html'): page, ('gidi', 'web/lib.js'): 'function go() {}\nfunction idle() {}\n// calls go()\n'}, set())
    s = {x['name']: x['state'] for x in g['symbols']}
    check('js function called by the page', s.get('go'), 'used')
    check('js function nothing calls', s.get('idle'), 'unused')
else:
    fails.append('no TypeScript compiler: the JavaScript cases could not run')

print('\n'.join(fails) or 'test_inventory: all cases pass')
sys.exit(1 if fails else 0)

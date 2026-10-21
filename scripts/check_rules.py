"""Every rule in decisions/DECISIONS.md has a row in decisions/CHECKS.md saying what holds it (owner, 21 Oct 2026: gaps must not
turn up only when someone asks). Fails on a rule with no row; lists the rules marked GAP. Usage: python3 scripts/check_rules.py"""
import re
import sys

rules = [m.strip() for m in re.findall(r'^- \*\*([^*]+)\*\*', open('decisions/DECISIONS.md').read(), re.M)]
rows = {}
for l in open('decisions/CHECKS.md'):
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    if len(c) == 3 and c[0] not in ('Rule', '---'):
        rows[c[0]] = c[2]
missing = [r for r in rules if r not in rows]
gaps = [(r, rows[r]) for r in rules if r in rows and 'GAP' in rows[r]]
print('%-5s %-34s %s' % ('PASS' if not missing else 'FAIL', 'R* every rule has a check', '%d rules; no row: %s' % (len(rules), '; '.join(missing) or 'none')))
for r, c in gaps:
    print('GAP   %-34s %s' % (r[:34], c))
sys.exit(1 if missing else 0)

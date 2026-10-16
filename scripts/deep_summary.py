# All districts against their studies on one page (docs/data/deep-check/*.json, from scripts/deep_check.py).
# Usage: python3 scripts/deep_summary.py [out.md]      prints a table; with a path, writes it as markdown too
import json, os, sys

ORDER = ['border', 'bazaar', 'jungle', 'port', 'maze', 'hub', 'railside', 'capital', 'estate', 'foodgate', 'watertown', 'oldshore',
         'oldisland', 'heights', 'frontier', 'airport', 'yaba']
NAMES = {'border': 'The Border', 'bazaar': 'The Bazaar', 'jungle': 'Jungle City', 'port': 'The Port', 'maze': 'The Maze', 'hub': 'The Hub',
         'railside': 'Railside', 'capital': 'The Capital', 'estate': 'The Estate', 'foodgate': 'Food Gate', 'watertown': 'Water Town',
         'oldshore': 'Old Shore', 'oldisland': 'Old Island', 'heights': 'The Heights', 'frontier': 'The Frontier', 'airport': 'The Airport', 'yaba': 'Saba'}
COLS = [('buildings per km2 (built squares)', 'Density'), ('ground built over', 'Cover'), ('touching', 'Touching'), ('under 40 m2', 'Small'),
        ('footprint median m2', 'House size'), ('storeys 3+ (by area)', '3+ storeys'), ('drivable km per km2 (whole land)', 'Streets'),
        ('line to the street, deg', 'Skew')]
rows = []
for d in ORDER:
    f = f'docs/data/deep-check/{d}.json'
    if not os.path.exists(f):
        continue
    C = json.load(open(f)); M = C['measures']
    cells = []
    for k, lab in COLS:
        m = M.get(k) or {}
        g, r = m.get('gidi'), m.get('real')
        if g is None or not r:
            cells.append('—'); continue
        off = (g - r) / r
        cells.append(f"{off:+.0%}" + (' ⚠' if abs(off) > 0.2 else ''))
    ok = sum(1 for c in cells if '⚠' not in c and c != '—')
    rows.append(f"| {NAMES[d]} | {C['buildings']:,} | {C['squares']} | " + ' | '.join(cells) + f" | {ok}/{len(cells)} |")
head = '| District | Buildings | Squares | ' + ' | '.join(l for k, l in COLS) + ' | Within 20% |\n|' + '---|' * (len(COLS) + 4)
out = head + '\n' + '\n'.join(rows)
print(out)
if len(sys.argv) > 1:
    open(sys.argv[1], 'w').write('Each cell is Gidi against its real inspiration (0% = the same; ⚠ = more than 20% off). "Squares" = built 500 m squares measured (under 5: a small sample).\n\n' + out + '\n')

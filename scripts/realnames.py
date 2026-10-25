"""Gidi's names are its own: no name on the map may share its core with a real name (decisions: invented names only).

The list of real name cores is docs/hand/realnames.txt; check_map.py fails on a map name whose core is on it. The list
was gathered on 21 Oct from the old map's twin streets, their photo notes and Overture names near them (git tag
before-cleanup-25oct, scripts/realnames.py gather()); it covers the places the old map studied, not all of Lagos.
"""
import os
import re

FILE = 'docs/hand/realnames.txt'
GENERIC = {'road', 'street', 'close', 'avenue', 'crescent', 'way', 'lane', 'drive', 'st', 'rd', 'ave', 'the', 'old', 'new', 'market', 'church',
           'mosque', 'school', 'link', 'bridge', 'expressway', 'service', 'estate', 'park', 'garage', 'motor', 'bus', 'stop', 'junction', 'oshodi',
           'surulere', 'lagos', 'unnamed', 'none'}


def core(n):
    return ' '.join(w for w in re.findall(r"[a-zà-ÿ']+", (n or '').lower()) if w not in GENERIC and len(w) > 1)


def cores():
    return set(open(FILE).read().split('\n')[1:]) - {''} if os.path.exists(FILE) else set()

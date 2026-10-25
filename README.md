# Gidi

The city for an open-world game: Gidi is real Lagos miniaturised, 51 districts, each street and place drawn by hand
from the real one. This repo is the map. It holds every road, block, building and thing the game puts there, as
records in `map/`, plus the drawing board they are made on. The game itself (the builders and the Unreal project) is
[NewDara-Star/gidi-game](https://github.com/NewDara-Star/gidi-game).

**Rule zero:** study yes, lift no. We study real Lagos (data, Google Earth and Street View) and draw our own. No
outline, picture or name is copied in. Invented names only.

## Start here
- `CLAUDE.md` and `decisions/` (NOW, DECISIONS, IDEAS): where the work stands and the owner's rules
- `decisions/CODEBASE.md`: what each part of the three repos is, and what is live, old or history
- `docs/MAP-FORMAT.md`: the map's records

## Use
- The drawing board: `~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, then
  `http://127.0.0.1:8779/web/board.html?frame=new`
- Check the map: `~/.venvs/gidi/bin/python scripts/check_map.py map` (PASS means no problem; fields still to fill are counted on its TODO line; `--strict` fails on them) and
  `scripts/check_rules.py`
- What the repos hold: `~/.venvs/gidi/bin/python scripts/inventory.py` (writes `docs/inventory/`)

The old generated city (13-21 Oct) was deleted on 25 Oct; git tag `before-cleanup-25oct` holds it, and `docs/OLD-MAP-LESSONS.md` what it taught.

## Data credits
- OpenStreetMap contributors (ODbL): the old map
- Microsoft Building Footprints (ODbL) and Overture Maps: building and place numbers
- Google Open Buildings 2.5D Temporal (CC-BY 4.0)
- ESA WorldCover 2021 (CC-BY 4.0)
- WorldPop 2020 (CC-BY 4.0)
- Copernicus DEM GLO-30 (© DLR/Airbus, provided under COPERNICUS by the European Union and ESA)

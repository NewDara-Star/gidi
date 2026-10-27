# Data sources, and what to delete later

Everything we've downloaded to study real Lagos lives on Daramola's Mac in `~/gidi-data/research/data/` (about 20 GB, mostly Google's 2.5D tiles). The OpenStreetMap extract (`lagos.osm.pbf`, 55 MB) is gone from the Mac; the repo's links to it were removed on 24 Oct.

**The rule:**
- We **study** these files: numbers, patterns, our own eyes on Google Earth and Street View.
- **Nothing is copied into Gidi.** No outlines, no imagery, no names.

**Delete when** the map is properly built and the game is deep in development (owner, 15 Oct 2026). Until then, keep everything, so the studies can be rerun.

| Folder or file | What it is | Licence | Size | Used for | Delete when |
|---|---|---|---|---|---|
| `open-buildings-2023/` | Google Open Buildings 2.5D Temporal, 2016–2023: where buildings are, how tall, roughly how many, on a 4 m grid | CC BY 4.0 | 17 GB | storey bands in 11 district studies | map final |
| `open-buildings-v3/lagos_open_buildings_v3.csv.gz` | Google Open Buildings v3: every building outline in Lagos (4.09 million) | CC BY 4.0 | 433 MB | real density, sizes and structure (the old map's `scripts/study_google.py`, deleted 25 Oct) | map final |
| `open-buildings-v3/103_buildings.csv.gz` | the same, for a whole slice of West Africa (the Lagos file was cut from it) | CC BY 4.0 | 2.0 GB | nothing more: the Lagos cut replaces it | **now, if you want the space** |
| `ms-buildings/` | Microsoft building outlines over Lagos (4 tiles), a second machine-traced set | CDLA Permissive 2.0 | 186 MB | cross-check of Google's | map final |
| `overture-lagos/` | Overture Maps for Lagos: 63,204 places (shops, churches, salons, event planners...), infrastructure, land use, roads, land | CDLA / ODbL by layer | 42 MB | what each district has, beyond OSM | map final |
| `yaba_*` | early samples for Yaba (Google, Overture) | as above | ~13 MB | superseded by the Lagos files | map final |
| `dem/`, `lagos_copernicus_glo30_dsm.tif` | Copernicus 30 m surface model | Copernicus licence | 95 MB | `web/terrain.json` | keep until Unreal has its Landscape |
| `worldcover/` | ESA WorldCover 10 m, 2021 | CC BY 4.0 | 271 MB | empty land vs untraced land | map final |
| `worldpop/` | WorldPop 100 m population, 2020 | CC BY 4.0 | 59 MB | people per district | map final |
| `lagos.osm.pbf` (repo folder) | OpenStreetMap, Lagos | ODbL | 55 MB | roads, land use, the first district studies | deleted (24 Oct: not on the Mac) |
| `deep-cache/` | the buildings of each district's study area, cut once from Google's and Microsoft's files (`scripts/deep_prep.py`, deleted 25 Oct with the old map) | as above | ~250 MB | the deep study (`docs/DEEP-STUDY.md`) | map final |
| `study-*.pkl` (scratch folders) | each district study's extract | from the above | small | regenerating districts | map final |
| `~/gidi-data/tools/CodeWalker/` | CodeWalker's C# source (github.com/dexyfex/CodeWalker, shallow clone 27 Oct, owner's OK), read to open GTA V's archives for study | copyright dexyfex (no licence file; parts MIT) | 22 MB | DECISIONS "Study other games from the inside" | when the GTA study is done |
| `~/gidi-data/tools/gta5-nativedb/natives.json` | the public list of GTA V script command names (github.com/alloc8or/gta5-nativedb-data, 27 Oct, owner's OK), read to name the commands in GTA V's mission scripts for study | community project (see its repo) | 2.8 MB | DECISIONS "Study other games from the inside" | when the GTA study is done |
| `~/gidi-data/tools/ppsspp/` | PPSSPP's PSP decryption source only (github.com/hrydgard/ppsspp, sparse clone of Core/ELF and ext/libkirk, 27 Oct, owner's OK), read to decrypt the owner's Vice City Stories program for study | GPL-2.0 (PPSSPP), libkirk's own notices | 4.4 MB | DECISIONS "Study other games from the inside" | when the PSP study is done |

**What can't be downloaded:**
- Google Earth imagery and Street View: for looking only.
- Mapillary: no access.

Google has about 10,000 km of Street View in Lagos.

#!/bin/bash
# Gidi data pull. Run on the Mac (Terminal): bash ~/Real-world/research/data/pull-data.sh
# Downloads open datasets for the Lagos study into this folder. Safe to stop and re-run: finished files are skipped.
cd "$(dirname "$0")"
get() { # url file
  if [ -s "$2" ] && [ ! -e "$2.part" ]; then echo "have  $2"; return; fi
  echo "get   $2"; curl -fL --retry 3 -C - -o "$2.part" "$1" && mv "$2.part" "$2" || echo "FAILED $1"
}
mkdir -p open-buildings-2023 dem worldcover worldpop
# 1. Google Open Buildings 2.5D Temporal, 2023, tiles over Lagos (CC-BY 4.0) - building height + presence
while read -r u; do get "$u" "open-buildings-2023/$(basename "$u")"; done < open-buildings-2023/lagos_keep_2023.txt
# 2. Copernicus DEM 30 m (ground height), 1x1 degree tiles over Lagos State
for e in 002 003 004; do n="Copernicus_DSM_COG_10_N06_00_E${e}_00_DEM"; get "https://copernicus-dem-30m.s3.amazonaws.com/$n/$n.tif" "dem/$n.tif"; done
# 3. ESA WorldCover 10 m, 2021 (trees, built-up, water, bare) - CC-BY 4.0
for t in N06E000 N06E003; do get "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_${t}_Map.tif" "worldcover/$t.tif"; done
# 4. WorldPop 100 m population, Nigeria 2020 (constrained, UN-adjusted) - CC-BY 4.0
get "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/maxar_v1/NGA/nga_ppp_2020_UNadj_constrained.tif" "worldpop/nga_ppp_2020_UNadj_constrained.tif"
# 5. Location check for the eastern tiles (Epe, Ibeju-Lekki): first 128 KB of each only
mkdir -p open-buildings-2023/headers
while read -r u; do f="open-buildings-2023/headers/$(basename "$u")"; [ -s "$f" ] || curl -s -r 0-131071 -o "$f" "$u"; done < open-buildings-2023/east_tiles_2023.txt
echo "done. Sizes:"; du -sh open-buildings-2023 dem worldcover worldpop

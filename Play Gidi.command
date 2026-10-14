#!/bin/zsh
# Double-click to open Gidi (the map, with the 2D, 3D and Mock tabs) as a desktop app.
# The first run installs the Mock's packages; every run rebuilds it so it's never stale.
cd "$(dirname "$0")/mock" || exit 1
[ -d node_modules ] || npm install
if [ ! -f ../web/city/manifest.json ]; then
  echo "The city tiles aren't built yet: run  python3 blender/city_run.py  first (see mock/README.md)."
fi
[ -f ../web/city/walk/carwalls.json ] || python3 ../tools/walkmap/bake_walk.py
npm run desktop

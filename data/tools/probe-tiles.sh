#!/bin/bash
# Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minute.
cd "$(dirname "$0")"; mkdir -p open-buildings-2023/headers
while read -r u; do f="open-buildings-2023/headers/$(basename "$u")"; [ -s "$f" ] || curl -s -r 0-131071 -o "$f" "$u"; done < open-buildings-2023/lagos_tiles_2023.txt
echo "probe done: $(ls open-buildings-2023/headers | wc -l) headers"

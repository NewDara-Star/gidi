# Worked example of the new map format

One short home street in district d15 (20 m, invented names), written as the map would hold it (docs/MAP-FORMAT.md):

- `d15/district.json`: the district record (a stand-in outline round the example).
- `d15/plan.json`: the road, three plots, three frontages (a shop step, a lean-to front, a wall with a gate), two buildings (a two-storey shop-under-flats and a bungalow stamped from test spot ot175), a lean-to, a table stall, a pole and its wire, a parked okada, a buka place.
- `d15/dress/128_60.json`: both buildings' faces (windows, doors, shopfronts, a balcony, stains, add-ons, a sign, an awning), the bungalow's and the lean-to's roof sheets, the gate wall's bays, posters on the pole, the left gutter's slabs, tar and mud patches, a relief grid, a pothole and a rut, litter, the lean-to's goods and two person spots.

Check it: `~/.venvs/gidi/bin/python scripts/check_map.py docs/map-format-example --kit schema/kit_reads.json`

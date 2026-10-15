# Gidi v2: the layout

Chosen by the owner on 15 Oct 2026: a fictional Lagos with its real shape first, our own twists after. The first map (8.8 × 6.7 km) was boxy and squeezed the far ends of Lagos in.

![Gidi v2 at 1:4](img/layout-v2.png)

## The rule
- **One even scale, 1:4.**
  - Each district sits where its inspiration really is in Lagos: the centre of its study area, divided by four, with no turning and nothing squeezed.
  - The map is 19.6 × 9.3 km, with about 55 km² of built city: 2.5 times the old one.
- **Every shape is drawn fresh.**
  - The coast, the lagoon, the harbour and the creeks are smooth curves of our own.
  - The district borders bend like roads and creeks.
  - Nothing is traced from the real map.
- **New districts:**
  - **The Airport,** where Murtala Muhammed sits between Ikeja (the Capital), Agege and Alimosho (Railside) and Oshodi (the Hub).
  - **Yaba/Akoka,** between Mushin (the Maze) and the lagoon, beside Bariga and Makoko (Water Town), with the university on the waterfront.
- **Lagos Island is an island:** the harbour to its west, the lagoon to its north, a creek to the east.
- **Growing later:** 1:2.5 (29 × 12 km) is the same layout rescaled, if we ever want more room.

## The arterials and the rail (drawn by hand, each playing its real counterpart's part)

| Gidi | Plays the part of | Runs |
|---|---|---|
| Coastal Expressway | Lagos–Badagry Expressway | the Border, the Bazaar, Jungle City, to the Port, inland of the creek |
| Ring Road | Apapa–Oshodi Expressway | the Port, the Hub, the Airport |
| Agege Road | Agege Motor Road (west) | the Capital to Railside |
| Ayinde Avenue | Agege Motor Road / Obafemi Awolowo Way | the Hub, past the Airport, the Capital, the Estate |
| Northern Road | Ikorodu Road | Yaba, Food Gate, round the lagoon to Old Shore |
| The Long Bridge | Third Mainland Bridge | from Yaba, curving out over the lagoon, to the Island |
| Wharf Bridge | Eko and Carter Bridges | across the harbour to the Island |
| Waterfront Drive, Creek Bridge | Ozumba Mbadiwe and Falomo | the Island across the creek to the Heights |
| Peninsula Expressway | Lekki–Epe Expressway | the Heights east through the Frontier |
| Rail | the Lagos–Ibadan line | Agege, Oshodi, Mushin, Yaba, to the harbour |

## Files
- `scripts/layout_v2.py` writes `web/layout-v2.json`: size, water, districts, anchors, arterials and rail. It also writes the picture.
- The map build doesn't read it yet.

## Next
1. The map build takes its frame from `layout-v2.json`: districts, water, arterials, rail. The terrain is rebuilt for it.
2. Every district is rebuilt from Google's data in its new place, then frozen. Food Gate's frozen content moves with it as a block.
3. Hand placement.

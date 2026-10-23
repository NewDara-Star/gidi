"""Stitch legacy/blender/out/kinds/*.jpg into one labelled sheet: python3 legacy/blender/montage.py [out.jpg] [cols]"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'kinds')
tiles = json.load(open(os.path.join(d, 'tiles.json')))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(d, '..', 'kinds-sheet.jpg')
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 4
w, h = 480, 300
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), 'white')
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 22)
except OSError:
    font = ImageFont.load_default()
for i, (k, p) in enumerate(tiles):
    im = Image.open(p).resize((w, h))
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, 0, 12 + 13 * len(k), 34), fill=(20, 20, 20))
    dr.text((8, 5), k, fill=(255, 220, 60), font=font)
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=88)
print('WROTE', out)

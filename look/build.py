# Bundles the look test into one self-contained page: python3 look/build.py
import json, os
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(here, p)).read()
s = rd('src/shell.html')
s = s.replace('<!--THREE-->', '<script>' + rd('three.min.js') + '</script>')
s = s.replace('<!--DATA-->', '<script>window.AREA=' + json.dumps(json.load(open(os.path.join(here, 'area.json'))), separators=(',', ':')) + ';</script>')
s = s.replace('<!--CODE-->', '<script>\n' + '\n'.join(rd('src/' + f) for f in ['tex.js', 'kit.js', 'world.js', 'main.js']) + '\n</script>')
open(os.path.join(here, 'ladi-lane-look.html'), 'w').write(s)
print(len(s))

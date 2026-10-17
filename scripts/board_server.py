"""The drawing board's server (owner, 16 Oct 2026: "we should hand draw... know where something meets something").

python3 scripts/board_server.py [--port 8777]   then open http://127.0.0.1:8777/web/board.html

Serves the repo's files, and saves every edit made on the board into its district's hand file (web/hand/<d>.json, the
"edits" list, the same format scripts/hand.py applies), so the bake, the checks and the 3D all follow the drawing.

Edits made since the last bake are also kept in web/board-pending.json, so the board can draw them before the bake has
run: each carries the time it was made, and the board shows the ones newer than web/gidi-data.js.

Local only: it listens on 127.0.0.1, accepts only the hand-file operations below, and writes only web/hand/ and that file.
"""
import http.server
import json
import os
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND = os.path.join(ROOT, 'web', 'hand')
PENDING = os.path.join(ROOT, 'web', 'board-pending.json')
DATA = os.path.join(ROOT, 'web', 'gidi-data.js')
OPS = {'add building', 'delete building', 'move building', 'add furniture', 'delete furniture', 'move furniture',
       'add place', 'move place', 'delete place', 'add parcel', 'delete parcel', 'add monument', 'move monument',
       'delete monument', 'add zone', 'add street', 'delete street', 'cut street', 'name road', 'set surface', 'name',
       'reshape building', 'reshape parcel', 'reshape zone', 'reshape street',
       'cut wall', 'delete wall', 'add wall', 'add gate', 'delete gate'}
LOCK = threading.Lock()   # one edit at a time: two quick saves must not overwrite each other
ROAD_OPS = {'add street', 'delete street', 'cut street', 'name road', 'reshape street'}   # a frozen district needs a thaw bake for these


def districts():
    return {f[:-5] for f in os.listdir(HAND) if f.endswith('.json')}


def load_pending():
    try:
        return json.load(open(PENDING))
    except (OSError, ValueError):
        return []


def save_json(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(obj, fh, separators=(',', ':'))
    os.replace(tmp, path)


def numbers_ok(v):
    """Every number in an edit is finite (no NaN or infinity from a slip of the mouse)."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v == v and abs(v) < 1e7
    if isinstance(v, list):
        return all(numbers_ok(x) for x in v)
    if isinstance(v, dict):
        return all(numbers_ok(x) for x in v.values())
    return True


class Board(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, fmt, *args):
        if self.command != 'GET':
            sys.stderr.write('%s %s\n' % (self.command, fmt % args))

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if self.path.endswith('.js') or self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-store')   # always the latest bake and board code
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/pending'):
            return self.send_json({'data_time': os.path.getmtime(DATA), 'edits': load_pending()})
        return super().do_GET()

    def do_POST(self):
        with LOCK:
            return self.post()

    def post(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
        except ValueError:
            return self.send_json({'error': 'not JSON'}, 400)
        if self.path == '/api/edit':
            d, e = body.get('d'), body.get('edit')
            if d not in districts():
                return self.send_json({'error': f'no district {d!r}'}, 400)
            if not isinstance(e, dict) or e.get('op') not in OPS or not numbers_ok(e):
                return self.send_json({'error': 'not a hand-file edit'}, 400)
            e = dict(e, note=(str(e.get('note') or '') + ' (drawing board)').strip())
            path = os.path.join(HAND, d + '.json')
            H = json.load(open(path))
            H.setdefault('edits', []).append(e)
            save_json(path, H)
            P = load_pending()
            P.append({'t': time.time(), 'd': d, 'edit': e, 'thaw': e['op'] in ROAD_OPS})
            save_json(PENDING, P)
            return self.send_json({'ok': True, 'pending': len(P)})
        if self.path == '/api/undo':   # takes back the last edit made on the board, if it's still the last in its hand file
            P = load_pending()
            if not P:
                return self.send_json({'error': 'nothing to undo'}, 400)
            last = P[-1]
            path = os.path.join(HAND, last['d'] + '.json')
            H = json.load(open(path))
            if not H.get('edits') or H['edits'][-1] != last['edit']:
                return self.send_json({'error': 'that edit has been baked or changed since; undo it with a new edit'}, 409)
            H['edits'].pop()
            save_json(path, H)
            P.pop()
            save_json(PENDING, P)
            return self.send_json({'ok': True, 'pending': len(P)})
        return self.send_json({'error': 'unknown'}, 404)


if __name__ == '__main__':
    port = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8777
    print(f'Drawing board: http://127.0.0.1:{port}/web/board.html')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Board).serve_forever()

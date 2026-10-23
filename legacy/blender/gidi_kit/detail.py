"""Detail level for the whole kit: 'full' for renders, 'web' for the streamed city (flat roof
sheets, flat lettering, lighter bars and louvres, fewer cylinder segments)."""
LEVEL = 'full'


def web():
    return LEVEL == 'web'


def segs(n):
    return max(6, n // 2) if LEVEL == 'web' else n

# On the web, lettering is not geometry: each sign or painted text is recorded here (world matrix,
# size, text, colours) and the browser paints it onto a canvas texture.
SIGNS = []


def record_text(m, text, size, col, bg=None, w=None, h=None, hand=False):
    SIGNS.append(dict(m=[list(r) for r in m], text=text, size=size, col=list(col), bg=list(bg) if bg else None, w=w, h=h, hand=hand))

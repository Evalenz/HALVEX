"""Genera los SVG maestros del logo y la lista de trabajos de render (PNG y PDF)."""
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ISO_D, WM_D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'HALVEX-logos')
NEGRO, BLANCO, GRAF = '#111214', '#FFFFFF', '#1A1B1E'
COLS = {'negro': NEGRO, 'blanco': BLANCO}

ISO = ''.join(f'<path d="{d}"/>' for d in ISO_D)
WM = ''.join(f'<path d="{d}"/>' for d in WM_D)


def iso_g(x, y, h):
    s = h / 152
    return f'<g transform="translate({x} {y}) scale({s:.6f}) translate(-24 -20)">{ISO}</g>'


def wm_g(x, y, cap):
    return f'<g transform="translate({x} {y}) scale({cap/100:.6f})">{WM}</g>'


# piezas: nombre -> (viewBox x, y, w, h, contenido)
PIEZAS = {
    'imagotipo-horizontal': (0, -30, 784, 160, iso_g(0, -30, 160) + wm_g(232, 0, 100)),
    'imagotipo-vertical': (0, 0, 552, 388, iso_g(166, 0, 220) + wm_g(0, 284, 100)),
    'logotipo': (0, -4, 552, 108, wm_g(0, 0, 100)),
    'isotipo': (24, 20, 152, 152, f'<g>{ISO}</g>'),
}
CARPETA = {'imagotipo-horizontal': '01-imagotipo-horizontal', 'imagotipo-vertical': '02-imagotipo-vertical',
           'logotipo': '03-logotipo', 'isotipo': '04-isotipo'}
ANCHOS = {'imagotipo-horizontal': (4000, 1600, 600), 'imagotipo-vertical': (3000, 1200, 500),
          'logotipo': (4000, 1600, 600), 'isotipo': (2048, 1024, 512)}


def svg(vb, body, color, bg=None, pad=0):
    x, y, w, h = vb
    x2, y2, w2, h2 = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    rect = f'<rect x="{x2}" y="{y2}" width="{w2}" height="{h2}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x2} {y2} {w2} {h2}" width="{w2}" height="{h2}">'
            f'<title>HALVEX</title>{rect}<g fill="{color}">{body}</g></svg>')


jobs = []
os.makedirs(OUT, exist_ok=True)
for name, (x, y, w, h, body) in PIEZAS.items():
    d = os.path.join(OUT, CARPETA[name])
    for sub in ('svg', 'png', 'pdf'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    for cname, col in COLS.items():
        base = f'halvex-{name}-{cname}'
        p = os.path.join(d, 'svg', base + '.svg')
        open(p, 'w').write(svg((x, y, w, h), body, col))
        for W in ANCHOS[name]:
            jobs.append({'svg': p, 'png': os.path.join(d, 'png', f'{base}-{W}px.png'), 'width': W, 'transparent': True})
        jobs.append({'svg': p, 'pdf': os.path.join(d, 'pdf', base + '.pdf'), 'w': w, 'h': h})
    # con fondo (área de respeto incluida): negro sobre blanco y blanco sobre negro
    x_resp = 36 * (160 / 152) if name != 'isotipo' else 36
    if name == 'imagotipo-vertical': x_resp = 36 * (220 / 152)
    if name == 'logotipo': x_resp = 15 * 2.4
    for cname, col, bg in (('negro-sobre-blanco', NEGRO, BLANCO), ('blanco-sobre-negro', BLANCO, NEGRO)):
        base = f'halvex-{name}-{cname}'
        p = os.path.join(d, 'svg', base + '.svg')
        open(p, 'w').write(svg((x, y, w, h), body, col, bg, pad=round(x_resp, 2)))
        jobs.append({'svg': p, 'png': os.path.join(d, 'png', f'{base}-{ANCHOS[name][1]}px.png'), 'width': ANCHOS[name][1], 'transparent': False})

# 05 · iconos, favicon, avatares y redes
d5 = os.path.join(OUT, '05-iconos-y-redes')
os.makedirs(d5, exist_ok=True)


def icono(size, fg, bg, frac=.58):
    ih = 152 * frac / (1 - frac) if False else None
    # lienzo 1000: isotipo de alto 1000*frac centrado
    h = 1000 * frac
    s = h / 152
    off = (1000 - h) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="{size}" height="{size}"><title>HALVEX</title>'
            f'<rect width="1000" height="1000" fill="{bg}"/><g fill="{fg}" transform="translate({off} {off}) scale({s:.6f}) translate(-24 -20)">{ISO}</g></svg>')


for cname, fg, bg in (('negro', BLANCO, NEGRO), ('blanco', NEGRO, BLANCO)):
    p = os.path.join(d5, f'halvex-icono-{cname}.svg')
    open(p, 'w').write(icono(1024, fg, bg))
    for sz in (1024, 512, 192, 180, 64, 48, 32, 16):
        nm = {180: 'apple-touch-icon-180px', 192: 'android-192px'}.get(sz, f'{sz}px')
        jobs.append({'svg': p, 'png': os.path.join(d5, f'halvex-icono-{cname}-{nm}.png'), 'width': sz, 'transparent': False})
    pa = os.path.join(d5, f'halvex-avatar-redes-{cname}.svg')
    open(pa, 'w').write(icono(1080, fg, bg, .46))
    jobs.append({'svg': pa, 'png': os.path.join(d5, f'halvex-avatar-redes-{cname}-1080px.png'), 'width': 1080, 'transparent': False})

# portada LinkedIn 1584 x 396 y cabecera X 1500 x 500
for nm, W, H in (('portada-linkedin', 1584, 396), ('cabecera-x', 1500, 500)):
    cap = H * .16
    ww = 5.52 * cap
    body = wm_g((W - ww) / 2, (H - cap) / 2, cap)
    p = os.path.join(d5, f'halvex-{nm}.svg')
    open(p, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{GRAF}"/><g fill="#FFFFFF">{body}</g></svg>')
    jobs.append({'svg': p, 'png': os.path.join(d5, f'halvex-{nm}-{W}x{H}.png'), 'width': W, 'transparent': False})

# firma de correo (2x para pantallas retina)
p = os.path.join(OUT, '01-imagotipo-horizontal', 'svg', 'halvex-imagotipo-horizontal-negro.svg')
jobs.append({'svg': p, 'png': os.path.join(d5, 'halvex-firma-correo-240px.png'), 'width': 240, 'transparent': True})

json.dump(jobs, open(os.path.join(OUT, '..', 'id', 'jobs.json'), 'w'), indent=0)
print(len(jobs), 'trabajos')

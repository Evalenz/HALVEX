import base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, '..', 'fonts', 'plex.css')).read()

# Paleta
LACRE = '#9A3324'
LACRE_P = '#6E2419'
TINTA = '#111214'
ACERO = '#65676C'
NIEBLA = '#A3A4A8'
PIEDRA = '#EFEDE8'
BLANCO = '#FFFFFF'
FILETE = '#DAD8D2'

ISO_D = ('M24 20H60L96.2 172Z', 'M176 20H140L103.8 172Z')
WM_D = ['M0 0H15V43H63V0H78V100H63V57H15V100H0Z', 'M102 100L146 -3L190 100H173.6L146 37.3L118.4 100Z',
        'M214 0H229V85H276V100H214Z', 'M268 0H284.4L312 62.7L339.6 0H356L312 103Z',
        'M378 0H440V15H393V42.5H434V57.5H393V85H440V100H378Z',
        'M464 0H482L508 37.14L534 0H552L517 50L552 100H534L508 62.86L482 100H464L499 50Z']

DEFS = ('<svg width="0" height="0" style="position:absolute"><defs>'
        '<symbol id="wm" viewBox="0 -4 552 108">' + ''.join(f'<path d="{d}"/>' for d in WM_D) + '</symbol>'
        '<symbol id="iso" viewBox="24 20 152 152">' + ''.join(f'<path d="{d}"/>' for d in ISO_D) + '</symbol>'
        '</defs></svg>')


def img64(name):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'img', name + '.jpg'), 'rb').read()).decode()


def iso(style='', color=TINTA, cls=''):
    return (f'<svg class="{cls}" viewBox="24 20 152 152" style="{style}">'
            f'<path fill="{color}" d="{ISO_D[0]}"/><path fill="{color}" d="{ISO_D[1]}"/></svg>')


def wm(style='', color=TINTA, cls=''):
    return f'<svg class="{cls}" viewBox="0 -4 552 108" style="{style};fill:{color}"><use href="#wm" y="-4" width="552" height="108"/></svg>'


def iso_g(x, y, h, color):
    """isotipo como <g> dentro de otro svg: esquina sup. izq. (x,y), alto h"""
    s = h / 152
    return (f'<g transform="translate({x} {y}) scale({s:.5f}) translate(-24 -20)" fill="{color}">'
            f'<path d="{ISO_D[0]}"/><path d="{ISO_D[1]}"/></g>')


def wm_g(x, y, cap, color):
    s = cap / 100
    return (f'<g transform="translate({x} {y}) scale({s:.5f})" fill="{color}">' + ''.join(f'<path d="{d}"/>' for d in WM_D) + '</g>')


# Imagotipo horizontal: letra 100, isotipo 1,6 x letra (160), separación 0,45 x isotipo (72)
H_VB = '0 -30 784 160'
def horiz(iso_c=LACRE, wm_c=TINTA, style='', cls=''):
    return (f'<svg class="{cls}" viewBox="{H_VB}" style="{style}">' + iso_g(0, -30, 160, iso_c) + wm_g(232, 0, 100, wm_c) + '</svg>')


# Imagotipo vertical: isotipo 220 centrado, separación 64, palabra 552 x 100
V_VB = '0 0 552 388'
def vert(iso_c=LACRE, wm_c=TINTA, style='', cls=''):
    return (f'<svg class="{cls}" viewBox="{V_VB}" style="{style}">' + iso_g(166, 0, 220, iso_c) + wm_g(0, 284, 100, wm_c) + '</svg>')


def lum(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmyk(h):
    r, g, b = [x / 255 for x in rgb(h)]
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


CSS = FONTS + r'''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"IBM Plex Sans",Arial,sans-serif;color:#111214;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-weight:400}
svg{display:block}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;padding:15mm 18mm 0}
.page:last-child{page-break-after:auto;break-after:auto}
.mono{font-family:"IBM Plex Mono",monospace;font-size:6.6pt;letter-spacing:.06em;text-transform:uppercase;line-height:1.5}
.run{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:2.6mm;border-bottom:.25mm solid #111214}
.run .l{display:flex;gap:6mm}
.run b{font-weight:500}
.foot{position:absolute;left:18mm;right:18mm;bottom:10mm;display:flex;justify-content:space-between;color:#65676C}
.dk .run{border-color:rgba(255,255,255,.6)}
.dk .foot{color:rgba(255,255,255,.6)}
.steel{color:#65676C}
.lac{color:#9A3324}
.rh{display:inline-block;width:2.2mm;height:2.2mm;background:#9A3324;transform:rotate(45deg);margin-right:2.6mm;vertical-align:.25mm}
h1,h2{font-weight:200;letter-spacing:-.03em;line-height:1.02}
h1 b,h2 b{font-weight:400}
.h1{font-size:44pt}
.h2{font-size:30pt}
.h3{font-size:15pt;font-weight:400;letter-spacing:-.01em;line-height:1.2}
.lead{font-size:12pt;font-weight:300;line-height:1.5}
.txt{font-size:9pt;line-height:1.6}
.txt+.txt{margin-top:2.6mm}
.g12{display:grid;grid-template-columns:repeat(12,1fr);column-gap:5mm}
.rule{border-top:.25mm solid #111214}
.hair{border-top:.2mm solid #DAD8D2}
.k{font-family:"IBM Plex Mono",monospace;font-size:6.6pt;letter-spacing:.06em;text-transform:uppercase;color:#65676C}
.dk{background:#111214;color:#fff}
.lacbg{background:#9A3324;color:#fff}
.lacbg .run{border-color:rgba(255,255,255,.7)}
.lacbg .foot{color:rgba(255,255,255,.75)}
'''


def doc(title, pages):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style>'
            f'<style>{EXTRA}</style></head><body>{DEFS}' + ''.join(pages) + '</body></html>')


EXTRA = ''


def page(inner, num, sec, docname, cls='', run=True):
    r = ''
    if run:
        r = (f'<div class="run mono"><span class="l"><b>HALVEX</b><span>{docname}</span></span>'
             f'<span>{sec}</span></div>')
    f = f'<div class="foot mono"><span>Edición 1.0 · Noviembre 2026</span><span>{num:02d}</span></div>'
    return f'<section class="page {cls}">{r}{inner}{f}</section>'

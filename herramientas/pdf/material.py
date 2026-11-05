import os, re, random
HERE = os.path.dirname(os.path.abspath(__file__))
V = {'__file__': os.path.join(HERE, 'visual2.py'), '__name__': 'v2'}
exec(open(os.path.join(HERE, 'visual2.py')).read(), V)
for k, v in V.items():
    if not k.startswith('__') and k not in ('P', 'n', 'page', 'divider', 'toc', 'DOC', 'PART'):
        globals()[k] = v

DOC = 'Material corporativo'
PARTS = {'01': 'Tarjetas de visita', '02': 'Papelería y documentos', '03': 'Packaging y etiquetas', '04': 'Rótulos y señalética',
         '05': 'Uniforme y acreditación', '06': 'Carteles y publicidad', '07': 'Vehículos y objetos'}
CSS += r'''
.scn{position:relative;overflow:hidden}
.ob{position:absolute}
.cap2{display:grid;grid-template-columns:22mm 1fr 1.2fr;column-gap:6mm;align-items:baseline;margin-top:4mm}
.cap2 .nn{font-weight:200;font-size:30pt;letter-spacing:-.04em;line-height:.9}
.tg{font-family:"IBM Plex Mono",monospace;font-size:6.2pt;letter-spacing:.06em;text-transform:uppercase}
'''
SH = 'box-shadow:0 .5mm 1mm rgba(0,0,0,.16),0 3mm 7mm rgba(0,0,0,.20)'
SHD = 'box-shadow:0 .5mm 1mm rgba(0,0,0,.35),0 3mm 8mm rgba(0,0,0,.45)'
BG_P = 'background:radial-gradient(ellipse at 28% 18%,#F7F6F2 0%,#ECE9E3 55%,#E0DDD6 100%)'
BG_G = 'background:radial-gradient(ellipse at 28% 18%,#2A2B30 0%,#1B1C20 55%,#121316 100%)'

PAGES, TOCI = [], []
cur = {'part': ''}
FOL = '<div class="fol"><span class="m s">Edición 1.0 · Noviembre 2026</span><span class="n">%%N%%</span></div>'


def run(chap):
    p = cur['part']
    return (f'<div class="run m"><span><b>HALVEX</b>&nbsp;&nbsp;&nbsp;{DOC}</span>'
            f'<span>{("Parte " + p + " · " + PARTS[p]) if p else ""}</span><span>{chap}</span></div>')


def add(inner, chap, num=None, title=None, cls=''):
    if num: TOCI.append((cur['part'], num, title, len(PAGES)))
    PAGES.append(f'<section class="page {cls}">{run(chap)}{inner}{FOL}</section>')


def chh(num, t, k=''):
    return f'<div class="ch"><span class="num">{num}</span><h2>{t}</h2><span class="k m s">{k}</span></div>'


def divider(p, photo, intro, pos='center'):
    cur['part'] = p
    PAGES.append(('DIV', p, photo, intro, pos))


def scene_page(num, title, desc, scene, h=146, bg=BG_P, spec=''):
    add(f'''<div class="scn" style="margin-top:4mm;height:{h}mm;{bg}">{scene}</div>
<div class="cap2"><span class="nn">{num}</span><span class="h3" style="font-weight:300;font-size:16pt;letter-spacing:-.02em">{title}</span><span class="p s">{desc}{(" " + spec) if spec else ""}</span></div>''',
        f'{num} · {title}', num, title)


def ob(x, y, html, rot=0, z=1, sh=SH):
    return f'<div class="ob" style="left:{x}mm;top:{y}mm;transform:rotate({rot}deg);z-index:{z};{sh}">{html}</div>'


def lbl(t, d=''):
    return f'<div class="lbl"><b>{t}</b><span>{d}</span></div>'


def pt(v, s):
    return f'{v*s:.2f}pt'


def bars_s(ws, s, col='#E2E0DA', h=1.0, gap=1.4):
    return ''.join(f'<div style="height:{h*s:.2f}mm;background:{col};margin-bottom:{gap*s:.2f}mm;width:{w}%"></div>' if w else f'<div style="height:{(h+gap)*s:.2f}mm"></div>' for w in ws)


def barcode(w, h, seed=3, col=NEG):
    rnd = random.Random(seed)
    x, out = 0, []
    while x < 96:
        bw = rnd.choice((1, 1, 2, 3)); gap = rnd.choice((1, 1, 2))
        out.append(f'<rect x="{x}" y="0" width="{bw}" height="40"/>'); x += bw + gap
    return f'<svg viewBox="0 0 100 40" preserveAspectRatio="none" style="width:{w}mm;height:{h}mm;display:block"><g fill="{col}">{"".join(out)}</g></svg>'


# ------------------------------------------------------------------ renders 3D
import base64, io
from PIL import Image as _Img
RDIR = os.path.join(HERE, '..', 'real')
def REN(name):
    pth = os.path.join(RDIR, name + '.png')
    if not os.path.exists(pth):
        return None
    buf = io.BytesIO(); _Img.open(pth).convert('RGB').save(buf, 'JPEG', quality=88)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
def photo(name, pos='center'):
    u = REN(name)
    return f'<div style="position:absolute;inset:0;background:url({u}) {pos}/cover"></div>' if u else None


# ------------------------------------------------------------------ piezas
def card_front(s=1):
    return f'<div style="width:{85*s}mm;height:{55*s}mm;background:{NEG};display:flex;align-items:center;justify-content:center">{iso(f"width:{15*s}mm;height:{15*s}mm", BLA)}</div>'


def card_back(s=1, name='Nombre Apellido', role='Cargo', mail='nombre@halvex.com'):
    return (f'<div style="width:{85*s}mm;height:{55*s}mm;background:#FBFAF8;position:relative">'
            f'<div style="position:absolute;left:{6*s}mm;top:{6*s}mm">{horiz(NEG, NEG, f"width:{28*s}mm;height:auto")}</div>'
            f'<div style="position:absolute;left:{6*s}mm;bottom:{6*s}mm"><p style="font-size:{pt(9,s)};font-weight:500">{name}</p><p style="font-size:{pt(6.6,s)};color:{ACE};margin-top:{.5*s}mm">{role}</p>'
            f'<p class="m" style="font-size:{pt(5.2,s)};margin-top:{3*s}mm;line-height:1.6">+34 000 000 000<br>{mail}</p></div>'
            f'<span class="m" style="position:absolute;right:{6*s}mm;bottom:{6*s}mm;font-size:{pt(5.2,s)};color:{ACE};text-align:right;line-height:1.6">Madrid<br>halvex.com</span></div>')


def letter(s=.3, body=True):
    b = (f'<div style="position:absolute;left:{20*s}mm;top:{62*s}mm;width:{120*s}mm">{bars_s([36, 28, 0, 22], s, h=1.6, gap=2.2)}</div>'
         f'<div style="position:absolute;left:{20*s}mm;top:{110*s}mm;right:{20*s}mm">{bars_s([100, 97, 99, 92, 100, 64, 0, 100, 96, 98, 90, 100, 95, 72, 0, 30], s, h=1.4, gap=2.6)}</div>') if body else ''
    return (f'<div style="width:{210*s}mm;height:{297*s}mm;background:#FBFAF8;position:relative">'
            f'<div style="position:absolute;left:{20*s}mm;top:{18*s}mm">{horiz(NEG, NEG, f"width:{40*s}mm;height:auto")}</div>{b}'
            f'<div style="position:absolute;left:{20*s}mm;right:{20*s}mm;bottom:{12*s}mm;border-top:{max(.15, .25*s*3):.2f}mm solid {NEG};padding-top:{2*s}mm;display:flex;justify-content:space-between">'
            f'<span class="m" style="font-size:{pt(5.4,s)}">HALVEX · Madrid</span><span class="m" style="font-size:{pt(5.4,s)}">halvex.com · contacto@halvex.com</span></div></div>')


def envelope(s=.3, back=False, w=220, h=110, bg='#FBFAF8'):
    if back:
        return (f'<div style="width:{w*s}mm;height:{h*s}mm;background:{bg};position:relative"><svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">'
                f'<path d="M0 0L{w/2} {h*.55}L{w} 0" fill="#F1EFEA" stroke="#D8D6D0" stroke-width=".6"/><path d="M0 {h}L{w*.42} {h*.48}M{w} {h}L{w*.58} {h*.48}" stroke="#E2E0DA" stroke-width=".6" fill="none"/></svg>'
                f'<div style="position:absolute;left:50%;top:{h*.55*s - 9*s}mm;transform:translateX(-50%)">{iso(f"width:{7*s}mm;height:{7*s}mm", NEG)}</div></div>')
    return (f'<div style="width:{w*s}mm;height:{h*s}mm;background:{bg};position:relative"><div style="position:absolute;left:{10*s}mm;top:{10*s}mm">{horiz(NEG, NEG, f"width:{34*s}mm;height:auto")}</div>'
            f'<div style="position:absolute;left:{w*.5*s}mm;top:{h*.55*s}mm;width:{70*s}mm">{bars_s([60, 80, 50], s, h=1.8, gap=2.4)}</div>'
            f'<div style="position:absolute;right:0;top:0;bottom:0;width:{6*s}mm;background:{NEG}"></div></div>')


def compliment(s=.3):
    return (f'<div style="width:{210*s}mm;height:{99*s}mm;background:#FBFAF8;position:relative"><div style="position:absolute;left:{14*s}mm;top:{14*s}mm">{horiz(NEG, NEG, f"width:{36*s}mm;height:auto")}</div>'
            f'<p style="position:absolute;left:{14*s}mm;bottom:{14*s}mm;font-weight:200;font-size:{pt(14,s)};letter-spacing:-.02em">Con los saludos de</p>'
            f'<div style="position:absolute;right:{14*s}mm;bottom:{16*s}mm;width:{60*s}mm;border-top:{.25}mm solid {LIN}"></div></div>')


def folder(s=.3):
    return (f'<div style="width:{220*s}mm;height:{310*s}mm;background:{GRAF};position:relative"><div style="position:absolute;left:{18*s}mm;top:{18*s}mm">{horiz(BLA, BLA, f"width:{50*s}mm;height:auto")}</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;height:{70*s}mm;background:{NEG}"></div><span class="m" style="position:absolute;left:{18*s}mm;bottom:{24*s}mm;font-size:{pt(7,s)};color:{NIE}">Documentación confidencial</span></div>')


def notebook(s=.3):
    return (f'<div style="width:{148*s}mm;height:{210*s}mm;background:{NEG};position:relative"><div style="position:absolute;left:0;top:0;bottom:0;width:{8*s}mm;background:#25262B"></div>'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)">{iso(f"width:{36*s}mm;height:{36*s}mm", "#2B2C31")}</div>'
            f'<div style="position:absolute;right:{14*s}mm;top:0;bottom:0;width:{3*s}mm;background:#2B2C31"></div></div>')


def pen(s=.3, col=NEG):
    return (f'<div style="width:{140*s}mm;height:{9*s}mm;background:linear-gradient(180deg,#3A3B40,{col} 45%,#000);border-radius:{4.5*s}mm;position:relative">'
            f'<div style="position:absolute;left:{18*s}mm;top:-{1*s}mm;width:{40*s}mm;height:{3*s}mm;background:#55575C;border-radius:{1.5*s}mm"></div>'
            f'<span class="m" style="position:absolute;right:{30*s}mm;top:50%;transform:translateY(-50%);font-size:{pt(5,s)};color:#8A8C90">HALVEX</span></div>')


# ------------------------------------------------------------------ caja (proyección oblicua)
def box(w, h, d, front, top, side, fc=NEG, tc='#2A2B30', sc='#0B0B0D', fb=''):
    k = d * .5
    return (f'<div style="position:relative;width:{w+k}mm;height:{h+k}mm">'
            f'<div style="position:absolute;left:0;top:0;width:{w}mm;height:{k}mm;background:{tc};transform-origin:bottom left;transform:skewX(-45deg);overflow:hidden">{top}</div>'
            f'<div style="position:absolute;left:{w}mm;top:{k}mm;width:{k}mm;height:{h}mm;background:{sc};transform-origin:top left;transform:skewY(-45deg);overflow:hidden">{side}</div>'
            f'<div style="position:absolute;left:0;top:{k}mm;width:{w}mm;height:{h}mm;background:{fc};overflow:hidden;{fb}">{front}</div></div>')


def ctr(html):
    return f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{html}</div>'


# =================================================================== 01 TARJETAS
divider('01', 'hq-hero', 'La pieza que más se toca. Cartulina gruesa, negro mate y el isotipo en relieve.')

sc = (ob(22, 30, card_front(1.15), -14, 2) + ob(30, 40, card_front(1.15), -6, 3) + ob(128, 22, card_back(1.15), 9, 4)
      + ob(118, 86, card_back(1.15, 'Nombre Apellido', 'Dirección de Ingeniería'), -3, 5) + ob(36, 100, card_front(1.15), 4, 6))
scene_page('01', 'Tarjetas de visita', 'Anverso negro con el isotipo en golpe en seco; reverso blanco natural con imagotipo y datos.', photo('p2-tarjetas') or sc, bg=BG_P,
           spec='85 × 55 mm, cartulina de 400 g.')

dim = lambda w: f'<div style="display:flex;align-items:center;gap:2mm;margin-top:2mm"><span style="flex:1;border-top:.2mm solid {ACE}"></span><span class="m s">{w}</span><span style="flex:1;border-top:.2mm solid {ACE}"></span></div>'
vars_ = [('Dirección', 'Nombre Apellido', 'Consejero delegado'), ('Equipo', 'Nombre Apellido', 'Ingeniería de sistemas'), ('Genérica', 'HALVEX', 'Contacto general')]
vv = ''.join(f'<div>{ob_ if False else ""}<div style="{SH}">{card_back(.62, a if a != "HALVEX" else "HALVEX", c, "contacto@halvex.com" if t == "Genérica" else "nombre@halvex.com")}</div><p class="m s" style="margin-top:2mm">{t}</p></div>' for t, a, c in vars_)
add(f'''{chh('02', 'Tarjetas <b>· especificaciones</b>', 'Escala 1:1')}
<div style="display:grid;grid-template-columns:85mm 85mm 1fr;column-gap:10mm;margin-top:7mm;align-items:start">
 <div><div style="{SH}">{card_front()}</div>{dim('85 mm')}<p class="m s" style="margin-top:2mm">Anverso</p></div>
 <div><div style="{SH}">{card_back()}</div>{dim('85 mm')}<p class="m s" style="margin-top:2mm">Reverso</p></div>
 <div class="rows">
  <div class="row" style="grid-template-columns:24mm 1fr;padding:2.2mm 0"><span class="m s">Formato</span><span class="p">85 × 55 mm, esquinas rectas</span></div>
  <div class="row" style="grid-template-columns:24mm 1fr;padding:2.2mm 0"><span class="m s">Soporte</span><span class="p">Cartulina no estucada de 400 g, negra en anverso y blanco natural en reverso (duplex)</span></div>
  <div class="row" style="grid-template-columns:24mm 1fr;padding:2.2mm 0"><span class="m s">Impresión</span><span class="p">Serigrafía blanca (anverso) y negro K100 (reverso)</span></div>
  <div class="row" style="grid-template-columns:24mm 1fr;padding:2.2mm 0"><span class="m s">Acabado</span><span class="p">Isotipo con golpe en seco; canto negro</span></div>
 </div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,52.7mm) 1fr;column-gap:8mm;margin-top:8mm;align-items:end">{vv}<p class="p s">Tres variantes de reverso: dirección, equipo y genérica para recepción y eventos.</p></div>''',
    '02 · Especificaciones', '02', 'Especificaciones de la tarjeta')

# =================================================================== 02 PAPELERÍA
divider('02', 'hq-piramide', 'Carta, sobres, carpetas, documentos y sellos: todo lo que sale de la oficina con el nombre de HALVEX.')
sc = (ob(14, 14, letter(.43), -4, 2) + ob(100, 10, folder(.38), 6, 1) + ob(118, 92, envelope(.42), -8, 3) + ob(70, 98, card_front(.75), 12, 5)
      + ob(178, 18, notebook(.36), -10, 4) + ob(150, 120, pen(.55), -24, 6) + ob(30, 112, compliment(.36), 3, 4))
scene_page('03', 'Papelería', 'Carta, sobre, tarjetón, carpeta, cuaderno, tarjetas y bolígrafo: una misma familia en negro y blanco natural.', photo('p1-flatlay') or sc, bg=BG_G)

ann = lambda t: f'<span class="m" style="font-size:5.6pt;color:{ACE}">{t}</span>'
add(f'''{chh('04', 'Carta <b>A4</b>', '210 × 297 mm')}
<div style="display:grid;grid-template-columns:97mm 1fr;column-gap:14mm;margin-top:4mm">
 <div style="position:relative">
  <div style="{SH}">{letter(.46)}</div>
  <div style="position:absolute;left:-1mm;top:9mm;width:10mm;border-top:.2mm dashed {ACE}"></div>
 </div>
 <div>
  <div class="rows">
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Imagotipo</span><span class="p">40 mm de ancho, a 20 mm del borde izquierdo y 18 mm del superior.</span></div>
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Márgenes</span><span class="p">20 mm laterales; texto a partir de 110 mm desde arriba en la primera página.</span></div>
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Texto</span><span class="p">Plex Sans Regular 10/16 pt, alineado a la izquierda. Sustituta: Arial 10/15.</span></div>
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Pie</span><span class="p">Filete de 0,5 pt y datos de contacto en Plex Mono 7 pt.</span></div>
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Papel</span><span class="p">Offset no estucado blanco natural de 120 g. Impresión a una tinta (K).</span></div>
   <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Segunda hoja</span><span class="p">Solo el pie; sin imagotipo.</span></div>
  </div>
  <div style="display:flex;gap:6mm;margin-top:8mm;align-items:flex-end"><div style="{SH}">{letter(.2)}</div><div style="{SH}">{letter(.2, False).replace(horiz(NEG, NEG, f"width:{40*.2}mm;height:auto"), "")}</div><p class="p s" style="max-width:50mm">Primera hoja y hoja de continuación.</p></div>
 </div>
</div>''', '04 · Carta A4', '04', 'Carta A4')

c4 = (f'<div style="width:{229*.34}mm;height:{324*.34}mm;background:#F4F1EA;position:relative"><div style="position:absolute;left:5mm;top:5mm">{horiz(NEG, NEG, "width:20mm;height:auto")}</div>'
      f'<div style="position:absolute;left:30mm;top:52mm;width:40mm">{bars_s([70, 90, 60, 50], .4, h=2, gap=2.6)}</div><div style="position:absolute;left:0;right:0;bottom:0;height:8mm;background:{NEG}"></div></div>')
add(f'''{chh('05', 'Sobres', 'DL · C5 · C4')}
<div class="scn" style="height:112mm;margin-top:5mm;{BG_P}">
 {ob(14, 12, envelope(.5), -3, 2)}{ob(22, 60, envelope(.5, True), 4, 3)}{ob(140, 10, c4, 5, 2)}{ob(200, 40, envelope(.3, False, 229, 162), -6, 3)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Americano DL · 220 × 110 mm', 'Imagotipo arriba a la izquierda, canto negro y solapa con el isotipo.')}{lbl('Bolsa C4 · 229 × 324 mm', 'Kraft blanco con franja negra inferior para documentación.')}{lbl('C5 · 229 × 162 mm', 'Para informes doblados; mismas normas que el DL.')}</div>''',
    '05 · Sobres', '05', 'Sobres')

openf = (f'<div style="display:flex;{SHD}"><div style="width:{220*.36}mm;height:{310*.36}mm;background:{GRAF};position:relative"><div style="position:absolute;left:4mm;right:4mm;bottom:4mm;height:{100*.36}mm;background:#25262B;box-shadow:0 -.6mm 1mm rgba(0,0,0,.3)"></div></div>'
         f'<div style="width:{220*.36}mm;height:{310*.36}mm;background:{GRAF};position:relative;border-left:.3mm solid #101114"><div style="position:absolute;left:4mm;right:4mm;bottom:4mm;height:{100*.36}mm;background:#25262B;box-shadow:0 -.6mm 1mm rgba(0,0,0,.3)">'
         f'<div style="position:absolute;right:8mm;top:6mm;width:24mm;height:15mm;{SH}">{card_back(.28)}</div></div></div></div>')
add(f'''{chh('06', 'Carpeta <b>y tarjetón</b>', '220 × 310 mm')}
<div class="scn" style="height:118mm;margin-top:5mm;{BG_P}">
 {ob(14, 8, folder(.34), -4, 2, SHD)}{ob(100, 10, openf, 0, 3, '')}{ob(190, 20, compliment(.28), 8, 4)}{ob(196, 62, envelope(.28, True, 220, 110), -5, 5)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Carpeta cerrada', 'Cartulina grafito de 350 g con imagotipo en serigrafía blanca.')}{lbl('Carpeta abierta', 'Bolsillo interior y ranura para la tarjeta de visita.')}{lbl('Tarjetón · 210 × 99 mm', '«Con los saludos de», para acompañar envíos y regalos.')}</div>''',
    '06 · Carpeta y tarjetón', '06', 'Carpeta y tarjetón')


def a4p(s, inner, bg='#FBFAF8'):
    return f'<div style="width:{210*s}mm;height:{297*s}mm;background:{bg};position:relative;overflow:hidden">{inner}</div>'


s_ = .34
cov = a4p(s_, f'''<div style="position:absolute;inset:0;background:{NEG};color:#fff;padding:{16*s_}mm"><p class="m" style="font-size:{pt(6,s_*1.8)};color:{NIE}">Propuesta · Confidencial</p>
<p style="margin-top:{70*s_}mm;font-weight:200;font-size:{pt(34,s_*1.4)};letter-spacing:-.03em;line-height:1.05">Plataforma<br>de apoyo a la<br><b style="font-weight:400">decisión</b></p>
<div style="position:absolute;left:{16*s_}mm;right:{16*s_}mm;bottom:{16*s_}mm">{wm("width:100%;height:auto", BLA)}</div></div>''')
def inner_page(s, n_, t):
    return a4p(s, f'''<div style="padding:{14*s}mm"><div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:{2*s}mm"><span class="m" style="font-size:{pt(5.6,s*1.6)}">HALVEX · Propuesta</span><span class="m" style="font-size:{pt(5.6,s*1.6)}">{n_} · {t}</span></div>
<p style="font-weight:200;font-size:{pt(60,s*1.4)};letter-spacing:-.05em;line-height:.8;margin-top:{14*s}mm">{n_}</p><p style="font-weight:200;font-size:{pt(18,s*1.4)};letter-spacing:-.02em;margin-top:{5*s}mm">{t}</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:{8*s}mm;margin-top:{12*s}mm"><div>{bars_s([100, 96, 98, 90, 100, 60, 0, 100, 94, 97], s*2.2, h=1, gap=1.6)}</div><div>{bars_s([100, 94, 97, 92, 80, 0, 100, 96, 70], s*2.2, h=1, gap=1.6)}</div></div></div>''')
spread = f'<div style="display:flex;{SH}">{inner_page(s_, "02", "Enfoque")}<div style="width:.3mm;background:#D8D6D0"></div>{inner_page(s_, "03", "Arquitectura")}</div>'
add(f'''{chh('07', 'Documentos', 'Propuestas e informes')}
<div class="scn" style="height:118mm;margin-top:5mm;{BG_G}">
 {ob(16, 10, cov, -3, 2, SHD)}{ob(96, 14, spread, 0, 3, SHD)}
</div>
<div style="display:grid;grid-template-columns:1fr 2fr;column-gap:6mm">{lbl('Portada', 'Negro con el título en dos pesos y el logotipo a todo el ancho.')}{lbl('Interior', 'Cabecera con filete, número de capítulo grande y texto a dos columnas.')}</div>''',
    '07 · Documentos', '07', 'Propuestas e informes')


def form(s, title, rows=4):
    rr = ''.join(f'<div style="display:grid;grid-template-columns:3fr 1fr 1fr;gap:{2*s}mm;border-bottom:.15mm solid {LIN};padding:{2.6*s}mm 0"><div style="height:{1.4*s}mm;background:#E2E0DA;width:{w}%"></div><span class="m" style="font-size:{pt(5.4,s*1.6)};text-align:right">[ ]</span><span class="m" style="font-size:{pt(5.4,s*1.6)};text-align:right">[ ] €</span></div>' for w in (80, 62, 70, 55, 66)[:rows])
    return a4p(s, f'''<div style="padding:{14*s}mm">{horiz(NEG, NEG, f"width:{38*s}mm;height:auto")}
<div style="display:flex;justify-content:space-between;margin-top:{18*s}mm"><div><p class="m" style="font-size:{pt(5.4,s*1.6)};color:{ACE}">{title}</p><p style="font-size:{pt(14,s*1.6)};font-weight:300;margin-top:{1*s}mm">Nº [0000]</p></div><div style="text-align:right"><p class="m" style="font-size:{pt(5.4,s*1.6)};color:{ACE}">Fecha</p><p style="font-size:{pt(8,s*1.6)};margin-top:{1*s}mm">[dd/mm/aaaa]</p></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:{8*s}mm;margin-top:{12*s}mm"><div>{bars_s([80, 60, 70], s*2.2, h=1, gap=1.4)}</div><div>{bars_s([75, 65, 50], s*2.2, h=1, gap=1.4)}</div></div>
<div style="margin-top:{14*s}mm;border-top:.25mm solid {NEG}">{rr}</div>
<div style="display:flex;justify-content:flex-end;gap:{8*s}mm;margin-top:{6*s}mm;align-items:baseline"><span class="m" style="font-size:{pt(5.6,s*1.6)}">Total</span><span style="font-size:{pt(16,s*1.6)};font-weight:300">[ ] €</span></div>
<div style="position:absolute;left:{14*s}mm;right:{14*s}mm;bottom:{10*s}mm;border-top:.2mm solid {NEG};padding-top:{2*s}mm"><span class="m" style="font-size:{pt(4.6,s*1.6)};color:{ACE}">HALVEX · [Denominación social] · [NIF] · Madrid</span></div></div>''')
acta = a4p(.3, f'''<div style="padding:{14*.3}mm">{horiz(NEG, NEG, f"width:{38*.3}mm;height:auto")}<p class="m" style="font-size:{pt(5.4,.48)};color:{ACE};margin-top:{18*.3}mm">Acta de reunión</p><p style="font-size:{pt(14,.48)};font-weight:300;margin-top:{1*.3}mm">[Asunto]</p>
<div style="margin-top:{10*.3}mm">''' + ''.join(f'<div style="display:grid;grid-template-columns:1fr 3fr;border-top:.15mm solid {LIN};padding:{3*.3}mm 0"><span class="m" style="font-size:{pt(5,.48)};color:{ACE}">{t}</span><div>{bars_s([90, 70], .66, h=1, gap=1.2)}</div></div>' for t in ('Asistentes', 'Orden del día', 'Acuerdos', 'Próximos pasos', 'Responsables')) + '</div></div>')
add(f'''{chh('08', 'Formularios', 'Factura, presupuesto y acta')}
<div class="scn" style="height:118mm;margin-top:5mm;{BG_P}">
 {ob(20, 10, form(.32, "Factura"), -4, 2)}{ob(100, 8, form(.32, "Presupuesto", 5), 2, 3)}{ob(180, 12, acta, 6, 2)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Factura', 'Datos fiscales en el pie; total destacado en Light.')}{lbl('Presupuesto', 'Misma estructura; validez y condiciones al final.')}{lbl('Acta de reunión', 'Tabla de asistentes, acuerdos y responsables.')}</div>''',
    '08 · Formularios', '08', 'Formularios')


def stamp(text, w, rot):
    return (f'<div style="transform:rotate({rot}deg);border:.6mm solid {NEG};padding:1.6mm 3mm;opacity:.86;display:inline-block">'
            f'<span style="font-family:\'IBM Plex Mono\';font-weight:500;font-size:11pt;letter-spacing:.18em">{text}</span></div>')
round_stamp = (f'<svg viewBox="0 0 120 120" style="width:44mm;height:44mm;opacity:.86;transform:rotate(-8deg)"><defs><path id="cir" d="M60 60m-44 0a44 44 0 1 1 88 0a44 44 0 1 1-88 0"/></defs>'
               f'<circle cx="60" cy="60" r="56" fill="none" stroke="{NEG}" stroke-width="2"/><circle cx="60" cy="60" r="34" fill="none" stroke="{NEG}" stroke-width=".8"/>'
               f'<text font-family="IBM Plex Mono" font-size="9" letter-spacing="3.2" fill="{NEG}"><textPath href="#cir">HALVEX · MADRID · DOCUMENTO VERIFICADO ·</textPath></text>{iso_g(44, 44, 32, NEG)}</svg>')
stick = lambda t, bg, fg: f'<div style="background:{bg};color:{fg};padding:2mm 4mm;display:inline-flex;align-items:center;gap:2.4mm;{SH}">{iso("width:4mm;height:4mm", fg)}<span class="m" style="font-size:7pt;font-weight:500">{t}</span></div>'
add(f'''{chh('09', 'Sellos <b>y clasificación</b>', 'Confidencialidad de documentos')}
<div class="scn" style="height:112mm;margin-top:5mm;{BG_P}">
 {ob(18, 14, a4p(.32, f'<div style="position:absolute;left:8mm;top:6mm">{horiz(NEG, NEG, "width:13mm;height:auto")}</div><div style="position:absolute;left:8mm;top:26mm;right:8mm">{bars_s([100, 96, 98, 90, 100, 60, 0, 100, 94, 97, 92, 80], .8, h=1, gap=1.6)}</div><div style="position:absolute;left:14mm;top:58mm">{stamp("CONFIDENCIAL", 0, -6)}</div>'), -3, 2)}
 {ob(110, 18, f'<div style="background:#FBFAF8;padding:8mm 10mm;display:grid;gap:7mm">{stamp("CONFIDENCIAL", 0, 0)}{stamp("USO INTERNO", 0, 0)}{stamp("PÚBLICO", 0, 0)}</div>', 2, 2)}
 {ob(196, 14, f'<div style="background:#FBFAF8;padding:6mm">{round_stamp}</div>', -4, 3)}
 {ob(186, 82, stick("Confidencial", NEG, BLA), -3, 4)}{ob(212, 94, stick("Uso interno", BLA, NEG), 4, 4)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Sellos de clasificación', 'Plex Mono Medium con marco: Confidencial, Uso interno, Público.')}{lbl('Sello circular', 'Para validar documentos y entregas.')}{lbl('Adhesivos', 'Etiquetas de clasificación para carpetas y sobres.')}</div>''',
    '09 · Sellos y clasificación', '09', 'Sellos y clasificación')

# =================================================================== 03 PACKAGING
divider('03', 'hq-escaleras', 'Cajas, bolsas, etiquetas y precintos. La entrega también es parte de la seguridad.')
kit_top = ctr(horiz(BLA, BLA, 'width:40mm;height:auto'))
b1 = box(96, 26, 64, ctr(f'<span class="m" style="font-size:5.6pt;color:{NIE}">Kit de bienvenida</span>'), kit_top, '', NEG, '#1E1F23', '#0A0A0C')
b2 = box(56, 56, 40, ctr(iso('width:18mm;height:18mm', NEG)), ctr(wm('width:30mm;height:auto', NEG)), '', '#F6F4EF', '#FFFFFF', '#D9D6CF')
b3 = box(70, 18, 50, f'<div style="position:absolute;left:4mm;bottom:3mm">{horiz(BLA, BLA, "width:18mm;height:auto")}</div>', ctr(iso('width:10mm;height:10mm', '#3A3B40')), '', GRAF, '#26272B', '#101114')
bag = (f'<div style="position:relative;width:52mm;height:74mm"><svg viewBox="0 0 52 20" style="position:absolute;left:0;top:-14mm;width:52mm;height:20mm"><path d="M14 20Q14 2 26 2Q38 2 38 20" fill="none" stroke="{NEG}" stroke-width="1.2"/></svg>'
       f'<div style="position:absolute;inset:0;background:#F4F1EA;{SH}">{ctr(vert(NEG, NEG, "width:24mm;height:auto"))}</div><div style="position:absolute;right:0;top:0;bottom:0;width:6mm;background:linear-gradient(90deg,rgba(0,0,0,.05),rgba(0,0,0,.12))"></div></div>')
sc = ob(18, 46, b1, 0, 3, '') + ob(140, 30, b2, 0, 2, '') + ob(108, 92, b3, 0, 4, '') + ob(206, 46, bag, 0, 1, '')
sc += ''.join(f'<div class="ob" style="left:{x}mm;top:{y}mm;width:{w}mm;height:5mm;background:radial-gradient(ellipse at center,rgba(0,0,0,.28),transparent 70%)"></div>' for x, y, w in ((14, 104, 140), (134, 120, 100), (104, 136, 110), (200, 122, 66)))
scene_page('10', 'Packaging', 'Caja de bienvenida, caja de equipo, caja de envío y bolsa: negro, grafito y blanco natural, sin brillos.', sc, bg=BG_P)

items = [('Cuaderno', notebook(.2)), ('Bolígrafo', pen(.42)), ('Acreditación', f'<div style="width:30mm;height:46mm;background:#FBFAF8;position:relative"><div style="height:9mm;background:{NEG};display:flex;align-items:center;padding:0 2.6mm">{horiz(BLA, BLA, "width:13mm;height:auto")}</div><div style="width:11mm;height:14mm;background:#E2E0DA;margin:3mm 2.6mm 0"></div><p style="font-size:5pt;font-weight:500;margin:2mm 2.6mm 0">Nombre Apellido</p></div>'),
         ('Memoria USB', f'<div style="width:12mm;height:30mm;background:{NEG};position:relative;border-radius:1mm"><div style="position:absolute;left:3mm;right:3mm;top:-5mm;height:5mm;background:#9A9CA0"></div><div style="position:absolute;left:50%;bottom:5mm;transform:translateX(-50%)">{iso("width:5mm;height:5mm", BLA)}</div></div>'),
         ('Tarjeta', card_front(.5))]
kitopen = (f'<div style="width:150mm;height:96mm;background:{NEG};padding:6mm;{SHD}"><div style="width:100%;height:100%;background:{PIE};position:relative;box-shadow:inset 0 1mm 3mm rgba(0,0,0,.25)">'
           f'<div class="ob" style="left:8mm;top:10mm">{notebook(.28)}</div><div class="ob" style="left:62mm;top:12mm;{SH}">{items[2][1]}</div>'
           f'<div class="ob" style="left:100mm;top:14mm;{SH}">{items[3][1]}</div><div class="ob" style="left:56mm;top:68mm;transform:rotate(-4deg)">{pen(.4)}</div><div class="ob" style="left:100mm;top:56mm;{SH}">{card_front(.42)}</div></div></div>')
lid = f'<div style="width:96mm;height:66mm;background:#1E1F23;{SHD};position:relative">{ctr(horiz(BLA, BLA, "width:44mm;height:auto"))}<span class="m" style="position:absolute;left:5mm;bottom:5mm;font-size:5pt;color:#5A5C61">Kit de bienvenida</span></div>'
add(f'''{chh('11', 'Kit <b>de bienvenida</b>', 'Para equipo y clientes')}
<div class="scn" style="height:118mm;margin-top:5mm;{BG_P}">
 {ob(16, 12, kitopen, 0, 2, '')}{ob(176, 30, lid, 8, 3, '')}
</div>
<div style="display:grid;grid-template-columns:2fr 1fr;column-gap:6mm">{lbl('Contenido', 'Cuaderno, bolígrafo, acreditación, memoria USB cifrada y tarjeta, sobre fondo Piedra.')}{lbl('Tapa', 'Cartón rígido forrado en negro mate con imagotipo en serigrafía blanca.')}</div>''',
    '11 · Kit de bienvenida', '11', 'Kit de bienvenida')

ship = (f'<div style="width:66mm;height:100mm;background:#fff;padding:4mm;position:relative;{SH}"><div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:.3mm solid {NEG};padding-bottom:2mm">{horiz(NEG, NEG, "width:20mm;height:auto")}<span class="m" style="font-size:4.6pt">Envío</span></div>'
        f'<p class="m" style="font-size:4.4pt;color:{ACE};margin-top:3mm">Remitente</p>{bars_s([70, 55, 60], .9, h=1, gap=1.1)}<p class="m" style="font-size:4.4pt;color:{ACE};margin-top:3mm">Destinatario</p>{bars_s([90, 80, 70, 60], 1.4, h=1, gap=1.2)}'
        f'<div style="position:absolute;left:4mm;right:4mm;bottom:4mm">{barcode(58, 14, 5)}<p class="m" style="font-size:4.4pt;margin-top:1mm">[Nº de seguimiento]</p></div></div>')
asset = (f'<div style="width:62mm;height:26mm;background:#fff;display:grid;grid-template-columns:16mm 1fr;{SH}"><div style="background:{NEG};display:flex;align-items:center;justify-content:center">{iso("width:8mm;height:8mm", BLA)}</div>'
         f'<div style="padding:2.4mm 3mm"><p class="m" style="font-size:4.4pt;color:{ACE}">Propiedad de HALVEX</p><p class="m" style="font-size:7pt;font-weight:500;margin-top:.6mm">HX-[000000]</p><div style="margin-top:1.4mm">{barcode(40, 7, 9)}</div></div></div>')
rack = (f'<div style="width:120mm;height:12mm;background:#2A2B2F;display:flex;align-items:center;gap:4mm;padding:0 4mm;{SH}"><div style="display:flex;gap:1.4mm">' + ''.join('<i style="width:1.6mm;height:1.6mm;border-radius:50%;background:#55575C"></i>' for _ in range(6)) + '</div>'
        f'<div style="background:#fff;padding:1mm 2.4mm;display:flex;align-items:center;gap:2mm">{iso("width:3mm;height:3mm", NEG)}<span class="m" style="font-size:5pt;font-weight:500">HX-NODO-[00]</span></div><span class="m" style="font-size:4.6pt;color:#8A8C90;margin-left:auto">Rack [A] · U[00]</span></div>')
rs = f'<div style="width:22mm;height:22mm;border-radius:50%;background:{NEG};display:flex;align-items:center;justify-content:center;{SH}">{iso("width:10mm;height:10mm", BLA)}</div>'
sq = f'<div style="width:22mm;height:22mm;background:#fff;display:flex;align-items:center;justify-content:center;{SH}">{iso("width:11mm;height:11mm", NEG)}</div>'
arch = (f'<div style="width:62mm;height:34mm;background:#fff;padding:3mm;{SH}"><div style="display:flex;justify-content:space-between">{horiz(NEG, NEG, "width:16mm;height:auto")}<span class="m" style="font-size:4.6pt;font-weight:500">Confidencial</span></div>'
        f'<p style="font-weight:200;font-size:18pt;letter-spacing:-.03em;margin-top:2mm">Caja 00</p><p class="m" style="font-size:4.6pt;color:{ACE}">Archivo · [Proyecto] · [Año]</p></div>')
add(f'''{chh('12', 'Etiquetas', 'Envío, inventario y archivo')}
<div class="scn" style="height:116mm;margin-top:5mm;{BG_P}">
 {ob(14, 8, ship, -3, 2, '')}{ob(92, 10, asset, 2, 2, '')}{ob(92, 46, arch, -2, 2, '')}{ob(166, 12, rs, 0, 2, '')}{ob(194, 12, sq, 0, 2, '')}{ob(166, 46, rack.replace("width:120mm", "width:82mm"), 0, 2, '')}
 {ob(162, 72, f'<div style="width:86mm;height:34mm;background:#E7E3DA;position:relative;{SH}"><div style="position:absolute;left:10mm;top:6mm;transform:rotate(-2deg)">{asset}</div></div>', 0, 1, '')}
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm">{lbl('Envío · 100 × 150 mm', 'Imagotipo, remitente, destinatario y código de seguimiento.')}{lbl('Activo e inventario', 'Poliéster blanco laminado, con código y nº de activo.')}{lbl('Archivo', 'Cajas de documentación con nivel de confidencialidad.')}{lbl('Equipos y adhesivos', 'Etiquetas de rack y adhesivos del isotipo.')}</div>''',
    '12 · Etiquetas', '12', 'Etiquetas')

tape_txt = ' · '.join(['PRECINTO DE SEGURIDAD', 'NO ABRIR'] * 6)
tape = lambda w, rot: f'<div style="width:{w}mm;height:13mm;background:{NEG};display:flex;align-items:center;gap:5mm;overflow:hidden;transform:rotate({rot}deg);white-space:nowrap;padding:0 4mm;{SH}">' + ''.join(f'{iso("width:5mm;height:5mm", BLA)}<span class="m" style="color:#fff;font-size:6pt">Precinto de seguridad · No abrir</span>' for _ in range(6)) + '</div>'
seal = (f'<div style="width:80mm;height:30mm;background:#fff;display:grid;grid-template-columns:22mm 1fr;{SH}"><div style="background:{NEG};display:flex;align-items:center;justify-content:center">{iso("width:10mm;height:10mm", BLA)}</div>'
        f'<div style="padding:3mm;background:repeating-linear-gradient(45deg,#fff 0 2mm,#F1EFEA 2mm 2.4mm)"><p class="m" style="font-size:6pt;font-weight:500">Sello de seguridad</p><p style="font-size:6pt;margin-top:1mm;line-height:1.35">Si este sello está roto o despegado, no acepte el envío.</p><p class="m" style="font-size:5.4pt;margin-top:1.6mm">Nº [000000]</p></div></div>')
cbox = box(120, 60, 70, ctr(seal), f'<div style="position:absolute;left:0;right:0;top:50%;height:12mm;transform:translateY(-50%);background:{NEG};display:flex;align-items:center;gap:4mm;padding:0 3mm;overflow:hidden">' + ''.join(f'{iso("width:4mm;height:4mm", BLA)}<span class="m" style="color:#fff;font-size:4.6pt;white-space:nowrap">Precinto · No abrir</span>' for _ in range(4)) + '</div>', '', '#D9CDB8', '#E6DCC9', '#BFB29B')
add(f'''{chh('13', 'Precintos <b>y sellos</b>', 'Envíos que no se pueden abrir sin que se note')}
<div class="scn" style="height:116mm;margin-top:5mm;{BG_P}">
 {ob(16, 26, cbox, 0, 2, '')}{ob(160, 14, tape(96, -6), 0, 3, '')}{ob(170, 44, tape(80, 4), 0, 3, '')}{ob(168, 78, seal, -3, 3, '')}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Caja de envío', 'Cartón kraft con precinto negro y sello de seguridad numerado.')}{lbl('Cinta de precinto · 50 mm', 'Polipropileno negro con texto e isotipo en blanco.')}{lbl('Sello de seguridad', 'Adhesivo que deja marca al despegarse, con número de serie.')}</div>''',
    '13 · Precintos y sellos', '13', 'Precintos y sellos')

# =================================================================== 04 RÓTULOS
divider('04', 'hq-fachada', 'La marca en el edificio: fachada, recepción, orientación y control de accesos.')
joints = ''.join(f'<path d="M0 {y}H1000"/>' for y in range(40, 500, 46)) + ''.join(f'<path d="M{x + (23 if (i % 2) else 0)} {40 + i*46}V{86 + i*46}"/>' for i in range(10) for x in range(0, 1000, 92))
fac = (f'<svg viewBox="0 0 1000 540" style="width:100%;height:100%" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="gl" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#9FA5A9"/><stop offset=".5" stop-color="#7C8287"/><stop offset="1" stop-color="#5E6468"/></linearGradient>'
       f'<filter id="bl"><feGaussianBlur stdDeviation="3"/></filter><linearGradient id="wl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ECE9E2"/><stop offset="1" stop-color="#DCD8D0"/></linearGradient></defs>'
       f'<rect width="1000" height="470" fill="url(#wl)"/><g stroke="#D3CFC6" stroke-width="1.2">{joints}</g>'
       f'<rect y="470" width="1000" height="70" fill="#BEBAB2"/><rect y="470" width="1000" height="6" fill="#A9A59D"/>'
       f'<g transform="translate(106 196)"><g opacity=".35" filter="url(#bl)" transform="translate(6 8)">{iso_g(0, -30, 80, "#000")}{wm_g(116, 0, 50, "#000")}</g>{iso_g(0, -30, 80, NEG)}{wm_g(116, 0, 50, NEG)}</g>'
       f'<rect x="590" y="190" width="230" height="280" fill="{NEG}"/><rect x="602" y="202" width="100" height="268" fill="url(#gl)"/><rect x="708" y="202" width="100" height="268" fill="url(#gl)"/>'
       f'<path d="M602 202L660 202L602 300Z" fill="#fff" opacity=".12"/><path d="M708 202L770 202L708 320Z" fill="#fff" opacity=".12"/><rect x="692" y="300" width="4" height="70" fill="#C9CBCE"/><rect x="714" y="300" width="4" height="70" fill="#C9CBCE"/>'
       f'<rect x="520" y="250" width="46" height="62" fill="{GRAF}"/>{iso_g(532, 262, 22, BLA)}<text x="543" y="300" text-anchor="middle" font-family="IBM Plex Mono" font-size="5" fill="{NIE}">PLANTA 2</text>'
       f'<rect x="836" y="100" width="6" height="44" fill="{NEG}"/><rect x="840" y="118" width="110" height="4" fill="{NEG}"/><rect x="866" y="124" width="76" height="76" fill="{NEG}"/>{iso_g(882, 140, 44, BLA)}'
       f'<rect x="590" y="468" width="230" height="6" fill="#8E8A83"/></svg>')
scene_page('14', 'Fachada', 'Imagotipo en letra corpórea de acero lacado negro mate, separada 20 mm de la pared; placa junto a la puerta y banderola.', fac, h=150, bg='background:#E5E2DB')

tot = (f'<div style="width:46mm;height:118mm;background:{NEG};position:relative;{SHD}"><div style="position:absolute;left:0;right:0;top:10mm;display:flex;justify-content:center">{vert(BLA, BLA, "width:28mm;height:auto")}</div>'
       f'<div style="position:absolute;left:6mm;right:6mm;bottom:12mm;border-top:.2mm solid #3A3B40;padding-top:2mm"><p class="m" style="font-size:5pt;color:{NIE}">[Calle], 00</p><p class="m" style="font-size:5pt;color:{NIE}">28000 Madrid</p></div><div style="position:absolute;left:-3mm;right:-3mm;bottom:-4mm;height:4mm;background:#3A3B40"></div></div>')
flag = f'<div style="display:flex;align-items:flex-start"><div style="width:5mm;height:56mm;background:#3A3B40"></div><div style="margin-top:4mm"><div style="width:22mm;height:1.6mm;background:{NEG}"></div><div style="width:40mm;height:40mm;background:{NEG};margin-left:4mm;{SHD};display:flex;align-items:center;justify-content:center">{iso("width:22mm;height:22mm", BLA)}</div></div></div>'
plate = f'<div style="width:52mm;height:66mm;background:{GRAF};{SHD};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6mm">{vert(BLA, BLA, "width:30mm;height:auto")}<span class="m" style="font-size:4.6pt;color:{NIE}">Planta 2 · Madrid</span></div>'
add(f'''{chh('15', 'Tótem, banderola <b>y placa</b>', 'Exterior')}
<div class="scn" style="height:120mm;margin-top:5mm;background:linear-gradient(180deg,#E9E6DF 0%,#E9E6DF 82%,#C9C5BD 82%)">
 {ob(30, 0, tot, 0, 2, '')}{ob(112, 14, flag, 0, 2, '')}{ob(190, 24, plate, 0, 2, '')}
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Tótem · 60 × 180 cm', 'Monolito negro con imagotipo vertical y dirección en Plex Mono.')}{lbl('Banderola · 50 × 50 cm', 'Doble cara, isotipo blanco sobre negro.')}{lbl('Placa · 30 × 40 cm', 'Acero lacado grafito con imagotipo vertical en blanco.')}</div>''',
    '15 · Exterior', '15', 'Tótem, banderola y placa')

rec = (f'<svg viewBox="0 0 1000 540" style="width:100%;height:100%" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="fl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#3B3C40"/><stop offset="1" stop-color="#1E1F22"/></linearGradient>'
       f'<linearGradient id="wa" x1="0" x2="1"><stop offset="0" stop-color="#EDEAE3"/><stop offset=".5" stop-color="#F4F2EE"/><stop offset="1" stop-color="#E4E1DA"/></linearGradient></defs>'
       f'<rect width="1000" height="400" fill="url(#wa)"/><rect y="0" width="1000" height="26" fill="#DCD8D0"/>'
       + ''.join(f'<rect x="{x}" y="26" width="2" height="374" fill="#E1DDD5"/>' for x in range(80, 1000, 120)) +
       f'<g transform="translate(250 120)">{iso_g(0, -30, 112, NEG)}{wm_g(162, 0, 70, NEG)}</g>'
       f'<rect y="400" width="1000" height="140" fill="url(#fl)"/>'
       f'<path d="M230 330H770L800 352H200Z" fill="#2E2F33"/><rect x="200" y="352" width="600" height="120" fill="{NEG}"/><rect x="200" y="352" width="600" height="6" fill="#3A3B40"/>'
       f'<g opacity=".25"><rect x="200" y="472" width="600" height="40" fill="url(#fl)"/></g>{iso_g(484, 396, 32, "#2C2D32")}'
       f'<rect x="860" y="250" width="60" height="150" fill="#2A2B2F"/><rect x="866" y="256" width="48" height="70" fill="#4A4C51"/></svg>')
scene_page('16', 'Recepción', 'Imagotipo en vinilo o letra corpórea negra sobre pared Piedra; mostrador negro con el isotipo en relieve tono sobre tono.', rec, h=150, bg='background:#E9E6DF')

dirp = (f'<div style="width:70mm;height:96mm;background:{NEG};color:#fff;padding:6mm;{SHD}"><div>{horiz(BLA, BLA, "width:26mm;height:auto")}</div><div style="margin-top:10mm">'
        + ''.join(f'<div style="display:grid;grid-template-columns:16mm 1fr;border-top:.2mm solid rgba(255,255,255,.22);padding:2.6mm 0"><span class="m" style="font-size:5pt;color:{NIE}">{a}</span><span style="font-size:8pt;font-weight:300">{b}</span></div>' for a, b in (('Planta 3', 'Dirección'), ('Planta 2', 'Ingeniería'), ('Planta 2', 'Operaciones'), ('Planta 1', 'Salas de reunión'), ('Planta 0', 'Recepción'))) + '</div></div>')
room = f'<div style="width:62mm;height:30mm;background:{NEG};color:#fff;padding:4mm;position:relative;{SHD}"><span class="m" style="font-size:4.6pt;color:{NIE}">Sala 01 · 8 personas</span><p style="font-weight:200;font-size:17pt;letter-spacing:-.03em;margin-top:1.6mm">Vértice</p><span style="position:absolute;right:4mm;bottom:4mm">{iso("width:5mm;height:5mm", BLA)}</span></div>'
arrow = f'<div style="width:62mm;height:14mm;background:#fff;display:flex;align-items:center;gap:3mm;padding:0 4mm;{SH}"><svg viewBox="0 0 20 10" style="width:9mm"><path d="M0 5H18M14 1L18 5L14 9" fill="none" stroke="{NEG}" stroke-width="1"/></svg><span style="font-size:7.4pt">Salas de reunión</span><span class="m" style="font-size:4.6pt;color:{ACE};margin-left:auto">01–04</span></div>'
restr = (f'<div style="width:66mm;height:92mm;background:{NEG};color:#fff;padding:6mm;position:relative;{SHD}"><div style="display:flex;justify-content:space-between;align-items:flex-start">{iso("width:8mm;height:8mm", BLA)}<span class="m" style="font-size:5pt;color:{NIE}">Nivel 3</span></div>'
         f'<p style="font-weight:200;font-size:19pt;letter-spacing:-.03em;line-height:1.05;margin-top:12mm">Acceso<br><b style="font-weight:400">restringido</b></p><p style="font-size:6.6pt;color:{NIE};margin-top:3mm;line-height:1.45">Solo personal autorizado. Identifíquese con su acreditación.</p>'
         f'<div style="position:absolute;left:6mm;right:6mm;bottom:6mm;height:14mm;border:.25mm solid #3A3B40;display:flex;align-items:center;justify-content:center;gap:3mm"><svg viewBox="0 0 24 24" style="width:6mm" fill="none" stroke="#fff" stroke-width="1.4"><rect x="5" y="3" width="14" height="18"/><path d="M9 8H15M9 12H15"/></svg><span class="m" style="font-size:4.6pt">Lector de acreditación</span></div></div>')
add(f'''{chh('17', 'Señalética <b>interior</b>', 'Orientación y accesos')}
<div class="scn" style="height:118mm;margin-top:5mm;background:linear-gradient(180deg,#EFEDE8,#E4E1DA)">
 {ob(16, 10, dirp, 0, 2, '')}{ob(100, 14, room, 0, 2, '')}{ob(100, 54, arrow, 0, 2, '')}{ob(100, 78, room.replace('Sala 01 · 8 personas', 'Sala 02 · 4 personas').replace('Vértice', 'Horizonte'), 0, 2, '')}{ob(184, 12, restr, 0, 2, '')}
</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:6mm">{lbl('Directorio', 'Panel negro, plantas en Plex Mono y destinos en Plex Sans Light.')}{lbl('Salas y orientación', 'Las salas llevan nombres de la marca; flechas de trazo fino.')}{lbl('Acceso restringido', 'Señal de zona con nivel de acceso y lector de acreditación.')}</div>''',
    '17 · Señalética interior', '17', 'Señalética interior')

iso_row = ''.join(iso_g(x, 0, 18, '#FFFFFF') for x in range(0, 1000, 30))
glass = (f'<svg viewBox="0 0 1000 520" style="width:100%;height:100%" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="gs" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#C8CDD0"/><stop offset="1" stop-color="#A9AFB3"/></linearGradient>'
         f'<pattern id="ip" width="34" height="34" patternUnits="userSpaceOnUse">{iso_g(8, 8, 18, "#FFFFFF")}</pattern></defs>'
         f'<rect width="1000" height="520" fill="#E7E4DD"/><rect x="40" y="30" width="920" height="440" fill="url(#gs)"/>'
         f'<rect x="40" y="200" width="920" height="60" fill="url(#ip)" opacity=".75"/><rect x="40" y="196" width="920" height="2" fill="#fff" opacity=".7"/><rect x="40" y="262" width="920" height="2" fill="#fff" opacity=".7"/>'
         + ''.join(f'<path d="M{x} 30L{x+120} 30L{x-80} 470L{x-200} 470Z" fill="#fff" opacity=".08"/>' for x in (300, 700)) +
         ''.join(f'<rect x="{x}" y="30" width="10" height="440" fill="{NEG}"/>' for x in (40, 340, 640, 950)) +
         f'<rect x="40" y="26" width="920" height="10" fill="{NEG}"/><rect x="40" y="466" width="920" height="10" fill="{NEG}"/>'
         f'<rect x="660" y="300" width="4" height="90" fill="#D6D8DA"/><text x="690" y="130" font-family="IBM Plex Sans" font-weight="200" font-size="34" fill="#fff" opacity=".9">Sala Vértice</text>'
         f'<text x="692" y="152" font-family="IBM Plex Mono" font-size="11" letter-spacing="2" fill="#fff" opacity=".9">SALA 01 · 8 PERSONAS</text></svg>')
scene_page('18', 'Vinilos de cristal', 'Franja de seguridad a la altura de los ojos con el isotipo repetido en vinilo esmerilado; rótulo de sala en vinilo blanco.', glass, h=150, bg='background:#E7E4DD')

# =================================================================== 05 UNIFORME
divider('05', 'hq-equipo-w', 'Prendas sobrias en grafito y negro, con el isotipo bordado tono sobre tono o en blanco.')
G = '#24252A'; GS = '#33343A'
tee = 'M62 12L82 4Q100 18 118 4L138 12L188 40L170 78L150 66L150 212L50 212L50 66L30 78L12 40Z'
lsl = 'M62 12L82 4Q100 16 118 4L138 12L176 30L196 196L172 200L152 70L152 214L48 214L48 70L28 200L4 196L24 30Z'
hood = 'M58 16Q70 0 100 0Q130 0 142 16L178 34L198 198L172 202L154 74L154 216L46 216L46 74L28 202L2 198L22 34Z'
def garment(path, extra='', fill=G, chest=True, w=56):
    logo = iso_g(118, 52, 14, '#FFFFFF') if chest else ''
    return (f'<svg viewBox="0 0 200 220" style="width:{w}mm;height:auto;filter:drop-shadow(0 1.4mm 2mm rgba(0,0,0,.3))"><path d="{path}" fill="{fill}"/>'
            f'<g fill="none" stroke="{GS}" stroke-width="1.2">{extra}</g>{logo}</svg>')
polo = garment(tee, f'<path d="M82 4L100 30L118 4"/><path d="M100 30V60"/><circle cx="100" cy="42" r="1.4" fill="{GS}"/><circle cx="100" cy="52" r="1.4" fill="{GS}"/><path d="M50 200H150"/>')
tshirt = garment(tee, '<path d="M82 4Q100 22 118 4"/><path d="M50 200H150"/>', NEG)
sweat = garment(hood, '<path d="M70 18Q100 50 130 18"/><path d="M100 40V216"/><path d="M60 150H140"/><path d="M46 204H154"/>')
soft = garment(lsl, '<path d="M100 10V214"/><path d="M82 4L92 22H108L118 4"/><path d="M60 110H86M114 110H140"/><path d="M48 204H152"/>', '#1B1C20')
cap = (f'<svg viewBox="0 0 200 130" style="width:50mm;height:auto;filter:drop-shadow(0 1.4mm 2mm rgba(0,0,0,.3))"><path d="M30 96Q30 26 100 24Q170 26 170 96Z" fill="{G}"/>'
       f'<path d="M16 96Q100 126 184 96Q100 108 16 96Z" fill="#17181B"/><path d="M100 24V96M58 34Q72 64 70 96M142 34Q128 64 130 96" stroke="{GS}" stroke-width="1.2" fill="none"/>{iso_g(86, 50, 28, "#FFFFFF")}</svg>')
sc = ob(14, 18, polo, 0, 2, '') + ob(70, 14, sweat, 0, 3, '') + ob(130, 18, soft, 0, 2, '') + ob(190, 22, tshirt.replace('width:56mm', 'width:48mm'), 0, 2, '') + ob(196, 96, cap, 0, 4, '')
scene_page('19', 'Colección', 'Polo, sudadera, softshell, camiseta y gorra en grafito y negro, con el isotipo bordado.', sc, bg=BG_P)
if REN('r1-hero'):
    scene_page('19a', 'Gorra', 'Seis paneles en negro, isotipo bordado en hilo blanco con puntada de satén en relieve; ojales y botón a tono.', photo('r1-hero'), bg=BG_P)
    add(f'''<div style="display:grid;grid-template-columns:1.25fr 1fr;column-gap:5mm;margin-top:4mm">
 <div class="scn" style="height:146mm">{photo('r2-macro')}</div>
 <div class="scn" style="height:146mm">{photo('r3-piedra')}</div></div>
<div class="cap2"><span class="nn">19b</span><span class="h3" style="font-weight:300;font-size:16pt;letter-spacing:-.02em">Bordado en detalle</span><span class="p s">Puntada de satén cruzando cada cuña, con relieve de 1,5 mm. A la derecha, gorra en color Piedra con el isotipo en hilo negro.</span></div>''',
        '19b · Bordado en detalle', '19b', 'Bordado en detalle')
    scene_page('19c', 'Combinaciones', 'Negro con hilo blanco y grafito con bordado tono sobre tono: la versión discreta para el día a día.', photo('r4-pareja'), bg=BG_P)

back = garment(tee, '<path d="M82 4Q100 10 118 4"/><path d="M50 200H150"/>', G, False, 74)
back = back.replace('</svg>', f'<rect x="60" y="40" width="80" height="16" fill="none" stroke="#9A9CA0" stroke-dasharray="2 2" stroke-width=".8"/>{wm_g(66, 43, 10, "#FFFFFF")}</svg>')
front = garment(tee, '<path d="M82 4Q100 22 118 4"/><path d="M50 200H150"/>', G, True, 74).replace('</svg>', '<rect x="112" y="46" width="26" height="26" fill="none" stroke="#9A9CA0" stroke-dasharray="2 2" stroke-width=".8"/><rect x="166" y="46" width="12" height="12" fill="none" stroke="#9A9CA0" stroke-dasharray="2 2" stroke-width=".8" transform="rotate(-24 172 52)"/></svg>')
add(f'''{chh('20', 'Marcaje <b>de prendas</b>', 'Posiciones y técnicas')}
<div style="display:grid;grid-template-columns:78mm 78mm 1fr;column-gap:8mm;margin-top:6mm;align-items:start">
 <div style="background:{PIE};padding:4mm 2mm;display:flex;justify-content:center">{front}</div>
 <div style="background:{PIE};padding:4mm 2mm;display:flex;justify-content:center">{back}</div>
 <div class="rows">
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Pecho izquierdo</span><span class="p">Isotipo de 6 cm, a 18 cm del hombro. Bordado blanco o tono sobre tono.</span></div>
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Espalda</span><span class="p">Logotipo de 25 cm, a 8 cm del cuello. Solo en prendas de equipo técnico y eventos.</span></div>
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Manga</span><span class="p">Isotipo de 4 cm en la manga izquierda, opcional.</span></div>
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Técnica</span><span class="p">Bordado (isotipo de 15 mm como mínimo) o serigrafía blanca mate.</span></div>
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2.4mm 0"><span class="m s">Colores</span><span class="p">Prendas en grafito, negro o Piedra. Nunca en colores vivos.</span></div>
 </div>
</div>
<div style="display:grid;grid-template-columns:78mm 78mm;column-gap:8mm">{lbl('Delantero', 'Pecho y manga.')}{lbl('Espalda', 'Logotipo centrado.')}</div>''', '20 · Marcaje de prendas', '20', 'Marcaje de prendas')

badge_f = (f'<div style="width:54mm;height:86mm;background:#FBFAF8;position:relative;{SHD}"><div style="height:18mm;background:{NEG};display:flex;align-items:center;padding:0 5mm">{horiz(BLA, BLA, "width:24mm;height:auto")}</div>'
           f'<div style="width:22mm;height:28mm;background:#E2E0DA;margin:6mm 5mm 0"></div><p style="font-size:8pt;font-weight:500;margin:4mm 5mm 0">Nombre Apellido</p><p class="m" style="font-size:5pt;color:{ACE};margin:1mm 5mm 0">Ingeniería</p>'
           f'<div style="position:absolute;right:5mm;top:24mm;background:{NEG};color:#fff;padding:1mm 2mm"><span class="m" style="font-size:5pt">Nivel 2</span></div>'
           f'<div style="position:absolute;left:5mm;right:5mm;bottom:5mm">{barcode(44, 7, 11)}</div></div>')
badge_b = (f'<div style="width:54mm;height:86mm;background:{NEG};color:#fff;position:relative;{SHD}"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{iso("width:20mm;height:20mm", "#2C2D32")}</div>'
           f'<p style="position:absolute;left:5mm;right:5mm;bottom:6mm;font-size:5.4pt;color:{NIE};line-height:1.45">Esta acreditación es personal e intransferible. Si la encuentra, devuélvala a HALVEX · Madrid.</p></div>')
lan = f'<div style="width:6mm;height:70mm;background:{NEG};display:flex;flex-direction:column;align-items:center;gap:8mm;padding-top:6mm;overflow:hidden">' + ''.join(iso("width:3.4mm;height:3.4mm", "#5A5C61") for _ in range(6)) + '</div>'
visit = (f'<div style="width:54mm;height:86mm;background:{PIE};position:relative;{SH}"><div style="padding:5mm">{horiz(NEG, NEG, "width:22mm;height:auto")}</div>'
         f'<p style="font-weight:200;font-size:26pt;letter-spacing:-.04em;position:absolute;left:5mm;top:30mm">Visita</p><p class="m" style="position:absolute;left:5mm;top:46mm;font-size:5pt;color:{ACE}">Acompañado en todo momento</p>'
         f'<div style="position:absolute;left:5mm;right:5mm;bottom:5mm;border-top:.2mm solid {NEG};padding-top:1.6mm"><span class="m" style="font-size:5pt">Fecha [dd/mm] · Nº [000]</span></div></div>')
pin = f'<div style="width:14mm;height:14mm;border-radius:50%;background:radial-gradient(circle at 35% 30%,#4A4C51,{NEG});display:flex;align-items:center;justify-content:center;{SH}">{iso("width:7mm;height:7mm", "#C9CACD")}</div>'
add(f'''{chh('21', 'Acreditación', 'Equipo y visitas')}
<div class="scn" style="height:118mm;margin-top:5mm;{BG_P}">
 {ob(24, 0, lan, 0, 1, '')}{ob(16, 18, badge_f, -4, 2, '')}{ob(80, 20, badge_b, 3, 2, '')}{ob(148, 16, visit, -2, 2, '')}{ob(220, 40, pin, 0, 3, '')}{ob(226, 70, pin, 0, 3, '')}
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm">{lbl('Acreditación de equipo', 'PVC con foto, área y nivel de acceso.')}{lbl('Reverso', 'Isotipo tono sobre tono y texto de devolución.')}{lbl('Pase de visita', 'Fondo Piedra para distinguirlo a distancia.')}{lbl('Insignia', 'Metal pavonado con el isotipo.')}</div>''',
    '21 · Acreditación', '21', 'Acreditación')

# =================================================================== 06 CARTELES
divider('06', 'hq-banca', 'Carteles, mupis, prensa y ferias: pocas palabras, mucho espacio y el logo siempre en su sitio.')
def poster(w, kind, hh=None):
    h = hh or w * 1.4
    if kind == 1:
        lines_ = ''.join(f'<path d="M0 {i*5}L100 70"/>' for i in range(0, 29))
        return (f'<div style="width:{w}mm;height:{h}mm;background:{GRAF};color:#fff;position:relative;overflow:hidden"><svg viewBox="0 0 100 140" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%"><g stroke="#fff" stroke-width=".15" fill="none" opacity=".55">{lines_}</g></svg>'
                f'<p style="position:absolute;left:{w*.08}mm;top:{h*.07}mm;font-weight:200;font-size:{w*.36:.1f}pt;letter-spacing:-.03em;line-height:1.05">Mirar con amplitud.<br><b style="font-weight:400">Actuar con precisión.</b></p>'
                f'<div style="position:absolute;left:{w*.08}mm;right:{w*.08}mm;bottom:{w*.08}mm">{wm("width:100%;height:auto", BLA)}</div></div>')
    if kind == 2:
        return (f'<div style="width:{w}mm;height:{h}mm;background-image:linear-gradient(180deg,rgba(0,0,0,.08) 0%,rgba(0,0,0,.5) 40%,rgba(0,0,0,.86) 100%),url({img64("hq-hero")});background-size:cover;background-position:center;color:#fff;position:relative">'
                f'<p style="position:absolute;left:{w*.08}mm;right:{w*.08}mm;bottom:{h*.17}mm;font-weight:200;font-size:{w*.32:.1f}pt;letter-spacing:-.03em;line-height:1.05">Tecnología para decisiones que <b style="font-weight:400">no admiten error.</b></p>'
                f'<div style="position:absolute;left:{w*.08}mm;bottom:{w*.08}mm">{horiz(BLA, BLA, f"width:{w*.38}mm;height:auto")}</div></div>')
    return (f'<div style="width:{w}mm;height:{h}mm;background:{PIE};position:relative;overflow:hidden"><div style="position:absolute;right:{w*.08}mm;top:{w*.08}mm;width:{w*.6}mm;height:{w*.6}mm">{iso("width:100%;height:100%", NEG)}</div>'
            f'<p style="position:absolute;left:{w*.08}mm;bottom:{h*.17}mm;font-weight:200;font-size:{w*.36:.1f}pt;letter-spacing:-.03em;line-height:1.05">Pocos clientes.<br><b style="font-weight:400">Equipos estables.</b></p>'
            f'<div style="position:absolute;left:{w*.08}mm;bottom:{w*.08}mm">{horiz(NEG, NEG, f"width:{w*.38}mm;height:auto")}</div></div>')
frame = lambda html: f'<div style="padding:1.6mm;background:{NEG};{SHD}"><div style="padding:3mm;background:#fff">{html}</div></div>'
wall = 'background:linear-gradient(180deg,#EEECE7 0%,#E6E3DC 84%,#B9B5AD 84%,#A9A59D 100%)'
sc = ob(28, 14, frame(poster(56, 1)), 0, 2, '') + ob(102, 14, frame(poster(56, 2)), 0, 2, '') + ob(176, 14, frame(poster(56, 3)), 0, 2, '')
scene_page('22', 'Serie de carteles', 'Tres carteles de 50 × 70 cm: lema con convergencia, promesa sobre fotografía y principio tipográfico.', sc, h=148, bg=wall)

add(f'''{chh('23', 'Cartel <b>· anatomía</b>', '50 × 70 cm')}
<div style="display:grid;grid-template-columns:96mm 1fr;column-gap:12mm;margin-top:4mm;align-items:start">
 <div style="{SH}">{poster(96, 1, 134)}</div>
 <div class="rows">
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Margen</span><span class="p">8 % del ancho en los cuatro lados.</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Titular</span><span class="p">Arriba a la izquierda, Plex Sans 200 + 400. Una sola frase, de seis a diez palabras.</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Logo</span><span class="p">Abajo: logotipo a todo el ancho o imagotipo al 38 % del ancho.</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Fondo</span><span class="p">Grafito con convergencia, Piedra con el isotipo grande o fotografía en blanco y negro.</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Nunca</span><span class="p">Listas, precios, más de un mensaje ni sellos de «nuevo».</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:2.6mm 0"><span class="m s">Producción</span><span class="p">Papel estucado mate de 200 g, impresión digital.</span></div>
 </div>
</div>''', '23 · Anatomía del cartel', '23', 'Anatomía del cartel')

mupi = (f'<div style="position:relative;width:74mm"><div style="width:74mm;height:104mm;background:#3A3B40;padding:3mm;{SHD}"><div style="width:100%;height:100%;box-shadow:0 0 6mm rgba(255,255,255,.35)">{poster(68, 2, 98)}</div></div>'
        f'<div style="width:10mm;height:22mm;background:#3A3B40;margin:0 auto"></div><div style="width:34mm;height:3mm;background:#2A2B2F;margin:0 auto"></div></div>')
press = (f'<div style="display:flex;{SHD}"><div style="width:76mm;height:104mm;background:#FBFAF8;padding:7mm"><p class="m" style="font-size:5pt;color:{ACE}">Tecnología · Análisis</p><div style="height:5mm;background:#C9C7C1;margin-top:4mm;width:80%"></div><div style="height:5mm;background:#C9C7C1;margin-top:2mm;width:60%"></div>'
         f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:6mm"><div>{bars_s([100, 96, 98, 90, 100, 94, 97, 92, 60, 0, 100, 96, 98, 90, 100, 70], 1.2, h=1, gap=1.4)}</div><div>{bars_s([100, 94, 97, 92, 80, 0, 100, 96, 98, 90, 100, 94, 97, 92, 60], 1.2, h=1, gap=1.4)}</div></div></div>'
         f'<div style="width:.4mm;background:linear-gradient(90deg,#BDBAB3,#E8E6E1)"></div>{poster(74.3, 3, 104)}</div>')
add(f'''{chh('24', 'Mupi <b>y prensa</b>', 'Exterior y revistas')}
<div class="scn" style="height:120mm;margin-top:5mm;background:linear-gradient(180deg,#E6E3DC 0%,#E6E3DC 86%,#BDB9B1 86%)">
 {ob(26, 4, mupi, 0, 2, '')}{ob(112, 8, press, 0, 2, '')}
</div>
<div style="display:grid;grid-template-columns:1fr 2fr;column-gap:6mm">{lbl('Mupi · 120 × 176 cm', 'Papel backlight; mismo diseño que el cartel.')}{lbl('Anuncio a página completa', 'En prensa económica y sectorial: una frase, el isotipo grande y el imagotipo.')}</div>''',
    '24 · Mupi y prensa', '24', 'Mupi y prensa')

booth = (f'<svg viewBox="0 0 1000 520" style="width:100%;height:100%" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="fl2" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#CFCBC3"/><stop offset="1" stop-color="#B3AFA7"/></linearGradient></defs>'
         f'<rect width="1000" height="520" fill="#E9E6E0"/><path d="M0 420H1000V520H0Z" fill="url(#fl2)"/><path d="M180 420L260 360H880L960 420Z" fill="#8E8A83"/>'
         f'<rect x="260" y="80" width="620" height="280" fill="{NEG}"/>{wm_g(380, 150, 76, BLA)}<text x="380" y="268" font-family="IBM Plex Sans" font-weight="200" font-size="19" fill="#C9CACD">Tecnología para decisiones que no admiten error.</text>'
         f'<path d="M180 120L260 80V360L180 420Z" fill="{PIE}"/>' + ''.join(f'<path d="M180 {130+i*14}L260 {220}" stroke="{NEG}" stroke-width=".7" opacity=".5"/>' for i in range(20)) +
         f'<rect x="480" y="330" width="200" height="120" fill="{GRAF}"/><rect x="480" y="330" width="200" height="8" fill="#3A3B40"/>{iso_g(564, 370, 32, "#3A3B40")}'
         f'<rect x="905" y="220" width="44" height="200" fill="{NEG}"/><rect x="899" y="220" width="56" height="6" fill="{NEG}"/>{iso_g(916, 240, 22, BLA)}<rect x="915" y="420" width="24" height="5" fill="#55575C"/></svg>')
scene_page('25', 'Stand de feria', 'Fondo negro con el logotipo y la promesa, lateral Piedra con convergencia, mostrador grafito y roll-up.', booth, h=150, bg='background:#E9E6E0')

# =================================================================== 07 VEHÍCULOS Y OBJETOS
divider('07', 'hq-c-defensa', 'El vehículo de los equipos técnicos y los objetos que acompañan a la marca.')
van = (f'<svg viewBox="0 0 1000 460" style="width:100%;height:100%" preserveAspectRatio="xMidYMid meet"><defs><linearGradient id="vb" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2E2F34"/><stop offset=".6" stop-color="#1B1C20"/><stop offset="1" stop-color="#111214"/></linearGradient>'
       f'<linearGradient id="vw" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#7A8085"/><stop offset="1" stop-color="#4C5257"/></linearGradient></defs>'
       f'<ellipse cx="500" cy="392" rx="420" ry="18" fill="#000" opacity=".22"/>'
       f'<path d="M110 360V130Q110 96 144 94L640 90Q700 90 740 120L840 210Q890 220 900 260V360Z" fill="url(#vb)"/>'
       f'<path d="M660 112Q700 112 726 136L800 206H660Z" fill="url(#vw)"/><path d="M110 250H900" stroke="#2C2D32" stroke-width="2"/><path d="M640 96V360M380 96V360" stroke="#0E0F11" stroke-width="2"/>'
       f'<g transform="translate(160 170)">{iso_g(0, -30, 80, BLA)}{wm_g(116, 0, 50, BLA)}</g><text x="160" y="300" font-family="IBM Plex Mono" font-size="16" letter-spacing="3" fill="#8A8C90">HALVEX.COM</text>'
       f'<rect x="680" y="270" width="40" height="6" fill="#55575C"/>'
       + ''.join(f'<circle cx="{cx}" cy="362" r="48" fill="#0B0B0D"/><circle cx="{cx}" cy="362" r="26" fill="#4A4C51"/><circle cx="{cx}" cy="362" r="8" fill="#2A2B2F"/>' for cx in (240, 760)) +
       f'<rect x="880" y="292" width="24" height="16" fill="#C9CACD"/></svg>')
scene_page('26', 'Vehículo', 'Furgoneta de los equipos técnicos en negro o grafito; imagotipo y web en vinilo de corte blanco mate. Sin más mensajes.', van, h=146, bg=BG_P)

mug = (f'<svg viewBox="0 0 120 120" style="width:34mm;height:34mm;filter:drop-shadow(0 1.4mm 2mm rgba(0,0,0,.25))"><path d="M88 40Q112 40 112 62Q112 84 88 84" fill="none" stroke="#F4F2EE" stroke-width="10"/><path d="M20 20H92V100Q92 108 84 108H28Q20 108 20 100Z" fill="#F7F5F1"/>'
       f'<path d="M20 20H92V28H20Z" fill="#E7E4DD"/>{iso_g(43, 50, 26, NEG)}</svg>')
thermo = (f'<div style="width:20mm;height:66mm;background:linear-gradient(90deg,#0B0B0D,#2E2F34 40%,#111214);border-radius:3mm 3mm 2mm 2mm;position:relative;{SH}"><div style="position:absolute;left:0;right:0;top:-8mm;height:10mm;background:linear-gradient(90deg,#555,#999 40%,#555);border-radius:2mm 2mm 0 0"></div>'
          f'<div style="position:absolute;left:50%;top:22mm;transform:translateX(-50%) rotate(-90deg)">{wm("width:28mm;height:auto", "#C9CACD")}</div></div>')
tote = (f'<div style="position:relative;width:60mm;height:70mm"><svg viewBox="0 0 60 24" style="position:absolute;left:0;top:-20mm;width:60mm;height:24mm"><path d="M14 24Q14 2 22 2Q30 2 30 24M30 24Q30 2 38 2Q46 2 46 24" fill="none" stroke="#D9D3C6" stroke-width="2.4"/></svg>'
        f'<div style="position:absolute;inset:0;background:#E8E2D6;{SH}">{ctr(vert(NEG, NEG, "width:28mm;height:auto"))}</div></div>')
usb = f'<div style="width:14mm;height:36mm;background:{NEG};position:relative;border-radius:1.4mm;{SH}"><div style="position:absolute;left:3.5mm;right:3.5mm;top:-6mm;height:6mm;background:linear-gradient(90deg,#888,#CCC,#888)"></div><div style="position:absolute;left:50%;bottom:6mm;transform:translateX(-50%)">{iso("width:6mm;height:6mm", BLA)}</div></div>'
umb = (f'<svg viewBox="0 0 40 200" style="width:12mm;height:60mm;filter:drop-shadow(0 1.4mm 2mm rgba(0,0,0,.25))"><path d="M20 4L32 150H8Z" fill="{NEG}"/><path d="M20 4L20 150" stroke="#2C2D32" stroke-width="1"/>'
       f'<rect x="18" y="150" width="4" height="30" fill="#55575C"/><path d="M20 180V188Q20 196 12 196Q6 196 6 190" fill="none" stroke="{NEG}" stroke-width="5"/>{iso_g(15, 120, 10, "#5A5C61")}</svg>')
sc = (ob(14, 26, notebook(.42), -6, 2) + ob(30, 120, pen(.6), -10, 4) + ob(96, 40, thermo, 4, 3, '') + ob(130, 70, mug, 0, 3, '') + ob(176, 40, tote, -3, 2, '')
      + ob(150, 18, usb, 18, 4, '') + ob(242, 30, umb, 8, 3, ''))
scene_page('27', 'Objetos', 'Cuaderno, bolígrafo, termo, taza, memoria USB, bolsa de tela y paraguas: negro y blanco natural, sin brillos ni colores.', sc, bg=BG_P)

prod = [('Tarjeta de visita', '85 × 55 mm', 'Cartulina no estucada 400 g, duplex negro y blanco', 'Serigrafía blanca · K100', 'Golpe en seco'),
        ('Carta', 'A4', 'Offset no estucado 120 g, blanco natural', 'Offset K', '—'),
        ('Sobres', 'DL · C5 · C4', 'Offset 110–120 g · kraft blanco', 'Offset K', 'Solapa con isotipo'),
        ('Carpeta', '220 × 310 mm', 'Cartulina 350 g grafito', 'Serigrafía blanca', 'Bolsillo y ranura'),
        ('Cuaderno', 'A5', 'Tapa dura negra', '—', 'Golpe en seco'),
        ('Kit de bienvenida', '300 × 200 × 60 mm', 'Cartón rígido forrado negro mate', 'Serigrafía blanca', 'Interior Piedra'),
        ('Etiquetas', 'Varios', 'Poliéster blanco adhesivo', 'Térmica · digital', 'Laminado mate'),
        ('Precinto', '50 mm', 'Cinta de polipropileno negra', 'Flexografía blanca', '—'),
        ('Letras de fachada', 'A medida', 'Acero lacado negro mate', '—', 'Separadas 20 mm'),
        ('Placas y señales', '30 × 40 cm', 'Acero o aluminio lacado', 'Vinilo o serigrafía blanca', 'Mate'),
        ('Vinilos de cristal', 'Franja de 6 cm', 'Vinilo esmerilado', 'Corte', '—'),
        ('Prendas', 'Tallas', 'Algodón y softshell grafito o negro', 'Bordado blanco o tono sobre tono', '—'),
        ('Carteles', '50 × 70 cm', 'Estucado mate 200 g', 'Digital', '—'),
        ('Vehículo', 'Furgoneta', 'Vinilo de corte blanco mate', '—', '—')]
cols_ = 'grid-template-columns:40mm 32mm 1fr 52mm 34mm'
pp = ''.join(f'<div class="row" style="{cols_};padding:.85mm 0"><span class="h4" style="font-size:8.6pt">{a}</span><span class="p" style="font-size:8.4pt">{b}</span><span class="p" style="font-size:8.4pt">{c}</span><span class="p" style="font-size:8.4pt">{d}</span><span class="p s" style="font-size:8.4pt">{e}</span></div>' for a, b, c, d, e in prod)
add(f'''{chh('28', 'Ficha <b>de producción</b>', 'Referencia para proveedores')}
<div style="margin-top:4mm"><div class="row" style="{cols_};border:0;padding:0 0 1.4mm"><span class="m s">Pieza</span><span class="m s">Formato</span><span class="m s">Soporte</span><span class="m s">Impresión</span><span class="m s">Acabado</span></div><div class="rows">{pp}</div></div>
<p class="m s" style="margin-top:2.4mm;text-transform:none;letter-spacing:.02em">Especificaciones orientativas: pedir siempre muestra y prueba de color al proveedor antes de producir.</p>''',
    '28 · Ficha de producción', '28', 'Ficha de producción')

# =================================================================== RENUMERACIÓN
_new = {}
for i, (part, num, title, idx) in enumerate(TOCI):
    nn = f'{i+1:02d}'; _new[idx] = (num, nn)
    TOCI[i] = (part, nn, title, idx)
for idx, (old, nn) in _new.items():
    pg = PAGES[idx]
    pg = pg.replace(f'<span class="num">{old}</span>', f'<span class="num">{nn}</span>').replace(f'<span class="nn">{old}</span>', f'<span class="nn">{nn}</span>').replace(f'<span>{old} · ', f'<span>{nn} · ')
    PAGES[idx] = pg

# =================================================================== ENSAMBLAJE
cur['part'] = ''
cover = f'''<section class="page" style="padding:0">
<div class="scn" style="position:absolute;inset:0;{BG_G}">
 {(photo('p1-flatlay', 'center') + '<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,19,22,.96) 0%,rgba(18,19,22,.85) 36%,rgba(18,19,22,0) 62%)"></div>') if REN('p1-flatlay') else (ob(150, 20, letter(.46), -6, 2, SHD) + ob(212, 72, folder(.3), 8, 1, SHD) + ob(168, 120, card_front(.95), 12, 4, SHD) + ob(214, 140, card_back(.95), -8, 5, SHD) + ob(126, 150, pen(.6), -18, 6, SHD))}
</div>
<div style="position:absolute;left:18mm;top:14mm;right:18mm;display:flex;justify-content:space-between;color:#fff" class="m"><b style="font-weight:500">HALVEX</b><span>Documento 04</span></div>
<div style="position:absolute;left:18mm;top:52mm;color:#fff;width:110mm">
 <p class="m" style="color:{NIE}">Catálogo</p>
 <h1 class="d1" style="font-size:58pt;margin-top:5mm">Material<br><b>corporativo</b></h1>
 <p class="lead" style="margin-top:7mm;color:#C9CACD;max-width:95mm;font-size:11.5pt">Tarjetas, papelería, packaging, señalética, uniforme, carteles, vehículos y objetos.</p>
</div>
<div class="m" style="position:absolute;left:18mm;bottom:14mm;width:110mm;color:#fff;border-top:.25mm solid rgba(255,255,255,.5);padding-top:2.6mm">Edición 1.0 · Noviembre 2026</div>
</section>'''

princ = [('Papel natural', 'Blanco natural y no estucado. Tacto antes que brillo.'), ('Negro mate', 'El negro de la marca en masa, sin barnices brillantes.'),
         ('Relieve, no tinta', 'Golpe en seco y tono sobre tono cuando la pieza se toca.'), ('Un solo gesto', 'Cada pieza lleva el logo una vez y una sola idea.')]
pr_ = ''.join(f'<div class="r" style="padding-top:3mm"><span class="m s">0{i+1}</span><p class="h3" style="margin-top:2mm;font-weight:300;font-size:17pt;letter-spacing:-.02em">{a}</p><p class="p s" style="margin-top:1.6mm">{b}</p></div>' for i, (a, b) in enumerate(princ))
intro = f'''<section class="page">{run('Introducción')}
<div class="g" style="margin-top:12mm"><p class="m s" style="grid-column:1/3">Introducción</p>
 <h2 class="d1" style="grid-column:3/12;font-size:36pt">Lo que se toca <b>también es marca.</b></h2></div>
<div class="g" style="margin-top:9mm"><div style="grid-column:3/9"><p class="p">Este catálogo muestra cómo se aplica la identidad de HALVEX a todo el material físico y visual de la compañía, con la referencia de producción de cada pieza. Las normas de base están en el Manual corporativo (documento 03).</p></div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:7mm;margin-top:14mm">{pr_}</div>{FOL}</section>'''

final = [cover, None, intro] + PAGES
final.append(f'''<section class="page" style="padding:0"><div class="scn" style="position:absolute;inset:0;{BG_P}">
{ob(118, 70, card_front(.9), -8, 2, SHD)}{ob(150, 82, card_back(.9), 6, 3, SHD)}</div>
<div class="m" style="position:absolute;left:18mm;right:18mm;bottom:13mm;display:flex;justify-content:space-between;border-top:.25mm solid {NEG};padding-top:2.6mm"><span>HALVEX · Material corporativo · Edición 1.0</span><span class="s">contacto@halvex.com</span></div></section>''')

OFF = 3
chap_by_part = {}
for part, num, title, idx in TOCI:
    chap_by_part.setdefault(part, []).append((num, title, idx + OFF + 1))
for i, p in enumerate(final):
    if isinstance(p, tuple):
        _, part, photo, intro_, pos = p
        it = ''.join(f'<div class="row" style="grid-template-columns:10mm 1fr 8mm;padding:2.2mm 0"><span class="m s">{a}</span><span style="font-size:10.5pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in chap_by_part.get(part, []))
        final[i] = f'''<section class="page dk" style="padding:0">
<div class="photo" style="position:absolute;left:0;top:0;bottom:0;width:50%;background-image:url({img64(photo)});background-position:{pos}"></div>
<div style="position:absolute;left:50%;right:0;top:0;bottom:0;padding:14mm 18mm 0 14mm">
 <div class="m" style="display:flex;justify-content:space-between;border-bottom:.25mm solid rgba(255,255,255,.6);padding-bottom:2.4mm"><span>Parte {part}</span><span class="s">{i+1:02d}</span></div>
 <p style="font-weight:200;font-size:120pt;line-height:.8;letter-spacing:-.06em;margin-top:12mm">{part}</p>
 <h2 class="d1" style="font-size:34pt;margin-top:7mm">{PARTS[part]}</h2>
 <p class="lead" style="margin-top:4mm;color:#C9CACD;max-width:100mm;font-size:11pt">{intro_}</p>
 <div class="rows" style="position:absolute;left:14mm;right:18mm;bottom:14mm">{it}</div>
</div></section>'''

cols = ''
for part, name in PARTS.items():
    it = ''.join(f'<div class="row" style="grid-template-columns:8mm 1fr 8mm;padding:1.6mm 0"><span class="m s">{a}</span><span style="font-size:9pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in chap_by_part.get(part, []))
    cols += f'<div><div style="display:flex;align-items:baseline;gap:3mm;padding-bottom:2mm"><span style="font-weight:200;font-size:20pt;letter-spacing:-.04em;line-height:1">{part}</span><span class="h4">{name}</span></div><div class="rows">{it}</div></div>'
final[1] = f'''<section class="page">{run('Contenido')}
<div class="g" style="margin-top:9mm">
 <div style="grid-column:1/4"><h2 class="d1" style="font-size:38pt">Contenido</h2><p class="p s" style="margin-top:5mm">Siete partes, maquetas y fotografía de producto, con la ficha de producción.</p></div>
 <div style="grid-column:4/13;display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm;row-gap:7mm">{cols}</div>
</div>{FOL}</section>'''

for i in range(len(final)):
    final[i] = final[i].replace('%%N%%', f'{i+1:02d}')
html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>HALVEX · Material corporativo</title><style>{CSS}</style></head><body>{C.DEFS}' + ''.join(final) + '</body></html>')
open(os.path.join(HERE, 'material.html'), 'w').write(html)
print(len(final), 'páginas')

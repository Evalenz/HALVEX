import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# estilos y utilidades compartidos con la plataforma de marca
exec(open(os.path.join(HERE, 'plataforma2.py')).read().split('P = []')[0])
from common import horiz, vert, H_VB, contraste, rgb, cmyk

DOC = 'Identidad visual'
NEG, GRAF, ACE, NIE, LIN, PIE, BLA = '#111214', '#1A1B1E', '#65676C', '#A3A4A8', '#D8D6D0', '#EFEDE8', '#FFFFFF'
PART = {'I': 'La marca', 'II': 'Color y tipografía', 'III': 'Lenguaje gráfico', 'IV': 'Aplicaciones'}
CSS += r'''
.box{display:flex;align-items:center;justify-content:center;position:relative}
.box .cap{position:absolute;left:3.5mm;top:3mm}
.bd{box-shadow:inset 0 0 0 .2mm #D8D6D0}
.lbl{margin-top:2.4mm}
.lbl b{display:block;font-weight:500;font-size:8.8pt}
.lbl span{font-size:8pt;color:#65676C;line-height:1.45;display:block;margin-top:.5mm}
.fx{display:grid;grid-template-columns:30mm 1fr;padding:2.6mm 0;border-top:.2mm solid #D8D6D0;align-items:baseline}
.fxs>.fx:last-child{border-bottom:.2mm solid #D8D6D0}
.fx .v{font-size:8.8pt;line-height:1.5}
.icn{display:grid;grid-template-columns:repeat(6,1fr);border-top:.2mm solid #D8D6D0;border-left:.2mm solid #D8D6D0}
.icn>div{border-right:.2mm solid #D8D6D0;border-bottom:.2mm solid #D8D6D0;height:42mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm}
.icn svg{width:12mm;height:12mm}
.icn span{font-family:"IBM Plex Mono",monospace;font-size:6pt;letter-spacing:.05em;text-transform:uppercase;color:#65676C}
.si li,.no li{list-style:none;font-size:8.8pt;line-height:1.45;padding:2mm 0;border-bottom:.2mm solid #D8D6D0}
.si li:first-child,.no li:first-child{border-top:.25mm solid #111214}
.si li::before{content:"";display:inline-block;width:1.7mm;height:1.7mm;background:#111214;transform:rotate(45deg);margin-right:2.8mm;vertical-align:.3mm}
.no li{color:#65676C}
.no li::before{content:"×";margin-right:2.6mm;color:#111214}
'''

P = []
n = 0


def chhead(num, title, k=''):
    return f'<div class="ch"><span class="num">{num}</span><h2>{title}</h2><span class="k m s">{k}</span></div>'


def page(inner, part='', chap='', cls='', run=True, fol=True):
    global n
    n += 1
    r = ''
    if run:
        r = (f'<div class="run m"><span><b>HALVEX</b>&nbsp;&nbsp;&nbsp;{DOC}</span>'
             f'<span>{("Parte " + part + " · " + PART[part]) if part else ""}</span><span>{chap}</span></div>')
    f = f'<div class="fol"><span class="m s">Edición 1.0 · Noviembre 2026</span><span class="n">{n:02d}</span></div>' if fol else ''
    P.append(f'<section class="page {cls}">{r}{inner}{f}</section>')


def divider(roman, name, photo, intro, items, pos='center'):
    global n
    n += 1
    it = ''.join(f'<div class="row" style="grid-template-columns:10mm 1fr 8mm;padding:2.3mm 0"><span class="m s">{a}</span><span style="font-size:10.5pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
    P.append(f'''<section class="page dk" style="padding:0">
<div class="photo" style="position:absolute;left:0;top:0;bottom:0;width:50%;background-image:url({img64(photo)});background-position:{pos}"></div>
<div style="position:absolute;left:50%;right:0;top:0;bottom:0;padding:14mm 18mm 0 14mm">
 <div class="m" style="display:flex;justify-content:space-between;border-bottom:.25mm solid rgba(255,255,255,.6);padding-bottom:2.4mm"><span>Parte {roman}</span><span class="s">{n:02d}</span></div>
 <p style="font-weight:200;font-size:130pt;line-height:.8;letter-spacing:-.06em;margin-top:13mm">{roman}</p>
 <h2 class="d1" style="font-size:36pt;margin-top:7mm">{name}</h2>
 <p class="lead" style="margin-top:4mm;color:#C9CACD;max-width:100mm;font-size:11pt">{intro}</p>
 <div class="rows" style="position:absolute;left:14mm;right:18mm;bottom:14mm">{it}</div>
</div></section>''')


toc = [('I', 'La marca', [('01', 'Logotipo', 5), ('02', 'Isotipo', 6), ('03', 'Imagotipo', 7), ('04', 'Versiones del logo', 8),
                          ('05', 'Área de respeto y tamaño mínimo', 9), ('06', 'Versiones monocromáticas', 10),
                          ('07', 'Fondos e imágenes', 11), ('08', 'Usos incorrectos', 12)]),
       ('II', 'Color y tipografía', [('09', 'Color identificativo', 14), ('10', 'Paleta cromática', 15), ('11', 'Contraste', 16),
                                     ('12', 'Tipografía principal', 17), ('13', 'Tipografía secundaria y jerarquía', 18)]),
       ('III', 'Lenguaje gráfico', [('14', 'Elementos gráficos', 20), ('15', 'Patrones', 21), ('16', 'Iconografía', 22),
                                    ('17', 'Estilo fotográfico', 23), ('18', 'Estilo de ilustración', 24)]),
       ('IV', 'Aplicaciones', [('19', 'Papelería', 26), ('20', 'Entorno digital', 27), ('21', 'Presentaciones', 28), ('22', 'Archivos del logo', 29)])]

# ======================= 1 · PORTADA =======================
n += 1
P.append(f'''<section class="page dk" style="padding:14mm 18mm">
<div style="display:flex;justify-content:space-between" class="m"><span><b style="font-weight:500">HALVEX</b></span><span>Documento 02 / 02</span><span>Edición 1.0 · Noviembre 2026</span></div>
<svg viewBox="0 0 297 210" style="position:absolute;left:0;top:0;width:297mm;height:210mm">{iso_g(122, 50, 192, '#FFFFFF')}</svg>
<div style="position:absolute;left:18mm;top:46mm;width:120mm">
 <p class="m s">Manual de identidad</p>
 <h1 class="d1" style="font-size:58pt;margin-top:5mm">Identidad<br><b>visual</b></h1>
 <p class="lead" style="margin-top:7mm;color:#C9CACD;max-width:92mm">Cómo se dibuja, se compone y se aplica la marca HALVEX en cualquier soporte.</p>
</div>
<div style="position:absolute;left:18mm;bottom:14mm;width:110mm;border-top:.25mm solid rgba(255,255,255,.5);padding-top:2.6mm" class="m">La marca · Color y tipografía · Lenguaje gráfico · Aplicaciones</div>
</section>''')

# ======================= 2 · CONTENIDO =======================
cols = ''
for roman, name, items in toc:
    it = ''.join(f'<div class="row" style="grid-template-columns:9mm 1fr 8mm;padding:1.9mm 0"><span class="m s">{a}</span><span style="font-size:9.8pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
    cols += f'<div><div style="display:flex;align-items:baseline;gap:4mm;padding-bottom:2.6mm"><span style="font-weight:200;font-size:28pt;letter-spacing:-.04em;line-height:1">{roman}</span><span class="h3">{name}</span></div><div class="rows">{it}</div></div>'
page(f'''<div class="g" style="margin-top:10mm">
 <div style="grid-column:1/5"><h2 class="d1" style="font-size:40pt">Contenido</h2>
  <p class="p s" style="margin-top:6mm;max-width:68mm">Cuatro partes y veintidós capítulos. Quién es HALVEX y cómo habla se recoge en el documento 01, Plataforma de marca.</p></div>
 <div style="grid-column:5/13;display:grid;grid-template-columns:1fr 1fr;column-gap:9mm;row-gap:7mm">{cols}</div>
</div>''', chap='Contenido')

# ======================= 3 · INTRODUCCIÓN =======================
pr = [('Forma antes que color', 'La marca se reconoce por el dibujo de sus cuñas y de sus letras, no por un tono.'),
      ('Contraste máximo', 'Negro sobre blanco y blanco sobre negro: la lectura más clara y con más autoridad.'),
      ('Espacio', 'El vacío es parte del diseño. Pocas cosas por página, con aire alrededor.'),
      ('Precisión', 'Filetes, cotas y retículas: el oficio de quien mide antes de actuar.')]
prr = ''.join(f'<div class="row" style="grid-template-columns:52mm 1fr;padding:3.2mm 0"><span class="h4">{a}</span><span class="p">{b}</span></div>' for a, b in pr)
page(f'''<div class="g" style="margin-top:12mm">
 <p class="m s" style="grid-column:1/3">Introducción</p>
 <h2 class="d1" style="grid-column:3/11;font-size:38pt">Un sistema en <b>blanco y negro.</b></h2>
</div>
<div class="g" style="margin-top:12mm">
 <div style="grid-column:3/7">
  <p class="p">HALVEX no necesita un color para reconocerse. El negro y el blanco dan la máxima autoridad y contraste, funcionan en cualquier soporte, de una pantalla a un grabado en metal, y no pasan de moda.</p>
  <p class="p">La calidez la aporta el Piedra, un blanco de papel y caliza. El carácter, la tipografía y las líneas de construcción. Así la marca es sobria sin resultar fría.</p>
 </div>
 <div class="rows" style="grid-column:8/13">{prr}</div>
</div>''', chap='Introducción')

# ======================= 4 · PARTE I =======================
divider('I', 'La marca', 'hq-portada', 'El logotipo, el isotipo y sus versiones: cómo se construyen, cómo se combinan y cómo no se usan.', toc[0][2])

# ======================= 5 · LOGOTIPO =======================
g = ['<svg viewBox="-30 -50 612 200" style="width:100%;height:auto">']
for y in (0, 100):
    g.append(f'<path d="M-30 {y}H582" stroke="{NIE}" stroke-width=".6" stroke-dasharray="3 3"/>')
g.append(f'<g font-family="IBM Plex Mono" font-size="7.5" letter-spacing=".6" fill="{ACE}"><text x="582" y="-6" text-anchor="end">ALTURA DE LETRA · 100</text><text x="582" y="112" text-anchor="end">LÍNEA BASE</text></g>')
g.append(wm_g(0, 0, 100, NEG))
g.append(f'<g stroke="{NEG}" stroke-width=".7" fill="none"><path d="M0 -22V-14M15 -22V-14M0 -18H15"/><path d="M146 -3V-32"/><path d="M312 103V132"/><path d="M464 -14V-22M552 -14V-22M464 -18H552"/></g>')
g.append(f'<g font-family="IBM Plex Mono" font-size="7.5" letter-spacing=".6" fill="{NEG}"><text x="7.5" y="-27" text-anchor="middle">15</text><text x="146" y="-37" text-anchor="middle">A SIN TRAVESAÑO</text><text x="312" y="143" text-anchor="middle">COMPENSACIÓN ÓPTICA · 3</text><text x="508" y="-27" text-anchor="middle">X COMPLETA · 88</text></g></svg>')
page(f'''{chhead('01', 'Logotipo', 'La palabra')}
<div class="g" style="margin-top:14mm">
 <div style="grid-column:1/9">{''.join(g)}</div>
 <div style="grid-column:9/13;padding-left:5mm">
  <p class="p">El logotipo es la palabra HALVEX dibujada a medida. No es una fuente: no se escribe, se coloca siempre desde los archivos originales.</p>
  <div class="fxs" style="margin-top:5mm">
   <div class="fx"><span class="m s">Trazo</span><span class="v">Constante: 15 de cada 100 de altura.</span></div>
   <div class="fx"><span class="m s">La A</span><span class="v">Sin travesaño. Repite el ángulo del isotipo.</span></div>
   <div class="fx"><span class="m s">V y X</span><span class="v">Completas. La V baja 3 unidades para compensar su punta.</span></div>
   <div class="fx"><span class="m s">Espaciado</span><span class="v">Fijo. No se abre ni se cierra.</span></div>
  </div>
 </div>
</div>''', 'I', '01 · Logotipo')

# ======================= 6 · ISOTIPO =======================
plan = f'''<svg viewBox="-8 -8 216 222" style="width:100%;height:auto;overflow:visible">
<g fill="none" stroke="{NIE}" stroke-width=".45"><path d="M2 20H198"/><path d="M100 2V206" stroke-dasharray="1.5 1.5"/><path d="M24 20L14.5 0M176 20L185.5 0"/>
<path d="M96.2 172L100 180L103.8 172" stroke-dasharray="1.5 1.5"/><circle cx="100" cy="180" r="2"/><path d="M100 120A60 60 0 0 0 74.3 125.8"/></g>
<g fill="none" stroke="{NEG}" stroke-width=".55"><path d="M24 194H176M24 191V197M176 191V197"/><path d="M190 20V172M187 20H193M187 172H193"/><path d="M24 14V8M60 14V8M140 14V8M176 14V8"/></g>
<path fill="{NEG}" d="{ISO_D[0]}"/><path fill="{NEG}" d="{ISO_D[1]}"/>
<g font-family="IBM Plex Mono" font-size="4.3" letter-spacing=".25" fill="{ACE}"><text x="38" y="6.5">36</text><text x="154" y="6.5">36</text><text x="94" y="203">152</text>
<text x="193" y="91" transform="rotate(90 193 91)">152</text><text x="54" y="131">25,4°</text><text x="106" y="185">VÉRTICE VIRTUAL · AIRE 7,6</text></g></svg>'''
page(f'''{chhead('02', 'Isotipo', 'El símbolo')}
<div class="g" style="margin-top:3mm">
 <div style="grid-column:2/7">{plan}</div>
 <div style="grid-column:8/13;padding-top:8mm">
  <p class="lead">Dos cuñas que bajan hacia un mismo punto y se detienen antes de tocarse. Arriba, la apertura: la mirada amplia. Abajo, el vértice: la decisión precisa.</p>
  <div class="fxs" style="margin-top:7mm">
   <div class="fx"><span class="m s">Retícula</span><span class="v">Cuadrado de 152 × 152 unidades.</span></div>
   <div class="fx"><span class="m s">Boca</span><span class="v">36 unidades por cuña. Es la medida del área de respeto (x).</span></div>
   <div class="fx"><span class="m s">Vértice</span><span class="v">Virtual: las cuñas convergen en un punto que no se dibuja.</span></div>
   <div class="fx"><span class="m s">Aire</span><span class="v">7,6 unidades entre las puntas. Nunca se cierra.</span></div>
   <div class="fx"><span class="m s">Uso</span><span class="v">Firma reducida, icono, avatar y sello. No sustituye al imagotipo en la primera aparición.</span></div>
  </div>
 </div>
</div>''', 'I', '02 · Isotipo')

# ======================= 7 · IMAGOTIPO =======================
cot = f'''<svg viewBox="-110 -60 1000 270" style="width:100%;height:auto">
{iso_g(0, -30, 160, NEG)}{wm_g(232, 0, 100, NEG)}
<g stroke="{ACE}" stroke-width=".8" fill="none"><path d="M-26 -30V130M-31 -30H-21M-31 130H-21"/><path d="M800 0V100M795 0H805M795 100H805"/><path d="M160 160H232M160 155V165M232 155V165"/></g>
<g stroke="{NIE}" stroke-width=".6" fill="none"><path d="M-40 -30H784M-40 130H784" stroke-dasharray="3 3"/><path d="M-40 50H784" stroke-dasharray="1 4"/></g>
<g font-family="IBM Plex Mono" font-size="11" letter-spacing=".6" fill="{ACE}"><text x="-34" y="54" text-anchor="end">1,6 A</text><text x="812" y="54">A</text><text x="196" y="184" text-anchor="middle">0,45 × ISOTIPO</text><text x="784" y="148" text-anchor="end">EJE ÓPTICO COMÚN</text></g></svg>'''
facts = [('Proporción', 'El isotipo mide 1,6 veces la altura de letra (A).'), ('Separación', '0,45 veces la altura del isotipo.'),
         ('Alineación', 'Centrados sobre el mismo eje horizontal.'), ('Color', 'Una sola tinta: negro o blanco.')]
ff = ''.join(f'<div class="r" style="padding-top:3mm"><p class="m s">{a}</p><p class="p" style="margin-top:1.5mm">{b}</p></div>' for i, (a, b) in enumerate(facts))
page(f'''{chhead('03', 'Imagotipo', 'La firma principal')}
<div class="g" style="margin-top:8mm"><div style="grid-column:2/12">{cot}</div></div>
<div class="g" style="position:absolute;left:18mm;right:18mm;bottom:22mm">
 <p class="p" style="grid-column:1/5;padding-top:3mm;padding-right:6mm">El imagotipo une isotipo y logotipo. Es la firma de HALVEX por defecto: web, documentos, propuestas y cualquier primera aparición de la marca.</p>
 <div style="grid-column:5/13;display:grid;grid-template-columns:repeat(4,1fr);column-gap:5mm">{ff}</div>
</div>''', 'I', '03 · Imagotipo')

# ======================= 8 · VERSIONES =======================
fav = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:2mm"><div style="width:{s}mm;height:{s}mm;background:{NEG};display:flex;align-items:center;justify-content:center">{iso(f"width:{s*.58:.2f}mm;height:{s*.58:.2f}mm", BLA)}</div><span class="m s">{l}</span></div>' for s, l in ((15, '512 px'), (9, '64 px'), (5, '32 px'), (3, '16 px')))
page(f'''{chhead('04', 'Versiones <b>del logo</b>', 'Una versión para cada espacio')}
<div style="display:grid;grid-template-columns:1.55fr 1fr 1fr;gap:5mm;margin-top:8mm">
 <div><div class="box bd" style="height:60mm">{horiz(NEG, NEG, 'width:72%;height:auto')}<span class="cap m s">A · Horizontal</span></div><div class="lbl"><b>Horizontal · principal</b><span>Web, documentos, firmas y cabeceras. La versión por defecto.</span></div></div>
 <div><div class="box bd" style="height:60mm">{vert(NEG, NEG, 'width:62%;height:auto')}<span class="cap m s">B · Vertical</span></div><div class="lbl"><b>Vertical</b><span>Formatos estrechos o cuadrados: portadas, carteles, perfiles.</span></div></div>
 <div><div class="box bd" style="height:60mm">{iso('width:30mm;height:30mm', NEG)}<span class="cap m s">C · Reducido</span></div><div class="lbl"><b>Reducido · isotipo</b><span>Iconos, avatares, sellos y espacios muy pequeños.</span></div></div>
</div>
<div style="display:grid;grid-template-columns:1.55fr 2fr;gap:5mm;margin-top:6mm">
 <div><div class="box bd" style="height:30mm">{wm('width:56%;height:auto', NEG)}<span class="cap m s">D · Logotipo</span></div><div class="lbl"><b>Solo logotipo</b><span>Cuando el isotipo ya está cerca o el espacio es muy horizontal.</span></div></div>
 <div><div class="box bd" style="height:30mm;justify-content:flex-end;gap:8mm;padding-right:10mm;align-items:flex-end;padding-bottom:4mm">{fav}<span class="cap m s">E · Icono y favicon</span></div><div class="lbl"><b>Icono</b><span>Isotipo blanco sobre negro. El sistema operativo aplica sus propias esquinas.</span></div></div>
</div>''', 'I', '04 · Versiones del logo')

# ======================= 9 · ÁREA DE RESPETO =======================
x = 37.9
ar = [f'<svg viewBox="-80 -112 944 384" style="width:100%;height:auto">',
      f'<rect x="{-x}" y="{-30-x}" width="{784+2*x}" height="{160+2*x}" fill="none" stroke="{NEG}" stroke-width=".8" stroke-dasharray="4 3"/>',
      f'<rect x="0" y="-30" width="784" height="160" fill="none" stroke="{NIE}" stroke-width=".6"/>', iso_g(0, -30, 160, NEG) + wm_g(232, 0, 100, NEG)]
for (cx, cy) in ((-x, -30 - x), (784, -30 - x), (-x, 130), (784, 130)):
    ar.append(f'<rect x="{cx}" y="{cy}" width="{x}" height="{x}" fill="{PIE}"/><text x="{cx+x/2}" y="{cy+x/2+4}" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="{NEG}">x</text>')
ar.append(f'<path d="M0 -86H37.9M0 -91V-81M37.9 -91V-81" stroke="{NEG}" stroke-width=".8"/><text x="48" y="-82" font-family="IBM Plex Mono" font-size="11" letter-spacing=".6" fill="{ACE}">x = BOCA DE UNA CUÑA</text></svg>')
mins = [('Horizontal', '30 mm', '120 px', horiz(NEG, NEG, 'width:30mm;height:auto')), ('Vertical', '18 mm', '72 px', vert(NEG, NEG, 'width:18mm;height:auto')),
        ('Isotipo', '5 mm', '16 px', iso('width:5mm;height:5mm', NEG)), ('Logotipo', '22 mm', '90 px', wm('width:22mm;height:auto', NEG))]
mm = ''.join(f'<div class="row" style="grid-template-columns:34mm 1fr;align-items:center;padding:3.2mm 0"><div>{s}</div><div><b style="font-weight:500;font-size:9pt">{a}</b><p class="m s" style="margin-top:1mm">Impreso {b} · Pantalla {c}</p></div></div>' for a, b, c, s in mins)
page(f'''{chhead('05', 'Área de respeto <b>y tamaño mínimo</b>', '')}
<div class="g" style="margin-top:9mm">
 <div style="grid-column:1/9">{''.join(ar)}<p class="p s" style="margin-top:4mm;max-width:125mm">Ningún texto, imagen ni borde entra en el área de respeto. Su medida, x, es la boca de una cuña del isotipo, así que crece y decrece con el logo.</p></div>
 <div style="grid-column:9/13;padding-left:4mm"><p class="m s" style="margin-bottom:2mm">Tamaño mínimo · ancho</p><div class="rows">{mm}</div></div>
</div>''', 'I', '05 · Área de respeto y tamaño mínimo')

# ======================= 10 · MONOCROMÁTICAS =======================
ph = img64('hq-portada')
tiles = [('Positivo', 'Negro sobre blanco. La versión principal.', BLA, NEG, True, ''),
         ('Negativo', 'Blanco sobre negro o grafito.', NEG, BLA, False, ''),
         ('Sobre Piedra', 'Negro sobre el blanco cálido de la marca.', PIE, NEG, False, ''),
         ('Gris Acero', 'Una tinta gris para usos discretos: marcas de agua y pies.', BLA, ACE, True, ''),
         ('Sobre grafito', 'Blanco sobre las superficies oscuras de pantalla.', GRAF, BLA, False, ''),
         ('Sobre fotografía', 'Blanco, solo en zonas oscuras y tranquilas.', NEG, BLA, False, f"background-image:linear-gradient(rgba(0,0,0,.25),rgba(0,0,0,.25)),url({ph});background-size:cover;background-position:center 30%")]
tt = ''.join(f'<div><div class="box {"bd" if b else ""}" style="height:45mm;background:{bg};{ex}">{horiz(c, c, "width:62%;height:auto")}</div><div class="lbl"><b>{t}</b><span>{d}</span></div></div>' for t, d, bg, c, b, ex in tiles)
page(f'''{chhead('06', 'Versiones <b>monocromáticas</b>', 'Siempre una sola tinta')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:5mm;row-gap:5mm;margin-top:7mm">{tt}</div>''', 'I', '06 · Versiones monocromáticas')

# ======================= 11 · FONDOS =======================
steps = ''
for i in range(11):
    v = round(255 - i * 25.5); hx = '#%02x%02x%02x' % (v, v, v)
    c = NEG if i <= 4 else BLA
    ok = 'Negro' if i <= 3 else ('Evitar' if i in (4, 5, 6) else 'Blanco')
    sty = 'opacity:.35' if ok == 'Evitar' else ''
    steps += f'<div style="flex:1;display:flex;flex-direction:column"><div style="height:26mm;background:{hx};display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 .15mm #D8D6D0"><div style="{sty}">{iso("width:9mm;height:9mm", c)}</div></div><span class="m s" style="margin-top:1.6mm;text-align:center">{i*10} %</span><span class="m" style="text-align:center">{ok}</span></div>'
pl, pd, pb = img64('hq-salud'), img64('hq-portada'), img64('hq-energia')
def ptile(img, pos, logo, t, d, bad=False):
    x_ = f'<span style="position:absolute;right:3mm;top:3mm;width:6mm;height:6mm;background:#fff;display:flex;align-items:center;justify-content:center;font-size:12pt">×</span>' if bad else ''
    return f'<div><div class="photo box" style="height:50mm;background-image:url({img});background-position:{pos}">{logo}{x_}</div><div class="lbl"><b>{t}</b><span>{d}</span></div></div>'
page(f'''{chhead('07', 'Fondos <b>e imágenes</b>', 'Qué versión sobre cada fondo')}
<div style="display:flex;gap:1.6mm;margin-top:8mm">{steps}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:5mm;margin-top:7mm">
 {ptile(pl, 'center 35%', horiz(NEG, NEG, 'width:55%;height:auto'), 'Fondo claro', 'Logo negro en la zona más limpia de la imagen.')}
 {ptile(pd, 'center 30%', horiz(BLA, BLA, 'width:55%;height:auto'), 'Fondo oscuro', 'Logo blanco sobre sombras amplias y uniformes.')}
 {ptile(pb, 'center', horiz(BLA, BLA, 'width:55%;height:auto'), 'Fondo con detalle', 'Nunca sobre texturas o líneas que compitan con el logo.', True)}
</div>''', 'I', '07 · Fondos e imágenes')

# ======================= 12 · USOS INCORRECTOS =======================
def Hs(style='', c=NEG, extra_g=''):
    return f'<svg viewBox="{H_VB}" style="width:64%;height:auto;{style}">{iso_g(0,-30,160,c)}{wm_g(232,0,100,c)}</svg>'
grad = f'<svg viewBox="{H_VB}" style="width:64%;height:auto"><defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" stop-color="#111214"/><stop offset="1" stop-color="#B8B9BC"/></linearGradient></defs><g fill="url(#gr)">{iso_g(0,-30,160,"url(#gr)")}{wm_g(232,0,100,"url(#gr)")}</g></svg>'
outline = f'<svg viewBox="{H_VB}" style="width:64%;height:auto"><g fill="none" stroke="{NEG}" stroke-width="3">{iso_g(0,-30,160,"none")}{wm_g(232,0,100,"none")}</g></svg>'
order = f'<svg viewBox="0 -30 784 160" style="width:64%;height:auto">{wm_g(0,0,100,NEG)}{iso_g(624,-30,160,NEG)}</svg>'
bads = [('No deformar', Hs('transform:scaleX(1.35) scaleY(.8)'), BLA), ('No girar', Hs('transform:rotate(-12deg)'), BLA),
        ('No añadir color', Hs('', '#2456A6'), BLA), ('No usar degradados', grad, BLA),
        ('No añadir sombras ni efectos', Hs('filter:drop-shadow(1.6mm 1.6mm 1mm rgba(0,0,0,.45))'), BLA), ('No usar solo el contorno', outline, BLA),
        ('No cambiar el orden', order, BLA), ('No usar fondos sin contraste', Hs('', '#5E6064'), '#808286')]
X = '<span style="position:absolute;right:3mm;top:2.4mm;font-size:13pt;line-height:1">×</span>'
bb = ''.join(f'<div><div class="box bd" style="height:43mm;background:{bg}">{s}{X}</div><div class="lbl"><b>{t}</b></div></div>' for t, s, bg in bads)
page(f'''{chhead('08', 'Usos <b>incorrectos</b>', 'Lo que nunca se hace')}
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:5mm;row-gap:4mm;margin-top:7mm">{bb}</div>''', 'I', '08 · Usos incorrectos')

# ======================= 13 · PARTE II =======================
divider('II', 'Color y tipografía', 'hq-escaleras', 'Un color que es una decisión, una paleta de neutros y una familia tipográfica de origen técnico.', toc[1][2])

# ======================= 14 · COLOR IDENTIFICATIVO =======================
r_, g_, b_ = rgb(NEG); c_, m_, y_, k_ = cmyk(NEG)
n += 1
P.append(f'''<section class="page" style="padding:0">
<div style="position:absolute;left:0;top:0;bottom:0;width:58%;background:{NEG};color:#fff;padding:14mm 18mm">
 <div class="m" style="display:flex;justify-content:space-between;border-bottom:.25mm solid rgba(255,255,255,.6);padding-bottom:2.4mm"><span><b style="font-weight:500">HALVEX</b>&nbsp;&nbsp;&nbsp;Identidad visual</span><span>Parte II · Color y tipografía</span></div>
 <p style="position:absolute;left:18mm;bottom:50mm;font-weight:200;font-size:66pt;letter-spacing:-.045em;line-height:.95">Negro<br><b style="font-weight:400">HALVEX</b></p>
 <div class="m" style="position:absolute;left:18mm;right:18mm;bottom:14mm;display:grid;grid-template-columns:repeat(4,1fr);border-top:.25mm solid rgba(255,255,255,.6);padding-top:2.8mm">
  <span>HEX<br>{NEG}</span><span>RGB<br>{r_} · {g_} · {b_}</span><span>CMYK*<br>60 · 40 · 40 · 100</span><span>Pantone*<br>Black 6 C</span></div>
</div>
<div style="position:absolute;left:58%;right:0;top:0;bottom:0;padding:14mm 18mm 0 12mm">
 <div class="m" style="text-align:right;border-bottom:.25mm solid #111214;padding-bottom:2.4mm">09 · Color identificativo</div>
 <h2 class="d1" style="font-size:28pt;margin-top:11mm">El color <b>de la autoridad.</b></h2>
 <p class="p" style="margin-top:6mm">El color de HALVEX es un negro profundo con un punto frío: el de la tinta, el acero pavonado y la pantalla apagada. Es el tono de lo que no necesita llamar la atención.</p>
 <p class="p">En un sector lleno de azules, el negro distingue. Da autoridad, contraste máximo y funciona igual en una pantalla que impreso o grabado.</p>
 <div class="fxs" style="margin-top:6mm">
  <div class="fx"><span class="m s">Uso</span><span class="v">Logotipo, textos, superficies oscuras y fondos de portada.</span></div>
  <div class="fx"><span class="m s">Su pareja</span><span class="v">El Piedra, un blanco cálido que evita la frialdad.</span></div>
  <div class="fx"><span class="m s">Impresión</span><span class="v">Negro enriquecido en grandes superficies; negro 100 % en textos pequeños.</span></div>
 </div>
 <p class="m s" style="position:absolute;bottom:10mm;left:12mm;right:18mm;text-transform:none;letter-spacing:.02em">* CMYK de negro enriquecido y Pantone de referencia: confirmar con prueba de imprenta.</p>
</div></section>''')

# ======================= 15 · PALETA =======================
pal = [('Negro HALVEX', NEG, 'Black 6 C', 'Identificativo · logo y texto', BLA),
       ('Grafito', GRAF, '—', 'Superficies oscuras en pantalla', BLA),
       ('Acero', ACE, 'Cool Gray 10 C', 'Texto secundario', BLA),
       ('Niebla', NIE, 'Cool Gray 6 C', 'Datos, inactivo, decoración', NEG),
       ('Línea', LIN, 'Warm Gray 2 C', 'Filetes y separadores', NEG),
       ('Piedra', PIE, 'Warm Gray 1 C', 'Fondos de sección', NEG),
       ('Blanco', BLA, '—', 'Fondo principal', NEG)]
cc = ''
for name, hx, pm, use, fg in pal:
    r1, g1, b1 = rgb(hx); cm = cmyk(hx)
    if hx == NEG: cm = (60, 40, 40, 100)
    sh = 'box-shadow:inset 0 0 0 .2mm #D8D6D0;' if hx in (BLA, PIE, LIN) else ''
    cc += (f'<div><div style="height:58mm;padding:3.5mm;display:flex;flex-direction:column;justify-content:space-between;background:{hx};color:{fg};{sh}"><span class="m">{use}</span><b style="font-weight:400;font-size:12pt">{name}</b></div>'
           f'<div class="rows" style="margin-top:2.4mm">' + ''.join(f'<div class="row" style="grid-template-columns:14mm 1fr;padding:1.1mm 0"><span class="m s">{a}</span><span class="m">{b}</span></div>' for a, b in (('Hex', hx), ('RGB', f'{r1} {g1} {b1}'), ('CMYK', ' '.join(map(str, cm))), ('Pantone', pm))) + '</div></div>')
prop = [(BLA, 56, 'Blanco 56 %'), (NEG, 22, 'Negro 22 %'), (PIE, 12, 'Piedra 12 %'), (GRAF, 4, ''), (ACE, 3, ''), (NIE, 2, ''), (LIN, 1, '')]
pb_ = ''.join(f'<div style="flex:{w};background:{hx};box-shadow:inset 0 0 0 .2mm #D8D6D0;display:flex;align-items:flex-end;padding:1.6mm"><span class="m" style="color:{BLA if hx in (NEG, GRAF, ACE) else NEG};white-space:nowrap">{t}</span></div>' for hx, w, t in prop)
page(f'''{chhead('10', 'Paleta <b>cromática</b>', 'Neutros con intención')}
<div style="display:grid;grid-template-columns:repeat(7,1fr);column-gap:3.5mm;margin-top:7mm">{cc}</div>
<div style="margin-top:6mm"><p class="m s" style="margin-bottom:2mm">Proporción de uso</p><div style="display:flex;height:10mm">{pb_}</div></div>
<p class="m s" style="margin-top:2.5mm;text-transform:none;letter-spacing:.02em">CMYK y Pantone son referencias orientativas: confirmar con prueba de imprenta y guía física.</p>''', 'II', '10 · Paleta cromática')

# ======================= 16 · CONTRASTE =======================
combos = [(NEG, BLA, 'Negro sobre Blanco', 'Texto principal'), (BLA, NEG, 'Blanco sobre Negro', 'Portadas y secciones oscuras'),
          (NEG, PIE, 'Negro sobre Piedra', 'Fondos de sección'), (BLA, GRAF, 'Blanco sobre Grafito', 'Pantallas oscuras'),
          (ACE, BLA, 'Acero sobre Blanco', 'Texto secundario'), (NIE, GRAF, 'Niebla sobre Grafito', 'Texto secundario en oscuro'),
          (NIE, BLA, 'Niebla sobre Blanco', 'Solo decoración'), (ACE, GRAF, 'Acero sobre Grafito', 'No apto para texto')]
def verdict(cr):
    return 'AAA' if cr >= 7 else 'AA' if cr >= 4.5 else 'Solo grande' if cr >= 3 else 'No apto'
rows = []
for fg, bg, t, u in combos:
    cr = contraste(fg, bg)
    rows.append(f'<div class="row" style="grid-template-columns:26mm 1fr 20mm 20mm;align-items:center;padding:0;border-color:#D8D6D0"><span style="height:14mm;background:{bg};color:{fg};display:flex;align-items:center;justify-content:center;font-size:15pt;box-shadow:inset 0 0 0 .2mm #D8D6D0">Aa</span><span style="padding-left:4mm"><b style="font-weight:500;font-size:9pt">{t}</b><br><span class="p s" style="font-size:8pt">{u}</span></span><span class="m" style="text-align:right">{cr:.1f} : 1</span><span class="m" style="text-align:right">{verdict(cr)}</span></div>')
page(f'''{chhead('11', 'Contraste', 'Legibilidad según WCAG 2.1')}
<div class="g" style="margin-top:8mm">
 <div class="rows" style="grid-column:1/7">{''.join(rows[:4])}</div>
 <div class="rows" style="grid-column:7/13">{''.join(rows[4:])}</div>
</div>
<div class="g" style="margin-top:7mm"><p class="p s" style="grid-column:1/9">AA (4,5 : 1) es el mínimo para cualquier texto; AAA (7 : 1), lo recomendable para textos largos. Niebla y Acero sobre fondos oscuros solo valen para rótulos grandes o decoración.</p></div>''', 'II', '11 · Contraste')

# ======================= 17 · TIPOGRAFÍA PRINCIPAL =======================
wts = [(200, 'ExtraLight', 'Titulares grandes'), (300, 'Light', 'Entradillas'), (400, 'Regular', 'Texto'), (500, 'Medium', 'Énfasis y botones'), (600, 'SemiBold', 'Cifras destacadas')]
ww = ''.join(f'<div class="row" style="grid-template-columns:30mm 1fr 32mm;padding:2.4mm 0"><span class="m s">{w} · {nm}</span><span style="font-weight:{w};font-size:19pt;letter-spacing:-.02em;line-height:1.1">Sin margen de error</span><span class="m s" style="text-align:right">{u}</span></div>' for w, nm, u in wts)
page(f'''{chhead('12', 'Tipografía <b>principal</b>', 'IBM Plex Sans')}
<div class="g" style="margin-top:5mm">
 <div style="grid-column:1/5">
  <p style="font-weight:200;font-size:150pt;line-height:.8;letter-spacing:-.05em">Aa</p>
  <p class="p" style="margin-top:6mm">Diseñada para la tecnología y la ingeniería: neutra, exacta y muy legible en pantalla y papel. Licencia libre (SIL Open Font License), sin coste de uso.</p>
  <p style="font-size:10.5pt;font-weight:300;margin-top:5mm;line-height:1.55;letter-spacing:.02em">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz<br>0123456789 ¿?¡!(.,;:) € % · áéíóúü</p>
 </div>
 <div style="grid-column:6/13;padding-top:4mm"><div class="rows">{ww}</div>
  <p class="m s" style="margin-top:4mm;text-transform:none;letter-spacing:.02em">Sustitutas cuando Plex no está disponible (correo, ofimática): Helvetica Neue y Arial.</p></div>
</div>''', 'II', '12 · Tipografía principal')

# ======================= 18 · SECUNDARIA Y JERARQUÍA =======================
hier = [('Display', 'Plex Sans 200 · 44–120 pt', '<span style="font-weight:200;font-size:30pt;letter-spacing:-.035em">Hablemos.</span>'),
        ('Titular', 'Plex Sans 200 y 400 · 24–36 pt', '<span style="font-weight:200;font-size:19pt;letter-spacing:-.03em">Seis capacidades, <b style="font-weight:400">un mismo rigor.</b></span>'),
        ('Entradilla', 'Plex Sans 300 · 12–15 pt', '<span style="font-weight:300;font-size:12pt">Trabajamos donde se cruzan los datos, la seguridad y la operación.</span>'),
        ('Texto', 'Plex Sans 400 · 9–11 pt', '<span style="font-size:9pt">Modelos que analizan, anticipan y recomiendan, desplegados allí donde están los datos.</span>'),
        ('Etiqueta', 'Plex Mono 400 · 6,5–8 pt', '<span class="m" style="font-size:7pt">02 · Capacidades · Madrid 40.4168° N</span>')]
hh = ''.join(f'<div class="row" style="grid-template-columns:22mm 44mm 1fr;padding:3mm 0;align-items:baseline"><span class="m">{a}</span><span class="m s" style="text-transform:none;letter-spacing:.01em">{b}</span>{c}</div>' for a, b, c in hier)
page(f'''{chhead('13', 'Secundaria <b>y jerarquía</b>', 'IBM Plex Mono')}
<div class="g" style="margin-top:6mm">
 <div style="grid-column:1/4">
  <p style="font-family:'IBM Plex Mono';font-size:64pt;line-height:.9;letter-spacing:-.04em">Aa</p>
  <p class="p" style="margin-top:5mm">Plex Mono es para datos, cifras, coordenadas, numeración y etiquetas, siempre en mayúsculas con un 6 % de espaciado. Aporta el carácter técnico y nunca se usa en textos largos.</p>
  <p style="font-family:'IBM Plex Mono';font-size:8.2pt;margin-top:4mm;line-height:1.6">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>0123456789 · ° ' " / % €</p>
  <p class="m s" style="margin-top:4mm;text-transform:none;letter-spacing:.02em">Sustitutas: Menlo y Consolas.</p>
 </div>
 <div class="rows" style="grid-column:5/13">{hh}</div>
</div>''', 'II', '13 · Tipografía secundaria y jerarquía')

# ======================= 19 · PARTE III =======================
divider('III', 'Lenguaje gráfico', 'hq-equipo-w', 'Los recursos que hacen reconocible una pieza aunque no lleve el logo: líneas, patrones, iconos e imágenes.', toc[2][2])

# ======================= 20 · ELEMENTOS =======================
def el(svg_, t, d):
    return f'<div><div class="box bd" style="height:42mm">{svg_}</div><div class="lbl"><b>{t}</b><span>{d}</span></div></div>'
e1 = f'<svg viewBox="0 0 200 60" style="width:80%"><path d="M0 18H200" stroke="{NEG}" stroke-width="1.2"/><path d="M0 42H200" stroke="{LIN}" stroke-width=".8"/><g font-family="IBM Plex Mono" font-size="6.3" fill="{ACE}"><text x="0" y="12">FILETE PRINCIPAL · 0,5 PT</text><text x="0" y="36">FILETE SECUNDARIO · 0,35 PT</text></g></svg>'
e2 = f'<svg viewBox="0 0 200 60" style="width:80%"><g stroke="{NEG}" stroke-width=".8"><path d="M20 30H180M20 24V36M180 24V36"/><path d="M20 47H60M20 43V51M60 43V51"/></g><g font-family="IBM Plex Mono" font-size="7" fill="{ACE}"><text x="100" y="22" text-anchor="middle">152</text><text x="66" y="50">x</text></g></svg>'
e3 = f'<svg viewBox="0 0 200 60" style="width:80%"><path d="M30 22l8 8-8 8-8-8z" fill="{NEG}"/><text x="48" y="33" font-family="IBM Plex Sans" font-size="10" font-weight="500" fill="{NEG}">Contacto</text><path d="M130 22l8 8-8 8-8-8z" fill="none" stroke="{NEG}" stroke-width=".8"/><path d="M160 22l8 8-8 8-8-8z" fill="{NEG}"/></svg>'
e4 = f'<svg viewBox="0 0 200 60" style="width:80%"><text x="0" y="42" font-family="IBM Plex Sans" font-weight="200" font-size="36" letter-spacing="-1.6" fill="{NEG}">01</text><text x="50" y="42" font-family="IBM Plex Mono" font-size="8" fill="{ACE}">/ 06</text><g font-family="IBM Plex Mono" font-size="7" fill="{NEG}"><text x="112" y="24">PARTE II</text><text x="112" y="38">S/01</text><text x="112" y="52" fill="{ACE}">40.4168° N</text></g></svg>'
e5 = f'<svg viewBox="0 0 200 60" style="width:86%"><g stroke="{NEG}" stroke-width=".7" fill="none"><path d="M0 4L180 30M0 17L180 30M0 30H180M0 43L180 30M0 56L180 30"/></g><path d="M184 26l4 4-4 4-4-4z" fill="{NEG}"/></svg>'
e6 = f'<svg viewBox="0 0 200 60" style="width:80%">{iso_g(10, 6, 48, NEG)}<g transform="translate(76 6)"><path d="M0 0H70V48H0Z" fill="{PIE}"/><path d="M0 0L23 48H0Z" fill="{NEG}"/></g><text x="156" y="34" font-family="IBM Plex Mono" font-size="6.5" fill="{ACE}">CUÑA</text></svg>'
page(f'''{chhead('14', 'Elementos <b>gráficos</b>', 'Recursos de composición')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:5mm;row-gap:4mm;margin-top:7mm">
{el(e1, 'Filetes', 'Ordenan la página. Uno fuerte para abrir sección, finos para separar filas.')}
{el(e2, 'Cotas', 'Medidas técnicas como recurso gráfico: dan precisión y oficio.')}
{el(e3, 'Rombo', 'El cuadrado girado señala lo activo o lo importante.')}
{el(e4, 'Numeración', 'Plex Mono en mayúsculas para índices, partes y coordenadas.')}
{el(e5, 'Convergencia', 'Líneas que van de lo amplio a un punto: la idea de la marca en un gesto.')}
{el(e6, 'Cuña', 'El triángulo del isotipo como corte de color o de imagen, siempre con su ángulo.')}
</div>''', 'III', '14 · Elementos gráficos')

# ======================= 21 · PATRONES =======================
pat1 = (f'<svg viewBox="0 0 300 200" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%"><defs><pattern id="pw" width="30" height="30" patternUnits="userSpaceOnUse">'
        f'{iso_g(7, 7, 16, "#2A2B30")}</pattern></defs><rect width="300" height="200" fill="{GRAF}"/><rect width="300" height="200" fill="url(#pw)"/></svg>')
lines = ''.join(f'<path d="M0 {i*8}L300 100"/>' for i in range(0, 26))
pat2 = f'<svg viewBox="0 0 300 200" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%"><rect width="300" height="200" fill="{BLA}"/><g stroke="{NEG}" stroke-width=".35" fill="none">{lines}</g></svg>'
crs = ''.join(f'<path d="M{x_-2.5} {y_}H{x_+2.5}M{x_} {y_-2.5}V{y_+2.5}"/>' for x_ in range(20, 300, 40) for y_ in range(20, 200, 40))
pat3 = (f'<svg viewBox="0 0 300 200" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%"><defs><pattern id="pg" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0V10H0" fill="none" stroke="{LIN}" stroke-width=".3"/></pattern></defs>'
        f'<rect width="300" height="200" fill="{PIE}"/><rect width="300" height="200" fill="url(#pg)"/><g stroke="{NEG}" stroke-width=".5">{crs}</g></svg>')
def pt(svg_, t, d):
    return f'<div><div style="height:98mm;overflow:hidden;box-shadow:inset 0 0 0 .2mm #D8D6D0">{svg_}</div><div class="lbl"><b>{t}</b><span>{d}</span></div></div>'
page(f'''{chhead('15', 'Patrones', 'Fondos de marca')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:5mm;margin-top:7mm">
{pt(pat1, 'Trama de cuñas', 'El isotipo repetido, tono sobre tono en grafito. Portadas, embalaje y fondos de marca.')}
{pt(pat2, 'Convergencia', 'Líneas finas que se reúnen en un punto. Separadores y fondos de presentación.')}
{pt(pat3, 'Retícula técnica', 'Cuadrícula de plano con marcas de registro. Diagramas y fondos de datos.')}
</div>''', 'III', '15 · Patrones')

# ======================= 22 · ICONOGRAFÍA =======================
IC = [('IA', '<path d="M5 6L12 11L19 6M12 11V19"/><rect x="3" y="4" width="4" height="4"/><rect x="17" y="4" width="4" height="4"/><rect x="10" y="17" width="4" height="4"/><rect x="10.5" y="9.5" width="3" height="3"/>'),
      ('Seguridad', '<path d="M12 3L20 6V13L12 21L4 13V6Z"/><path d="M12 8V15"/>'),
      ('Defensa', '<path d="M12 5L19 12L12 19L5 12Z"/><path d="M12 2V6M12 18V22M2 12H6M18 12H22"/>'),
      ('Software', '<path d="M8 7L3 12L8 17M16 7L21 12L16 17M13.5 5L10.5 19"/>'),
      ('Automatización', '<path d="M4 12V9H17M14 6L17 9L14 12M20 12V15H7M10 18L7 15L10 12"/>'),
      ('Consultoría', '<path d="M12 3V21M3 12H21"/><path d="M12 7L14.5 12L12 17L9.5 12Z"/>'),
      ('Datos', '<path d="M12 4L21 8.5L12 13L3 8.5Z"/><path d="M3 12.5L12 17L21 12.5M3 16.5L12 21L21 16.5"/>'),
      ('Despliegue local', '<rect x="4" y="4" width="16" height="6"/><rect x="4" y="14" width="16" height="6"/><path d="M7 7H9M7 17H9"/>'),
      ('Supervisión', '<path d="M2 12L7 6H17L22 12L17 18H7Z"/><path d="M12 9L15 12L12 15L9 12Z"/>'),
      ('Infraestructura', '<path d="M8 21L12 3L16 21M9.6 14H14.4M10.8 8.5H13.2M5 7H19"/>'),
      ('Confidencial', '<path d="M6 3H14L18 7V21H6Z"/><path d="M14 3V7H18"/><path d="M12 11L15 14L12 17L9 14Z"/>'),
      ('Alerta', '<path d="M12 3L22 20H2Z"/><path d="M12 9V14M12 16V17.5"/>')]
def icon(p_):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{NEG}" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">{p_}</svg>'
ii = ''.join(f'<div>{icon(p_)}<span>{t}</span></div>' for t, p_ in IC)
gl = ''.join(f'<path d="M{i} 0V24M0 {i}H24"/>' for i in range(0, 25, 2))
big = (f'<svg viewBox="-2 -2 28 28" style="width:100%;height:auto"><g stroke="{LIN}" stroke-width=".06" fill="none">{gl}</g>'
       f'<rect x="2" y="2" width="20" height="20" fill="none" stroke="{ACE}" stroke-width=".08" stroke-dasharray=".4 .3"/>'
       f'<g fill="none" stroke="{NEG}" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter"><path d="M12 3L20 6V13L12 21L4 13V6Z"/><path d="M12 8V15"/></g></svg>')
page(f'''{chhead('16', 'Iconografía', 'Doce iconos de base')}
<div class="g" style="margin-top:7mm">
 <div style="grid-column:1/4">{big}
  <div class="fxs" style="margin-top:3mm"><div class="fx" style="grid-template-columns:20mm 1fr"><span class="m s">Retícula</span><span class="v">24 × 24, margen de 2.</span></div>
  <div class="fx" style="grid-template-columns:20mm 1fr"><span class="m s">Trazo</span><span class="v">1,5 constante, terminales rectos.</span></div>
  <div class="fx" style="grid-template-columns:20mm 1fr"><span class="m s">Formas</span><span class="v">Rectas y ángulos vivos. Sin relleno ni esquinas redondeadas.</span></div></div>
 </div>
 <div class="icn" style="grid-column:4/13;align-self:start">{ii}</div>
</div>''', 'III', '16 · Iconografía')

# ======================= 23 · FOTOGRAFÍA =======================
f1, f2, f3, f4 = img64('hero'), img64('equipo-w'), img64('escaleras'), img64('c-consultoria')
page(f'''{chhead('17', 'Estilo <b>fotográfico</b>', 'Blanco y negro, con aire')}
<div style="display:grid;grid-template-columns:1fr 1.5fr 1fr 1.3fr;grid-template-rows:58mm 46mm;gap:3.5mm;margin-top:6mm">
 <div class="photo" style="grid-row:1/3;background-image:url({f1})"></div>
 <div class="photo" style="background-image:url({f2})"></div>
 <div class="photo" style="grid-row:1/3;background-image:url({f4})"></div>
 <div style="grid-row:1/3">
  <ul class="si"><li>Blanco y negro, contraste alto y negros profundos.</li><li>Arquitectura, horizontes y líneas que convergen.</li><li>Personas reales, de espaldas o a contraluz, sin posar.</li><li>Luz natural y mucho espacio vacío.</li></ul>
  <ul class="no" style="margin-top:3mm"><li>Encapuchados, código binario y hologramas azules.</li><li>Apretones de manos y sonrisas de banco de imágenes.</li><li>Filtros de color y dramatismo bélico.</li></ul>
 </div>
 <div class="photo" style="background-image:url({f3})"></div>
</div>
<p class="m s" style="margin-top:3mm;text-transform:none;letter-spacing:.02em">Imágenes de referencia de estilo (Unsplash). No son fotografías propias de la marca.</p>''', 'III', '17 · Estilo fotográfico')

# ======================= 24 · ILUSTRACIÓN =======================
def node(x_, y_, w_, t, sub='', fill=BLA, col=NEG):
    return (f'<rect x="{x_}" y="{y_}" width="{w_}" height="46" fill="{fill}" stroke="{NEG}" stroke-width=".8"/>'
            f'<text x="{x_+10}" y="{y_+20}" font-family="IBM Plex Sans" font-size="14" font-weight="500" fill="{col}">{t}</text>'
            f'<text x="{x_+10}" y="{y_+36}" font-family="IBM Plex Mono" font-size="8.5" letter-spacing=".5" fill="{NIE if fill != BLA else ACE}">{sub}</text>')
dd = [f'<svg viewBox="0 0 800 300" style="width:100%;height:auto"><defs><marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{NEG}" stroke-width="1"/></marker></defs>']
for i, (t, s_) in enumerate((('Sensores', 'S/01 · RADAR · CÁMARAS'), ('Fuentes abiertas', 'S/02 · PRENSA · REDES'), ('Sistemas internos', 'S/03 · ERP · REGISTROS'))):
    y0 = 30 + i * 90
    dd.append(node(10, y0, 170, t, s_))
    dd.append(f'<path d="M180 {y0+23}L330 150" stroke="{NEG}" stroke-width=".7" fill="none" marker-end="url(#ar)"/>')
dd.append(f'<rect x="318" y="96" width="384" height="104" fill="none" stroke="{NIE}" stroke-width=".6" stroke-dasharray="3 3"/><text x="420" y="110" text-anchor="middle" font-family="IBM Plex Mono" font-size="8" letter-spacing=".5" fill="{ACE}">DESPLIEGUE EN EL ENTORNO DEL CLIENTE</text>')
dd.append(node(330, 127, 190, 'Plataforma HALVEX', 'FUSIÓN · ANÁLISIS · ALERTA', NEG, BLA))
dd.append(f'<path d="M520 150H585" stroke="{NEG}" stroke-width=".7" marker-end="url(#ar)"/>')
dd.append(node(585, 127, 110, 'Analista', 'REVISA Y PROPONE'))
dd.append(f'<path d="M695 150H735" stroke="{NEG}" stroke-width=".7" marker-end="url(#ar)"/><path d="M760 128l22 22-22 22-22-22z" fill="{NEG}"/><text x="760" y="194" text-anchor="middle" font-family="IBM Plex Mono" font-size="8.5" letter-spacing=".5" fill="{NEG}">DECISIÓN</text></svg>')
page(f'''{chhead('18', 'Estilo <b>de ilustración</b>', 'Diagramas, no dibujos')}
<div class="g" style="margin-top:8mm">
 <div style="grid-column:1/9;padding-top:4mm">{''.join(dd)}<p class="m s" style="margin-top:3mm">Ejemplo · esquema de un sistema de apoyo a la decisión</p></div>
 <div style="grid-column:10/13">
  <p class="lead" style="font-size:11.5pt">HALVEX no usa ilustración figurativa. Explica con diagramas técnicos: planos, esquemas de sistemas, flujos y mapas.</p>
  <ul class="si" style="margin-top:5mm"><li>Línea de 0,5 a 1 pt en negro.</li><li>Un único elemento relleno: lo que importa.</li><li>Rótulos en Plex Mono, nombres en Plex Sans.</li><li>Ángulos rectos y flechas abiertas.</li></ul>
  <ul class="no" style="margin-top:3mm"><li>Personajes, mascotas y dibujos.</li><li>3D, degradados y brillos.</li></ul>
 </div>
</div>''', 'III', '18 · Estilo de ilustración')

# ======================= 25 · PARTE IV =======================
divider('IV', 'Aplicaciones', 'hq-banca', 'La marca en uso: papelería, entorno digital, presentaciones y los archivos para aplicarla.', toc[3][2])

# ======================= 26 · PAPELERÍA =======================
card_f = f'<div style="width:85mm;height:55mm;background:{NEG};display:flex;align-items:center;justify-content:center">{iso("width:15mm;height:15mm", BLA)}</div>'
card_b = (f'<div style="width:85mm;height:55mm;background:{BLA};box-shadow:inset 0 0 0 .25mm #C9C7C1;padding:6mm;position:relative">{horiz(NEG, NEG, "width:30mm;height:auto")}'
          f'<div style="position:absolute;left:6mm;bottom:6mm"><p style="font-size:9.5pt;font-weight:500">Nombre Apellido</p><p style="font-size:7pt;color:{ACE};margin-top:.5mm">Cargo</p>'
          f'<p class="m" style="font-size:5.6pt;margin-top:3mm">+34 000 000 000<br>nombre@halvex.com</p></div>'
          f'<span class="m s" style="position:absolute;right:6mm;bottom:6mm;font-size:5.6pt;text-align:right">Madrid<br>halvex.com</span></div>')
letter = (f'<div style="width:60mm;height:85mm;background:{BLA};box-shadow:inset 0 0 0 .25mm #C9C7C1;padding:6mm;position:relative">{horiz(NEG, NEG, "width:19mm;height:auto")}'
          f'<div style="margin-top:12mm">' + ''.join(f'<div style="height:1.1mm;background:{PIE};margin-bottom:1.6mm;width:{w}%"></div>' for w in (40, 30, 0, 100, 96, 98, 90, 0, 100, 94, 97, 60)) + '</div>'
          f'<div style="position:absolute;left:6mm;right:6mm;bottom:5mm;border-top:.2mm solid {NEG};padding-top:1.4mm;display:flex;justify-content:space-between"><span class="m" style="font-size:3.6pt">HALVEX · MADRID</span><span class="m" style="font-size:3.6pt">HALVEX.COM</span></div></div>')
envelope = (f'<div style="width:110mm;height:55mm;background:{BLA};box-shadow:inset 0 0 0 .25mm #C9C7C1;position:relative;padding:5mm">{horiz(NEG, NEG, "width:22mm;height:auto")}'
            f'<div style="position:absolute;left:52mm;top:24mm">' + ''.join(f'<div style="height:1.1mm;background:{PIE};margin-bottom:1.6mm;width:{w}mm"></div>' for w in (36, 44, 30)) + '</div>'
            f'<div style="position:absolute;right:0;top:0;bottom:0;width:6mm;background:{NEG}"></div></div>')
page(f'''{chhead('19', 'Papelería', '')}
<div style="display:grid;grid-template-columns:85mm 85mm 1fr;column-gap:8mm;row-gap:5mm;margin-top:7mm;align-items:start">
 <div>{card_f}<div class="lbl"><b>Tarjeta · anverso</b><span>85 × 55 mm. Isotipo blanco sobre negro.</span></div></div>
 <div>{card_b}<div class="lbl"><b>Tarjeta · reverso</b><span>Imagotipo, datos en Plex Sans y Plex Mono.</span></div></div>
 <div style="grid-row:1/3;grid-column:3">{letter}<div class="lbl"><b>Carta</b><span>A4. Imagotipo arriba a la izquierda, pie con filete.</span></div></div>
 <div style="grid-column:1/3">{envelope}<div class="lbl"><b>Sobre americano</b><span>220 × 110 mm, con canto negro.</span></div></div>
</div>''', 'IV', '19 · Papelería')

# ======================= 27 · DIGITAL =======================
web = (f'<div style="box-shadow:0 0 0 .2mm #D8D6D0;background:{BLA}">'
       f'<div style="height:6mm;background:{PIE};display:flex;align-items:center;gap:1.4mm;padding:0 3mm"><i style="width:1.8mm;height:1.8mm;border-radius:50%;background:{NIE}"></i><i style="width:1.8mm;height:1.8mm;border-radius:50%;background:{NIE}"></i><i style="width:1.8mm;height:1.8mm;border-radius:50%;background:{NIE}"></i>'
       f'<span style="margin-left:4mm;background:#fff;height:3.6mm;padding:0 3mm;display:flex;align-items:center;gap:1.6mm"><span style="width:2.6mm;height:2.6mm;background:{NEG};display:flex;align-items:center;justify-content:center">{iso("width:1.6mm;height:1.6mm", BLA)}</span><span class="m" style="font-size:4.5pt">HALVEX</span></span></div>'
       f'<div style="padding:4mm 6mm 6mm"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:.2mm solid {NEG};padding-bottom:2.4mm">{horiz(NEG, NEG, "width:20mm;height:auto")}<span class="m" style="font-size:4.6pt;word-spacing:2mm">Enfoque Capacidades Sectores Método Contacto</span></div>'
       f'<div style="margin-top:6mm">{wm("width:100%;height:auto", NEG)}</div><p style="font-weight:200;font-size:15pt;letter-spacing:-.03em;margin-top:6mm;line-height:1.05">Tecnología para decisiones<br>que <b style="font-weight:400">no admiten error.</b></p></div></div>')
sig = (f'<div style="padding:5mm;box-shadow:inset 0 0 0 .2mm #D8D6D0;background:{BLA}"><p style="font-size:8.5pt;font-weight:500">Nombre Apellido</p><p style="font-size:7.5pt;color:{ACE}">Cargo · HALVEX</p>'
       f'<div style="border-top:.2mm solid {LIN};margin:3mm 0"></div><div style="display:flex;align-items:center;justify-content:space-between">{horiz(NEG, NEG, "width:24mm;height:auto")}<span class="m s" style="font-size:5.6pt">nombre@halvex.com</span></div></div>')
av = ''.join(f'<div style="width:22mm;height:22mm;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;{"box-shadow:inset 0 0 0 .2mm #D8D6D0" if bg == BLA else ""}">{iso("width:10mm;height:10mm", fg)}</div>' for bg, fg in ((NEG, BLA), (BLA, NEG)))
page(f'''{chhead('20', 'Entorno <b>digital</b>', '')}
<div style="display:grid;grid-template-columns:1.35fr 1fr;column-gap:8mm;margin-top:7mm;align-items:start">
 <div>{web}<div class="lbl"><b>Web</b><span>Imagotipo en la cabecera; logotipo a todo el ancho en la portada. Favicon: isotipo blanco sobre negro.</span></div></div>
 <div style="display:grid;gap:6mm">
  <div>{sig}<div class="lbl"><b>Firma de correo</b><span>Imagotipo en PNG a 240 px (se ve a 120 px).</span></div></div>
  <div><div style="display:flex;gap:5mm">{av}</div><div class="lbl"><b>Avatar en redes</b><span>Las redes recortan en círculo: el isotipo ocupa menos de la mitad del lienzo.</span></div></div>
 </div>
</div>''', 'IV', '20 · Entorno digital')

# ======================= 28 · PRESENTACIONES =======================
s1 = (f'<div style="aspect-ratio:16/9;background:{GRAF};color:#fff;position:relative;padding:5mm 6mm">'
      f'<span class="m" style="font-size:4.6pt;color:{NIE}">HALVEX · Propuesta</span>'
      f'<p style="position:absolute;left:6mm;top:16mm;font-weight:200;font-size:19pt;letter-spacing:-.03em;line-height:1.05">Plataforma de apoyo<br><b style="font-weight:400">a la decisión</b></p>'
      f'<div style="position:absolute;left:6mm;right:6mm;bottom:5mm">{wm("width:100%;height:auto", BLA)}</div></div>')
s2 = (f'<div style="aspect-ratio:16/9;background:{BLA};box-shadow:0 0 0 .2mm #D8D6D0;position:relative;padding:5mm 6mm">'
      f'<div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:1.4mm"><span class="m" style="font-size:4.6pt">HALVEX</span><span class="m" style="font-size:4.6pt">02 · Enfoque</span></div>'
      f'<p style="font-weight:200;font-size:30pt;letter-spacing:-.05em;line-height:.8;margin-top:5mm">02</p>'
      f'<p style="font-weight:200;font-size:12pt;letter-spacing:-.02em;margin-top:3mm;line-height:1.1">Tres fases, <b style="font-weight:400">un único responsable.</b></p>'
      f'<div style="position:absolute;left:6mm;right:6mm;bottom:6mm;display:grid;grid-template-columns:repeat(3,1fr);column-gap:3mm">' + ''.join(f'<div style="border-top:.2mm solid {NEG};padding-top:1.2mm"><span class="m" style="font-size:4.4pt">0{i}</span><div style="height:.9mm;background:{PIE};margin-top:1.4mm;width:90%"></div><div style="height:.9mm;background:{PIE};margin-top:1mm;width:70%"></div></div>' for i in (1, 2, 3)) + '</div></div>')
page(f'''{chhead('21', 'Presenta<b>ciones</b>', '16:9')}
<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:8mm;margin-top:8mm">
 <div>{s1}<div class="lbl"><b>Portada</b><span>Fondo grafito, título en dos pesos y logotipo a todo el ancho.</span></div></div>
 <div>{s2}<div class="lbl"><b>Página interior</b><span>Cabecera con filete, número grande y contenido en columnas.</span></div></div>
</div>''', 'IV', '21 · Presentaciones')

# ======================= 29 · ARCHIVOS =======================
files = [('01-imagotipo-horizontal', 'SVG · PDF · PNG 4000 / 1600 / 600 px', 'Negro, blanco y con fondo', 'La firma por defecto'),
         ('02-imagotipo-vertical', 'SVG · PDF · PNG 3000 / 1200 / 500 px', 'Negro, blanco y con fondo', 'Portadas y formatos cuadrados'),
         ('03-logotipo', 'SVG · PDF · PNG 4000 / 1600 / 600 px', 'Negro, blanco y con fondo', 'Solo la palabra'),
         ('04-isotipo', 'SVG · PDF · PNG 2048 / 1024 / 512 px', 'Negro, blanco y con fondo', 'El símbolo'),
         ('05-iconos-y-redes', 'PNG · SVG · ICO', 'Iconos de 16 a 1024 px, favicon, avatares, portada de LinkedIn, cabecera de X, firma de correo', 'Web, apps y redes')]
fr = ''.join(f'<div class="row" style="grid-template-columns:62mm 64mm 1fr 46mm;column-gap:5mm;padding:3.2mm 0"><span class="m" style="font-size:7pt">{a}/</span><span class="p">{b}</span><span class="p s">{c}</span><span class="p">{d}</span></div>' for a, b, c, d in files)
fmt = [('SVG', 'Vectorial. Web y diseño: escala sin perder calidad.'), ('PDF', 'Vectorial. Imprenta, rotulación y documentos.'),
       ('PNG', 'Transparente. Ofimática, presentaciones y redes.'), ('ICO', 'Favicon del navegador.')]
fm = ''.join(f'<div class="r" style="padding-top:2.6mm"><p class="h4">{a}</p><p class="p s" style="margin-top:1mm">{b}</p></div>' for a, b in fmt)
page(f'''{chhead('22', 'Archivos <b>del logo</b>', 'Carpeta HALVEX-logos')}
<div style="margin-top:8mm"><div class="row" style="grid-template-columns:62mm 64mm 1fr 46mm;column-gap:5mm;border:0;padding:0 0 2mm"><span class="m s">Carpeta</span><span class="m s">Formatos</span><span class="m s">Variantes</span><span class="m s">Para qué</span></div><div class="rows">{fr}</div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm;margin-top:9mm">{fm}</div>
<p class="p s" style="margin-top:6mm">Los PNG transparentes van recortados al borde del dibujo; los «con fondo» incluyen el área de respeto. Usar siempre estos archivos: nunca redibujar ni reescribir el logo.</p>''', 'IV', '22 · Archivos del logo')

# ======================= 30 · CONTRAPORTADA =======================
n += 1
P.append(f'''<section class="page dk" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10mm">
{vert(BLA, BLA, 'width:62mm;height:auto')}
<div style="position:absolute;left:18mm;right:18mm;bottom:13mm;display:flex;justify-content:space-between;border-top:.25mm solid rgba(255,255,255,.4);padding-top:2.6mm" class="m"><span>HALVEX · Identidad visual · Edición 1.0</span><span style="color:#A3A4A8">contacto@halvex.com</span></div>
</section>''')

html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>HALVEX · Identidad visual</title><style>{CSS}</style></head><body>{C.DEFS}' + ''.join(P) + '</body></html>')
open(os.path.join(HERE, 'visual2.html'), 'w').write(html)
print(len(P), 'páginas')

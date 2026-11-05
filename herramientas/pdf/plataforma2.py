import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from common import TINTA, BLANCO, PIEDRA, ACERO, NIEBLA, FILETE, ISO_D, WM_D, iso, wm, iso_g, wm_g, img64

GRAF = '#1A1B1E'
DOC = 'Plataforma de marca'

CSS = C.FONTS + r'''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"IBM Plex Sans",Arial,sans-serif;color:#111214;-webkit-print-color-adjust:exact;print-color-adjust:exact}
svg{display:block}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;padding:14mm 18mm 0}
.page:last-child{page-break-after:auto;break-after:auto}
.m{font-family:"IBM Plex Mono",monospace;font-size:6.5pt;letter-spacing:.07em;text-transform:uppercase;line-height:1.55}
.s{color:#65676C}
.run{display:grid;grid-template-columns:1fr 1fr 1fr;align-items:baseline;padding-bottom:2.4mm;border-bottom:.25mm solid currentColor}
.run span:nth-child(2){text-align:center}.run span:last-child{text-align:right}
.run b{font-weight:500}
.fol{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;align-items:baseline}
.fol .n{font-family:"IBM Plex Mono",monospace;font-size:7pt;letter-spacing:.06em}
.dk{background:#1A1B1E;color:#fff}
.dk .s{color:#A3A4A8}
.st{background:#EFEDE8}
.g{display:grid;grid-template-columns:repeat(12,1fr);column-gap:5mm}
.ch{display:grid;grid-template-columns:repeat(12,1fr);column-gap:5mm;margin-top:9mm;align-items:end}
.ch .num{grid-column:1/3;font-weight:200;font-size:64pt;line-height:.78;letter-spacing:-.05em}
.ch h2{grid-column:3/10;font-weight:200;font-size:40pt;line-height:1;letter-spacing:-.035em}
.ch h2 b{font-weight:400}
.ch .k{grid-column:10/13;text-align:right}
.d1{font-weight:200;letter-spacing:-.035em;line-height:1.04}
.d1 b,.d2 b{font-weight:400}
.d2{font-weight:200;letter-spacing:-.025em;line-height:1.12}
.lead{font-size:12.5pt;font-weight:300;line-height:1.5}
.p{font-size:9.2pt;line-height:1.62}
.p+.p{margin-top:2.6mm}
.h3{font-size:14pt;font-weight:400;letter-spacing:-.01em;line-height:1.2}
.h4{font-size:10pt;font-weight:500;line-height:1.3}
.r{border-top:.25mm solid currentColor}
.hr{border-top:.2mm solid #D8D6D0}
.dk .hr{border-color:rgba(255,255,255,.18)}
.row{display:grid;align-items:baseline;border-top:.2mm solid #D8D6D0;padding:2.8mm 0}
.dk .row{border-color:rgba(255,255,255,.18)}
.rows>.row:last-child{border-bottom:.2mm solid #D8D6D0}
.dia{display:inline-block;width:1.9mm;height:1.9mm;background:currentColor;transform:rotate(45deg);margin-right:2.6mm;vertical-align:.35mm}
.dia.o{background:none;box-shadow:inset 0 0 0 .25mm currentColor}
.photo{background-size:cover;background-position:center}
ul.li{list-style:none}
ul.li li{font-size:8.8pt;line-height:1.5;padding:1.7mm 0;border-top:.2mm solid #D8D6D0}
ul.li li:last-child{border-bottom:.2mm solid #D8D6D0}
.dk ul.li li{border-color:rgba(255,255,255,.18)}
.strike{color:#A3A4A8;text-decoration:line-through;text-decoration-thickness:.2mm}
.tag{font-family:"IBM Plex Mono",monospace;font-size:6.2pt;letter-spacing:.06em;text-transform:uppercase;border:.2mm solid currentColor;padding:.6mm 1.6mm;display:inline-block}
'''

P = []
n = 0
PART = {'I': 'Esencia', 'II': 'Propósito', 'III': 'Carácter', 'IV': 'Mercado'}


def page(inner, part='', chap='', cls='', run=True, fol=True):
    global n
    n += 1
    r = ''
    if run:
        r = (f'<div class="run m"><span><b>HALVEX</b>&nbsp;&nbsp;&nbsp;{DOC}</span>'
             f'<span>{("Parte " + part + " · " + PART[part]) if part else ""}</span><span>{chap}</span></div>')
    f = f'<div class="fol"><span class="m s">Edición 1.0 · Noviembre 2026 · Uso interno</span><span class="n">{n:02d}</span></div>' if fol else ''
    P.append(f'<section class="page {cls}">{r}{inner}{f}</section>')


def chhead(num, title, k=''):
    return f'<div class="ch"><span class="num">{num}</span><h2>{title}</h2><span class="k m s">{k}</span></div>'


# ===================== 1 · PORTADA =====================
cons = (f'<svg viewBox="-20 -10 240 230" style="width:100%;height:auto;overflow:visible">'
        f'<g fill="none" stroke="#5A5C61" stroke-width=".35">'
        f'<path d="M-20 20H220"/><path d="M100 -10V215" stroke-dasharray="1.2 1.6"/>'
        f'<path d="M24 20L-2 -36M176 20L202 -36"/><path d="M96.2 172L100 180L103.8 172"/><circle cx="100" cy="180" r="2.2"/>'
        f'<path d="M24 196H176M24 193V199M176 193V199"/><path d="M194 20V172M191 20H197M191 172H197"/>'
        f'<circle cx="100" cy="96" r="104" stroke-dasharray="1 2.4"/></g>'
        f'<path fill="#FFFFFF" d="{ISO_D[0]}"/><path fill="#FFFFFF" d="{ISO_D[1]}"/>'
        f'<g font-family="IBM Plex Mono" font-size="4.2" letter-spacing=".3" fill="#7E8085">'
        f'<text x="94" y="206">152</text><text x="198" y="99" transform="rotate(90 198 99)">152</text><text x="106" y="186">VÉRTICE</text></g></svg>')
n += 1
P.append(f'''<section class="page dk" style="padding:14mm 18mm">
<div style="display:flex;justify-content:space-between" class="m"><span><b style="font-weight:500">HALVEX</b></span><span>Documento 01 / 02</span><span>Edición 1.0 · Noviembre 2026</span></div>
<div style="position:absolute;right:30mm;top:30mm;width:84mm">{cons}</div>
<div style="position:absolute;left:18mm;top:44mm;width:120mm">
 <p class="m s">Documento de marca</p>
 <h1 class="d1" style="font-size:58pt;margin-top:5mm">Plataforma<br><b>de marca</b></h1>
 <p class="lead" style="margin-top:7mm;color:#C9CACD;max-width:100mm">Quiénes somos, por qué existimos, en qué creemos y cómo queremos que se nos reconozca.</p>
</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:27mm">{wm('width:100%;height:auto', '#FFFFFF')}</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:13mm;display:flex;justify-content:space-between;border-top:.25mm solid rgba(255,255,255,.5);padding-top:2.6mm" class="m"><span>Esencia · Propósito · Carácter · Mercado</span><span class="s">Uso interno · Confidencial</span></div>
</section>''')

# ===================== 2 · CONTENIDO =====================
toc = [('I', 'Esencia', [('01', 'Nombre comercial', 5), ('02', 'Historia de la marca', 6), ('03', 'Manifiesto', 7)]),
       ('II', 'Propósito', [('04', 'Misión', 9), ('05', 'Visión', 10), ('06', 'Valores', 11)]),
       ('III', 'Carácter', [('07', 'Personalidad', 15), ('08', 'Lo que somos y lo que no', 16), ('09', 'Tono de voz', 17)]),
       ('IV', 'Mercado', [('10', 'Público objetivo', 21), ('11', 'Perfiles de decisión', 22), ('12', 'Posicionamiento', 23),
                          ('13', 'Pilares de marca', 25), ('14', 'Mensajes clave', 26), ('15', 'Casa de marca', 27)])]
cols = ''
for roman, name, items in toc:
    it = ''.join(f'<div class="row" style="grid-template-columns:9mm 1fr 8mm;padding:2.3mm 0"><span class="m s">{a}</span><span style="font-size:10.5pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
    cols += f'<div><div style="display:flex;align-items:baseline;gap:4mm;padding-bottom:3mm"><span style="font-weight:200;font-size:30pt;letter-spacing:-.04em;line-height:1">{roman}</span><span class="h3">{name}</span></div><div class="rows">{it}</div></div>'
page(f'''<div class="g" style="margin-top:10mm">
 <div style="grid-column:1/5"><h2 class="d1" style="font-size:40pt">Contenido</h2>
  <p class="p s" style="margin-top:6mm;max-width:66mm">Cuatro partes y quince capítulos. La identidad visual (logotipo, color, tipografía y aplicaciones) se desarrolla en el documento 02.</p></div>
 <div style="grid-column:5/13;display:grid;grid-template-columns:1fr 1fr;column-gap:9mm;row-gap:9mm">{cols}</div>
</div>''', chap='Contenido')

# ===================== 3 · INTRODUCCIÓN =====================
page(f'''<div class="g" style="margin-top:12mm">
 <p class="m s" style="grid-column:1/3">Introducción</p>
 <div style="grid-column:3/11">
  <h2 class="d1" style="font-size:38pt">Una marca es una promesa <b>que se cumple cada día.</b></h2>
 </div>
</div>
<div class="g" style="margin-top:12mm">
 <div style="grid-column:3/7">
  <p class="p">Este documento recoge lo que HALVEX es antes de cualquier logotipo: por qué existe, en qué cree, cómo habla y qué lugar quiere ocupar entre quienes deciden.</p>
  <p class="p">Es la referencia para quien escriba, diseñe, venda o represente a la compañía. Cuando haya dudas sobre cómo actuar o qué decir, la respuesta debe estar aquí. Y si no lo está, este documento debe actualizarse.</p>
 </div>
 <div style="grid-column:8/13">
  <div class="rows">
   <div class="row" style="grid-template-columns:42mm 1fr"><span class="m s">Dirección</span><span class="p">Para tomar decisiones coherentes con lo que somos.</span></div>
   <div class="row" style="grid-template-columns:42mm 1fr"><span class="m s">Comunicación</span><span class="p">Para escribir y diseñar con una sola voz.</span></div>
   <div class="row" style="grid-template-columns:42mm 1fr"><span class="m s">Equipo comercial</span><span class="p">Para explicar con precisión qué ofrecemos y por qué.</span></div>
   <div class="row" style="grid-template-columns:42mm 1fr"><span class="m s">Socios y proveedores</span><span class="p">Para representarnos sin desvirtuar la marca.</span></div>
  </div>
 </div>
</div>''', chap='Introducción')


# ===================== DIVIDER helper =====================
def divider(roman, name, photo, intro, items, pos='center'):
    global n
    n += 1
    it = ''.join(f'<div class="row" style="grid-template-columns:10mm 1fr 8mm;padding:2.6mm 0"><span class="m s">{a}</span><span style="font-size:11pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
    P.append(f'''<section class="page dk" style="padding:0">
<div class="photo" style="position:absolute;left:0;top:0;bottom:0;width:50%;background-image:url({img64(photo)});background-position:{pos}"></div>
<div style="position:absolute;left:50%;right:0;top:0;bottom:0;padding:14mm 18mm 0 14mm">
 <div class="m" style="display:flex;justify-content:space-between;border-bottom:.25mm solid rgba(255,255,255,.6);padding-bottom:2.4mm"><span>Parte {roman}</span><span class="s">{n:02d}</span></div>
 <p style="font-weight:200;font-size:150pt;line-height:.8;letter-spacing:-.06em;margin-top:14mm">{roman}</p>
 <h2 class="d1" style="font-size:40pt;margin-top:8mm">{name}</h2>
 <p class="lead" style="margin-top:5mm;color:#C9CACD;max-width:100mm;font-size:11.5pt">{intro}</p>
 <div class="rows" style="position:absolute;left:14mm;right:18mm;bottom:14mm">{it}</div>
</div></section>''')


# ===================== 4 · PARTE I =====================
divider('I', 'Esencia', 'hq-hero', 'De dónde viene el nombre, por qué nace la compañía y en qué cree.', toc[0][2])

# ===================== 5 · NOMBRE =====================
hal = '<svg viewBox="0 -4 276 108" style="width:100%;height:auto">' + wm_g(0, 0, 100, TINTA).replace(''.join(f'<path d="{d}"/>' for d in WM_D[3:]), '') + '</svg>'
vex_paths = ''.join(f'<path d="{d}"/>' for d in WM_D[3:])
vex = f'<svg viewBox="268 -4 284 108" style="width:100%;height:auto"><g fill="{TINTA}">{vex_paths}</g></svg>'
page(f'''{chhead('01', 'Nombre <b>comercial</b>', 'Cómo nos llamamos')}
<div class="g" style="margin-top:11mm">
 <div style="grid-column:1/7;padding-right:6mm;border-right:.25mm solid #111214">
  <div style="width:70%">{hal}</div>
  <p class="m s" style="margin-top:6mm">Del griego hálōs · halo</p>
  <p class="h3" style="margin-top:2mm">La amplitud de la mirada</p>
  <p class="p" style="margin-top:2mm;max-width:105mm">El halo es el círculo de luz que rodea y abarca. Representa la capacidad de ver el conjunto, el contexto y el horizonte antes que la parte.</p>
 </div>
 <div style="grid-column:7/13;padding-left:6mm">
  <div style="width:72%">{vex}</div>
  <p class="m s" style="margin-top:6mm">Del latín vertex · vértice</p>
  <p class="h3" style="margin-top:2mm">La precisión de la decisión</p>
  <p class="p" style="margin-top:2mm;max-width:105mm">El vértice es el punto donde convergen todas las líneas. Representa el criterio que separa lo esencial y el momento exacto de actuar.</p>
 </div>
</div>
<div class="g" style="position:absolute;left:18mm;right:18mm;bottom:22mm">
 <div style="grid-column:1/4" class="r"><p class="m s" style="margin-top:2.6mm">Escritura</p><p class="p" style="margin-top:1.4mm">Siempre HALVEX, en mayúsculas y en una palabra. Sin artículo: «HALVEX propone».</p></div>
 <div style="grid-column:4/7" class="r"><p class="m s" style="margin-top:2.6mm">Pronunciación</p><p class="p" style="margin-top:1.4mm">«Jálbex» en español, con acento en la primera sílaba. /ˈhæl.vɛks/ en inglés.</p></div>
 <div style="grid-column:7/10" class="r"><p class="m s" style="margin-top:2.6mm">Uso del significado</p><p class="p" style="margin-top:1.4mm">Es interno. No se explica en la web ni en publicidad: se demuestra.</p></div>
 <div style="grid-column:10/13" class="r"><p class="m s" style="margin-top:2.6mm">Pendiente</p><p class="p" style="margin-top:1.4mm">Denominación social, registro en OEPM y EUIPO, dominio y redes.</p></div>
</div>''', 'I', '01 · Nombre comercial')

# ===================== 6 · HISTORIA =====================
page(f'''{chhead('02', 'Historia <b>de la marca</b>', 'Por qué nacemos')}
<div class="g" style="margin-top:10mm">
 <div style="grid-column:1/5">
  <p class="d2" style="font-size:21pt">«Cada pieza funciona por separado; <b>el conjunto, casi nunca.</b>»</p>
  <div class="r" style="margin-top:9mm;padding-top:3mm">
   <div class="row" style="grid-template-columns:28mm 1fr;border:0;padding-top:0"><span class="m s">El problema</span><span class="p">Tecnología fragmentada y responsabilidad diluida.</span></div>
   <div class="row" style="grid-template-columns:28mm 1fr"><span class="m s">La respuesta</span><span class="p">Un único equipo responsable del conjunto.</span></div>
   <div class="row" style="grid-template-columns:28mm 1fr"><span class="m s">Lo que transmite</span><span class="p">Control, criterio y serenidad.</span></div>
  </div>
 </div>
 <div style="grid-column:6/13;column-count:2;column-gap:7mm">
  <p class="p"><span style="float:left;font-weight:200;font-size:38pt;line-height:.85;margin:.6mm 2mm 0 0;letter-spacing:-.04em">D</span>urante años, la tecnología de las organizaciones críticas ha crecido por capas. Un proveedor para los datos, otro para la seguridad, otro para cada aplicación. Cada pieza funciona por separado; el conjunto, casi nunca. Cuando algo falla, la responsabilidad se diluye entre contratos.</p>
  <p class="p">Al mismo tiempo, la inteligencia artificial ha cambiado lo que es posible: ver patrones que una persona no ve, anticipar en lugar de reaccionar. Pero también ha abierto preguntas nuevas. Dónde están los datos. Quién controla los modelos. Quién responde de una recomendación equivocada.</p>
  <p class="p">HALVEX nace para responder a esas preguntas con hechos: un solo equipo que diseña, construye y opera la inteligencia artificial, la seguridad y el software de una organización, desplegados donde ella decide y con una persona responsable de cada sistema.</p>
  <p class="p">No queremos ser el proveedor más grande. Queremos ser aquel al que se llama cuando el error no es una opción, y el que sigue allí cuando el sistema lleva años funcionando.</p>
 </div>
</div>''', 'I', '02 · Historia de la marca')

# ===================== 7 · MANIFIESTO =====================
man = ['Hay decisiones que no admiten un segundo intento.', 'Las que protegen a un país, a una red eléctrica, a un hospital.',
       'Para tomarlas hace falta ver el conjunto', 'y, después, actuar con exactitud.', '',
       'No creemos en la tecnología que hace ruido.', 'Creemos en la que funciona cuando nadie mira.',
       'En los datos que se quedan donde deben.', 'En que detrás de cada sistema haya una persona que responde.', '',
       'Trabajamos con pocos, para hacerlo bien.']
ml = ''.join(('<p style="height:3.5mm"></p>' if not t else f'<p>{t}</p>') for t in man)
page(f'''<div class="g" style="margin-top:10mm">
 <div style="grid-column:1/3"><p class="m s">03 · Manifiesto</p></div>
 <div style="grid-column:3/12" class="d2"><div style="font-size:17.5pt;line-height:1.38;color:#D3D4D7">{ml}</div>
  <p style="font-size:30pt;letter-spacing:-.03em;line-height:1.1;margin-top:7mm;font-weight:200">Miramos con amplitud.<br><b style="font-weight:400">Actuamos con precisión.</b></p>
 </div>
</div>
<div style="position:absolute;right:18mm;bottom:22mm">{iso('width:12mm;height:12mm', '#FFFFFF')}</div>''', 'I', '03 · Manifiesto', cls='dk')

# ===================== 8 · PARTE II =====================
divider('II', 'Propósito', 'hq-piramide', 'Para qué existimos, hasta dónde queremos llegar y qué no negociamos nunca.', toc[1][2])

# ===================== 9 · MISIÓN =====================
mis = [('Qué hacemos', 'Diseñamos, construimos y operamos inteligencia artificial, sistemas de seguridad y software.'),
       ('Para quién', 'Para organizaciones en las que una decisión tardía o un dato expuesto tienen consecuencias reales.'),
       ('Para qué', 'Para que decidan con información completa y actúen sin margen de error.'),
       ('Cómo', 'Con un solo equipo responsable, despliegue soberano y una persona detrás de cada decisión crítica.')]
mm = ''.join(f'<div class="r" style="padding-top:3mm"><p class="m s">{a}</p><p class="p" style="margin-top:2mm">{b}</p></div>' for a, b in mis)
page(f'''{chhead('04', 'Misión', 'Para qué existimos')}
<div class="g" style="margin-top:12mm">
 <p class="d1" style="grid-column:3/12;font-size:34pt;line-height:1.1">Dar a las organizaciones que no pueden fallar la tecnología para <b>decidir con información completa y actuar sin margen de error.</b></p>
</div>
<div class="g" style="position:absolute;left:18mm;right:18mm;bottom:22mm"><div style="grid-column:3/13;display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm">{mm}</div></div>''', 'II', '04 · Misión')

# ===================== 10 · VISIÓN =====================
hz = [('Horizonte 1', 'Consolidar', 'Socio de confianza de organizaciones críticas en España: defensa, administración, infraestructuras y grandes empresas.'),
      ('Horizonte 2', 'Extender', 'Referencia europea en tecnología soberana para decisiones críticas, con proyectos en varios países.'),
      ('Horizonte 3', 'Permanecer', 'Crecer sin perder lo que nos define: pocos clientes, equipos estables y control total de nuestra tecnología.')]
hh = ''.join(f'<div><p class="m s">{a}</p><p class="h3" style="margin:1.6mm 0 2mm">{b}</p><p class="p">{c}</p></div>' for a, b, c in hz)
lines = ''.join(f'<path d="M0 {y}L1000 40"/>' for y in (0, 10, 20, 30, 40, 50, 60, 70, 80))
page(f'''{chhead('05', 'Visión', 'Hasta dónde queremos llegar')}
<div class="g" style="margin-top:10mm">
 <p class="d1" style="grid-column:3/11;font-size:30pt;line-height:1.12">Ser la compañía tecnológica europea de referencia para las decisiones críticas: <b>la que se llama cuando el error no es una opción.</b></p>
</div>
<div class="g" style="margin-top:9mm"><div style="grid-column:3/13">
 <svg viewBox="0 0 1000 80" preserveAspectRatio="none" style="width:100%;height:12mm"><g stroke="#111214" stroke-width=".7" fill="none" vector-effect="non-scaling-stroke">{lines}</g></svg>
 <div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:7mm;margin-top:5mm">{hh}</div>
</div></div>
<div class="g" style="position:absolute;left:18mm;right:18mm;bottom:20mm"><div style="grid-column:3/13" class="r">
 <div style="display:grid;grid-template-columns:42mm 1fr 1fr 1fr;column-gap:6mm;padding-top:2.8mm">
  <p class="m s">Sabremos que vamos bien cuando</p>
  <p class="p">Los clientes renuevan y nos recomiendan sin que se lo pidamos.</p>
  <p class="p">Nos llaman para lo más delicado, no para lo rutinario.</p>
  <p class="p">Los mejores ingenieros quieren trabajar aquí y se quedan.</p>
 </div></div></div>''', 'II', '05 · Visión')

# ===================== 11 · VALORES · ÍNDICE =====================
VAL = [('Rigor', 'Lo que entregamos funciona a la primera.',
        'Probamos cada sistema en condiciones reales, documentamos las decisiones técnicas y auditamos lo que está en producción.',
        'Entregar algo sin verificar o prometer un plazo que no podemos cumplir.'),
       ('Discreción', 'Lo que sabemos de un cliente no sale del proyecto.',
        'Firmamos acuerdos de confidencialidad, damos acceso solo a quien lo necesita y no citamos a nadie sin permiso por escrito.',
        'Usar el nombre de un cliente como reclamo comercial sin su autorización.'),
       ('Soberanía', 'Los datos se quedan donde el cliente decide.',
        'Desplegamos en sus centros, en entornos aislados o en la nube que elija, y entregamos código y modelos documentados.',
        'Mover datos fuera de su jurisdicción o crear dependencias ocultas.'),
       ('Responsabilidad', 'Detrás de cada sistema hay una persona.',
        'Cada sistema tiene un responsable con nombre y cada recomendación queda registrada y se puede explicar.',
        'Dejar una decisión crítica en manos de un automatismo.'),
       ('Exclusividad', 'Pocos clientes, atendidos a fondo.',
        'Limitamos los proyectos simultáneos, mantenemos equipos estables y damos acceso directo a la dirección.',
        'Crecer a costa de la atención que merece cada cliente.'),
       ('Innovación útil', 'Tecnología nueva solo si resuelve algo.',
        'Evaluamos cada novedad contra el problema real del cliente e investigamos con aplicación concreta.',
        'Vender una tecnología porque está de moda.')]
romans = ['I', 'II', 'III', 'IV', 'V', 'VI']
Q = {'Rigor': '¿Lo hemos probado en condiciones reales?', 'Discreción': '¿Nos ha autorizado el cliente a contarlo?', 'Soberanía': '¿Sabe el cliente dónde están sus datos y quién accede a ellos?', 'Responsabilidad': '¿Quién responde si esto falla?', 'Exclusividad': '¿Podemos atender este proyecto como merece?', 'Innovación útil': '¿Qué problema del cliente resuelve?'}
vi = ''.join(f'<div class="row" style="grid-template-columns:14mm 70mm 1fr;padding:3.4mm 0"><span class="m s">{romans[i]}</span><span style="font-weight:200;font-size:24pt;letter-spacing:-.03em;line-height:1">{v[0]}</span><span class="lead" style="font-size:11.5pt">{v[1]}</span></div>' for i, v in enumerate(VAL))
page(f'''{chhead('06', 'Valores', 'En qué creemos')}
<div class="g" style="margin-top:9mm">
 <p class="p s" style="grid-column:1/3">Seis valores. No son aspiraciones: son criterios para decidir cuando hay dudas.</p>
 <div class="rows" style="grid-column:3/13">{vi}</div>
</div>''', 'II', '06 · Valores')


# ===================== 12-13 · VALORES · DETALLE =====================
def vdetail(items, start):
    out = ''
    for i, (name, d, how, never) in enumerate(items):
        out += f'''<div style="border-top:.25mm solid #111214;padding-top:3.5mm;display:flex;flex-direction:column;height:138mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><p style="font-weight:200;font-size:31pt;letter-spacing:-.035em;line-height:1">{name}</p><span class="m s">{romans[start+i]}</span></div>
  <p class="h4" style="margin-top:4mm">{d}</p>
  <p class="m s" style="margin-top:6mm">Lo demostramos</p><p class="p" style="margin-top:1.4mm">{how}</p>
  <p class="m s" style="margin-top:4mm">Nunca</p><p class="p" style="margin-top:1.4mm">{never}</p>
  <div style="margin-top:auto;background:#EFEDE8;padding:4mm 4.5mm 5mm;min-height:27mm"><p class="m s">La pregunta que nos hacemos</p><p class="d2" style="font-size:15pt;margin-top:2.5mm">{Q[name]}</p></div></div>'''
    return f'<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:8mm;margin-top:7mm">{out}</div>'


page(f'''<div class="g" style="margin-top:9mm"><p class="m s" style="grid-column:1/13">06 · Valores · I – III</p></div>{vdetail(VAL[:3], 0)}''', 'II', '06 · Valores')
page(f'''<div class="g" style="margin-top:9mm"><p class="m s" style="grid-column:1/13">06 · Valores · IV – VI</p></div>{vdetail(VAL[3:], 3)}''', 'II', '06 · Valores')

# ===================== 14 · PARTE III =====================
divider('III', 'Carácter', 'hq-c-defensa', 'Cómo es HALVEX cuando entra en una sala, y cómo suena cuando habla o escribe.', toc[2][2])

# ===================== 15 · PERSONALIDAD =====================
traits = [('Sobria', 'Lo justo, ni una palabra de más.'), ('Precisa', 'Datos exactos y afirmaciones verificables.'),
          ('Discreta', 'Habla de resultados, no de clientes.'), ('Serena', 'Calma también bajo presión.'),
          ('Exigente', 'Consigo misma antes que con nadie.'), ('Moderna', 'Tecnología actual, sin modas.')]
tt = ''.join(f'<div class="row" style="grid-template-columns:26mm 1fr;padding:2.5mm 0"><span class="h4">{a}</span><span class="p s">{b}</span></div>' for a, b in traits)
sc = [('Clásica', 'Moderna', 72), ('Juvenil', 'Madura', 78), ('Cercana', 'Reservada', 64), ('Expresiva', 'Contenida', 84),
      ('Técnica', 'Humana', 44), ('Masiva', 'Exclusiva', 86)]
scs = ''
for a, b, v in sc:
    scs += (f'<div class="row" style="grid-template-columns:22mm 1fr 22mm;column-gap:4mm;align-items:center;padding:2.6mm 0"><span class="p">{a}</span>'
            f'<svg viewBox="0 0 100 10" preserveAspectRatio="none" style="width:100%;height:4mm"><g stroke="#111214" stroke-width=".6" vector-effect="non-scaling-stroke"><path d="M0 5H100M0 2V8M50 3V7M100 2V8"/></g></svg>'
            f'<span class="p" style="text-align:right">{b}</span></div>')
scs_svg = scs
# marcadores
marks = ''
page(f'''{chhead('07', 'Personalidad', 'Cómo somos')}
<div class="g" style="margin-top:9mm">
 <div style="grid-column:1/5">
  <p class="d2" style="font-size:17pt">Si HALVEX fuera una persona, sería la que entra en una sala de crisis, escucha a todos, pregunta lo justo <b>y pone orden sin levantar la voz.</b></p>
  <div style="display:grid;grid-template-columns:1fr 1fr;column-gap:5mm;margin-top:9mm">
   <div class="r" style="padding-top:2.8mm"><p class="m s">Arquetipo principal</p><p class="h3" style="margin-top:1.5mm">El Sabio</p><p class="p s" style="margin-top:1mm">Conocimiento y criterio por encima de la opinión.</p></div>
   <div class="r" style="padding-top:2.8mm"><p class="m s">Arquetipo secundario</p><p class="h3" style="margin-top:1.5mm">El Gobernante</p><p class="p s" style="margin-top:1mm">Orden, control y responsabilidad.</p></div>
  </div>
 </div>
 <div style="grid-column:6/9"><p class="m s" style="margin-bottom:2mm">Rasgos</p><div class="rows">{tt}</div></div>
 <div style="grid-column:9/13"><p class="m s" style="margin-bottom:2mm">Escala</p><div class="rows" id="sc">{scs_svg}</div></div>
</div>''', 'III', '07 · Personalidad')
# insert marker diamonds by absolute positions: done with CSS overlay per row
P[-1] = P[-1].replace('<div class="rows" id="sc">', '<div class="rows" id="sc" style="position:relative">')
rows_html = ''
for a, b, v in sc:
    rows_html += (f'<div class="row" style="grid-template-columns:22mm 1fr 22mm;column-gap:4mm;align-items:center;padding:2.6mm 0"><span class="p">{a}</span>'
                  f'<div style="position:relative;height:4mm"><svg viewBox="0 0 100 10" preserveAspectRatio="none" style="width:100%;height:4mm"><g stroke="#111214" stroke-width=".6" vector-effect="non-scaling-stroke"><path d="M0 5H100M0 2V8M50 3V7M100 2V8"/></g></svg>'
                  f'<span style="position:absolute;left:{v}%;top:50%;width:2.8mm;height:2.8mm;background:#111214;transform:translate(-50%,-50%) rotate(45deg)"></span></div>'
                  f'<span class="p" style="text-align:right">{b}</span></div>')
P[-1] = P[-1].replace(scs_svg, rows_html)

# ===================== 16 · SOMOS / NO SOMOS =====================
pairs = [('Seguros', 'arrogantes'), ('Técnicos', 'herméticos'), ('Discretos', 'opacos'), ('Exclusivos', 'elitistas'),
         ('Modernos', 'de moda'), ('Serenos', 'fríos'), ('Exigentes', 'rígidos'), ('Cercanos', 'informales')]
pp = ''.join(f'<div class="row" style="grid-template-columns:1fr 14mm 1fr;padding:3.1mm 0;align-items:baseline"><span style="font-weight:300;font-size:22pt;letter-spacing:-.025em;line-height:1">{a}</span><span class="m s" style="text-align:center">pero no</span><span style="font-weight:200;font-size:22pt;letter-spacing:-.025em;line-height:1;color:#A3A4A8">{b}</span></div>' for a, b in pairs)
page(f'''{chhead('08', 'Lo que somos <b>y lo que no</b>', 'Los límites del carácter')}
<div class="g" style="margin-top:9mm">
 <p class="p s" style="grid-column:1/4;padding-right:4mm">Cada rasgo tiene un exceso que lo estropea. Estos pares marcan dónde está el límite.</p>
 <div class="rows" style="grid-column:5/13">{pp}</div>
</div>''', 'III', '08 · Lo que somos y lo que no', cls='st')

# ===================== 17 · TONO DE VOZ · PRINCIPIOS =====================
pr = [('Claro', 'Frases cortas. Una idea por frase. Si una palabra sobra, se quita.', 'Detectamos el incidente y lo contenemos.'),
      ('Exacto', 'Cifras verificables o ninguna. Sin superlativos ni comparaciones vacías.', 'Tiempo medio de respuesta: [dato], medido en los últimos doce meses.'),
      ('Sereno', 'Sin exclamaciones, sin urgencia artificial, sin emojis.', 'Le contestará un responsable del proyecto.'),
      ('Sin jerga', 'Español claro. Anglicismos solo cuando no hay alternativa.', 'Sus datos se quedan en sus centros de datos.'),
      ('De usted', 'En web, propuestas y documentos. De tú solo en canales internos.', 'Cuéntenos el reto.')]
prr = ''.join(f'<div class="row" style="grid-template-columns:34mm 1fr 1fr;column-gap:6mm;padding:3.6mm 0"><span style="font-weight:300;font-size:17pt;letter-spacing:-.02em;line-height:1">{a}</span><span class="p">{b}</span><span class="p s">«{c}»</span></div>' for a, b, c in pr)
page(f'''{chhead('09', 'Tono <b>de voz</b>', 'Cómo hablamos')}
<div class="g" style="margin-top:9mm">
 <p class="d2" style="grid-column:1/4;font-size:15pt;padding-right:3mm">Hablamos como alguien que sabe de lo que habla <b>y no necesita demostrarlo.</b></p>
 <div style="grid-column:5/13"><div class="row" style="grid-template-columns:34mm 1fr 1fr;column-gap:6mm;border:0;padding:0 0 2mm"><span class="m s">Principio</span><span class="m s">Qué significa</span><span class="m s">Ejemplo</span></div><div class="rows">{prr}</div></div>
</div>''', 'III', '09 · Tono de voz')

# ===================== 18 · VOZ POR CANAL =====================
ch = [('Web', 3, 2, 'Tecnología para decisiones que no admiten error.'),
      ('Propuesta', 4, 4, 'Proponemos desplegar la plataforma en su centro de datos de Madrid, en tres fases de seis semanas.'),
      ('Redes profesionales', 2, 2, 'Publicamos nuestro método de evaluación de modelos en entornos aislados.'),
      ('Correo', 3, 1, 'Gracias por su mensaje. Le propongo una reunión el martes a las 10:00.'),
      ('Incidente', 4, 3, 'A las 09:12 detectamos un acceso anómalo. Está contenido. A las 11:00 le enviamos el informe.')]
def dots(v):
    return ''.join(f'<span style="display:inline-block;width:2.4mm;height:2.4mm;margin-right:1.2mm;{"background:#111214" if i < v else "box-shadow:inset 0 0 0 .25mm #A3A4A8"}"></span>' for i in range(5))
cr = ''.join(f'<div class="row" style="grid-template-columns:38mm 34mm 34mm 1fr;column-gap:6mm;padding:3.6mm 0;align-items:center"><span class="h3" style="font-size:12.5pt">{a}</span><span>{dots(f)}</span><span>{dots(t)}</span><span class="p">«{e}»</span></div>' for a, f, t, e in ch)
page(f'''<div class="g" style="margin-top:9mm"><p class="m s" style="grid-column:1/7">09 · Tono de voz · Por canal</p></div>
<div class="g" style="margin-top:6mm">
 <h3 class="d1" style="grid-column:1/5;font-size:28pt">Una voz, <b>distintos registros.</b></h3>
 <p class="p s" style="grid-column:8/13;align-self:end">La personalidad no cambia. Cambia cuánto detalle damos y cuánta formalidad exige cada situación.</p>
</div>
<div style="margin-top:8mm"><div class="row" style="grid-template-columns:38mm 34mm 34mm 1fr;column-gap:6mm;border:0;padding:0 0 2mm"><span class="m s">Canal</span><span class="m s">Formalidad</span><span class="m s">Detalle técnico</span><span class="m s">Así suena</span></div>
<div class="rows">{cr}</div></div>''', 'III', '09 · Tono de voz')

# ===================== 19 · ANTES / DESPUÉS + VOCABULARIO =====================
ba = [('¡Llevamos tu seguridad al siguiente nivel con soluciones disruptivas basadas en IA!', 'Detectamos amenazas antes de que lleguen a sus sistemas. Una persona de nuestro equipo decide cómo responder.'),
      ('Somos líderes en transformación digital 360° para el sector público.', 'Diseñamos y operamos sistemas para administraciones que no pueden dejar de dar servicio.'),
      ('Nuestra IA lo decide todo por ti, sin errores.', 'Nuestros modelos proponen; la decisión final la toma una persona, y queda registrada.')]
bb = ''.join(f'<div class="row" style="grid-template-columns:1fr 1fr;column-gap:8mm;padding:3.4mm 0"><span class="p strike">{a}</span><span class="p">{b}</span></div>' for a, b in ba)
use = ['decisión', 'responsable', 'soberanía', 'verificado', 'despliegue', 'criterio', 'precisión', 'continuidad', 'control']
avoid = ['disruptivo', 'revolucionario', 'líder', 'ecosistema', 'sinergia', '360°', 'next-gen', 'mágico', 'ninja']
page(f'''<div class="g" style="margin-top:9mm"><p class="m s" style="grid-column:1/7">09 · Tono de voz · En la práctica</p></div>
<div class="g" style="margin-top:6mm">
 <div style="grid-column:1/9">
  <div class="row" style="grid-template-columns:1fr 1fr;column-gap:8mm;border:0;padding:0 0 2mm"><span class="m s">Así no</span><span class="m s">Así sí</span></div>
  <div class="rows">{bb}</div>
 </div>
 <div style="grid-column:10/13">
  <p class="m s">Palabras que usamos</p>
  <div style="display:flex;flex-wrap:wrap;gap:1.6mm;margin-top:2.4mm">{''.join(f'<span class="tag">{w}</span>' for w in use)}</div>
  <p class="m s" style="margin-top:8mm">Palabras que evitamos</p>
  <div style="display:flex;flex-wrap:wrap;gap:1.6mm;margin-top:2.4mm;color:#A3A4A8">{''.join(f'<span class="tag" style="text-decoration:line-through">{w}</span>' for w in avoid)}</div>
  <p class="p s" style="margin-top:8mm">Nunca: exclamaciones, emojis, mayúsculas para enfatizar ni promesas absolutas como «sin errores» o «100 % seguro».</p>
 </div>
</div>''', 'III', '09 · Tono de voz')

# ===================== 20 · PARTE IV =====================
divider('IV', 'Mercado', 'hq-fachada', 'Para quién trabajamos, qué nos diferencia y cómo lo contamos.', toc[3][2])

# ===================== 21 · PÚBLICO =====================
segs = [('Defensa y seguridad', 'Ministerios, fuerzas armadas y de seguridad, industria de defensa.', 'La seguridad de las personas y de las operaciones.'),
        ('Administración pública', 'Organismos estatales, autonómicos y locales con servicios críticos.', 'La continuidad del servicio y la confianza ciudadana.'),
        ('Infraestructuras y energía', 'Redes eléctricas, agua, transporte y telecomunicaciones.', 'El suministro de millones de personas.'),
        ('Banca y seguros', 'Entidades reguladas con datos sensibles.', 'El dinero de sus clientes y la confianza del regulador.'),
        ('Industria y logística', 'Grandes plantas y cadenas de suministro.', 'Producción que no puede parar.'),
        ('Salud', 'Hospitales y servicios de salud.', 'Datos clínicos y atención a pacientes.')]
sg = ''.join(f'<div class="row" style="grid-template-columns:10mm 62mm 1fr 1fr;column-gap:6mm;padding:3.3mm 0"><span class="m s">{i+1:02d}</span><span style="font-weight:300;font-size:15pt;letter-spacing:-.02em;line-height:1.1">{a}</span><span class="p s">{b}</span><span class="p">{c}</span></div>' for i, (a, b, c) in enumerate(segs))
page(f'''{chhead('10', 'Público <b>objetivo</b>', 'Para quién trabajamos')}
<div class="g" style="margin-top:8mm">
 <div style="grid-column:1/4;padding-right:3mm">
  <p class="d2" style="font-size:15pt">Organizaciones en las que <b>una decisión tardía o un dato expuesto tienen consecuencias reales.</b></p>
  <p class="p s" style="margin-top:5mm">Grandes organizaciones públicas y privadas, en España primero y en Europa después.</p>
 </div>
 <div style="grid-column:4/13">
  <div class="row" style="grid-template-columns:10mm 62mm 1fr 1fr;column-gap:6mm;border:0;padding:0 0 2mm"><span></span><span class="m s">Sector</span><span class="m s">Quiénes</span><span class="m s">Qué está en juego</span></div>
  <div class="rows">{sg}</div>
 </div>
</div>''', 'IV', '10 · Público objetivo')

# ===================== 22 · PERFILES =====================
pf = [('Dirección general', 'Comité de dirección', 'Resultados, reputación y continuidad.', 'Entender riesgos y decisiones sin jerga técnica.', 'Un incidente que acabe en los medios.', 'Consecuencias, control y responsabilidad.'),
      ('Tecnología', 'CIO · CTO', 'Arquitectura, integración y proveedores.', 'Sistemas que encajen con lo que ya tiene y se puedan mantener.', 'Depender de un proveedor y proyectos que no terminan.', 'Arquitectura, estándares y documentación.'),
      ('Seguridad', 'CISO', 'Protección de datos y sistemas, cumplimiento de ENS y NIS2.', 'Ver lo que pasa y responder a tiempo.', 'Una brecha o una fuga de información.', 'Detección, contención y trazabilidad.'),
      ('Operaciones', 'Mandos y jefes de operaciones', 'Que la misión o el servicio salgan adelante.', 'Información fiable en el terreno, incluso sin conexión.', 'Herramientas que fallan en el momento crítico.', 'Fiabilidad, rapidez y sencillez de uso.')]
lab = ['Responde de', 'Necesita', 'Le preocupa', 'Le hablamos de']
cards = ''
for a, b, *rest in pf:
    body = ''.join(f'<div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">{l}</span><span class="p" style="margin-top:.8mm">{t}</span></div>' for l, t in zip(lab, rest))
    cards += f'<div><div style="background:#1A1B1E;color:#fff;padding:4mm 4mm 4.5mm"><p class="m" style="color:#A3A4A8">{b}</p><p class="h3" style="margin-top:6mm;font-weight:300;font-size:17pt">{a}</p></div><div class="rows" style="margin-top:1mm">{body}</div></div>'
page(f'''{chhead('11', 'Perfiles <b>de decisión</b>', 'Quién decide y qué le importa')}
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:5mm;margin-top:9mm">{cards}</div>''', 'IV', '11 · Perfiles de decisión')

# ===================== 23 · POSICIONAMIENTO =====================
page(f'''{chhead('12', 'Posiciona<b>miento</b>', 'Qué lugar ocupamos')}
<div class="g" style="margin-top:10mm">
 <div style="grid-column:3/12" class="rows">
  <div class="row" style="grid-template-columns:34mm 1fr;padding:4mm 0"><span class="m s">Para</span><span class="d2" style="font-size:19pt">organizaciones que no pueden permitirse un error,</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:4mm 0"><span class="m s">HALVEX es</span><span class="d2" style="font-size:19pt"><b>la compañía tecnológica que une inteligencia artificial, seguridad y software en un solo equipo responsable</b></span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:4mm 0"><span class="m s">Que</span><span class="d2" style="font-size:19pt">despliega donde el cliente decide y deja cada decisión crítica en manos de una persona.</span></div>
  <div class="row" style="grid-template-columns:34mm 1fr;padding:4mm 0"><span class="m s">A diferencia de</span><span class="d2" style="font-size:19pt">consultoras, integradores y plataformas que reparten la responsabilidad entre muchos.</span></div>
 </div>
</div>''', 'IV', '12 · Posicionamiento')

# ===================== 24 · MAPA =====================
pts = [('Grandes consultoras', 590, 320), ('Integradores de defensa', 110, 110), ('Startups de IA', 120, 440),
       ('Fabricantes de ciberseguridad', 90, 320), ('Grandes nubes públicas', 560, 440)]
W, H = 900, 520
sv = [f'<svg viewBox="-150 -24 {W+170} {H+66}" style="width:100%;height:auto">',
      f'<rect x="0" y="0" width="{W}" height="{H}" fill="#EFEDE8"/>',
      f'<path d="M0 {H/2}H{W}M{W/2} 0V{H}" stroke="#111214" stroke-width="1" fill="none"/>']
for t, x, y in pts:
    sv.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="#111214" stroke-width="1.4"/><text x="{x+16}" y="{y+6}" font-family="IBM Plex Sans" font-size="20" fill="#111214">{t}</text>')
sv.append(f'<path d="M790 66l16 16-16 16-16-16z" fill="#111214"/><text x="764" y="89" text-anchor="end" font-family="IBM Plex Sans" font-weight="500" font-size="26" fill="#111214">HALVEX</text>')
lb = 'font-family="IBM Plex Mono" font-size="14" letter-spacing="1.2" fill="#65676C"'
sv.append(f'<text x="0" y="{H+34}" {lb}>ESPECIALISTA</text><text x="{W}" y="{H+34}" text-anchor="end" {lb}>INTEGRAL</text>')
sv.append(f'<text x="-16" y="16" text-anchor="end" {lb}>CRÍTICO Y</text><text x="-16" y="36" text-anchor="end" {lb}>SOBERANO</text><text x="-16" y="{H-4}" text-anchor="end" {lb}>GENERAL</text></svg>')
tb = [('Grandes consultoras', 'Escala y alcance', 'Equipos estables y tecnología propia, no subcontratada.'),
      ('Integradores de defensa', 'Experiencia en misión', 'Velocidad y software moderno con IA integrada.'),
      ('Startups de IA', 'Innovación rápida', 'Seguridad, soberanía y responsabilidad desde el primer día.'),
      ('Fabricantes de seguridad', 'Producto especializado', 'Un sistema completo, no una pieza más que integrar.'),
      ('Grandes nubes', 'Infraestructura global', 'Despliegue en el entorno y la jurisdicción del cliente.')]
tr = ''.join(f'<div class="row" style="grid-template-columns:30mm 28mm 1fr;column-gap:3mm;padding:2.5mm 0"><span class="h4" style="font-size:8.8pt">{a}</span><span class="p s" style="font-size:8.6pt">{b}</span><span class="p" style="font-size:8.6pt">{c}</span></div>' for a, b, c in tb)
page(f'''<div class="g" style="margin-top:9mm"><p class="m s" style="grid-column:1/7">12 · Posicionamiento · Mapa competitivo</p></div>
<div class="g" style="margin-top:5mm">
 <div style="grid-column:1/8">{''.join(sv)}</div>
 <div style="grid-column:8/13">
  <h3 class="d1" style="font-size:26pt">Integral <b>y soberano.</b></h3>
  <p class="p s" style="margin:3mm 0 5mm">El cuadrante que nadie ocupa del todo. Esquema conceptual por tipos de competidor; no es un estudio de mercado.</p>
  <div class="row" style="grid-template-columns:30mm 28mm 1fr;column-gap:3mm;border:0;padding:0 0 2mm"><span class="m s">Competidor</span><span class="m s">Su fuerza</span><span class="m s">Nuestra diferencia</span></div>
  <div class="rows">{tr}</div>
 </div>
</div>''', 'IV', '12 · Posicionamiento')

# ===================== 25 · PILARES =====================
pil = [('Integral', 'IA, seguridad y software pensados juntos.', 'Un único equipo y una única arquitectura para todo el proyecto.', 'Un interlocutor y ningún hueco entre proveedores.'),
       ('Soberano', 'Sus datos y sus sistemas, bajo su control.', 'Despliegue en sus centros o en entornos aislados; código y modelos documentados.', 'Independencia y cumplimiento normativo.'),
       ('Responsable', 'Una persona detrás de cada sistema.', 'Responsable con nombre, registro de cada recomendación y auditoría periódica.', 'Saber siempre quién responde y por qué.'),
       ('Dedicado', 'Pocos clientes, atendidos a fondo.', 'Proyectos simultáneos limitados y equipos estables de principio a fin.', 'Conocimiento profundo y respuesta rápida.')]
pl = ''
for i, (a, b, c, d) in enumerate(pil):
    pl += f'''<div style="display:flex;flex-direction:column">
 <div style="border-top:.6mm solid #111214;padding-top:3mm"><span class="m s">{i+1:02d}</span><p style="font-weight:200;font-size:30pt;letter-spacing:-.035em;line-height:1;margin-top:3mm">{a}</p></div>
 <p class="h4" style="margin-top:4mm;min-height:10mm">{b}</p>
 <div class="row" style="grid-template-columns:1fr;margin-top:3mm"><span class="m s">Cómo lo demostramos</span><span class="p" style="margin-top:1mm">{c}</span></div>
 <div class="row" style="grid-template-columns:1fr;border-bottom:.2mm solid #D8D6D0"><span class="m s">Qué gana el cliente</span><span class="p" style="margin-top:1mm">{d}</span></div></div>'''
page(f'''{chhead('13', 'Pilares <b>de marca</b>', 'Propuesta de valor')}
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:7mm;margin-top:11mm">{pl}</div>
<div style="position:absolute;left:18mm;right:18mm;bottom:20mm;background:#1A1B1E;color:#fff;padding:6mm 7mm;display:grid;grid-template-columns:60mm 1fr;align-items:center"><p class="m" style="color:#A3A4A8">Cuatro pilares,<br>una sola promesa</p><p class="d2" style="font-size:22pt">Tecnología para decisiones que <b>no admiten error.</b></p></div>''', 'IV', '13 · Pilares de marca')

# ===================== 26 · MENSAJES CLAVE =====================
caps = [('Inteligencia artificial', 'Modelos que analizan, anticipan y recomiendan, sobre sus datos y donde están.'),
        ('Sistemas de seguridad', 'De la detección temprana a la respuesta coordinada.'),
        ('Software para defensa', 'Mando, control y gestión de la misión en entornos exigentes.'),
        ('Software para empresas', 'Sistemas a medida para operaciones que no pueden parar.'),
        ('Automatización', 'Procesos que funcionan solos y bajo control.'),
        ('Consultoría estratégica', 'Qué hacer, en qué orden y con qué riesgos.')]
cp = ''.join(f'<div class="row" style="grid-template-columns:31mm 1fr;column-gap:3mm;padding:1.8mm 0"><span class="h4" style="font-size:8.4pt">{a}</span><span class="p" style="font-size:8.3pt;line-height:1.45">{b}</span></div>' for a, b in caps)
page(f'''{chhead('14', 'Mensajes <b>clave</b>', 'Cómo lo contamos')}
<div class="g" style="margin-top:8mm;row-gap:6mm">
 <div style="grid-column:1/5" class="r"><p class="m s" style="margin-top:2.6mm">Promesa · claim público</p><p class="d2" style="font-size:19pt;margin-top:2mm">Tecnología para decisiones que <b>no admiten error.</b></p></div>
 <div style="grid-column:5/9" class="r"><p class="m s" style="margin-top:2.6mm">Lema · uso interno</p><p class="d2" style="font-size:19pt;margin-top:2mm">Mirar con amplitud. <b>Actuar con precisión.</b></p></div>
 <div style="grid-column:9/13" class="r"><p class="m s" style="margin-top:2.6mm">En una frase</p><p class="p" style="margin-top:2mm;font-size:10pt">HALVEX diseña, construye y opera inteligencia artificial, sistemas de seguridad y software para organizaciones que no pueden fallar.</p></div>
 <div style="grid-column:1/5" class="r"><p class="m s" style="margin-top:2.6mm">En 30 segundos</p><p class="p" style="margin-top:2mm">Las organizaciones críticas tienen más datos que nunca y la tecnología repartida entre muchos proveedores. En HALVEX, un solo equipo diseña la inteligencia artificial, la seguridad y el software, los despliega donde el cliente decide y pone una persona responsable detrás de cada sistema. Trabajamos con pocos clientes a la vez para hacerlo bien.</p></div>
 <div style="grid-column:5/9" class="r"><p class="m s" style="margin-top:2.6mm">Párrafo corporativo</p><p class="p" style="margin-top:2mm">HALVEX es una compañía tecnológica con sede en Madrid especializada en inteligencia artificial, sistemas de seguridad y software para defensa, administraciones públicas y grandes empresas. Diseña, construye y opera sistemas para organizaciones en las que una decisión tardía o un dato expuesto tienen consecuencias reales, con despliegue soberano y supervisión humana en cada decisión crítica.</p></div>
 <div style="grid-column:9/13" class="r"><p class="m s" style="margin-top:2.6mm">Por capacidad</p><div class="rows" style="margin-top:1.4mm">{cp}</div></div>
</div>''', 'IV', '14 · Mensajes clave')

# ===================== 27 · CASA DE MARCA =====================
blk = 'display:flex;flex-direction:column;justify-content:center;padding:3.5mm 5mm'
page(f'''{chhead('15', 'Casa <b>de marca</b>', 'La marca en una página')}
<div style="margin-top:8mm;display:grid;grid-template-columns:repeat(4,1fr);gap:1.4mm">
 <div style="grid-column:1/5;background:#1A1B1E;color:#fff;{blk};align-items:center;text-align:center;height:24mm"><p class="m" style="color:#A3A4A8">Promesa</p><p class="d2" style="font-size:20pt;margin-top:1.6mm">Tecnología para decisiones que <b>no admiten error.</b></p></div>
 <div style="grid-column:1/3;background:#EFEDE8;{blk};height:19mm"><p class="m s">Misión</p><p class="p" style="margin-top:1mm">Dar a quien no puede fallar la tecnología para decidir con información completa y actuar sin margen de error.</p></div>
 <div style="grid-column:3/5;background:#EFEDE8;{blk};height:19mm"><p class="m s">Visión</p><p class="p" style="margin-top:1mm">Ser la referencia europea en tecnología para decisiones críticas.</p></div>
 {''.join(f'<div style="box-shadow:inset 0 0 0 .25mm #111214;{blk};height:30mm;justify-content:flex-start;padding-top:4mm"><p class="m s">Pilar {i+1:02d}</p><p style="font-weight:300;font-size:17pt;letter-spacing:-.02em;margin-top:2mm">{p[0]}</p><p class="p s" style="margin-top:1mm;font-size:8.4pt">{p[1]}</p></div>' for i, p in enumerate(pil))}
 <div style="grid-column:1/5;background:#EFEDE8;{blk};height:15mm;flex-direction:row;align-items:center;justify-content:space-between"><p class="m s">Valores</p><p style="font-size:11.5pt;font-weight:300;letter-spacing:.01em">Rigor · Discreción · Soberanía · Responsabilidad · Exclusividad · Innovación útil</p></div>
 <div style="grid-column:1/5;background:#1A1B1E;color:#fff;{blk};height:14mm;flex-direction:row;align-items:center;justify-content:space-between"><p class="m" style="color:#A3A4A8">Personalidad y voz</p><p style="font-size:11pt;font-weight:300">Sobria · precisa · discreta · serena · exigente · moderna — clara, exacta y de usted</p></div>
</div>''', 'IV', '15 · Casa de marca')

# ===================== 28 · CONTRAPORTADA =====================
n += 1
P.append(f'''<section class="page dk" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10mm">
{iso('width:22mm;height:22mm', '#FFFFFF')}
<p style="font-size:16pt;font-weight:200;letter-spacing:-.01em">Mirar con amplitud. <b style="font-weight:400">Actuar con precisión.</b></p>
<div style="position:absolute;left:18mm;right:18mm;bottom:13mm;display:flex;justify-content:space-between;border-top:.25mm solid rgba(255,255,255,.4);padding-top:2.6mm" class="m"><span>HALVEX · Plataforma de marca · Edición 1.0</span><span style="color:#A3A4A8">Documento interno · No distribuir</span></div>
</section>''')

html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>HALVEX · Plataforma de marca</title><style>{CSS}</style></head><body>{C.DEFS}' + ''.join(P) + '</body></html>')
open(os.path.join(C.HERE, 'plataforma2.html'), 'w').write(html)
print(len(P), 'páginas')

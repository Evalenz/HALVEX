import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
# Carga el manual de identidad visual (estilos, dibujos y páginas ya revisadas)
V = {'__file__': os.path.join(HERE, 'visual2.py'), '__name__': 'v2'}
exec(open(os.path.join(HERE, 'visual2.py')).read(), V)
for k, v in V.items():
    if not k.startswith('__') and k not in ('P', 'n', 'page', 'divider', 'toc', 'DOC', 'PART'):
        globals()[k] = v
VP = V['P']

DOC = 'Manual corporativo'
PARTS = {'01': 'Identidad visual', '02': 'Normas del logo', '03': 'Códigos de color', '04': 'Normas tipográficas',
         '05': 'Lenguaje gráfico', '06': 'Aplicaciones y ejemplos', '07': 'Recursos'}
CSS += r'''
.mk{box-shadow:inset 0 0 0 .25mm #C9C7C1;background:#fff;position:relative;overflow:hidden}
.bar{height:1mm;background:#E2E0DA;margin-bottom:1.4mm}
.ok,.ko{font-family:"IBM Plex Mono",monospace;font-size:6.4pt;letter-spacing:.06em;text-transform:uppercase;display:inline-flex;align-items:center;gap:1.6mm}
.ok::before{content:"";width:1.7mm;height:1.7mm;background:#111214;transform:rotate(45deg)}
.ko::before{content:"×";font-size:9pt;line-height:1}
.chk{display:grid;grid-template-columns:5mm 1fr;align-items:start;padding:2.3mm 0;border-top:.2mm solid #D8D6D0}
.chk i{width:3.2mm;height:3.2mm;box-shadow:inset 0 0 0 .25mm #111214;margin-top:.5mm}
.code{font-family:"IBM Plex Mono",monospace;font-size:7pt;line-height:1.7;background:#1A1B1E;color:#D3D4D7;padding:4mm 5mm;white-space:pre}
'''

PAGES = []   # (html con %%N%% para el folio)
TOCI = []    # (parte, número de capítulo, título, índice de página)
cur = {'part': ''}


def run(chap):
    p = cur['part']
    return (f'<div class="run m"><span><b>HALVEX</b>&nbsp;&nbsp;&nbsp;{DOC}</span>'
            f'<span>{("Parte " + p + " · " + PARTS[p]) if p else ""}</span><span>{chap}</span></div>')


FOL = '<div class="fol"><span class="m s">Edición 1.0 · Noviembre 2026</span><span class="n">%%N%%</span></div>'


def add(inner, chap='', num=None, title=None, cls=''):
    if num: TOCI.append((cur['part'], num, title, len(PAGES)))
    PAGES.append(f'<section class="page {cls}">{run(chap)}{inner}{FOL}</section>')


def reuse(idx, num, title):
    sec = VP[idx]
    sec = re.sub(r'<div class="run m">.*?</div>', '', sec, count=1, flags=re.S)
    sec = re.sub(r'<div class="fol">.*?</div>', '', sec, count=1, flags=re.S)
    sec = re.sub(r'<span class="num">\d+</span>', f'<span class="num">{num}</span>', sec, count=1)
    head, rest = sec.split('>', 1)
    body = rest.rsplit('</section>', 1)[0]
    TOCI.append((cur['part'], num, title, len(PAGES)))
    PAGES.append(f'{head}>{run(num + " · " + title)}{body}{FOL}</section>')


def chh(num, t, k=''):
    return f'<div class="ch"><span class="num">{num}</span><h2>{t}</h2><span class="k m s">{k}</span></div>'


def divider(p, photo, intro, pos='center'):
    cur['part'] = p
    PAGES.append(('DIV', p, photo, intro, pos))


def bars(ws, col='#E2E0DA', h=1, gap=1.4):
    return ''.join(f'<div style="height:{h}mm;background:{col};margin-bottom:{gap}mm;width:{w}%"></div>' if w else f'<div style="height:{h+gap}mm"></div>' for w in ws)


def lbl(t, d=''):
    return f'<div class="lbl"><b>{t}</b><span>{d}</span></div>'


# =================================================================== 01
divider('01', 'hq-hero', 'Los elementos que forman la marca y cómo se construyen.')

tiles = [('Logotipo', wm('width:66%;height:auto', NEG), 'La palabra HALVEX, dibujada a medida.'),
         ('Isotipo', iso('width:24mm;height:24mm', NEG), 'Dos cuñas hacia un mismo vértice.'),
         ('Imagotipo', horiz(NEG, NEG, 'width:70%;height:auto'), 'La firma principal: símbolo y palabra.'),
         ('Color', f'<div style="display:flex;gap:2mm"><span style="width:20mm;height:20mm;background:{NEG}"></span><span style="width:20mm;height:20mm;background:{PIE}"></span><span style="width:10mm;height:20mm;background:{ACE}"></span><span style="width:10mm;height:20mm;background:{NIE}"></span></div>', 'Negro HALVEX, Piedra y grises de apoyo.'),
         ('Tipografía', '<div style="display:flex;align-items:baseline;gap:6mm"><span style="font-weight:200;font-size:44pt;letter-spacing:-.04em;line-height:1">Aa</span><span style="font-family:\'IBM Plex Mono\';font-size:26pt;line-height:1">Aa</span></div>', 'IBM Plex Sans e IBM Plex Mono.'),
         ('Lenguaje gráfico', f'<svg viewBox="0 0 200 60" style="width:70%"><g stroke="{NEG}" stroke-width=".7" fill="none"><path d="M0 4L180 30M0 17L180 30M0 30H180M0 43L180 30M0 56L180 30"/></g><path d="M184 26l4 4-4 4-4-4z" fill="{NEG}"/></svg>', 'Filetes, cotas, convergencia e iconos.')]
tt = ''.join(f'<div><div class="box bd" style="height:46mm">{s}<span class="cap m s">{t}</span></div>{lbl(t, d)}</div>' for t, s, d in tiles)
add(f'''{chh('01', 'El sistema <b>de identidad</b>', 'Seis elementos, una marca')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:5mm;row-gap:5mm;margin-top:7mm">{tt}</div>''', '01 · El sistema de identidad', '01', 'El sistema de identidad')
reuse(4, '02', 'Logotipo')
reuse(5, '03', 'Isotipo')
reuse(6, '04', 'Imagotipo')
reuse(7, '05', 'Versiones del logo')

# =================================================================== 02
divider('02', 'hq-piramide', 'Cómo se coloca, se escala y se combina el logo, y lo que nunca se hace con él.')
reuse(8, '06', 'Área de respeto y tamaño mínimo')
reuse(9, '07', 'Versiones monocromáticas')
reuse(10, '08', 'Fondos e imágenes')


def fmt(w, h, mx, lw, pos, ver='h', extra=''):
    # w,h en mm; mx margen en mm; lw ancho del logo en mm
    logo = horiz(NEG, NEG, f'width:{lw}mm;height:auto') if ver == 'h' else vert(NEG, NEG, f'width:{lw}mm;height:auto')
    st = {'tl': f'left:{mx}mm;top:{mx}mm', 'bl': f'left:{mx}mm;bottom:{mx}mm', 'tc': f'left:50%;top:{mx}mm;transform:translateX(-50%)'}[pos]
    return (f'<div class="mk" style="width:{w}mm;height:{h}mm"><div style="position:absolute;inset:{mx}mm;box-shadow:inset 0 0 0 .2mm #A3A4A8;border-radius:0;outline:.2mm dashed transparent"></div>'
            f'<div style="position:absolute;inset:{mx}mm;border:.2mm dashed #A3A4A8"></div><div style="position:absolute;{st}">{logo}</div>{extra}</div>')


fm = [('A4 · carta', fmt(44, 62.2, 3.1, 8.4, 'tl', extra=f'<div style="position:absolute;left:3.1mm;right:3.1mm;top:18mm">{bars([60, 90, 85, 92, 40, 0, 88, 93, 70])}</div>')),
      ('Presentación 16:9', fmt(76, 42.75, 3.8, 9, 'tl', extra=f'<div style="position:absolute;left:4.2mm;top:18mm;width:50mm">{bars([80, 55], "#C9C7C1", 2.2, 1.6)}</div>')),
      ('Publicación 1:1', fmt(44, 44, 3.5, 12.3, 'bl', extra=f'<div style="position:absolute;left:4mm;top:5mm;width:38mm">{bars([90, 70, 40], "#C9C7C1", 2.2, 1.6)}</div>')),
      ('Story 9:16', fmt(26, 46.2, 2.1, 10.4, 'tl', extra=f'<div style="position:absolute;left:2.4mm;top:22mm;width:24mm">{bars([90, 70], "#C9C7C1", 1.8, 1.4)}</div>')),
      ('Cartel · roll-up', fmt(26, 57, 2.6, 13, 'tc', 'v'))]
ff = ''.join(f'<div style="display:flex;flex-direction:column;justify-content:flex-end">{s}<p class="m s" style="margin-top:2mm">{t}</p></div>' for t, s in fm)
spec = [('A4 · carta', 'Horizontal', '40 mm · 19 % del ancho', '15 mm', 'Arriba a la izquierda'),
        ('Presentación 16:9', 'Horizontal', '12 % del ancho', '5 % del ancho', 'Arriba a la izquierda'),
        ('Publicación 1:1', 'Horizontal', '28 % del ancho', '8 % del ancho', 'Abajo a la izquierda'),
        ('Story 9:16', 'Horizontal', '40 % del ancho', '8 % del ancho', 'Arriba a la izquierda'),
        ('Cartel · roll-up', 'Vertical', '50 % del ancho', '10 % del ancho', 'Arriba, centrado')]
sp = ''.join(f'<div class="row" style="grid-template-columns:40mm 28mm 44mm 34mm 1fr;padding:1.7mm 0"><span class="h4" style="font-size:8.8pt">{a}</span><span class="p">{b}</span><span class="p">{c}</span><span class="p">{d}</span><span class="p">{e}</span></div>' for a, b, c, d, e in spec)
add(f'''{chh('09', 'Posición <b>y tamaño</b>', 'El logo en cada formato')}
<div style="display:flex;gap:7mm;align-items:flex-end;margin-top:5mm">{ff}</div>
<div style="margin-top:4mm"><div class="row" style="grid-template-columns:40mm 28mm 44mm 34mm 1fr;border:0;padding:0 0 1.6mm"><span class="m s">Formato</span><span class="m s">Versión</span><span class="m s">Ancho del logo</span><span class="m s">Margen</span><span class="m s">Posición</span></div><div class="rows">{sp}</div></div>''',
    '09 · Posición y tamaño', '09', 'Posición y tamaño en formatos')

partner = lambda w, h: f'<div style="width:{w}mm;height:{h}mm;border:.25mm dashed #65676C;display:flex;align-items:center;justify-content:center"><span class="m s">Logo del socio</span></div>'
cb1 = (f'<div class="box bd" style="height:52mm;gap:0"><div style="display:flex;align-items:center">{horiz(NEG, NEG, "width:58mm;height:auto")}'
       f'<div style="width:0;height:16mm;border-left:.25mm solid #111214;margin:0 10mm"></div>{partner(40, 12)}</div>'
       f'<span class="cap m s">A · Emisor HALVEX</span></div>')
cb2 = (f'<div class="box bd" style="height:52mm;flex-direction:column;gap:4mm"><span class="m s">En colaboración con</span><div style="display:flex;align-items:center;gap:10mm">{partner(36, 12)}{partner(36, 12)}</div>'
       f'<div style="position:absolute;left:5mm;bottom:5mm">{horiz(NEG, NEG, "width:30mm;height:auto")}</div><span class="cap m s">B · Varios socios</span></div>')
rules = [('Emisor a la izquierda', 'Quien firma la pieza va primero. Si el emisor es el socio, HALVEX va a la derecha.'),
         ('Mismo peso visual', 'El alto del isotipo iguala el alto del logo del socio. Ninguno domina.'),
         ('Separación 2x', 'Dos veces el área de respeto, con un filete vertical de 0,5 pt en negro.'),
         ('Sin fusiones', 'No se combinan los logos en uno ni se cambian los colores de ninguno.')]
rr = ''.join(f'<div class="row" style="grid-template-columns:42mm 1fr;padding:2.8mm 0"><span class="h4">{a}</span><span class="p">{b}</span></div>' for a, b in rules)
add(f'''{chh('10', 'Convivencia <b>con otras marcas</b>', 'Coedición y patrocinio')}
<div class="g" style="margin-top:7mm">
 <div style="grid-column:1/8;display:grid;gap:5mm">{cb1}{cb2}</div>
 <div class="rows" style="grid-column:9/13;align-self:start">{rr}</div>
</div>''', '10 · Convivencia con otras marcas', '10', 'Convivencia con otras marcas')
reuse(11, '11', 'Usos incorrectos')

# =================================================================== 03
divider('03', 'hq-escaleras', 'Los colores de la marca con todos sus códigos, en pantalla, en papel y en materiales.')
sec = VP[13].replace('Parte II · Color y tipografía', 'Parte 03 · Códigos de color').replace('09 · Color identificativo', '12 · Color identificativo').replace('&nbsp;&nbsp;&nbsp;Identidad visual', '&nbsp;&nbsp;&nbsp;Manual corporativo')
TOCI.append(('03', '12', 'Color identificativo', len(PAGES)))
PAGES.append(sec)
reuse(14, '13', 'Paleta cromática')

tok = [('--halvex-negro', NEG, 'Texto, logotipo, botón principal'), ('--halvex-grafito', GRAF, 'Fondo en modo oscuro, pie de página'),
       ('--halvex-acero', ACE, 'Texto secundario sobre claro'), ('--halvex-niebla', NIE, 'Texto secundario sobre oscuro, inactivo'),
       ('--halvex-linea', LIN, 'Bordes, filetes, separadores'), ('--halvex-piedra', PIE, 'Fondos de sección'), ('--halvex-blanco', BLA, 'Fondo principal')]
tk = ''.join(f'<div class="row" style="grid-template-columns:8mm 40mm 20mm 1fr;align-items:center;padding:2mm 0"><span style="width:5mm;height:5mm;background:{h};box-shadow:inset 0 0 0 .2mm #C9C7C1"></span><span class="m">{t}</span><span class="m s">{h}</span><span class="p" style="font-size:8.4pt">{u}</span></div>' for t, h, u in tok)
btn = lambda bg, fg, bd='': f'<span style="display:inline-flex;align-items:center;gap:3mm;background:{bg};color:{fg};{bd}padding:2.2mm 3.4mm;font-size:7.4pt;font-weight:500;white-space:nowrap">Contactar <span style="width:5mm;border-top:.25mm solid currentColor"></span></span>'
def ui(bg, fg, sub, line, primary):
    return (f'<div style="background:{bg};color:{fg};padding:5mm;box-shadow:inset 0 0 0 .2mm #D8D6D0">'
            f'<p class="m" style="color:{sub}">Componentes</p><p style="font-weight:200;font-size:16pt;letter-spacing:-.02em;margin-top:2mm">Decidir <b style="font-weight:400">con criterio.</b></p>'
            f'<p style="font-size:7.6pt;color:{sub};margin-top:1.6mm;line-height:1.5">Texto secundario y <span style="color:{fg};border-bottom:.25mm solid {fg}">enlace subrayado</span>.</p>'
            f'<div style="display:flex;gap:3mm;margin-top:4mm">{primary}{btn("transparent", fg, f"box-shadow:inset 0 0 0 .25mm {fg};")}</div>'
            f'<div style="margin-top:4mm;border-bottom:.25mm solid {line};padding-bottom:1.6mm;font-size:8pt;color:{sub}">Correo profesional</div></div>')
code = (':root {\n  --halvex-negro:   #111214;\n  --halvex-grafito: #1A1B1E;\n  --halvex-acero:   #65676C;\n  --halvex-niebla:  #A3A4A8;\n'
        '  --halvex-linea:   #D8D6D0;\n  --halvex-piedra:  #EFEDE8;\n  --halvex-blanco:  #FFFFFF;\n}')
add(f'''{chh('14', 'Color <b>en pantalla</b>', 'Tokens para web y aplicaciones')}
<div class="g" style="margin-top:6mm">
 <div style="grid-column:1/7"><div class="rows">{tk}</div><div class="code" style="margin-top:4mm">{code}</div></div>
 <div style="grid-column:7/13;display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-content:start">
  {ui(BLA, NEG, ACE, NEG, btn(NEG, BLA))}{ui(GRAF, BLA, NIE, BLA, btn(BLA, NEG))}
  <p class="p s" style="grid-column:1/3">Modo claro y modo oscuro con los mismos componentes. El foco del teclado se marca con un contorno de 1 px a 4 px del elemento, en el color del texto. Los errores se indican con texto e icono, nunca solo con color.</p>
 </div>
</div>''', '14 · Color en pantalla', '14', 'Color en pantalla')

mats = [('Papel blanco natural', BLA, NEG, 'Papelería: no estucado de 120 g (carta) a 350 g (tarjeta).'),
        ('Papel o cartulina negra', NEG, BLA, 'Tarjetas y carpetas, con serigrafía o estampación blanca.'),
        ('Acero lacado', '#2A2B2F', BLA, 'Rotulación y placas: negro mate, referencia RAL 9005.'),
        ('Piedra · caliza', PIE, NEG, 'Paredes y fondos: vinilo negro mate o letra corpórea.')]
mm_ = ''.join(f'<div><div style="height:30mm;background:{bg};color:{fg};box-shadow:inset 0 0 0 .2mm #C9C7C1;display:flex;align-items:center;justify-content:center">{iso("width:11mm;height:11mm", fg)}</div>{lbl(t, d)}</div>' for t, bg, fg, d in mats)
pr = [('Negro en masas', 'Negro enriquecido C60 M40 Y40 K100 en fondos y superficies grandes.'),
      ('Negro en texto', 'K100 en textos de menos de 14 pt, para que no haya registro.'),
      ('Piedra', 'Mejor con papel de tono natural que con tinta; si se imprime, prueba de color previa.'),
      ('Acabados', 'Estampación en seco, serigrafía blanca sobre negro y barniz mate selectivo. Sin brillos ni metalizados.'),
      ('Textil', 'Bordado o serigrafía blanca sobre negro. Isotipo de 15 mm como mínimo en bordado.'),
      ('Pantalla y vídeo', 'Siempre en RGB o HEX; nunca convertir desde CMYK.')]
pp = ''.join(f'<div class="row" style="grid-template-columns:34mm 1fr;padding:2.4mm 0"><span class="h4" style="font-size:9pt">{a}</span><span class="p">{b}</span></div>' for a, b in pr)
add(f'''{chh('15', 'Impresión <b>y materiales</b>', 'El color fuera de la pantalla')}
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:5mm;margin-top:7mm">{mm_}</div>
<div class="g" style="margin-top:6mm"><div class="rows" style="grid-column:1/10">{pp}</div><p class="m s" style="grid-column:10/13;text-transform:none;letter-spacing:.02em;align-self:end">Las referencias CMYK, Pantone y RAL son orientativas: pedir siempre prueba al proveedor.</p></div>''',
    '15 · Impresión y materiales', '15', 'Impresión y materiales')
reuse(15, '16', 'Contraste')

# =================================================================== 04
divider('04', 'hq-fachada', 'Las familias tipográficas, sus tamaños y las reglas para componer textos de la marca.')
reuse(16, '17', 'Tipografía principal')
reuse(17, '18', 'Tipografía secundaria y jerarquía')

sc = [('Display', '60–120 pt', '64–120 px', '200', '1,0', '−3,5 %', '<span style="font-weight:200;font-size:22pt;letter-spacing:-.035em;line-height:1">Hablemos.</span>'),
      ('Título 1', '36–44 pt', '44–64 px', '200 + 400', '1,05', '−3 %', '<span style="font-weight:200;font-size:16pt;letter-spacing:-.03em;line-height:1">Decidir <b style="font-weight:400">sin error.</b></span>'),
      ('Título 2', '24–30 pt', '32–40 px', '200 + 400', '1,1', '−2,5 %', '<span style="font-weight:200;font-size:13pt;letter-spacing:-.025em">Un único <b style="font-weight:400">responsable.</b></span>'),
      ('Título 3', '14–16 pt', '20–24 px', '400', '1,2', '−1 %', '<span style="font-size:11pt;letter-spacing:-.01em">Sistemas de seguridad</span>'),
      ('Entradilla', '12–14 pt', '18–21 px', '300', '1,5', '0', '<span style="font-weight:300;font-size:10pt">Trabajamos donde se cruzan los datos.</span>'),
      ('Texto', '9–10,5 pt', '16–17 px', '400', '1,6', '0', '<span style="font-size:8.6pt">Modelos que analizan y recomiendan.</span>'),
      ('Nota', '7,5–8 pt', '13–14 px', '400', '1,5', '0', '<span style="font-size:7.4pt;color:#65676C">Fuente: elaboración propia.</span>'),
      ('Etiqueta', '6,5–8 pt', '11–12 px', 'Mono 400', '1,5', '+6 %', '<span class="m">02 · Capacidades</span>')]
cols_ = 'grid-template-columns:22mm 24mm 24mm 22mm 16mm 16mm 1fr'
ss = ''.join(f'<div class="row" style="{cols_};align-items:baseline;padding:2.2mm 0"><span class="m">{a}</span><span class="p">{b}</span><span class="p">{c}</span><span class="p">{d}</span><span class="p">{e}</span><span class="p">{f}</span>{g}</div>' for a, b, c, d, e, f, g in sc)
add(f'''{chh('19', 'Escala <b>tipográfica</b>', 'Tamaños para papel y pantalla')}
<div style="margin-top:6mm"><div class="row" style="{cols_};border:0;padding:0 0 1.6mm"><span class="m s">Nivel</span><span class="m s">Impreso</span><span class="m s">Pantalla</span><span class="m s">Peso</span><span class="m s">Interlín.</span><span class="m s">Espaciado</span><span class="m s">Muestra</span></div><div class="rows">{ss}</div></div>''',
    '19 · Escala tipográfica', '19', 'Escala tipográfica')

lorem = 'Trabajamos para organizaciones en las que una decisión tardía o un dato expuesto tienen consecuencias reales.'
cr = [('Alineado a la izquierda', 'Nunca justificado: se abren huecos y se pierde ritmo.', f'<p style="font-size:7pt;line-height:1.5">{lorem}</p>', f'<p style="font-size:7pt;line-height:1.5;text-align:justify;word-spacing:2.2mm">{lorem}</p>'),
      ('Dos pesos en titulares', '200 para la frase, 400 para la idea clave.', '<p style="font-weight:200;font-size:13pt;letter-spacing:-.025em;line-height:1.1">Decisiones que <b style="font-weight:400">no admiten error.</b></p>', '<p style="font-weight:700;font-size:13pt;line-height:1.1">DECISIONES QUE NO ADMITEN ERROR</p>'),
      ('Mayúsculas solo en etiquetas', 'En Plex Mono y con espaciado. Nunca en titulares.', '<p class="m">03 · Sectores</p><p style="font-size:10pt;margin-top:1mm">Banca y seguros</p>', '<p style="font-size:10pt;text-transform:uppercase;letter-spacing:.02em">Banca y seguros</p>'),
      ('Línea de 45 a 75 caracteres', 'Las líneas largas cansan; las cortas rompen la lectura.', f'<p style="font-size:7pt;line-height:1.5;max-width:42mm">{lorem}</p>', f'<p style="font-size:6pt;line-height:1.4;white-space:nowrap;overflow:hidden">{lorem} {lorem}</p>'),
      ('Énfasis con peso, no con estilo', 'Medium 500 para destacar. Sin subrayados ni colores.', '<p style="font-size:8pt">Despliegue <b style="font-weight:500">en sus centros de datos</b>.</p>', '<p style="font-size:8pt">Despliegue <u><i style="color:#2456A6">en sus centros de datos</i></u>.</p>'),
      ('Interlineado generoso', '1,0–1,1 en titulares y 1,5–1,6 en texto.', f'<p style="font-size:7pt;line-height:1.6">{lorem}</p>', f'<p style="font-size:7pt;line-height:1.05">{lorem}</p>')]
cc_ = ''
for t, d, yes, no in cr:
    cc_ += (f'<div class="r" style="padding-top:2.6mm"><p class="h4">{t}</p><p class="p s" style="margin-top:.8mm;font-size:8pt">{d}</p>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm"><div style="background:{PIE};padding:3mm;min-height:22mm"><span class="ok">Así</span><div style="margin-top:2mm">{yes}</div></div>'
            f'<div style="box-shadow:inset 0 0 0 .2mm #D8D6D0;padding:3mm;min-height:22mm;overflow:hidden"><span class="ko">Así no</span><div style="margin-top:2mm;color:#65676C">{no}</div></div></div></div>')
add(f'''{chh('20', 'Reglas <b>de composición</b>', 'Cómo se compone un texto HALVEX')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm;row-gap:5mm;margin-top:6mm">{cc_}</div>''', '20 · Reglas de composición', '20', 'Reglas de composición')

ot = [('Nombre de marca', 'HALVEX', 'Halvex · HalVex · la HALVEX'), ('Comillas', '«…», y “…” dentro', '"…"'),
      ('Cifras', '1.250.000 · 3,5', '1,250,000 · 3.5'), ('Porcentajes', '15 %', '15%'), ('Moneda', '2.500 €', '€2.500 · 2500€'),
      ('Fechas', '4 de noviembre de 2026 · 04/11/2026', 'November 4, 2026 · 11/04/26'), ('Horas', '10:00 · 16:30', '10.00h · 4:30 pm'),
      ('Unidades', '24 h · 5 mm · 120 px', '24h · 5mm · 120px'), ('Rangos', '2–4 semanas (raya corta)', '2-4 semanas'),
      ('Siglas', 'IA · CISO · ENS', 'I.A. · A.I. · Ia'), ('Titulares', 'Solo la inicial en mayúscula', 'Cada Palabra En Mayúscula'),
      ('Tratamiento', 'Usted, en comunicación externa', 'Tú, en web y propuestas')]
oo = ''.join(f'<div class="row" style="grid-template-columns:34mm 1fr 1fr;padding:1.55mm 0"><span class="h4" style="font-size:8.8pt">{a}</span><span class="p">{b}</span><span class="p strike">{c}</span></div>' for a, b, c in ot)
add(f'''{chh('21', 'Orto<b>tipografía</b>', 'Normas de escritura')}
<div class="g" style="margin-top:6mm">
 <p class="p s" style="grid-column:1/4;padding-right:3mm">La marca también se reconoce por cómo escribe. Estas normas siguen la Ortografía de la lengua española y se aplican a cualquier texto de HALVEX.</p>
 <div style="grid-column:4/13"><div class="row" style="grid-template-columns:34mm 1fr 1fr;border:0;padding:0 0 1.6mm"><span class="m s">Caso</span><span class="m s">Así</span><span class="m s">Así no</span></div><div class="rows">{oo}</div></div>
</div>''', '21 · Ortotipografía', '21', 'Ortotipografía')

# =================================================================== 05
divider('05', 'hq-equipo-w', 'Retícula, recursos gráficos, iconos, fotografía e ilustración.')


def grid_svg(W, H, cols, m, gut, extra=''):
    cw = (W - 2 * m - (cols - 1) * gut) / cols
    rects = ''.join(f'<rect x="{m + i*(cw+gut):.2f}" y="{m}" width="{cw:.2f}" height="{H-2*m}" fill="#EFEDE8"/>' for i in range(cols))
    return (f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;background:#fff;box-shadow:inset 0 0 0 .25mm #C9C7C1">{rects}'
            f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="#65676C" stroke-width=".4" stroke-dasharray="2 1.5"/>{extra}</svg>')


g1 = grid_svg(210, 297, 12, 15, 4, f'<g transform="translate(15 15)">' + horiz(NEG, NEG).replace('<svg class="" viewBox="0 -30 784 160" style="">', '<svg viewBox="0 -30 784 160" width="40" height="8.16">') + '</g>')
g2 = grid_svg(320, 180, 12, 16, 5)
g3 = grid_svg(108, 108, 6, 8.6, 3)
add(f'''{chh('22', 'Retícula <b>de maquetación</b>', 'La estructura de cada pieza')}
<div style="display:grid;grid-template-columns:50mm 128mm 56mm;column-gap:9mm;margin-top:6mm;align-items:end">
 <div>{g1}<p class="m s" style="margin-top:2mm">A4 · 12 columnas</p></div>
 <div>{g2}<p class="m s" style="margin-top:2mm">Presentación 16:9 · 12 columnas</p></div>
 <div>{g3}<p class="m s" style="margin-top:2mm">Publicación 1:1 · 6 columnas</p></div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm;margin-top:7mm">
 <div class="r" style="padding-top:2.6mm"><p class="h4">A4 y documentos</p><p class="p s" style="margin-top:1mm">Márgenes de 15 mm, 12 columnas y medianil de 4 mm.</p></div>
 <div class="r" style="padding-top:2.6mm"><p class="h4">Presentaciones</p><p class="p s" style="margin-top:1mm">Margen del 5 % del ancho, 12 columnas y medianil del 1,5 %.</p></div>
 <div class="r" style="padding-top:2.6mm"><p class="h4">Redes sociales</p><p class="p s" style="margin-top:1mm">Margen del 8 %, 6 columnas. Nada importante en el 10 % exterior.</p></div>
 <div class="r" style="padding-top:2.6mm"><p class="h4">Composición asimétrica</p><p class="p s" style="margin-top:1mm">El texto ocupa de 5 a 8 columnas; el resto respira.</p></div>
</div>''', '22 · Retícula de maquetación', '22', 'Retícula de maquetación')
reuse(19, '23', 'Elementos gráficos')
reuse(20, '24', 'Patrones')
reuse(21, '25', 'Iconografía')
reuse(22, '26', 'Estilo fotográfico')
reuse(23, '27', 'Estilo de ilustración')

# =================================================================== 06
divider('06', 'hq-c-defensa', 'La marca aplicada: papelería, documentos, presentaciones, web, redes, señalética, objetos y eventos.')
reuse(25, '28', 'Papelería')


def a4(w, inner, bg=BLA, extra=''):
    return f'<div class="mk" style="width:{w}mm;height:{w*1.414:.1f}mm;background:{bg};{extra}">{inner}</div>'


d1 = a4(62, f'''<div style="position:absolute;inset:0;background:{NEG};color:#fff;padding:6mm">
<p class="m" style="font-size:4.6pt;color:{NIE}">Propuesta · Confidencial</p>
<p style="margin-top:20mm;font-weight:200;font-size:15pt;letter-spacing:-.03em;line-height:1.05">Plataforma<br>de apoyo a la<br><b style="font-weight:400">decisión</b></p>
<p class="m" style="font-size:4.4pt;color:{NIE};margin-top:4mm">Para [Cliente] · Noviembre 2026</p>
<div style="position:absolute;left:6mm;right:6mm;bottom:6mm">{wm("width:100%;height:auto", BLA)}</div></div>''')
d2 = a4(62, f'''<div style="padding:5mm"><div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:1mm"><span class="m" style="font-size:3.8pt">HALVEX · Propuesta</span><span class="m" style="font-size:3.8pt">02 · Enfoque</span></div>
<p style="font-weight:200;font-size:22pt;letter-spacing:-.05em;line-height:.8;margin-top:5mm">02</p><p style="font-weight:200;font-size:9pt;letter-spacing:-.02em;margin-top:2mm">Tres fases, <b style="font-weight:400">un responsable.</b></p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:4mm"><div>{bars([100, 96, 98, 90, 100, 60])}</div><div>{bars([100, 94, 97, 92, 80])}</div></div>
<div style="margin-top:3mm;border-top:.2mm solid {NEG}">{''.join(f'<div style="display:grid;grid-template-columns:1fr 2fr;gap:2mm;border-bottom:.15mm solid {LIN};padding:1.2mm 0"><span class="m" style="font-size:3.6pt">0{i}</span><div style="height:.8mm;background:#E2E0DA;margin-top:.8mm"></div></div>' for i in (1, 2, 3, 4))}</div>
<div style="position:absolute;left:5mm;right:5mm;bottom:4mm;display:flex;justify-content:space-between"><span class="m" style="font-size:3.6pt;color:{ACE}">Edición 1.0</span><span class="m" style="font-size:3.6pt">07</span></div></div>''')
rowsF = ''.join(f'<div style="display:grid;grid-template-columns:3fr 1fr 1fr;gap:2mm;border-bottom:.15mm solid {LIN};padding:1.1mm 0"><div style="height:.8mm;background:#E2E0DA;margin-top:.8mm;width:{w}%"></div><span class="m" style="font-size:3.6pt;text-align:right">[ ]</span><span class="m" style="font-size:3.6pt;text-align:right">[ ] €</span></div>' for w in (80, 60, 70))
d3 = a4(62, f'''<div style="padding:5mm">{horiz(NEG, NEG, "width:18mm;height:auto")}
<div style="display:flex;justify-content:space-between;margin-top:7mm"><div><p class="m" style="font-size:3.8pt;color:{ACE}">Factura</p><p style="font-size:9pt;font-weight:300;margin-top:.6mm">Nº [2026-0001]</p></div><div style="text-align:right"><p class="m" style="font-size:3.8pt;color:{ACE}">Fecha</p><p style="font-size:6pt;margin-top:.6mm">[dd/mm/aaaa]</p></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:5mm"><div><p class="m" style="font-size:3.6pt;color:{ACE}">Emisor</p>{bars([80, 60, 70], h=.8, gap=1)}</div><div><p class="m" style="font-size:3.6pt;color:{ACE}">Cliente</p>{bars([75, 65, 50], h=.8, gap=1)}</div></div>
<div style="margin-top:5mm;border-top:.2mm solid {NEG}">{rowsF}</div>
<div style="display:flex;justify-content:flex-end;gap:5mm;margin-top:3mm;align-items:baseline"><span class="m" style="font-size:3.8pt">Total</span><span style="font-size:10pt;font-weight:300">[ ] €</span></div>
<div style="position:absolute;left:5mm;right:5mm;bottom:4mm;border-top:.2mm solid {NEG};padding-top:1mm"><span class="m" style="font-size:3.4pt;color:{ACE}">HALVEX · [Denominación social] · [NIF] · Madrid</span></div></div>''')
add(f'''{chh('29', 'Documentos', 'Propuestas, informes y facturas')}
<div style="display:grid;grid-template-columns:repeat(3,62mm) 1fr;column-gap:8mm;margin-top:6mm;align-items:start">
 <div>{d1}{lbl('Portada de propuesta', 'Negro, título en dos pesos, logotipo a todo el ancho.')}</div>
 <div>{d2}{lbl('Página interior', 'Cabecera con filete, número de capítulo y columnas.')}</div>
 <div>{d3}{lbl('Factura', 'Imagotipo, datos fiscales en el pie y tabla con filetes.')}</div>
 <div class="rows" style="align-self:start">
  <div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">Plantillas</span><span class="p" style="margin-top:1mm">Word y PowerPoint con estilos ya definidos. Pendientes de crear.</span></div>
  <div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">Confidencialidad</span><span class="p" style="margin-top:1mm">Marcar en la cabecera: Uso interno, Confidencial o Público.</span></div>
  <div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">Datos pendientes</span><span class="p" style="margin-top:1mm">Denominación social y NIF, en cuanto exista la sociedad.</span></div>
 </div>
</div>''', '29 · Documentos', '29', 'Documentos')


def slide(w, inner, bg=BLA, dark=False):
    return f'<div class="mk" style="width:{w}mm;height:{w*9/16:.2f}mm;background:{bg};{"color:#fff;" if dark else ""}">{inner}</div>'


W_ = 96
sl = [slide(W_, f'''<div style="padding:5mm 6mm;height:100%;position:relative"><span class="m" style="font-size:4.4pt;color:{NIE}">HALVEX · Propuesta</span>
<p style="position:absolute;left:6mm;top:15mm;font-weight:200;font-size:17pt;letter-spacing:-.03em;line-height:1.05">Plataforma de apoyo<br><b style="font-weight:400">a la decisión</b></p>
<div style="position:absolute;left:6mm;right:6mm;bottom:5mm">{wm("width:100%;height:auto", BLA)}</div></div>''', GRAF, True),
      slide(W_, f'''<div style="padding:5mm 6mm"><div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:1.2mm"><span class="m" style="font-size:4.2pt">HALVEX</span><span class="m" style="font-size:4.2pt">Contenido</span></div>
<div style="display:grid;grid-template-columns:1fr 1.4fr;gap:6mm;margin-top:5mm"><p style="font-weight:200;font-size:16pt;letter-spacing:-.03em">Contenido</p><div>{''.join(f'<div style="display:grid;grid-template-columns:7mm 1fr;border-top:.15mm solid {LIN};padding:1.3mm 0"><span class="m" style="font-size:4pt;color:{ACE}">0{i}</span><span style="font-size:6pt;font-weight:300">{t}</span></div>' for i, t in enumerate(('Contexto', 'Enfoque', 'Arquitectura', 'Plan y fases', 'Equipo'), 1))}</div></div></div>'''),
      slide(W_, f'''<div style="padding:5mm 6mm;position:relative;height:100%"><div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:1.2mm"><span class="m" style="font-size:4.2pt">HALVEX</span><span class="m" style="font-size:4.2pt">04 · Plan</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:5mm"><div><p style="font-weight:200;font-size:44pt;letter-spacing:-.06em;line-height:.8">3</p><p class="m" style="font-size:4.2pt;margin-top:2mm">Fases de seis semanas</p></div>
<div><p style="font-weight:200;font-size:10pt;letter-spacing:-.02em;line-height:1.15">Un único equipo, <b style="font-weight:400">de principio a fin.</b></p><div style="margin-top:3mm">{bars([100, 92, 96, 70], h=.8, gap=1.1)}</div></div></div></div>'''),
      slide(W_, f'''<div style="padding:5mm 6mm;position:relative;height:100%;background:{NEG};color:#fff"><span class="m" style="font-size:4.2pt;color:{NIE}">HALVEX</span>
<p style="position:absolute;left:6mm;top:14mm;font-weight:200;font-size:30pt;letter-spacing:-.05em;line-height:.9">Hablemos.</p>
<div style="position:absolute;left:6mm;right:6mm;bottom:5mm;display:flex;justify-content:space-between;align-items:flex-end">{horiz(BLA, BLA, "width:24mm;height:auto")}<span class="m" style="font-size:4.2pt">contacto@halvex.com</span></div></div>''')]
names = [('Portada', 'Grafito, título en dos pesos y logotipo a todo el ancho.'), ('Índice', 'Lista con numeración en Plex Mono.'),
         ('Contenido con cifra', 'Un dato grande y una idea. Una sola cosa por diapositiva.'), ('Cierre', 'Negro, «Hablemos.» y contacto.')]
ss_ = ''.join(f'<div>{s}{lbl(a, b)}</div>' for s, (a, b) in zip(sl, names))
add(f'''{chh('30', 'Presenta<b>ciones</b>', 'Plantilla 16:9')}
<div style="display:grid;grid-template-columns:{W_}mm {W_}mm;column-gap:12mm;row-gap:3mm;margin-top:4mm;justify-content:start">{ss_}</div>''', '30 · Presentaciones', '30', 'Presentaciones')

desk = (f'<div class="mk" style="width:168mm;height:104mm">'
        f'<div style="height:6mm;background:{PIE};display:flex;align-items:center;gap:1.4mm;padding:0 3mm">{"".join(f"<i style=\"width:1.8mm;height:1.8mm;border-radius:50%;background:{NIE}\"></i>" for _ in range(3))}<span style="margin-left:4mm;background:#fff;height:3.6mm;padding:0 3mm;display:flex;align-items:center;gap:1.6mm"><span style="width:2.6mm;height:2.6mm;background:{NEG};display:flex;align-items:center;justify-content:center">{iso("width:1.6mm;height:1.6mm", BLA)}</span><span class="m" style="font-size:4.4pt">HALVEX</span></span></div>'
        f'<div style="padding:4mm 8mm"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:.2mm solid {NEG};padding-bottom:2.4mm">{horiz(NEG, NEG, "width:22mm;height:auto")}<span class="m" style="font-size:4.6pt;word-spacing:2.4mm">Enfoque Capacidades Sectores Método Compañía Contacto</span></div>'
        f'<div style="margin-top:6mm">{wm("width:100%;height:auto", NEG)}</div>'
        f'<div style="display:grid;grid-template-columns:1.4fr 1fr;gap:8mm;margin-top:6mm;align-items:end"><p style="font-weight:200;font-size:17pt;letter-spacing:-.03em;line-height:1.05">Tecnología para decisiones<br>que <b style="font-weight:400">no admiten error.</b></p>'
        f'<span style="display:inline-flex;align-items:center;gap:3mm;font-size:6.4pt;font-weight:500">Hablar con nuestro equipo <span style="width:10mm;border-top:.25mm solid {NEG}"></span></span></div></div></div>')
mob = (f'<div class="mk" style="width:44mm;height:90mm;border-radius:4mm;box-shadow:inset 0 0 0 .6mm {NEG}">'
       f'<div style="padding:5mm 4mm"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:.2mm solid {NEG};padding-bottom:1.6mm">{horiz(NEG, NEG, "width:14mm;height:auto")}<span style="font-size:4.6pt;font-weight:500">Menú</span></div>'
       f'<div style="margin-top:6mm">{wm("width:100%;height:auto", NEG)}</div><p style="font-weight:200;font-size:10pt;letter-spacing:-.02em;line-height:1.1;margin-top:5mm">Tecnología para decisiones que <b style="font-weight:400">no admiten error.</b></p>'
       f'<div style="margin-top:5mm">{bars([100, 92, 70], h=.8, gap=1.1)}</div><span style="display:inline-flex;align-items:center;gap:2mm;font-size:4.8pt;font-weight:500;margin-top:3mm">Hablar con nuestro equipo <span style="width:6mm;border-top:.25mm solid {NEG}"></span></span></div></div>')
mail = (f'<div class="mk" style="width:44mm;padding:4mm"><p style="font-size:6.2pt;font-weight:500">Nombre Apellido</p><p style="font-size:5.4pt;color:{ACE}">Cargo · HALVEX</p>'
        f'<div style="border-top:.2mm solid {LIN};margin:2.4mm 0"></div>{horiz(NEG, NEG, "width:20mm;height:auto")}<p class="m" style="font-size:4.2pt;color:{ACE};margin-top:1.6mm">nombre@halvex.com · +34 000 000 000</p></div>')
add(f'''{chh('31', 'Web <b>y correo</b>', 'Escritorio, móvil y firma')}
<div style="display:grid;grid-template-columns:168mm 44mm 1fr;column-gap:8mm;margin-top:5mm;align-items:start">
 <div>{desk}{lbl('Web · escritorio', 'Imagotipo en la cabecera, logotipo a todo el ancho y mucho blanco.')}</div>
 <div>{mob}{lbl('Web · móvil', 'Las mismas piezas apiladas.')}</div>
 <div>{mail}{lbl('Firma de correo', 'Texto real (no imagen) y el imagotipo en PNG a 120 px.')}</div>
</div>''', '31 · Web y correo', '31', 'Web y correo')

prof = (f'<div class="mk" style="width:118mm;height:58mm"><div style="height:24mm;background:{GRAF};display:flex;align-items:center;justify-content:center">{wm("width:44mm;height:auto", BLA)}</div>'
        f'<div style="position:absolute;left:6mm;top:15mm;width:18mm;height:18mm;background:{NEG};border:.8mm solid #fff;display:flex;align-items:center;justify-content:center">{iso("width:8mm;height:8mm", BLA)}</div>'
        f'<div style="padding:11mm 6mm 0"><p style="font-size:9pt;font-weight:500">HALVEX</p><p style="font-size:6.4pt;color:{ACE};margin-top:.6mm">Inteligencia artificial, seguridad y software para decisiones críticas · Madrid</p>'
        f'<div style="display:flex;gap:2mm;margin-top:3mm"><span style="background:{NEG};color:#fff;font-size:5.4pt;padding:1.2mm 3mm">Seguir</span><span style="box-shadow:inset 0 0 0 .2mm {NEG};font-size:5.4pt;padding:1.2mm 3mm">Visitar web</span></div></div></div>')
p1 = (f'<div class="mk" style="width:50mm;height:50mm;background:{PIE};padding:4mm"><span class="m" style="font-size:4pt;color:{ACE}">Principios · 03</span>'
      f'<p style="font-weight:200;font-size:11.5pt;letter-spacing:-.02em;line-height:1.1;margin-top:4mm">«Ninguna decisión crítica <b style="font-weight:400">es automática.</b>»</p>'
      f'<div style="position:absolute;left:4mm;bottom:4mm">{horiz(NEG, NEG, "width:14mm;height:auto")}</div></div>')
p2 = (f'<div class="mk" style="width:50mm;height:50mm;background:{NEG};color:#fff;padding:4mm"><span class="m" style="font-size:4pt;color:{NIE}">Método</span>'
      f'<p style="font-weight:200;font-size:30pt;letter-spacing:-.06em;line-height:.8;margin-top:5mm">04</p><p style="font-weight:200;font-size:8.5pt;letter-spacing:-.02em;margin-top:2mm;line-height:1.1">fases, del diagnóstico <b style="font-weight:400">a la decisión.</b></p>'
      f'<div style="position:absolute;left:4mm;bottom:4mm">{horiz(BLA, BLA, "width:14mm;height:auto")}</div></div>')
p3 = (f'<div class="mk photo" style="width:50mm;height:50mm;background-image:linear-gradient(rgba(0,0,0,.15),rgba(0,0,0,.45)),url({img64("hq-portada")});color:#fff;padding:4mm">'
      f'<span class="m" style="font-size:4pt">Publicación</span><p style="position:absolute;left:4mm;right:4mm;bottom:11mm;font-weight:300;font-size:8.5pt;line-height:1.15">Cómo evaluamos modelos en entornos aislados.</p>'
      f'<div style="position:absolute;left:4mm;bottom:4mm">{horiz(BLA, BLA, "width:14mm;height:auto")}</div></div>')
st_ = (f'<div class="mk" style="width:28mm;height:50mm;background:{GRAF};color:#fff;padding:3mm"><div>{horiz(BLA, BLA, "width:12mm;height:auto")}</div>'
       f'<p style="font-weight:200;font-size:9pt;letter-spacing:-.02em;line-height:1.1;margin-top:12mm">Mirar con amplitud. <b style="font-weight:400">Actuar con precisión.</b></p>'
       f'<span class="m" style="position:absolute;left:3mm;bottom:3mm;font-size:3.6pt;color:{NIE}">halvex.com</span></div>')
add(f'''{chh('32', 'Redes <b>sociales</b>', 'Perfil y publicaciones')}
<div style="display:grid;grid-template-columns:118mm 1fr;column-gap:9mm;margin-top:5mm;align-items:start">
 <div>{prof}{lbl('Página de empresa', 'Portada en grafito con el logotipo; avatar con el isotipo.')}
  <div class="rows" style="margin-top:4mm"><div class="row" style="grid-template-columns:30mm 1fr;padding:2mm 0"><span class="m s">Frecuencia</span><span class="p">Poca y con contenido propio: método, principios, publicaciones.</span></div>
  <div class="row" style="grid-template-columns:30mm 1fr;padding:2mm 0"><span class="m s">Nunca</span><span class="p">Nombres de clientes sin permiso, emojis ni fotos de banco de imágenes.</span></div></div></div>
 <div><div style="display:flex;gap:4mm;align-items:flex-end">{p1}{p2}{p3}{st_}</div>
  <div style="display:grid;grid-template-columns:50mm 50mm 50mm 28mm;column-gap:4mm">{lbl('Cita', 'Fondo Piedra.')}{lbl('Cifra', 'Negro.')}{lbl('Imagen', 'Foto B/N con velo.')}{lbl('Story', '9:16.')}</div></div>
</div>''', '32 · Redes sociales', '32', 'Redes sociales')

wall = f'background:{PIE};background-image:repeating-linear-gradient(0deg,transparent 0 9.6mm,#E2E0DA 9.6mm 9.8mm),repeating-linear-gradient(90deg,transparent 0 19.6mm,#E2E0DA 19.6mm 19.8mm)'
s1_ = (f'<div style="height:88mm;{wall};display:flex;align-items:center;justify-content:center"><div style="width:52mm;height:62mm;background:{GRAF};box-shadow:1mm 1.4mm 0 rgba(0,0,0,.12);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5mm">'
       f'{vert(BLA, BLA, "width:30mm;height:auto")}<span class="m" style="font-size:4.4pt;color:{NIE}">Planta 2 · Madrid</span></div></div>')
dirs = [('Planta 3', 'Dirección'), ('Planta 2', 'Ingeniería · Operaciones'), ('Planta 1', 'Reuniones · Sala Vértice'), ('Planta 0', 'Recepción')]
s2_ = (f'<div style="height:88mm;background:{NEG};color:#fff;padding:6mm"><div>{horiz(BLA, BLA, "width:24mm;height:auto")}</div><div style="margin-top:9mm">'
       + ''.join(f'<div style="display:grid;grid-template-columns:16mm 1fr;border-top:.2mm solid rgba(255,255,255,.25);padding:2.4mm 0"><span class="m" style="font-size:5pt;color:{NIE}">{a}</span><span style="font-size:8pt;font-weight:300">{b}</span></div>' for a, b in dirs) + '</div></div>')
s3_ = (f'<div style="height:88mm;background:#fff;box-shadow:inset 0 0 0 .25mm #C9C7C1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6mm">'
       f'<div style="width:46mm;height:26mm;background:{NEG};color:#fff;padding:3.5mm;position:relative"><span class="m" style="font-size:4.4pt;color:{NIE}">Sala 01</span><p style="font-weight:200;font-size:15pt;letter-spacing:-.03em;margin-top:1mm">Vértice</p><span style="position:absolute;right:3.5mm;bottom:3.5mm">{iso("width:4mm;height:4mm", BLA)}</span></div>'
       f'<div style="width:46mm;height:12mm;background:{PIE};display:flex;align-items:center;gap:3mm;padding:0 3.5mm"><svg viewBox="0 0 20 10" style="width:8mm"><path d="M0 5H18M14 1L18 5L14 9" fill="none" stroke="{NEG}" stroke-width="1"/></svg><span style="font-size:7pt">Salas de reunión</span></div></div>')
add(f'''{chh('33', 'Señalética', 'Fachada, recepción y salas')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm;margin-top:6mm">
 <div>{s1_}{lbl('Placa de entrada', 'Acero lacado negro mate (RAL 9005 de referencia) con el imagotipo vertical en blanco.')}</div>
 <div>{s2_}{lbl('Directorio', 'Panel negro, plantas en Plex Mono y destinos en Plex Sans Light.')}</div>
 <div>{s3_}{lbl('Salas y orientación', 'Placas negras con nombre en Light y flechas de trazo fino sobre Piedra.')}</div>
</div>''', '33 · Señalética', '33', 'Señalética')

badge = (f'<div style="display:flex;flex-direction:column;align-items:center"><div style="width:3mm;height:16mm;background:{NEG}"></div>'
         f'<div class="mk" style="width:44mm;height:68mm"><div style="height:14mm;background:{NEG};display:flex;align-items:center;padding:0 4mm">{horiz(BLA, BLA, "width:20mm;height:auto")}</div>'
         f'<div style="width:18mm;height:22mm;background:#E2E0DA;margin:5mm 4mm 0"></div><p style="font-size:7pt;font-weight:500;margin:3mm 4mm 0">Nombre Apellido</p><p class="m" style="font-size:4.4pt;color:{ACE};margin:1mm 4mm 0">Ingeniería · Acceso nivel 2</p>'
         f'<div style="position:absolute;left:4mm;right:4mm;bottom:4mm;height:5mm;background:repeating-linear-gradient(90deg,{NEG} 0 .4mm,transparent .4mm .9mm,{NEG} .9mm 1.6mm,transparent 1.6mm 2mm)"></div></div></div>')
nb = (f'<div style="width:52mm;height:74mm;background:{NEG};position:relative;box-shadow:1.2mm 1.2mm 0 #D8D6D0"><div style="position:absolute;left:0;top:0;bottom:0;width:3mm;background:#2A2B30"></div>'
      f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)">{iso("width:16mm;height:16mm", "#2C2D32")}</div><span class="m" style="position:absolute;left:7mm;bottom:5mm;font-size:4.2pt;color:#5A5C61">HALVEX</span></div>')
fold = (f'<div style="width:62mm;height:80mm;background:{GRAF};position:relative;box-shadow:1.2mm 1.2mm 0 #D8D6D0"><div style="position:absolute;left:6mm;top:6mm">{horiz(BLA, BLA, "width:24mm;height:auto")}</div>'
        f'<div style="position:absolute;left:0;right:0;bottom:0;height:22mm;background:{NEG}"></div><span class="m" style="position:absolute;left:6mm;bottom:8mm;font-size:4.2pt;color:{NIE}">Documentación confidencial</span></div>')
add(f'''{chh('34', 'Objetos <b>corporativos</b>', 'Acreditación, cuaderno y carpeta')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm;margin-top:6mm;align-items:end">
 <div style="display:flex;flex-direction:column;align-items:center"><div style="height:92mm;display:flex;align-items:flex-end">{badge}</div></div>
 <div style="display:flex;flex-direction:column;align-items:center"><div style="height:92mm;display:flex;align-items:flex-end">{nb}</div></div>
 <div style="display:flex;flex-direction:column;align-items:center"><div style="height:92mm;display:flex;align-items:flex-end">{fold}</div></div>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:6mm">{lbl('Acreditación', 'PVC blanco, cabecera negra, foto y nivel de acceso. Cinta negra lisa.')}{lbl('Cuaderno', 'Tapa negra con el isotipo en golpe en seco, sin tinta.')}{lbl('Carpeta', 'Grafito con imagotipo blanco y franja negra inferior.')}</div>''',
    '34 · Objetos corporativos', '34', 'Objetos corporativos')

ru = (f'<div style="width:36mm;height:92mm;background:{NEG};color:#fff;position:relative;box-shadow:0 2mm 0 #C9C7C1"><div style="position:absolute;left:0;right:0;top:9mm;display:flex;justify-content:center">{vert(BLA, BLA, "width:22mm;height:auto")}</div>'
      f'<p style="position:absolute;left:4mm;right:4mm;top:44mm;font-weight:200;font-size:9.5pt;letter-spacing:-.02em;line-height:1.1">Tecnología para decisiones que <b style="font-weight:400">no admiten error.</b></p>'
      f'<span class="m" style="position:absolute;left:4mm;bottom:5mm;font-size:4pt;color:{NIE}">halvex.com</span></div>')
rep = ''.join(f'<div style="display:flex;justify-content:{"flex-start" if r % 2 == 0 else "flex-end"};gap:12mm;padding:0 6mm">' + ''.join(horiz(NEG, NEG, "width:20mm;height:auto") for _ in range(4)) + '</div>' for r in range(5))
pc = f'<div style="width:150mm;height:92mm;background:{PIE};display:flex;flex-direction:column;justify-content:space-around;padding:4mm 0;box-shadow:inset 0 0 0 .25mm #C9C7C1">{rep}</div>'
add(f'''{chh('35', 'Eventos', 'Roll-up y photocall')}
<div style="display:grid;grid-template-columns:36mm 150mm 1fr;column-gap:10mm;margin-top:6mm;align-items:end">
 <div>{ru}{lbl('Roll-up', '85 × 200 cm. Imagotipo vertical arriba y una sola frase.')}</div>
 <div>{pc}{lbl('Photocall', 'Imagotipo repetido al tresbolillo sobre Piedra, sin más textos.')}</div>
 <div class="rows" style="align-self:start">
  <div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">Pantalla de escenario</span><span class="p" style="margin-top:1mm">Portada de presentación en grafito con el logotipo a todo el ancho.</span></div>
  <div class="row" style="grid-template-columns:1fr;padding:2.4mm 0"><span class="m s">Coorganización</span><span class="p" style="margin-top:1mm">Aplicar las normas de convivencia con otras marcas (capítulo 10).</span></div>
 </div>
</div>''', '35 · Eventos', '35', 'Eventos')

# Bien y mal
okp = p2.replace('width:50mm;height:50mm', 'width:40mm;height:40mm').replace('font-size:30pt', 'font-size:24pt')
kop = (f'<div class="mk" style="width:40mm;height:40mm;background:linear-gradient(135deg,#2456A6,#7B3FA0);color:#fff;padding:4mm;text-align:center">'
       f'<p style="font-size:9pt;font-weight:700;margin-top:4mm">¡¡NOVEDAD!! 🚀</p><p style="font-size:6pt;margin-top:2mm;font-family:Georgia,serif">La IA más revolucionaria del mercado</p>'
       f'<div style="position:absolute;left:50%;top:60%;transform:translate(-50%,-50%) scaleX(1.3)">{horiz("#FFD23F", "#FFD23F", "width:20mm;height:auto")}</div></div>')
oks = slide(64, f'''<div style="padding:4mm 5mm"><div style="display:flex;justify-content:space-between;border-bottom:.2mm solid {NEG};padding-bottom:1mm"><span class="m" style="font-size:3.6pt">HALVEX</span><span class="m" style="font-size:3.6pt">02 · Enfoque</span></div><p style="font-weight:200;font-size:20pt;letter-spacing:-.05em;line-height:.8;margin-top:4mm">02</p><p style="font-weight:200;font-size:8pt;letter-spacing:-.02em;margin-top:2mm">Tres fases, <b style="font-weight:400">un responsable.</b></p></div>''')
kos = slide(64, f'''<div style="padding:3mm 4mm;background:#fff"><p style="font-size:7pt;font-weight:700;text-align:center;text-decoration:underline">ENFOQUE DEL PROYECTO</p><div style="display:flex;gap:2mm;margin-top:2mm">{iso("width:8mm;height:8mm", "#2456A6")}<div style="flex:1">{bars([100, 100, 100, 100, 100, 100, 100, 100], "#9A9CA0", .7, .8)}</div></div><p style="font-family:Georgia,serif;font-size:5pt;margin-top:1mm">• Punto uno • Punto dos • Punto tres • Punto cuatro</p></div>''')
okc = f'<div class="mk" style="width:64mm;height:40mm;padding:4mm">{horiz(NEG, NEG, "width:26mm;height:auto")}<div style="position:absolute;left:5mm;bottom:5mm"><p style="font-size:8pt;font-weight:500">Nombre Apellido</p><p class="m" style="font-size:4.6pt;margin-top:2mm">nombre@halvex.com</p></div></div>'
koc = f'<div class="mk" style="width:64mm;height:40mm;padding:3mm;text-align:center"><div style="display:inline-block;transform:scaleY(1.5)">{horiz(NEG, "#7A7C80", "width:30mm;height:auto")}</div><p style="font-family:Georgia,serif;font-style:italic;font-size:8pt;margin-top:6mm">Nombre Apellido</p><p style="font-family:Courier,monospace;font-size:6pt;font-weight:700">NOMBRE@HALVEX.COM</p></div>'
pairs = [('Publicación en redes', okp, 'Una idea, una cifra, logo abajo a la izquierda.', kop, 'Degradado, emojis, exclamaciones, logo en color y deformado.'),
         ('Diapositiva', oks, 'Número grande, título en dos pesos, mucho aire.', kos, 'Texto centrado y subrayado, viñetas, otra tipografía.'),
         ('Tarjeta', okc, 'Imagotipo original y datos ordenados.', koc, 'Logo estirado y en dos tonos, tres tipografías.')]
pr_ = ''
for t, ok_, okd, ko_, kod in pairs:
    pr_ += (f'<div class="row" style="grid-template-columns:30mm 1fr 1fr;column-gap:8mm;align-items:center;padding:2.4mm 0"><span class="h4">{t}</span>'
            f'<div style="display:flex;gap:4mm;align-items:center">{ok_}<div><span class="ok">Así</span><p class="p s" style="margin-top:1mm;font-size:8pt">{okd}</p></div></div>'
            f'<div style="display:flex;gap:4mm;align-items:center">{ko_}<div><span class="ko">Así no</span><p class="p s" style="margin-top:1mm;font-size:8pt">{kod}</p></div></div></div>')
add(f'''{chh('36', 'Así sí, <b>así no</b>', 'Ejemplos comparados')}
<div class="rows" style="margin-top:4mm">{pr_}</div>''', '36 · Así sí, así no', '36', 'Así sí, así no')

# =================================================================== 07
divider('07', 'hq-banca', 'Los archivos de la marca, cuál usar en cada caso y cómo se gestiona.')
reuse(28, '37', 'Archivos del logo')

uses = [('Web: cabecera y pie', 'imagotipo-horizontal-negro.svg', 'SVG'), ('Favicon y app', 'favicon.ico · apple-touch-icon · android-192', 'ICO · PNG'),
        ('Word, PowerPoint, Keynote', 'imagotipo-horizontal-negro-1600px.png', 'PNG'), ('Diapositiva o fondo oscuro', 'imagotipo-horizontal-blanco-1600px.png', 'PNG'),
        ('Imprenta: tarjetas, cartas, carpetas', 'imagotipo-horizontal-negro.pdf', 'PDF vectorial'), ('Rotulación, vinilo, placas', 'imagotipo-vertical-negro.pdf / .svg', 'PDF · SVG'),
        ('Bordado y textil', 'isotipo-blanco.pdf + tamaño final', 'PDF'), ('Foto de perfil en redes', 'avatar-redes-negro-1080px.png', 'PNG'),
        ('Portada de LinkedIn / cabecera de X', 'portada-linkedin-1584x396 · cabecera-x-1500x500', 'PNG'), ('Firma de correo', 'firma-correo-240px.png', 'PNG'),
        ('Vídeo y rótulos', 'imagotipo-horizontal-blanco-4000px.png', 'PNG')]
uu = ''.join(f'<div class="row" style="grid-template-columns:62mm 1fr 30mm;padding:2.1mm 0"><span class="h4" style="font-size:8.8pt">{a}</span><span class="m" style="font-size:6.6pt;text-transform:none;letter-spacing:.02em">halvex-{b}</span><span class="p s">{c}</span></div>' for a, b, c in uses)
add(f'''{chh('38', 'Qué archivo <b>usar</b>', 'Guía rápida')}
<div class="g" style="margin-top:5mm">
 <div style="grid-column:1/9"><div class="row" style="grid-template-columns:62mm 1fr 30mm;border:0;padding:0 0 1.6mm"><span class="m s">Necesito el logo para…</span><span class="m s">Archivo</span><span class="m s">Formato</span></div><div class="rows">{uu}</div></div>
 <div style="grid-column:10/13">
  <p class="m s">Nombre de los archivos</p>
  <p style="font-family:'IBM Plex Mono';font-size:8pt;margin-top:3mm;line-height:1.7">halvex-<b style="font-weight:500">pieza</b>-<b style="font-weight:500">color</b>-<b style="font-weight:500">ancho</b>.png</p>
  <div class="rows" style="margin-top:3mm">
   <div class="row" style="grid-template-columns:16mm 1fr;padding:2mm 0"><span class="m s">Pieza</span><span class="p" style="font-size:8.4pt">imagotipo-horizontal, imagotipo-vertical, logotipo, isotipo</span></div>
   <div class="row" style="grid-template-columns:16mm 1fr;padding:2mm 0"><span class="m s">Color</span><span class="p" style="font-size:8.4pt">negro, blanco, negro-sobre-blanco, blanco-sobre-negro</span></div>
   <div class="row" style="grid-template-columns:16mm 1fr;padding:2mm 0"><span class="m s">Ancho</span><span class="p" style="font-size:8.4pt">en píxeles (solo PNG)</span></div>
  </div>
 </div>
</div>''', '38 · Qué archivo usar', '38', 'Qué archivo usar')

groups = [('Logo', ['Uso el archivo original, no una captura ni un redibujo.', 'La versión es la adecuada al formato.', 'Respeta el área de respeto (x).', 'Supera el tamaño mínimo.', 'Contrasta con el fondo: negro sobre claro, blanco sobre oscuro.']),
          ('Color y tipografía', ['Solo colores de la paleta.', 'Solo IBM Plex Sans y Plex Mono (o sus sustitutas).', 'Titulares en dos pesos; texto alineado a la izquierda.', 'Ortotipografía revisada: cifras, fechas, comillas.', 'Contraste AA como mínimo en todo el texto.']),
          ('Contenido e imagen', ['El tono es claro, exacto y sereno; trato de usted.', 'Fotos en blanco y negro, según el estilo de la marca.', 'Ninguna cifra sin verificar ni dato inventado.', 'Ningún cliente citado sin permiso por escrito.', 'Revisado por el responsable de marca.'])]
gg_ = ''.join(f'<div><div style="display:flex;align-items:baseline;gap:3mm;padding-bottom:2.4mm;border-bottom:.25mm solid #111214"><span class="m s">0{i+1}</span><span class="h3">{t}</span></div>' + ''.join(f'<div class="chk"><i></i><span class="p">{x}</span></div>' for x in xs) + '</div>' for i, (t, xs) in enumerate(groups))
add(f'''{chh('39', 'Lista <b>de comprobación</b>', 'Antes de publicar o imprimir')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);column-gap:8mm;margin-top:7mm">{gg_}</div>''', '39 · Lista de comprobación', '39', 'Lista de comprobación')

steps = [('01', 'Encargo', 'Quien necesita la pieza describe objetivo, público, formato y fecha.'), ('02', 'Propuesta', 'Diseño o texto siguiendo este manual y la lista de comprobación.'),
         ('03', 'Revisión', 'El responsable de marca revisa y devuelve comentarios.'), ('04', 'Aprobación', 'Se aprueba, se publica y se archiva la versión final.')]
st2 = ''.join(f'<div style="border-top:.6mm solid #111214;padding-top:3mm"><span class="m s">{a}</span><p style="font-weight:200;font-size:20pt;letter-spacing:-.03em;margin-top:2mm">{b}</p><p class="p" style="margin-top:2mm">{c}</p></div>' for a, b, c in steps)
add(f'''{chh('40', 'Gestión <b>de la marca</b>', 'Aprobaciones y versiones')}
<div style="display:grid;grid-template-columns:repeat(4,1fr);column-gap:7mm;margin-top:8mm">{st2}</div>
<div class="g" style="margin-top:10mm">
 <div style="grid-column:1/7" class="rows">
  <div class="row" style="grid-template-columns:44mm 1fr;padding:2.6mm 0"><span class="m s">Responsable de marca</span><span class="p">[Nombre y apellidos] · [cargo] · [correo]</span></div>
  <div class="row" style="grid-template-columns:44mm 1fr;padding:2.6mm 0"><span class="m s">Archivos de la marca</span><span class="p">[Carpeta compartida]/HALVEX-logos</span></div>
  <div class="row" style="grid-template-columns:44mm 1fr;padding:2.6mm 0"><span class="m s">Documentos de referencia</span><span class="p">01 Plataforma de marca · 02 Identidad visual · 03 Manual corporativo</span></div>
 </div>
 <div style="grid-column:8/13">
  <p class="m s">Control de versiones</p>
  <div class="rows" style="margin-top:2mm"><div class="row" style="grid-template-columns:18mm 34mm 1fr;padding:2.4mm 0"><span class="m">1.0</span><span class="p">Noviembre 2026</span><span class="p">Primera edición.</span></div>
  <div class="row" style="grid-template-columns:18mm 34mm 1fr;padding:2.4mm 0"><span class="m s">—</span><span class="p s">—</span><span class="p s">Próximas revisiones.</span></div></div>
 </div>
</div>''', '40 · Gestión de la marca', '40', 'Gestión de la marca')

# =================================================================== ENSAMBLAJE
cur['part'] = ''
cover = f'''<section class="page" style="padding:0">
<div style="position:absolute;left:0;top:0;bottom:0;width:52%;background:{NEG};color:#fff;padding:14mm 18mm">
 <div class="m" style="display:flex;justify-content:space-between"><b style="font-weight:500">HALVEX</b><span>Documento 03</span></div>
 <p class="m" style="color:{NIE};margin-top:34mm">Manual corporativo</p>
 <h1 class="d1" style="font-size:60pt;margin-top:5mm">Manual<br><b>corporativo</b></h1>
 <p class="lead" style="margin-top:7mm;color:#C9CACD;max-width:105mm;font-size:11.5pt">Identidad visual, normas de uso del logo, códigos de color, normas tipográficas, aplicaciones y ejemplos.</p>
 <div class="m" style="position:absolute;left:18mm;right:14mm;bottom:14mm;border-top:.25mm solid rgba(255,255,255,.5);padding-top:2.6mm;display:flex;justify-content:space-between"><span>Edición 1.0 · Noviembre 2026</span><span style="color:{NIE}">40 capítulos</span></div>
</div>
<div style="position:absolute;left:52%;right:0;top:0;bottom:0;background:{PIE};display:flex;flex-direction:column;align-items:center;justify-content:center">
 <div style="width:104mm">{plan}</div>
 <p class="m s" style="margin-top:6mm">Isotipo · construcción</p>
</div></section>'''

intro = f'''<section class="page">{run('Presentación').replace('<span></span>', '<span></span>')}
<div class="g" style="margin-top:12mm">
 <p class="m s" style="grid-column:1/3">Presentación</p>
 <h2 class="d1" style="grid-column:3/11;font-size:36pt">Una marca se construye <b>con coherencia.</b></h2>
</div>
<div class="g" style="margin-top:10mm">
 <div style="grid-column:3/7">
  <p class="p">Este manual reúne todas las normas para aplicar la marca HALVEX: cómo es, cómo se usa el logo, qué colores y tipografías la forman y cómo se ve en cada soporte, con ejemplos.</p>
  <p class="p">Está pensado para el equipo de HALVEX y para cualquier agencia, imprenta, proveedor o socio que trabaje con la marca. Si una situación no está prevista aquí, se consulta al responsable de marca antes de publicar.</p>
  <div style="margin-top:7mm;display:flex;align-items:center;gap:5mm">{horiz(NEG, NEG, 'width:42mm;height:auto')}</div>
 </div>
 <div class="rows" style="grid-column:8/13">
  {''.join(f'<div class="row" style="grid-template-columns:10mm 46mm 1fr;padding:2.4mm 0"><span class="m s">{k}</span><span class="h4" style="font-size:9pt">{v}</span><span class="p s" style="font-size:8pt">{d}</span></div>' for (k, v), d in zip(PARTS.items(), ['Los elementos de la marca', 'Cómo se usa el logo', 'Colores y sus códigos', 'Familias, tamaños y reglas', 'Retícula, iconos e imagen', 'La marca en cada soporte', 'Archivos y gestión']))}
 </div>
</div>{FOL}</section>'''

one = f'''<section class="page st">{run('La marca en una página')}
<div class="g" style="margin-top:10mm">
 <p class="m s" style="grid-column:1/3">La marca en una página</p>
 <div style="grid-column:3/13;display:grid;grid-template-columns:repeat(3,1fr);column-gap:7mm;row-gap:7mm">
  <div class="r" style="grid-column:1/3;padding-top:3mm"><p class="m s">Promesa</p><p class="d1" style="font-size:28pt;margin-top:2mm">Tecnología para decisiones que <b>no admiten error.</b></p></div>
  <div class="r" style="padding-top:3mm"><p class="m s">Lema interno</p><p class="d2" style="font-size:16pt;margin-top:2mm">Mirar con amplitud. <b>Actuar con precisión.</b></p></div>
  <div class="r" style="padding-top:3mm"><p class="m s">Qué somos</p><p class="p" style="margin-top:2mm">Una compañía tecnológica de inteligencia artificial, sistemas de seguridad y software para defensa, instituciones y grandes empresas.</p></div>
  <div class="r" style="padding-top:3mm"><p class="m s">Valores</p><p class="p" style="margin-top:2mm">Rigor · Discreción · Soberanía · Responsabilidad · Exclusividad · Innovación útil</p></div>
  <div class="r" style="padding-top:3mm"><p class="m s">Personalidad y voz</p><p class="p" style="margin-top:2mm">Sobria, precisa, discreta y serena. Clara, exacta y de usted.</p></div>
 </div>
</div>
<p class="m s" style="position:absolute;left:18mm;bottom:20mm;text-transform:none;letter-spacing:.02em">El desarrollo completo está en el documento 01 · Plataforma de marca.</p>{FOL}</section>'''

# Construye la lista final con folios
final = [cover, None, intro, one]
for p in PAGES:
    final.append(p)
final.append(f'''<section class="page dk" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
{vert(BLA, BLA, 'width:60mm;height:auto')}
<div style="position:absolute;left:18mm;right:18mm;bottom:13mm;display:flex;justify-content:space-between;border-top:.25mm solid rgba(255,255,255,.4);padding-top:2.6mm" class="m"><span>HALVEX · Manual corporativo · Edición 1.0</span><span style="color:#A3A4A8">contacto@halvex.com</span></div></section>''')

OFF = 4  # páginas antes de PAGES
pageno = lambda i: i + OFF + 1
# divisores: capítulos por parte
chap_by_part = {}
for part, num, title, idx in TOCI:
    chap_by_part.setdefault(part, []).append((num, title, pageno(idx)))
for i, p in enumerate(final):
    if isinstance(p, tuple):
        _, part, photo, intro_, pos = p
        items = chap_by_part.get(part, [])
        it = ''.join(f'<div class="row" style="grid-template-columns:10mm 1fr 8mm;padding:2mm 0"><span class="m s">{a}</span><span style="font-size:10pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
        final[i] = f'''<section class="page dk" style="padding:0">
<div class="photo" style="position:absolute;left:0;top:0;bottom:0;width:50%;background-image:url({img64(photo)});background-position:{pos}"></div>
<div style="position:absolute;left:50%;right:0;top:0;bottom:0;padding:14mm 18mm 0 14mm">
 <div class="m" style="display:flex;justify-content:space-between;border-bottom:.25mm solid rgba(255,255,255,.6);padding-bottom:2.4mm"><span>Parte {part}</span><span class="s">{i+1:02d}</span></div>
 <p style="font-weight:200;font-size:120pt;line-height:.8;letter-spacing:-.06em;margin-top:12mm">{part}</p>
 <h2 class="d1" style="font-size:34pt;margin-top:7mm">{PARTS[part]}</h2>
 <p class="lead" style="margin-top:4mm;color:#C9CACD;max-width:100mm;font-size:11pt">{intro_}</p>
 <div class="rows" style="position:absolute;left:14mm;right:18mm;bottom:14mm">{it}</div>
</div></section>'''

# Índice
cols = ''
for part, name in PARTS.items():
    items = chap_by_part.get(part, [])
    it = ''.join(f'<div class="row" style="grid-template-columns:7mm 1fr 7mm;padding:1.05mm 0"><span class="m s">{a}</span><span style="font-size:7.8pt;font-weight:300">{b}</span><span class="m s" style="text-align:right">{c:02d}</span></div>' for a, b, c in items)
    cols += f'<div><div style="display:flex;align-items:baseline;gap:2.6mm;padding-bottom:1.6mm"><span style="font-weight:200;font-size:17pt;letter-spacing:-.04em;line-height:1">{part}</span><span class="h4">{name}</span></div><div class="rows">{it}</div></div>'
final[1] = f'''<section class="page">{run('Contenido')}
<div class="g" style="margin-top:8mm">
 <div style="grid-column:1/4"><h2 class="d1" style="font-size:38pt">Contenido</h2><p class="p s" style="margin-top:5mm">Siete partes y cuarenta capítulos.</p>
  <div class="rows" style="margin-top:6mm"><div class="row" style="grid-template-columns:7mm 1fr 7mm;padding:1.4mm 0"><span class="m s">·</span><span style="font-size:8.4pt;font-weight:300">Presentación</span><span class="m s">03</span></div><div class="row" style="grid-template-columns:7mm 1fr 7mm;padding:1.4mm 0"><span class="m s">·</span><span style="font-size:8.4pt;font-weight:300">La marca en una página</span><span class="m s">04</span></div></div></div>
 <div style="grid-column:4/13;display:grid;grid-template-columns:repeat(4,1fr);column-gap:6mm;row-gap:6mm">{cols}</div>
</div>{FOL}</section>'''

for i in range(len(final)):
    final[i] = final[i].replace('%%N%%', f'{i+1:02d}')

html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>HALVEX · Manual corporativo</title><style>{CSS}</style></head><body>{C.DEFS}' + ''.join(final) + '</body></html>')
open(os.path.join(HERE, 'manual.html'), 'w').write(html)
print(len(final), 'páginas')

# HALVEX

Identidad de marca y web de HALVEX: inteligencia artificial, sistemas de seguridad y software para decisiones que no admiten error.

## Contenido

| Carpeta | Qué hay |
|---|---|
| `web/` | La web (HTML, CSS y JS en un solo `index.html`, más imágenes). Es lo que se publica en Vercel. |
| `marca/` | Documentos de marca: plataforma de marca, identidad visual, manual corporativo y material corporativo (PDF). |
| `marca/exploraciones/` | Exploraciones previas de isotipo, color y símbolos. |
| `logos/` | Archivos del logo: imagotipo horizontal y vertical, logotipo, isotipo (SVG, PDF y PNG) e iconos y redes. Ver `logos/LEEME.txt`. |
| `renders/` | Renders 3D: gorras, papelería, tarjetas y el isotipo como escultura. |
| `video/` | Piezas de vídeo de presentación. |
| `herramientas/` | Scripts que generan los PDF (Python + Playwright) y los renders 3D (Blender `bpy`). |

## Web

Página estática, sin dependencias de compilación. Para verla en local:

```bash
cd web
python3 -m http.server 8000
# http://localhost:8000
```

- Tipografía: sistema de Apple (SF Pro) con Inter como alternativa.
- Hero en 3D con three.js 0.160 (CDN).
- Desplazamiento suave con Lenis 1.1.13 (CDN); si no carga, la web funciona con el scroll nativo.
- Respeta `prefers-reduced-motion`.
- El formulario de contacto es de maqueta: valida, pero no envía.

## Hero · «La linterna»

Todo empieza a oscuras: el isotipo de titanio liso está ahí, pero no se ve. El cursor es una luz que lo va descubriendo por sus reflejos (un círculo en pantalla que enciende el metal, una luz puntual para los brillos y un halo tenue sobre la pared del fondo); la pieza se inclina un poco hacia la luz. Si nadie mueve el ratón, o en pantallas táctiles, la luz pasea sola sobre el isotipo. El titular entra cuando se enciende la luz (unos 1,7 s tras la apertura). Con el scroll, la luz se abre hasta descubrir la pieza entera y entra «Precisión. Sin margen.». three.js 0.160 sin compilación, iluminación de estudio propia (paneles de luz en un PMREM) y resplandor con UnrealBloomPass. Si el dispositivo no tiene WebGL o pide movimiento reducido, se muestra `img/hero-poster.jpg`.

## Lenguaje de movimiento

- **La firma: las dos mitades.** El isotipo son dos cuñas; el movimiento de la marca es que se separan. Aparece en la apertura (el isotipo se traza, se abre un instante y vuela a la navegación), al final del hero (las dos cuñas de titanio se separan y queda una sola línea de luz: «Precisión. Sin margen.») y en el logotipo de la navegación al pasar el cursor.
- **Navegación por corte.** Los enlaces del menú no recorren la página: un velo de 0,2 s tapa el salto y la sección de destino aparece ya resuelta. Las animaciones solo se reproducen al hacer scroll.
- **Por qué HALVEX · despiece.** El isotipo se abre en cinco capas, como la ficha técnica de un producto, y cada capa es un compromiso con su etiqueta: carcasa de una sola pieza de titanio (un solo equipo), junta de sellado (su perímetro), núcleo de cristal negro con un único punto de luz en el vértice (una persona decide), estructura en celosía (probado a fondo) y base negra sin marcas (discreción). La capa activa se adelanta y se ilumina; en móvil la cámara la sigue como un carrusel. Al final las capas se cierran y vuelve a ser una sola pieza.
- **Sectores:** carrusel de tarjetas con fotografía.
- **Compañía · desde dentro de la letra.** La sección empieza con una fotografía a pantalla completa; al bajar, la cámara se aleja y resulta que era el interior de la «t» de «crítico»: la foto queda solo dentro de «Menos proyectos.» y debajo sube «Más precisión.».
- **Hablemos · el cierre.** Las dos cuñas de titanio que se separaron al final del hero vuelven desde los lados; la línea de luz se acorta hasta desaparecer, destello en el vértice al unirse, y «Hablemos.» entra letra a letra desde el desenfoque.
- Titulares con líneas que suben desde una máscara; barra de progreso bajo la navegación y subrayado en la sección activa.
- Fotografía en blanco y negro (`img/x-*.jpg`, con recorte vertical `-m` para móvil), de Unsplash y provisional.

La secuencia renderizada del hero anterior («Punto de vista») sigue en el historial de git y su generador en `herramientas/3d/secuencia.py`.

## Despliegue

Vercel sirve la carpeta `web/` como sitio estático (directorio raíz del proyecto: `web`).

## Regenerar los PDF

```bash
cd herramientas/pdf
python3 plataforma2.py && node pdf.js "$PWD/plataforma2.html" "$PWD/HALVEX-plataforma-de-marca.pdf"
```

Requiere Python 3 con Pillow y Node con Playwright. Los renders 3D usan `bpy==4.2.0` (Python 3.11).

## Pendiente

- Fotografías propias (las de la web y las portadillas son de Unsplash, provisionales).
- Correo, dirección y datos legales reales; envío del formulario.
- Denominación social y registro de la marca.

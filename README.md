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

## Hero · «Titanio»

El isotipo es un objeto 3D en tiempo real (three.js 0.160, sin compilación): dos cuñas de titanio pulido que aparecen de canto, como una línea de luz, giran hasta revelarse, siguen al cursor y se colocan de frente con el scroll. Si el dispositivo no tiene WebGL o pide movimiento reducido, se muestra `img/hero-poster.jpg`.

Tipografía: la del sistema de Apple (SF Pro en Mac, iPhone e iPad) con Inter (Google Fonts) como equivalente en el resto.

## Lenguaje de movimiento

- **La firma: las dos mitades.** El isotipo son dos cuñas; el movimiento de la marca es que se separan. Aparece en la apertura (el isotipo se traza, se abre un instante y vuela a la navegación), al final del hero (las dos cuñas de titanio se separan y queda una sola línea de luz: «Precisión. Sin margen.»), en «Despliegue soberano» (la fotografía se ve a través del isotipo y las dos cuñas se abren hasta ser las dos mitades de la pantalla) y en el logotipo de la navegación al pasar el cursor.
- **Navegación por corte.** Los enlaces del menú no recorren la página: un velo de 0,2 s tapa el salto y la sección de destino aparece ya resuelta. Las animaciones solo se reproducen al hacer scroll.
- **Por qué HALVEX · un universo que se ordena.** 15.000 partículas de luz en 3D (three.js; 7.000 en móvil). La galaxia inicial se reorganiza en una estructura matemática por compromiso: un atractor de Aizawa (un solo equipo), una cúpula geodésica con datos en órbitas de Lissajous dentro (su perímetro), las líneas de campo de un dipolo que convergen en un punto (una persona decide), la fibración de Hopf (rigor) y un agujero negro con disco kepleriano y anillo de luz (discreción); al final, el isotipo. Entre formaciones la cámara orbita y las partículas viajan en ola; el texto entra desde el desenfoque.
- **Sectores:** carrusel de tarjetas con fotografía.
- **Compañía · desde dentro de la letra.** La sección empieza con una fotografía a pantalla completa; al bajar, la cámara se aleja y resulta que era el interior de la «t» de «proyectos»: la foto queda solo dentro de «Menos proyectos.» y debajo sube «Más precisión.».
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

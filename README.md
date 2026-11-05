# HALVEX

Identidad de marca y web de HALVEX: inteligencia artificial, sistemas de seguridad y software para decisiones que no admiten error.

## Contenido

| Carpeta | Qué hay |
|---|---|
| `web/` | La web (HTML, CSS y JS en un solo `index.html`, imágenes y `seq/`, la secuencia 3D del hero). Es lo que se publica en Vercel. |
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

- Tipografía: IBM Plex Sans, Plex Serif y Plex Mono (Google Fonts).
- Desplazamiento suave con Lenis 1.1.13 (CDN); si no carga, la web funciona con el scroll nativo.
- Respeta `prefers-reduced-motion`.
- El formulario de contacto es de maqueta: valida, pero no envía.

## Hero · «Punto de vista»

Las dos cuñas del isotipo son esculturas separadas en el espacio, a distinta profundidad. Desde cualquier ángulo parecen dos piezas sin relación; solo desde un punto exacto se alinean y forman el isotipo. El scroll mueve la cámara hasta ese punto (60 fotogramas en `web/seq/`, renderizados con `herramientas/3d/secuencia.py`); al alinearse, el render se convierte en el símbolo y se atraviesa el vacío entre las cuñas hacia el contenido. `herramientas/3d/iso.json` guarda la posición exacta del isotipo en el último fotograma, que la web usa para superponer el SVG.

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

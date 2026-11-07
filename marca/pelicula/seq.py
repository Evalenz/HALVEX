# Convierte los fotogramas del render en la secuencia de la web: 145 WebP (pares + el último).
# Uso: python3 seq.py SRC OUT ANCHO ALTO CALIDAD
import sys, os
from PIL import Image
src, out, W, H, Q = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
os.makedirs(out, exist_ok=True)
idx = list(range(0, 288, 2)) + [287]
tot = 0
for i, f in enumerate(idx):
    im = Image.open(os.path.join(src, f'f{f:04d}.png')).convert('RGB')
    if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
    p = os.path.join(out, f'{i:03d}.webp'); im.save(p, 'WEBP', quality=Q, method=6)
    tot += os.path.getsize(p)
print(len(idx), 'fotogramas', round(tot / 1e6, 2), 'MB')

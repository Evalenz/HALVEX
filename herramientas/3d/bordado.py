"""Genera el mapa de alturas del isotipo bordado (puntada de satén) y su máscara."""
import numpy as np, sys
from PIL import Image, ImageDraw
from scipy import ndimage

N = 2048
K = 1600 / 152          # px por unidad del isotipo
STITCH_MM = 0.42
SIZE_M = 0.064          # el lienzo cubre 64 mm
PX_MM = N / (SIZE_M * 1000)

L = [(24, 20), (60, 20), (96.2, 172)]
R = [(176, 20), (140, 20), (103.8, 172)]


def P(pt):
    return (N / 2 + (pt[0] - 100) * K, N / 2 + (pt[1] - 96) * K)


def wedge(poly, mouth_a, mouth_b, tip):
    im = Image.new('L', (N, N), 0)
    ImageDraw.Draw(im).polygon([P(p) for p in poly], fill=255)
    m = np.array(im) > 0
    d = ndimage.distance_transform_edt(m)
    edge = 0.55 * PX_MM
    prof = np.sin(np.clip(d / edge, 0, 1) * np.pi / 2)
    # eje de la cuña: del centro de la boca a la punta; la puntada cruza la cuña
    a = np.array(P(((mouth_a[0] + mouth_b[0]) / 2, (mouth_a[1] + mouth_b[1]) / 2)))
    b = np.array(P(tip))
    ax = (b - a) / np.linalg.norm(b - a)
    yy, xx = np.mgrid[0:N, 0:N]
    t = (xx - a[0]) * ax[0] + (yy - a[1]) * ax[1]
    period = STITCH_MM * PX_MM
    ridge = 0.5 + 0.5 * np.cos(2 * np.pi * t / period)
    ridge = ridge ** 0.6
    h = prof * (0.78 + 0.22 * ridge)
    return h, m


hl, ml = wedge(L, L[0], L[1], L[2])
hr, mr = wedge(R, R[0], R[1], R[2])
h = np.maximum(hl, hr)
m = (ml | mr).astype(np.float32)
m = ndimage.gaussian_filter(m, 1.2)
Image.fromarray((h * 65535).astype(np.uint16)).save(sys.argv[1])
Image.fromarray((m * 255).astype(np.uint8)).save(sys.argv[2])
print('ok', h.max())

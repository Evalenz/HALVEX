"""Secuencia del hero «Punto de vista».

Las dos cuñas del isotipo son esculturas a distinta profundidad. Solo desde un punto exacto
(la cámara final) se alinean y proyectan el isotipo perfecto. La cámara viaja desde un ángulo
oblicuo y cercano hasta ese punto. Se exportan los fotogramas y la posición del isotipo en la
imagen final para alinear el SVG en la web.

Uso: python secuencia.py -- '{"out":"frames","res":1080,"samples":24,"frames":72}'
"""
import bpy, bmesh, math, sys, json, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

A = json.loads(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else {}
OUT = os.path.abspath(A.get('out', 'frames'))
RES = A.get('res', 1080)
NF = A.get('frames', 72)
ONLY = A.get('only')            # lista de fotogramas para pruebas
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = A.get('samples', 24); sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.render.resolution_x = sc.render.resolution_y = RES
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - High Contrast'
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 84
sc.frame_start, sc.frame_end = 1, NF

H = 1.6; S = H / 152
CAM_D = 6.2; CAM_Z = 1.0          # punto de vista exacto
DEPTH = {'L': -1.2, 'R': 1.4}     # desplazamiento en profundidad de cada cuña
THK = 0.20


def logo_pt(x, y):
    return (x - 100) * S, CAM_Z + (96 - y) * S


metal = bpy.data.materials.new('metal'); metal.use_nodes = True
b = metal.node_tree.nodes['Principled BSDF']
b.inputs['Base Color'].default_value = (0.03, 0.03, 0.033, 1)
b.inputs['Metallic'].default_value = 0.55
b.inputs['Roughness'].default_value = 0.3

WEDGES = {'L': [(24, 20), (60, 20), (96.2, 172)], 'R': [(176, 20), (140, 20), (103.8, 172)]}
front_pts = {}
WC = bpy.data.collections.new('cunas'); sc.collection.children.link(WC)
for side, pts in WEDGES.items():
    yoff = DEPTH[side]; d = CAM_D + yoff; k = d / CAM_D
    fp = []
    for p in pts:
        X, Z = logo_pt(*p)
        fp.append(Vector((X * k, yoff, CAM_Z + (Z - CAM_Z) * k)))
    front_pts[side] = fp
    bm = bmesh.new()
    f = [bm.verts.new(v) for v in fp]
    bk = [bm.verts.new(v + Vector((0, THK * k, 0))) for v in fp]
    bm.faces.new(f); bm.faces.new(list(reversed(bk)))
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((f[i], bk[i], bk[j], f[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(side); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(side, me); WC.objects.link(o)
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.004; bv.segments = 3
    o.data.materials.append(metal)

# suelo
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
fl = bpy.context.object
fm = bpy.data.materials.new('suelo'); fm.use_nodes = True
N = fm.node_tree.nodes; L = fm.node_tree.links
fb = N['Principled BSDF']; fb.inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1); fb.inputs['Specular IOR Level'].default_value = 0.5
nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 6
mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.3; mr.inputs['To Max'].default_value = 0.5
L.new(nz.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs[0], fb.inputs['Roughness'])
fl.data.materials.append(fm)

# rendija de luz detrás del vértice (en el eje del punto de vista)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 9.0, 0.5), rotation=(math.radians(90), 0, 0))
st = bpy.context.object; st.scale = (0.035, 1.0, 1)
em = bpy.data.materials.new('em'); em.use_nodes = True
en = em.node_tree.nodes; en.clear()
e = en.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1, 0.97, 0.92, 1); e.inputs['Strength'].default_value = 30
oo = en.new('ShaderNodeOutputMaterial'); em.node_tree.links.new(e.outputs[0], oo.inputs[0]); st.data.materials.append(em)


def area(name, loc, size, energy, tgt, sy=None, spread=180):
    ld = bpy.data.lights.new(name, 'AREA'); ld.shape = 'RECTANGLE'; ld.size = size; ld.size_y = sy or size
    ld.energy = energy; ld.spread = math.radians(spread)
    ob = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    ob.light_linking.receiver_collection = WC
    return ld


rimL = area('rimL', (-3.0, 0.4, 1.9), 0.15, 260, (0, 0, 1.2), 2.8, 35)
rimR = area('rimR', (3.0, 2.2, 1.9), 0.15, 260, (0, 1.4, 1.2), 2.8, 35)
top = area('top', (0, 0.2, 4.0), 1.4, 30, (0, 0.2, 1.0), 0.5, 40)

# caja de luz frontal (no la ve la cámara): da lectura a las caras
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -11, 1.4), rotation=(math.radians(90), 0, 0))
sb = bpy.context.object; sb.scale = (9, 3, 1); sb.visible_camera = False
sb.light_linking.receiver_collection = WC
sm = bpy.data.materials.new('sb'); sm.use_nodes = True; sn = sm.node_tree.nodes; sn.clear()
se = sn.new('ShaderNodeEmission'); se.inputs['Strength'].default_value = 2.4
so = sn.new('ShaderNodeOutputMaterial'); sm.node_tree.links.new(se.outputs[0], so.inputs[0]); sb.data.materials.append(sm)

world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)

cd = bpy.data.cameras.new('cam'); cd.lens = 40; cd.sensor_fit = 'HORIZONTAL'
cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new('tgt', None); bpy.context.collection.objects.link(tgt)
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'


def ease(t):
    return t * t * (3 - 2 * t)


def smoother(t):
    return t * t * t * (t * (6 * t - 15) + 10)


def cam_at(t):
    """t en [0,1]: de oblicuo y cercano al punto de vista exacto."""
    m = smoother(min(1.0, t / 0.88))
    th = math.radians(46) * (1 - m)            # ángulo alrededor del eje vertical
    r = 4.6 + (CAM_D - 4.6) * m                # distancia
    h = 0.55 + (CAM_Z - 0.55) * m              # altura de cámara
    piv = Vector((0.0, 0.0, 0.0))
    loc = Vector((r * math.sin(th), -r * math.cos(th), h)) + piv
    look = Vector((0.0, 0.6 * (1 - m), 0.9 + (CAM_Z - 0.9) * m))
    return loc, look


def lights_at(t):
    a = 0.12 + 0.88 * ease(min(1.0, t / 0.35))
    rimL.energy = 260 * a; rimR.energy = 260 * a
    top.energy = 30 * ease(min(1.0, max(0.0, (t - 0.1) / 0.5)))
    se.inputs['Strength'].default_value = 0.4 + 2.0 * ease(min(1.0, t / 0.6))


frames = ONLY or list(range(NF))
for i in frames:
    t = i / (NF - 1)
    loc, look = cam_at(t)
    cam.location = loc; tgt.location = look
    lights_at(t)
    sc.render.filepath = os.path.join(OUT, f'f{i:03d}.jpg')
    bpy.ops.render.render(write_still=True)
    print('FRAME', i, flush=True)

# posición del isotipo en la imagen final (coordenadas normalizadas, origen arriba a la izquierda)
loc, look = cam_at(1.0); cam.location = loc; tgt.location = look
bpy.context.view_layer.update()
pts = {}
for side, fp in front_pts.items():
    pts[side] = []
    for v in fp:
        c = world_to_camera_view(sc, cam, v)
        pts[side].append([round(c.x, 5), round(1 - c.y, 5)])
json.dump({'frames': NF, 'res': RES, 'iso': pts}, open(os.path.join(OUT, 'iso.json'), 'w'), indent=1)
print('ISO', json.dumps(pts))

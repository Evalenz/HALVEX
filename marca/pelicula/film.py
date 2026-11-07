# Película de producto del isotipo HALVEX en titanio liso (Blender / Cycles).
# Uso: python film.py OUT_DIR FRAMES(ej. 0-287 o 10,80,150) ESCALA_RES SAMPLES
import bpy, math, sys, os
from mathutils import Vector

OUT, FR, RES, SPP = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
FPS = 24
SHOTS = [72, 60, 60, 96]          # 3 s · 2,5 s · 2,5 s · 4 s  = 288 fotogramas
START = [sum(SHOTS[:i]) for i in range(4)]
TOTAL = sum(SHOTS)

def cl(v, a, b): return a if v < a else b if v > b else v
def sg(v, a, b): return cl((v - a) / (b - a), 0, 1)
def lerp(a, b, t): return a + (b - a) * t
def eio(t): return 4 * t * t * t if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def L3(a, b, t): return Vector([lerp(a[i], b[i], t) for i in range(3)])

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SPP
sc.cycles.use_denoising = True
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.transmission_bounces = 0
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.cycles.blur_glossy = 0.5
sc.render.resolution_x = int(1920 * RES); sc.render.resolution_y = int(1080 * RES); sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'
sc.render.film_transparent = False
try:
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Punchy'
except Exception:
    sc.view_settings.view_transform = 'Filmic'
sc.view_settings.exposure = 0.0
w = bpy.data.worlds.new('negro'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1); sc.world = w

# ---------- el isotipo: dos cuñas de 0,2 de grosor con bisel ----------
def P(x, y): return ((x - 100) / 152, (96 - y) / 152)
LT = [(24, 20), (60, 20), (96.2, 172)]; RT = [(176, 20), (140, 20), (103.8, 172)]
def wedge(name, T):
    pts = [P(*p) for p in T]
    verts = [(x, -0.1, z) for x, z in pts] + [(x, 0.1, z) for x, z in pts]
    # cara frontal mirando a -Y (hacia la cámara)
    a = [0, 1, 2]
    n = Vector(verts[1]) - Vector(verts[0]); m = Vector(verts[2]) - Vector(verts[0])
    if n.cross(m).y > 0: a = [0, 2, 1]
    faces = [a, [i + 3 for i in reversed(a)]]
    for i in range(3):
        j = (i + 1) % 3; faces.append([i, j, j + 3, i + 3])
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.validate();
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob)
    bv = ob.modifiers.new('bisel', 'BEVEL'); bv.width = 0.012; bv.segments = 6; bv.limit_method = 'ANGLE'; bv.harden_normals = True
    for p in me.polygons: p.use_smooth = True
    return ob

ti = bpy.data.materials.new('titanio'); ti.use_nodes = True
b = ti.node_tree.nodes['Principled BSDF']
b.inputs['Base Color'].default_value = (0.60, 0.585, 0.555, 1)
b.inputs['Metallic'].default_value = 1.0
b.inputs['Roughness'].default_value = 0.14
try:
    b.inputs['Coat Weight'].default_value = 0.4; b.inputs['Coat Roughness'].default_value = 0.04
except Exception: pass
iso = bpy.data.objects.new('iso', None); sc.collection.objects.link(iso)
for nm, T in (('izq', LT), ('der', RT)):
    o = wedge(nm, T); o.data.materials.append(ti); o.parent = iso

# ---------- suelo negro brillante (plano final) ----------
fl = bpy.data.meshes.new('suelo'); s = 30
fl.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [[0, 1, 2, 3]])
floor = bpy.data.objects.new('suelo', fl); sc.collection.objects.link(floor); floor.location.z = -0.62
fm = bpy.data.materials.new('suelo'); fm.use_nodes = True; fb = fm.node_tree.nodes['Principled BSDF']
fb.inputs['Base Color'].default_value = (0.004, 0.004, 0.004, 1); fb.inputs['Roughness'].default_value = 0.12
nt = fm.node_tree
tc = nt.nodes.new('ShaderNodeTexCoord'); gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'
mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.62, 0.62, 0.62)
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[1].position = 0.55
nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs[0], gr.inputs['Vector']); nt.links.new(gr.outputs['Fac'], cr.inputs['Fac'])
mx = nt.nodes.new('ShaderNodeMixShader'); dk = nt.nodes.new('ShaderNodeBsdfDiffuse'); dk.inputs['Color'].default_value = (0, 0, 0, 1)
out = nt.nodes['Material Output']; nt.links.new(cr.outputs['Color'], mx.inputs['Fac']); nt.links.new(dk.outputs[0], mx.inputs[1]); nt.links.new(fb.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])
fl.materials.append(fm)

# ---------- estudio: planos de luz que se ven en los reflejos ----------
def panel(name, w_, h_, loc, target, strength):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-w_/2, -h_/2, 0), (w_/2, -h_/2, 0), (w_/2, h_/2, 0), (-w_/2, h_/2, 0)], [], [[0, 1, 2, 3]])
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.location = loc
    d = (Vector(target) - Vector(loc)).normalized(); ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    out = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], out.inputs[0])
    me.materials.append(m)
    ob.visible_camera = False      # se ven en el metal, no en cámara
    return ob, em
top, eTop = panel('arriba', 5, 5, (0, -0.6, 3.2), (0, 0, 0), 3.5)
front, eFront = panel('frente', 7, 1.6, (0, -4.5, 1.6), (0, 0, 0), 2.6)
sideL, eSL = panel('lateral_i', .35, 6, (-3.2, -1.2, .4), (0, 0, 0), 10)
sideR, eSR = panel('lateral_d', .25, 6, (3.0, -0.6, .6), (0, 0, 0), 12)
back, eBack = panel('contra', 6, .3, (0, 3.2, 1.4), (0, 0, 0), 14)
sweep, eSw = panel('barrido', .18, 7, (0, -3, .5), (0, 0, 0), 0)

cam_d = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.sensor_fit = 'HORIZONTAL'; cam_d.sensor_width = 36; cam_d.clip_start = 0.01; cam_d.dof.use_dof = True
foc = bpy.data.objects.new('foco', None); sc.collection.objects.link(foc); cam_d.dof.focus_object = foc

def look(loc, tgt, lens, fstop, roll=0.0):
    cam.location = Vector(loc); foc.location = Vector(tgt)
    d = (Vector(tgt) - Vector(loc)).normalized(); q = d.to_track_quat('-Z', 'Y'); cam.rotation_euler = q.to_euler()
    cam.rotation_euler.rotate_axis('Z', roll)
    cam_d.lens = lens; cam_d.dof.aperture_fstop = fstop

def place_sweep(x, y, z, strength, tgt=(0, 0, 0)):
    sweep.location = (x, y, z); d = (Vector(tgt) - Vector((x, y, z))).normalized(); sweep.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); eSw.inputs['Strength'].default_value = strength

def set_frame(f):
    k = 0
    while k < 3 and f >= START[k + 1]: k += 1
    t = (f - START[k]) / (SHOTS[k] - 1)
    iso.rotation_euler = (0, 0, 0); floor.hide_render = k != 3
    eTop.inputs['Strength'].default_value = 3.5; eFront.inputs['Strength'].default_value = 2.6
    eSL.inputs['Strength'].default_value = 10; eSR.inputs['Strength'].default_value = 12; eBack.inputs['Strength'].default_value = 14
    if k == 0:
        # macro: la oscuridad se rompe con una línea de luz que corre por el bisel superior
        ign = sg(t, 0, .35)
        for e, v in ((eTop, 3.5), (eFront, 2.6), (eSL, 10), (eSR, 12), (eBack, 14)): e.inputs['Strength'].default_value = v * (.15 + .85 * ign)
        eTop.inputs['Strength'].default_value = .6 * (.15 + .85 * ign)
        look(L3((-.68, -.42, .53), (-.38, -.40, .53), eio(t)), L3((-.5, -.1, .47), (-.3, -.1, .47), eio(t)), 60, 1.4, -.06)
        place_sweep(lerp(-2.5, 2.5, t), -2.2, 2.2, 40 * math.sin(math.pi * t))
    elif k == 1:
        # el vértice: las dos puntas se encuentran; contraluz rasante
        look(L3((.2, -.62, -.72), (.07, -.46, -.62), eio(t)), (0, -.08, -.47), 70, 1.6, .05)
        place_sweep(lerp(2.4, -2.4, t), -2.0, -.8, 45 * math.sin(math.pi * t))
        eBack.inputs['Strength'].default_value = 26
    elif k == 2:
        # tres cuartos: la pieza gira y enseña el grosor; los reflejos resbalan
        iso.rotation_euler = (0, 0, lerp(-.95, -1.25, eio(t)))
        look(L3((.08, -1.8, .34), (.04, -1.6, .24), eio(t)), (0, 0, -.02), 50, 2.8)
        place_sweep(lerp(-2.6, 2.6, t), -2.4, 1.2, 38 * math.sin(math.pi * t))
        eBack.inputs['Strength'].default_value = 22
    else:
        # el plano final: la cámara se aleja y queda el isotipo entero sobre el suelo negro
        e = eio(sg(t, 0, .75)); d = lerp(3.2, 4.7, e)
        look((0, -d, lerp(.05, .18, e)), (0, 0, lerp(-.1, -.32, e)), 40, lerp(2.2, 5.6, e))
        place_sweep(lerp(3.2, -3.2, sg(t, .15, .85)), -3.0, .9, 34 * math.sin(math.pi * sg(t, .15, .85)))

frames = []
for part in FR.split(','):
    if '-' in part: a, b2 = part.split('-'); frames += list(range(int(a), int(b2) + 1))
    else: frames.append(int(part))
os.makedirs(OUT, exist_ok=True)
for f in frames:
    path = os.path.join(OUT, f'f{f:04d}.png')
    if os.path.exists(path): continue
    set_frame(f); sc.frame_set(f)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('frame', f, flush=True)

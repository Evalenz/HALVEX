"""Render fotorrealista de una gorra HALVEX con el isotipo bordado (Blender / Cycles)."""
import bpy, bmesh, math, sys, json, os
from mathutils import Vector

ARGS = json.loads(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else {}
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARGS.get('out', os.path.join(HERE, 'gorra.png'))
CAP = ARGS.get('cap', [0.006, 0.006, 0.007])        # color del tejido (lineal)
THREAD = ARGS.get('thread', [0.62, 0.62, 0.60])     # color del hilo
BG = ARGS.get('bg', [0.80, 0.78, 0.74])
CAM = ARGS.get('cam', [-0.52, -0.80, 0.32])
TGT = ARGS.get('tgt', [0.0, -0.02, 0.045])
LENS = ARGS.get('lens', 85)
RES = ARGS.get('res', [1800, 1200])
SAMPLES = ARGS.get('samples', 128)
FSTOP = ARGS.get('fstop', 5.6)
ROT = ARGS.get('rot', 0)          # giro de la gorra (grados, eje Z)
SECOND = ARGS.get('second')       # segunda gorra opcional {cap, thread, loc, rot}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.feature_set = 'EXPERIMENTAL'
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 8
sc.render.resolution_x, sc.render.resolution_y = RES
sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = OUT

RX, RY, H = 0.094, 0.104, 0.112


def deform(v):
    """copa estructurada: delantero más alto y recto, trasero más bajo"""
    x, y, z = v
    f = max(0.0, -y / RY)              # 1 delante, 0 detrás
    b = max(0.0, y / RY)
    z = z * (1 + 0.10 * f - 0.10 * b)
    y = y * (1 - 0.06 * (z / H) * f)
    return Vector((x, y, z))


# ------------------------------------------------------------------ materiales
def tela(name, color, front_logo=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.cycles.displacement_method = 'BOTH'
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    N.clear()
    out = N.new('ShaderNodeOutputMaterial'); out.location = (1400, 0)
    bs = N.new('ShaderNodeBsdfPrincipled'); bs.location = (900, 200)
    bs.inputs['Roughness'].default_value = 0.86
    bs.inputs['Specular IOR Level'].default_value = 0.25
    bs.inputs['Sheen Weight'].default_value = 0.18
    bs.inputs['Sheen Roughness'].default_value = 0.35
    bs.inputs['Sheen Tint'].default_value = (0.6, 0.6, 0.6, 1)
    tc = N.new('ShaderNodeTexCoord'); tc.location = (-1400, 0)
    # sarga diagonal
    mp = N.new('ShaderNodeMapping'); mp.location = (-1200, 0)
    mp.inputs['Rotation'].default_value = (0, 0.6, 0.8)
    Lk.new(tc.outputs['Object'], mp.inputs['Vector'])
    wv = N.new('ShaderNodeTexWave'); wv.location = (-1000, 100)
    wv.inputs['Scale'].default_value = 1350
    wv.inputs['Distortion'].default_value = 2
    wv.inputs['Detail'].default_value = 1
    Lk.new(mp.outputs['Vector'], wv.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.location = (-1000, -150)
    nz.inputs['Scale'].default_value = 2600
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    mix0 = N.new('ShaderNodeMath'); mix0.operation = 'ADD'; mix0.location = (-780, 0)
    Lk.new(wv.outputs['Fac'], mix0.inputs[0]); Lk.new(nz.outputs['Fac'], mix0.inputs[1])
    big = N.new('ShaderNodeTexNoise'); big.location = (-1000, -300)
    big.inputs['Scale'].default_value = 28; big.inputs['Detail'].default_value = 3
    Lk.new(tc.outputs['Object'], big.inputs['Vector'])
    mix = N.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'; mix.location = (-650, 0)
    Lk.new(big.outputs['Fac'], mix.inputs[0]); mix.inputs[1].default_value = 1.5; Lk.new(mix0.outputs[0], mix.inputs[2])
    # costuras de los paneles (a partir del ángulo)
    sep = N.new('ShaderNodeSeparateXYZ'); sep.location = (-1200, -400)
    Lk.new(tc.outputs['Object'], sep.inputs[0])
    neg = N.new('ShaderNodeMath'); neg.operation = 'MULTIPLY'; neg.inputs[1].default_value = -1; neg.location = (-1050, -450)
    Lk.new(sep.outputs['Y'], neg.inputs[0])
    at = N.new('ShaderNodeMath'); at.operation = 'ARCTAN2'; at.location = (-900, -400)
    Lk.new(sep.outputs['X'], at.inputs[0]); Lk.new(neg.outputs[0], at.inputs[1])
    m3 = N.new('ShaderNodeMath'); m3.operation = 'MULTIPLY'; m3.inputs[1].default_value = 3; m3.location = (-760, -400)
    Lk.new(at.outputs[0], m3.inputs[0])
    sn = N.new('ShaderNodeMath'); sn.operation = 'SINE'; sn.location = (-620, -400)
    Lk.new(m3.outputs[0], sn.inputs[0])
    ab = N.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; ab.location = (-480, -400)
    Lk.new(sn.outputs[0], ab.inputs[0])
    # surco de la costura
    seam = N.new('ShaderNodeMapRange'); seam.location = (-320, -350)
    seam.inputs['From Min'].default_value = 0.0; seam.inputs['From Max'].default_value = 0.035
    seam.inputs['To Min'].default_value = -1.0; seam.inputs['To Max'].default_value = 0.0
    Lk.new(ab.outputs[0], seam.inputs['Value'])
    # pespuntes paralelos (dos filas) con puntadas a lo largo de Z
    band = N.new('ShaderNodeMapRange'); band.location = (-320, -560); band.interpolation_type = 'SMOOTHSTEP'
    Lk.new(ab.outputs[0], band.inputs['Value'])
    band.inputs['From Min'].default_value = 0.05; band.inputs['From Max'].default_value = 0.065
    band2 = N.new('ShaderNodeMapRange'); band2.location = (-320, -760); band2.interpolation_type = 'SMOOTHSTEP'
    Lk.new(ab.outputs[0], band2.inputs['Value'])
    band2.inputs['From Min'].default_value = 0.085; band2.inputs['From Max'].default_value = 0.07
    bmul = N.new('ShaderNodeMath'); bmul.operation = 'MULTIPLY'; bmul.location = (-150, -650)
    Lk.new(band.outputs[0], bmul.inputs[0]); Lk.new(band2.outputs[0], bmul.inputs[1])
    dash = N.new('ShaderNodeTexWave'); dash.location = (-320, -950); dash.wave_type = 'BANDS'; dash.bands_direction = 'Z'
    dash.inputs['Scale'].default_value = 330
    Lk.new(tc.outputs['Object'], dash.inputs['Vector'])
    dmul = N.new('ShaderNodeMath'); dmul.operation = 'MULTIPLY'; dmul.location = (0, -700)
    Lk.new(bmul.outputs[0], dmul.inputs[0]); Lk.new(dash.outputs['Fac'], dmul.inputs[1])
    # suma de alturas
    h1 = N.new('ShaderNodeMath'); h1.operation = 'MULTIPLY_ADD'; h1.location = (150, -200)
    Lk.new(mix.outputs[0], h1.inputs[0]); h1.inputs[1].default_value = 0.03; Lk.new(seam.outputs[0], h1.inputs[2])
    h2 = N.new('ShaderNodeMath'); h2.operation = 'MULTIPLY_ADD'; h2.location = (300, -300)
    Lk.new(dmul.outputs[0], h2.inputs[0]); h2.inputs[1].default_value = 1.3; Lk.new(h1.outputs[0], h2.inputs[2])
    bump = N.new('ShaderNodeBump'); bump.location = (600, -200)
    bump.inputs['Strength'].default_value = 0.6; bump.inputs['Distance'].default_value = 0.0006
    Lk.new(h2.outputs[0], bump.inputs['Height'])
    color = N.new('ShaderNodeRGB'); color.location = (600, 300); color.outputs[0].default_value = (*color_lin(color_val := color), 1) if False else (*CAPCOL[name], 1)
    if front_logo:
        uv = N.new('ShaderNodeUVMap'); uv.uv_map = 'logo'; uv.location = (-1200, 500)
        himg = N.new('ShaderNodeTexImage'); himg.location = (-900, 600)
        himg.image = bpy.data.images.load(os.path.join(HERE, 'iso_h.png')); himg.image.colorspace_settings.name = 'Non-Color'
        himg.extension = 'CLIP'; himg.interpolation = 'Cubic'
        mimg = N.new('ShaderNodeTexImage'); mimg.location = (-900, 300)
        mimg.image = bpy.data.images.load(os.path.join(HERE, 'iso_m.png')); mimg.image.colorspace_settings.name = 'Non-Color'
        mimg.extension = 'CLIP'
        Lk.new(uv.outputs['UV'], himg.inputs['Vector']); Lk.new(uv.outputs['UV'], mimg.inputs['Vector'])
        # solo en la mitad delantera
        front = N.new('ShaderNodeMath'); front.operation = 'LESS_THAN'; front.inputs[1].default_value = 0.0; front.location = (-700, 450)
        Lk.new(sep.outputs['Y'], front.inputs[0])
        hm = N.new('ShaderNodeMath'); hm.operation = 'MULTIPLY'; hm.location = (-550, 600)
        Lk.new(himg.outputs['Color'], hm.inputs[0]); Lk.new(front.outputs[0], hm.inputs[1])
        mm = N.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.location = (-550, 350)
        Lk.new(mimg.outputs['Color'], mm.inputs[0]); Lk.new(front.outputs[0], mm.inputs[1])
        thr = N.new('ShaderNodeRGB'); thr.location = (300, 450); thr.outputs[0].default_value = (*THREADCOL[name], 1)
        cm = N.new('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.location = (700, 450)
        Lk.new(mm.outputs[0], cm.inputs['Factor']); Lk.new(color.outputs[0], cm.inputs['A']); Lk.new(thr.outputs[0], cm.inputs['B'])
        Lk.new(cm.outputs['Result'], bs.inputs['Base Color'])
        rm = N.new('ShaderNodeMapRange'); rm.location = (700, 150)
        rm.inputs['To Min'].default_value = 0.86; rm.inputs['To Max'].default_value = 0.38
        Lk.new(mm.outputs[0], rm.inputs['Value']); Lk.new(rm.outputs[0], bs.inputs['Roughness'])
        # desplazamiento real del bordado
        disp = N.new('ShaderNodeDisplacement'); disp.location = (1150, -300)
        disp.inputs['Scale'].default_value = 0.0016; disp.inputs['Midlevel'].default_value = 0.0
        Lk.new(hm.outputs[0], disp.inputs['Height'])
        Lk.new(disp.outputs['Displacement'], out.inputs['Displacement'])
        # relieve fino del hilo
        hb = N.new('ShaderNodeMath'); hb.operation = 'MULTIPLY_ADD'; hb.location = (450, -50)
        Lk.new(hm.outputs[0], hb.inputs[0]); hb.inputs[1].default_value = 1.5; Lk.new(h2.outputs[0], hb.inputs[2])
        Lk.new(hb.outputs[0], bump.inputs['Height'])
    else:
        Lk.new(color.outputs[0], bs.inputs['Base Color'])
    Lk.new(bump.outputs['Normal'], bs.inputs['Normal'])
    Lk.new(bs.outputs[0], out.inputs['Surface'])
    return m


def color_lin(c):
    return c


def brim_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bs = N['Principled BSDF']
    bs.inputs['Base Color'].default_value = (*CAPCOL[name], 1)
    bs.inputs['Roughness'].default_value = 0.84
    bs.inputs['Specular IOR Level'].default_value = 0.25
    bs.inputs['Sheen Weight'].default_value = 0.18
    bs.inputs['Sheen Roughness'].default_value = 0.35
    uv = N.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'
    sep = N.new('ShaderNodeSeparateXYZ'); Lk.new(uv.outputs['UV'], sep.inputs[0])
    # pespuntes concéntricos en la visera (v) con puntadas a lo largo de u
    mv = N.new('ShaderNodeMath'); mv.operation = 'MULTIPLY'; mv.inputs[1].default_value = 16; Lk.new(sep.outputs['Y'], mv.inputs[0])
    fr = N.new('ShaderNodeMath'); fr.operation = 'FRACT'; Lk.new(mv.outputs[0], fr.inputs[0])
    rows = N.new('ShaderNodeMapRange'); rows.interpolation_type = 'SMOOTHSTEP'
    rows.inputs['From Min'].default_value = 0.46; rows.inputs['From Max'].default_value = 0.5
    Lk.new(fr.outputs[0], rows.inputs['Value'])
    rows2 = N.new('ShaderNodeMapRange'); rows2.interpolation_type = 'SMOOTHSTEP'
    rows2.inputs['From Min'].default_value = 0.54; rows2.inputs['From Max'].default_value = 0.5
    Lk.new(fr.outputs[0], rows2.inputs['Value'])
    rm = N.new('ShaderNodeMath'); rm.operation = 'MULTIPLY'; Lk.new(rows.outputs[0], rm.inputs[0]); Lk.new(rows2.outputs[0], rm.inputs[1])
    # solo en la zona de pespuntes (v < 0.55) y filas a lo largo de u
    lim = N.new('ShaderNodeMath'); lim.operation = 'LESS_THAN'; lim.inputs[1].default_value = 1.01; Lk.new(sep.outputs['Y'], lim.inputs[0])
    mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 900; Lk.new(sep.outputs['X'], mu.inputs[0])
    sn = N.new('ShaderNodeMath'); sn.operation = 'SINE'; Lk.new(mu.outputs[0], sn.inputs[0])
    sp = N.new('ShaderNodeMath'); sp.operation = 'GREATER_THAN'; sp.inputs[1].default_value = -0.4; Lk.new(sn.outputs[0], sp.inputs[0])
    a = N.new('ShaderNodeMath'); a.operation = 'MULTIPLY'; Lk.new(rm.outputs[0], a.inputs[0]); Lk.new(lim.outputs[0], a.inputs[1])
    b = N.new('ShaderNodeMath'); b.operation = 'MULTIPLY'; Lk.new(a.outputs[0], b.inputs[0]); Lk.new(sp.outputs[0], b.inputs[1])
    tc = N.new('ShaderNodeTexCoord')
    wv = N.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 1350; Lk.new(tc.outputs['Object'], wv.inputs['Vector'])
    s = N.new('ShaderNodeMath'); s.operation = 'MULTIPLY_ADD'; Lk.new(wv.outputs['Fac'], s.inputs[0]); s.inputs[1].default_value = 0.1; Lk.new(b.outputs[0], s.inputs[2])
    bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25; bump.inputs['Distance'].default_value = 0.0004
    Lk.new(s.outputs[0], bump.inputs['Height']); Lk.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


CAPCOL, THREADCOL = {}, {}


# ------------------------------------------------------------------ geometría
def make_cap(prefix, cap_col, thread_col, loc=(0, 0, 0), rot=0, logo=True):
    CAPCOL[prefix + 'tela'] = tuple(cap_col); THREADCOL[prefix + 'tela'] = tuple(thread_col)
    CAPCOL[prefix + 'visera'] = tuple(cap_col)
    objs = []
    # copa
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=1.0)
    for v in [v for v in bm.verts if v.co.z < -0.075]:
        bm.verts.remove(v)
    for v in bm.verts:
        c = v.co
        low = c.z < -1e-4
        if low:
            k = 1 / math.hypot(c.x, c.y); c = Vector((c.x * k, c.y * k, 0.0))
        r = math.hypot(c.x, c.y); zz = max(c.z, 0)
        rs = (r ** 0.55) / r if r > 1e-6 else 0
        az = math.atan2(c.x, -c.y)
        s3 = abs(math.sin(3 * az))
        pull = 1 - 0.022 * math.exp(-(s3 / 0.09) ** 2) * min(1.0, r * 1.6) - 0.006 * (1 - s3)
        v.co = deform(Vector((c.x * rs * RX * pull, c.y * rs * RY * pull, (zz ** 0.9) * H * (1 - 0.01 * math.exp(-(s3 / 0.09) ** 2)))))
        if low:
            v.co.z = -0.007
    me = bpy.data.meshes.new(prefix + 'copa'); bm.to_mesh(me); bm.free()
    copa = bpy.data.objects.new(prefix + 'copa', me); bpy.context.collection.objects.link(copa)
    # UV del logo: proyección frontal
    me.uv_layers.new(name='logo')
    SZ, ZC = 0.064, 0.060
    uvl = me.uv_layers['logo']
    for poly in me.polygons:
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uvl.data[li].uv = (0.5 + co.x / SZ, 0.5 + (co.z - ZC) / SZ)
    for p in me.polygons: p.use_smooth = True
    sol = copa.modifiers.new('grosor', 'SOLIDIFY'); sol.thickness = 0.0022; sol.offset = -1
    sub = copa.modifiers.new('sub', 'SUBSURF'); sub.levels = 2; sub.render_levels = 3
    if logo:
        copa.cycles.use_adaptive_subdivision = True
    copa.data.materials.append(tela(prefix + 'tela', cap_col, front_logo=logo))
    objs.append(copa)
    # visera
    bm = bmesh.new(); NU, NV = 64, 16
    grid = []
    for i in range(NU + 1):
        u = -1 + 2 * i / NU
        th = u * math.radians(78)
        inner = deform(Vector((RX * math.sin(th), -RY * math.cos(th), 0)))
        d = Vector((math.sin(th) * 1.0, -math.cos(th) * 1.18, 0)).normalized()
        Lb = 0.072 * (max(0.0, math.cos(u * math.pi / 2)) ** 0.55) + 0.002
        row = []
        for j in range(NV + 1):
            v = j / NV
            p = Vector((inner.x * (0.975 + 0.075 * v), inner.y * (0.975 + 0.025 * v) - Lb * v, 0))
            lv = Lb * v / 0.072
            p.z = -0.0018 - 0.008 * lv - 0.028 * (abs(p.x) / 0.095) ** 2 * lv - 0.004 * lv ** 2
            row.append(bm.verts.new(p))
        grid.append(row)
    uvlay = bm.loops.layers.uv.new('UVMap')
    for i in range(NU):
        for j in range(NV):
            f = bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
            for lp, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                lp[uvlay].uv = (a / NU, b / NV)
    me = bpy.data.meshes.new(prefix + 'visera'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    vis = bpy.data.objects.new(prefix + 'visera', me); bpy.context.collection.objects.link(vis)
    s2 = vis.modifiers.new('grosor', 'SOLIDIFY'); s2.thickness = 0.0034; s2.offset = 0; s2.use_rim = True
    bv = vis.modifiers.new('bisel', 'BEVEL'); bv.width = 0.0012; bv.segments = 3
    s3 = vis.modifiers.new('sub', 'SUBSURF'); s3.levels = 1; s3.render_levels = 2
    vis.data.materials.append(brim_mat(prefix + 'visera'))
    objs.append(vis)
    # botón y ojales
    tela_m = bpy.data.materials.new(prefix + 'boton'); tela_m.use_nodes = True
    tela_m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*cap_col, 1)
    tela_m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.7
    top = deform(Vector((0, 0, H)))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0062, location=top + Vector((0, 0, -0.0015)))
    bt = bpy.context.object; bt.scale = (1, 1, 0.45); bt.data.materials.append(tela_m); bpy.ops.object.shade_smooth(); objs.append(bt)
    ring = bpy.data.materials.new(prefix + 'ojal'); ring.use_nodes = True
    ring.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (cap_col[0] * .6, cap_col[1] * .6, cap_col[2] * .6, 1)
    for k in range(6):
        az = math.radians(30 + 60 * k); el = math.radians(52)
        u = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        p = deform(Vector((u.x * RX, u.y * RY, u.z * H)))
        n = Vector((u.x / RX, u.y / RY, u.z / H)).normalized()
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0028, minor_radius=0.0009, location=p + n * 0.0006)
        t = bpy.context.object; t.rotation_mode = 'QUATERNION'; t.rotation_quaternion = n.to_track_quat('Z', 'Y')
        t.data.materials.append(ring); bpy.ops.object.shade_smooth(); objs.append(t)
    # agrupar
    root = bpy.data.objects.new(prefix + 'gorra', None); bpy.context.collection.objects.link(root)
    for o in objs: o.parent = root
    root.location = loc; root.rotation_euler = (0, 0, math.radians(rot))
    return root


make_cap('a_', CAP, THREAD, (0, 0, 0), ROT)
if SECOND:
    make_cap('b_', SECOND['cap'], SECOND['thread'], tuple(SECOND['loc']), SECOND.get('rot', 0))

# ------------------------------------------------------------------ estudio
bm = bmesh.new(); prof = []
for i in range(40):
    t = i / 39
    if t < 0.5:
        prof.append((-1.5 + 2.6 * (t / 0.5), 0))
    else:
        a = (t - 0.5) / 0.5 * math.pi / 2
        prof.append((1.1 + 0.6 * math.sin(a), 0.6 * (1 - math.cos(a))))
prof.append((1.7, 3.0))
vs = [[bm.verts.new((x, y, z)) for (y, z) in prof] for x in (-4, 4)]
for i in range(len(prof) - 1):
    bm.faces.new((vs[0][i], vs[1][i], vs[1][i + 1], vs[0][i + 1]))
me = bpy.data.meshes.new('fondo'); bm.to_mesh(me); bm.free()
for p in me.polygons: p.use_smooth = True
fondo = bpy.data.objects.new('fondo', me); bpy.context.collection.objects.link(fondo)
fm = bpy.data.materials.new('fondo'); fm.use_nodes = True
fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*BG, 1)
fm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
fondo.data.materials.append(fm)
fondo.location.z = ARGS.get('floor', -0.036)  # la visera toca el suelo

world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.25


def area(name, loc, size, energy, tgt=(0, 0, 0.05)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.shape = 'RECTANGLE'; ld.size = size; ld.size_y = size * 0.7; ld.energy = energy
    o = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(o); o.location = loc
    d = Vector(tgt) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


area('key', (-0.7, -0.8, 1.4), 1.3, ARGS.get('key', 70))
area('fill', (1.1, -0.6, 0.5), 1.4, ARGS.get('fill', 14))
area('rim', (0.4, 1.0, 0.9), 0.8, ARGS.get('rim', 40))

cd = bpy.data.cameras.new('cam'); cd.lens = LENS
cd.dof.use_dof = True; cd.dof.aperture_fstop = FSTOP
cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam)
cam.location = CAM
d = Vector(TGT) - Vector(CAM); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
fo = bpy.data.objects.new('foco', None); bpy.context.collection.objects.link(fo)
fo.location = ARGS.get('focus', [0, -0.10, 0.06]); cd.dof.focus_object = fo
sc.camera = cam
bpy.ops.render.render(write_still=True)
print('RENDER', OUT)

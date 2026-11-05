"""Render cinematográfico: el isotipo HALVEX como dos monolitos de metal negro con luz por el vértice."""
import bpy, bmesh, math, sys, json, os
from mathutils import Vector

ARGS = json.loads(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else {}
OUT = ARGS.get('out', 'monolito.png')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = ARGS.get('samples', 64); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = ARGS.get('res', [2400, 1350])
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - High Contrast'
sc.render.filepath = OUT

H = 1.6                     # altura del isotipo (m)
S = H / 152
D = ARGS.get('depth', 0.22) # grosor
LIFT = 0.03

def P(x, y):
    return ((x - 100) * S, (172 - y) * S + LIFT)

metal = bpy.data.materials.new('metal'); metal.use_nodes = True
b = metal.node_tree.nodes['Principled BSDF']
b.inputs['Base Color'].default_value = (0.018, 0.018, 0.02, 1)
b.inputs['Metallic'].default_value = 0.6
b.inputs['Roughness'].default_value = 0.26
b.inputs['Anisotropic'].default_value = 0.5

for pts in ([(24, 20), (60, 20), (96.2, 172)], [(176, 20), (140, 20), (103.8, 172)]):
    bm = bmesh.new()
    vs = [bm.verts.new((P(*p)[0], -D / 2, P(*p)[1])) for p in pts]
    f = bm.faces.new(vs)
    bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in bm.verts:
        if abs(v.co.y + D / 2) < 1e-6 and v not in vs:
            pass
    me = bpy.data.meshes.new('w'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('w', me); bpy.context.collection.objects.link(o)
    # mover la cara extruida a +D/2
    for v in me.vertices:
        if v.index >= 3:
            v.co.y = D / 2
    me.update()
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = 0.004; bv.segments = 3; bv.limit_method = 'ANGLE'
    o.data.materials.append(metal)
    for p in me.polygons: p.use_smooth = False
    me.validate(); me.update()
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode='OBJECT')
    o.select_set(False)

# suelo reflectante
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
fl = bpy.context.object
fm = bpy.data.materials.new('suelo'); fm.use_nodes = True
fb = fm.node_tree.nodes['Principled BSDF']
fb.inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1)
fb.inputs['Roughness'].default_value = 0.22
fb.inputs['Specular IOR Level'].default_value = 0.5
N = fm.node_tree.nodes; L = fm.node_tree.links
nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 6
mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.28; mr.inputs['To Max'].default_value = 0.45
L.new(nz.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs[0], fb.inputs['Roughness'])
fl.data.materials.append(fm)

# tira de luz detrás del vértice
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 5.0, 0.55), rotation=(math.radians(90), 0, 0))
st = bpy.context.object; st.scale = (ARGS.get('strip', 0.025), 1.1, 1)
em = bpy.data.materials.new('em'); em.use_nodes = True
en = em.node_tree.nodes; en.clear()
e = en.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1, 0.97, 0.92, 1); e.inputs['Strength'].default_value = ARGS.get('strip_e', 25)
o_ = en.new('ShaderNodeOutputMaterial'); em.node_tree.links.new(e.outputs[0], o_.inputs[0])
st.data.materials.append(em)

def area(loc, size, energy, tgt, sy=None, color=(1, 1, 1), spread=180):
    ld = bpy.data.lights.new('a', 'AREA'); ld.shape = 'RECTANGLE'; ld.size = size; ld.size_y = sy or size; ld.energy = energy; ld.color = color; ld.spread = math.radians(spread)
    ob = bpy.data.objects.new('a', ld); bpy.context.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()

k = ARGS.get('k', 1.0)
area((-2.6, 1.2, 1.5), 0.12, 220 * k, (0, 0, 1.3), 2.4, spread=25)     # rim izquierdo
area((2.6, 1.2, 1.5), 0.12, 220 * k, (0, 0, 1.3), 2.4, spread=25)      # rim derecho
area((0, -3, 4.5), 2.0, 30 * k, (0, 0, 1.0))
area((0, -1.5, 3.2), 0.6, 25 * k, (0, 0, 1.4), 0.6)                # relleno frontal muy suave

bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -9, 1.4), rotation=(math.radians(90), 0, 0))
sb = bpy.context.object; sb.scale = (7, 2.4, 1)
sm = bpy.data.materials.new('sb'); sm.use_nodes = True; sn = sm.node_tree.nodes; sn.clear()
se = sn.new('ShaderNodeEmission'); se.inputs['Strength'].default_value = ARGS.get('soft', 1.2)
so = sn.new('ShaderNodeOutputMaterial'); sm.node_tree.links.new(se.outputs[0], so.inputs[0]); sb.data.materials.append(sm)
sb.visible_camera = False
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)

cd = bpy.data.cameras.new('c'); cd.lens = ARGS.get('lens', 40)
cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6
cam = bpy.data.objects.new('c', cd); bpy.context.collection.objects.link(cam)
cam.location = ARGS.get('cam', [0, -6.2, 0.55])
tgt = ARGS.get('tgt', [0, 0, 1.05])
cam.rotation_euler = (Vector(tgt) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
fo = bpy.data.objects.new('f', None); bpy.context.collection.objects.link(fo); fo.location = (0, 0, 0.8); cd.dof.focus_object = fo
sc.camera = cam
bpy.ops.render.render(write_still=True)
print('RENDER', OUT)

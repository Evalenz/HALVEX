"""Render fotorrealista de la papelería HALVEX (Blender / Cycles)."""
import bpy, bmesh, math, sys, json, os
from mathutils import Vector

ARGS = json.loads(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else {}
HERE = os.path.dirname(os.path.abspath(__file__))
T = lambda n: os.path.join(HERE, 'tex', n + '.png')
SCENE = ARGS.get('scene', 'flatlay')

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = ARGS.get('samples', 160); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = ARGS.get('res', [2000, 1334])
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.filepath = ARGS.get('out', os.path.join(HERE, 'p.png'))


def img(path, non_color=False):
    i = bpy.data.images.load(path)
    if non_color: i.colorspace_settings.name = 'Non-Color'
    return i


def paper_mat(name, tex=None, color=(0.9, 0.89, 0.86), rough=0.82, emboss=None, emb_strength=0.6, sheen=0.25):
    m = bpy.data.materials.new(name); m.use_nodes = True
    N = m.node_tree.nodes; Lk = m.node_tree.links
    bs = N['Principled BSDF']
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Specular IOR Level'].default_value = 0.35
    bs.inputs['Sheen Weight'].default_value = sheen
    tc = N.new('ShaderNodeTexCoord')
    if tex:
        it = N.new('ShaderNodeTexImage'); it.image = img(tex); it.interpolation = 'Cubic'
        Lk.new(tc.outputs['UV'], it.inputs['Vector']); Lk.new(it.outputs['Color'], bs.inputs['Base Color'])
    else:
        bs.inputs['Base Color'].default_value = (*color, 1)
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1800; nz.inputs['Detail'].default_value = 6
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    h = nz.outputs['Fac']
    bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.08; bump.inputs['Distance'].default_value = 0.0002
    if emboss:
        ie = N.new('ShaderNodeTexImage'); ie.image = img(emboss, True); ie.interpolation = 'Cubic'
        Lk.new(tc.outputs['UV'], ie.inputs['Vector'])
        bl = N.new('ShaderNodeMath'); bl.operation = 'MULTIPLY_ADD'
        Lk.new(ie.outputs['Color'], bl.inputs[0]); bl.inputs[1].default_value = emb_strength; Lk.new(h, bl.inputs[2])
        h = bl.outputs[0]
        bump.inputs['Strength'].default_value = 0.5
        bump.inputs['Distance'].default_value = 0.0004
    Lk.new(h, bump.inputs['Height']); Lk.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


def edge_mat(name, color):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = 0.9
    return m


def sheet(name, w, h, t, top_mat, edge, loc, rot, z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(loc[0], loc[1], z + t))
    o = bpy.context.object; o.name = name; o.scale = (w, h, 1)
    bpy.ops.object.transform_apply(scale=True)
    o.rotation_euler = (0, 0, math.radians(rot))
    o.data.materials.append(top_mat); o.data.materials.append(edge)
    s = o.modifiers.new('g', 'SOLIDIFY'); s.thickness = t; s.offset = -1; s.material_offset_rim = 1
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = min(t * 0.3, 0.0004); bv.segments = 2
    return o


BLACK = (0.012, 0.012, 0.013)
mat = {}
mat['cf'] = paper_mat('card_front', T('card_front'), rough=0.9, emboss=T('card_emboss'), emb_strength=1.0, sheen=0.35)
mat['cb'] = paper_mat('card_back', T('card_back'), rough=0.85)
mat['letter'] = paper_mat('letter', T('letter'))
mat['env'] = paper_mat('env', T('envelope'))
mat['comp'] = paper_mat('comp', T('compliment'))
mat['nb'] = paper_mat('nb', T('notebook'), rough=0.7, emboss=T('nb_emboss'), emb_strength=-1.0, sheen=0.06)
mat['fold'] = paper_mat('fold', T('folder'), rough=0.85)
e_black = edge_mat('eb', BLACK); e_white = edge_mat('ew', (0.85, 0.84, 0.81))

if SCENE == 'flatlay':
    sheet('letter', 0.210, 0.297, 0.00015, mat['letter'], e_white, (-0.105, 0.06), -7)
    sheet('folder', 0.220, 0.310, 0.0005, mat['fold'], e_black, (0.165, 0.115), 7, z=-0.0005)
    sheet('nb', 0.148, 0.210, 0.012, mat['nb'], e_black, (0.225, -0.075), -12, z=0.0005)
    sheet('env', 0.220, 0.110, 0.0006, mat['env'], e_white, (-0.055, -0.17), 4, z=0.0003)
    sheet('comp', 0.210, 0.099, 0.0003, mat['comp'], e_white, (-0.20, -0.105), 13, z=0.0009)
    sheet('c1', 0.085, 0.055, 0.0006, mat['cf'], e_black, (0.075, -0.13), 16, z=0.0012)
    sheet('c2', 0.085, 0.055, 0.0006, mat['cf'], e_black, (0.082, -0.136), 7, z=0.0018)
    sheet('c3', 0.085, 0.055, 0.0006, mat['cb'], e_white, (0.07, -0.205), -6, z=0.0012)
    # bolígrafo
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.0048, depth=0.14, location=(0.02, -0.055, 0.006), rotation=(0, math.radians(90), math.radians(-32)))
    pen = bpy.context.object; bpy.ops.object.shade_smooth()
    pm = bpy.data.materials.new('pen'); pm.use_nodes = True; pb = pm.node_tree.nodes['Principled BSDF']
    pb.inputs['Base Color'].default_value = (0.01, 0.01, 0.011, 1); pb.inputs['Metallic'].default_value = 0.7; pb.inputs['Roughness'].default_value = 0.3
    pen.data.materials.append(pm)
    bv = pen.modifiers.new('b', 'BEVEL'); bv.width = 0.002; bv.segments = 6
    cam_loc, cam_tgt, lens, fstop, focus = ARGS.get('cam', [0.02, -0.42, 0.66]), [0.02, -0.02, 0], 50, 8, [0.06, -0.10, 0]
    surface = ARGS.get('surface', (0.028, 0.029, 0.032))
else:
    # tarjetas en detalle
    sheet('c1', 0.085, 0.055, 0.0006, mat['cf'], e_black, (-0.02, 0.0), -10, z=0.0)
    sheet('c2', 0.085, 0.055, 0.0006, mat['cf'], e_black, (-0.016, 0.004), -4, z=0.0006)
    sheet('c3', 0.085, 0.055, 0.0006, mat['cf'], e_black, (-0.012, 0.002), 2, z=0.0012)
    sheet('c4', 0.085, 0.055, 0.0006, mat['cb'], e_white, (0.065, -0.035), 14, z=0.0)
    cam_loc, cam_tgt, lens, fstop, focus = ARGS.get('cam', [-0.13, -0.24, 0.13]), [0.0, -0.005, 0], 90, 3.5, [-0.012, 0.0, 0.0018]
    surface = ARGS.get('surface', (0.70, 0.68, 0.64))

# superficie
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
fl = bpy.context.object
sm = bpy.data.materials.new('mesa'); sm.use_nodes = True; N = sm.node_tree.nodes; Lk = sm.node_tree.links
sb = N['Principled BSDF']; sb.inputs['Base Color'].default_value = (*surface, 1); sb.inputs['Roughness'].default_value = 0.92
nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900; nz.inputs['Detail'].default_value = 8
bu = N.new('ShaderNodeBump'); bu.inputs['Strength'].default_value = 0.12; bu.inputs['Distance'].default_value = 0.0003
Lk.new(nz.outputs['Fac'], bu.inputs['Height']); Lk.new(bu.outputs['Normal'], sb.inputs['Normal'])
fl.data.materials.append(sm)

world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.15


def area(name, loc, size, energy, tgt=(0, 0, 0)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.size = size; ld.energy = energy
    o = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


k = ARGS.get('k', 1.0)
area('key', (-0.8, 0.5, 1.2), 0.9, 220 * k)
area('fill', (0.9, -0.6, 0.8), 1.6, 40 * k)
cd = bpy.data.cameras.new('cam'); cd.lens = lens; cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam); cam.location = cam_loc
cam.rotation_euler = (Vector(cam_tgt) - Vector(cam_loc)).to_track_quat('-Z', 'Y').to_euler()
fo = bpy.data.objects.new('f', None); bpy.context.collection.objects.link(fo); fo.location = focus; cd.dof.focus_object = fo
sc.camera = cam
bpy.ops.render.render(write_still=True)
print('RENDER', sc.render.filepath)

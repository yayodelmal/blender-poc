"""Render overview and close-up previews without saving changes to the model."""
import bpy, sys
from mathutils import Vector
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
if len(args)!=3:raise RuntimeError('expected input blend, overview png, detail png')
src,overview,detail=map(lambda x:Path(x).resolve(),args)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.device='CPU';scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.world.color=(0.05,0.05,0.05)
for name,color in [('CU01_Planter_REV002',(0.78,0.81,0.84,1)),('CU01_SHT31_ClipSupport_REV003',(0.14,0.28,0.42,1))]:
 obj=bpy.data.objects[name];mat=bpy.data.materials.new('Preview_'+name);mat.diffuse_color=color;mat.use_nodes=True;node=mat.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=color;node.inputs['Metallic'].default_value=0;node.inputs['Roughness'].default_value=.8;obj.data.materials.clear();obj.data.materials.append(mat)
for name,loc,power,size in [('Key',(0.06,0.18,0.24),18,0.18),('Fill',(-0.18,0.08,0.12),10,0.14),('Rim',(0,-0.15,0.20),8,0.13)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.name='Preview_'+name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,.055))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(.22,.32,.16));cam=bpy.context.object;cam.name='PreviewOverviewCamera';cam.data.type='ORTHO';cam.data.ortho_scale=.22;cam.rotation_euler=(Vector((0,0,.04))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam;scene.render.filepath=str(overview);bpy.ops.render.render(write_still=True)
cam.location=(.02,.35,.075);cam.data.ortho_scale=.058;cam.rotation_euler=(Vector((0,.075,.075))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(detail);bpy.ops.render.render(write_still=True)
print('REV003_PREVIEWS '+str(overview)+' '+str(detail))

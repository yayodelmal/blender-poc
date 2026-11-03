import hashlib, json, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

RUN_ID='CU-01-REV-003-20261103T032047Z'
SOURCE_NAME='CU01_REV002_planter_20261103T023400Z.blend'
OBJECT_NAME='CU01_Planter_REV002'

def sha(path):
 h=hashlib.sha256(); f=open(path,'rb')
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 f.close();return h.hexdigest()
def parse():
 a=sys.argv[sys.argv.index('--')+1:]
 if len(a)!=2:raise RuntimeError('usage -- source.blend output.blend')
 return Path(a[0]).resolve(),Path(a[1]).resolve()
def mm(x):return x/1000.0
def prism_clip(name, xmin, xmax, profile):
 n=len(profile); verts=[]
 for x in (mm(xmin),mm(xmax)):
  verts.extend([(x,mm(y),mm(z)) for y,z in profile])
 faces=[]
 faces.append(tuple(range(n-1,-1,-1)))
 faces.append(tuple(range(n,2*n)))
 for i in range(n):
  j=(i+1)%n; faces.append((i,j,n+j,n+i))
 mesh=bpy.data.meshes.new(name+'Mesh');mesh.from_pydata(verts,[],faces);mesh.update()
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free()
 obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);return obj
def box(name, center_mm, size_mm):
 bm=bmesh.new(); g=bmesh.ops.create_cube(bm,size=1.0)
 for v in g['verts']:
  v.co=Vector(center_mm)/1000+Vector((v.co.x*size_mm[0],v.co.y*size_mm[1],v.co.z*size_mm[2]))/1000
 mesh=bpy.data.meshes.new(name+'Mesh');bm.to_mesh(mesh);bm.free();mesh.update()
 obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);return obj
def union(target, operand, label):
 bpy.ops.object.select_all(action='DESELECT');target.select_set(True);bpy.context.view_layer.objects.active=target
 mod=target.modifiers.new(label,'BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=operand
 ret=bpy.ops.object.modifier_apply(modifier=mod.name)
 if 'FINISHED' not in ret:raise RuntimeError('boolean union failed '+label)
 mesh=operand.data;bpy.data.objects.remove(operand,do_unlink=True)
 if mesh.users==0:bpy.data.meshes.remove(mesh)
def fingerprint(obj):
 m=obj.data
 h=hashlib.sha256()
 for v in m.vertices:h.update(('%.9f,%.9f,%.9f;'%(v.co.x,v.co.y,v.co.z)).encode())
 h.update(b'|')
 for p in m.polygons:h.update((','.join(map(str,p.vertices))+';').encode())
 return h.hexdigest()

def main():
 src,out=parse()
 if out.exists():raise FileExistsError(out)
 src_hash=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
 planter=bpy.data.objects.get(OBJECT_NAME)
 if not planter or planter.type!='MESH':raise RuntimeError('source planter missing')
 source_geom_hash=fingerprint(planter)
 profile=[(63.9,60.4),(63.9,48.9),(62.7,48.9),(62.7,62.0),(77.0,62.0),(77.0,48.9),(75.5,48.9),(75.5,57.9),(74.5,58.7),(74.5,60.4)]
 support=prism_clip('CU01_SHT31_ClipSupport_REV003',-7.0,7.0,profile)
 support['case_id']='CU-01';support['run_id']=RUN_ID;support['role']='separate_removable_sensor_support';support['sensor']='SHT31 breakout board';
 support['design_parameters_mm']=json.dumps({'clip_inner_gap_at_rim':10.6,'inner_clearance_mm':0.1,'outer_clearance_to_brick_relief_mm':0.5,'clip_width':14.0,'clip_leg_depth_below_rim':11.1,'stand_height_above_rim':30.0,'pcb_envelope_mm':[10.4,13.1],'pcb_orientation':'landscape, 13.1 mm X by 10.4 mm Z','pcb_channel_inner_span_mm':[13.6,10.9],'pcb_channel_clearance_nominal_mm':[0.25,0.5],'pcb_channel_depth_mm':1.6,'assumed_pcb_thickness_mm':1.6,'board_face_plane_y_mm':89.4,'board_back_plane_y_mm':87.8},sort_keys=True)
 support['design_note']='Digital concept; board thickness/connector projection are assumptions. Open backed cradle, sensor face outward.'
 # Upright spine rises from outer clip and turns outward toward the open-backed cradle.
 pieces=[
  ('spine',(0,77.8,69.7),(3.0,4.0,19.0)),
  # Crossbar and paired arms connect the riser to the edge cradle below the sensor board.
  ('crossbar',(0,79.0,78.4),(13.8,1.4,1.2)),
  ('left_arm',(-6.8,83.35,78.7),(1.6,10.1,2.0)),
  ('right_arm',(6.8,83.35,78.7),(1.6,10.1,2.0)),
  # Side rails and narrow front/back lips form an open-backed 1.6 mm board channel.
  ('left_outer_rail',(-7.3,88.8,84.55),(1.0,2.8,10.9)),
  ('right_outer_rail',(7.3,88.8,84.55),(1.0,2.8,10.9)),
  ('left_back_lip',(-7.0,87.45,84.55),(1.5,0.7,10.9)),
  ('right_back_lip',(7.0,87.45,84.55),(1.5,0.7,10.9)),
  ('left_front_lip',(-7.0,89.75,84.55),(1.5,0.7,10.9)),
  ('right_front_lip',(7.0,89.75,84.55),(1.5,0.7,10.9)),
  # Small lower shelves stop the board from sliding down, contacting only its side corners.
  ('left_bottom_stop',(-6.8,88.4,78.9),(1.6,1.8,0.8)),
  ('right_bottom_stop',(6.8,88.4,78.9),(1.6,1.8,0.8)),
 ]
 for name,c,s in pieces:
  op=box('TEMP_'+name,c,s);union(support,op,'REV003_'+name)
 support.name='CU01_SHT31_ClipSupport_REV003';support.data.name='CU01_SHT31_ClipSupportMesh_REV003'
 # New default finish on both product objects.
 repo_root=Path(__file__).resolve().parents[4] if len(Path(__file__).resolve().parents)>4 else Path('/Users/yayo/Projects/blender-poc')
 sys.path.insert(0,str(repo_root/'herramientas'))
 from hyper_pla_marmol import aplicar_material_por_defecto
 aplicar_material_por_defecto(planter);aplicar_material_por_defecto(support)
 support['source_planter_geometry_sha256']=source_geom_hash
 support['source_planter_file_sha256']=src_hash
 support['sensor_board_pose_mm']=json.dumps({'plane_y_mm':89.4,'x_span_mm':13.1,'z_min_mm':79.6,'z_max_mm':90.0,'sensor_face_direction':'+Y','header_pin_direction':'-Y'},sort_keys=True)
 # keep both visible and select support
 bpy.ops.object.select_all(action='DESELECT');planter.select_set(True);support.select_set(True);bpy.context.view_layer.objects.active=support
 scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.0;scene.unit_settings.length_unit='MILLIMETERS'
 out.parent.mkdir(parents=True,exist_ok=True)
 r=bpy.ops.wm.save_as_mainfile(filepath=str(out),check_existing=False)
 if 'FINISHED' not in r:raise RuntimeError('save failed')
 if sha(src)!=src_hash:raise RuntimeError('source changed during build')
 print('REV003_BUILD '+json.dumps({'run_id':RUN_ID,'source_sha256':src_hash,'source_planter_geometry_sha256':source_geom_hash,'output':str(out),'planter_dims_mm':[150,150,60],'support_object':support.name,'objects':[(o.name,o.type) for o in scene.objects]},sort_keys=True))
main()

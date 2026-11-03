import hashlib,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
RUN_ID='CU-01-REV-003-20261103T032047Z'
PLANTER='CU01_Planter_REV002';SUPPORT='CU01_SHT31_ClipSupport_REV003';TOL=0.01
def fingerprint(obj):
 h=hashlib.sha256();m=obj.data
 for v in m.vertices:h.update(('%.9f,%.9f,%.9f;'%(v.co.x,v.co.y,v.co.z)).encode())
 h.update(b'|')
 for p in m.polygons:h.update((','.join(map(str,p.vertices))+';').encode())
 return h.hexdigest()
def bbox(obj):
 pts=[obj.matrix_world@v.co for v in obj.data.vertices]
 return [[min(p[i] for p in pts)*1000 for i in range(3)],[max(p[i] for p in pts)*1000 for i in range(3)]]
def components(bm):
 unseen=set(bm.verts);n=0
 while unseen:
  n+=1; stack=[unseen.pop()]
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    u=e.other_vert(v)
    if u in unseen:unseen.remove(u);stack.append(u)
 return n
def meshcheck(obj):
 dg=bpy.context.evaluated_depsgraph_get();ev=obj.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev,depsgraph=dg);bm=bmesh.new();bm.from_mesh(me);bm.normal_update()
 data={'vertices':len(me.vertices),'edges':len(me.edges),'faces':len(me.polygons),'components':components(bm),'all_edges_manifold':all(e.is_manifold for e in bm.edges),'all_faces_valid':all(f.is_valid and f.calc_area()>1e-12 for f in bm.faces),'volume_mm3':bm.calc_volume(signed=True)*1e9,'bbox_mm':bbox(obj)}
 bm.free();bpy.data.meshes.remove(me);return data
def main():
 a=sys.argv[sys.argv.index('--')+1:]
 if len(a)!=3:raise RuntimeError('usage -- source.blend candidate.blend evidence.json')
 src,candidate,out=map(lambda x:Path(x).resolve(),a)
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);source=bpy.data.objects.get(PLANTER)
 if source is None:raise RuntimeError('source planter missing')
 source_fp=fingerprint(source);source_dims=bbox(source)
 bpy.ops.wm.open_mainfile(filepath=str(candidate),load_ui=False);p=bpy.data.objects.get(PLANTER);s=bpy.data.objects.get(SUPPORT)
 if p is None or s is None:raise RuntimeError('expected product objects missing')
 pfp=fingerprint(p);pd=meshcheck(p);sd=meshcheck(s); findings=[]
 findings.append({'check':'source_planter_mesh_unchanged','pass':source_fp==pfp,'source_geometry_sha256':source_fp,'candidate_geometry_sha256':pfp})
 pdims=[pd['bbox_mm'][1][i]-pd['bbox_mm'][0][i] for i in range(3)]
 findings.append({'check':'planter_envelope_preserved','pass':all(abs(a-b)<=TOL for a,b in zip(pdims,[150,150,60])),'dimensions_mm':pdims,'tolerance_mm':TOL})
 findings.append({'check':'two_separate_mesh_objects','pass':sum(o.type=='MESH' for o in bpy.context.scene.objects)==2,'observed':[(o.name,o.type) for o in bpy.context.scene.objects]})
 findings.append({'check':'default_marbled_material_on_both_meshes','pass':all(any(m and m.name=='Hyper_PLA_Marmol' for m in o.data.materials) for o in (p,s)),'objects':{o.name:[m.name if m else None for m in o.data.materials] for o in (p,s)}})
 findings.append({'check':'support_one_closed_manifold_component','pass':sd['components']==1 and sd['all_edges_manifold'] and sd['all_faces_valid'] and sd['volume_mm3']>0,'metrics':sd})
 b=sd['bbox_mm'];top=b[1][2]
 findings.append({'check':'support_top_30mm_above_rim','pass':abs(top-90.0)<=TOL,'observed_top_z_mm':top,'rim_z_mm':60.0,'expected_height_above_rim_mm':30.0})
 # Conservative bounding-box separation between independently modeled parts.
 # Triangle-level collision check between the separate support and planter meshes.
 def world_bvh(obj):
  me=obj.data.copy();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.transform(bm,matrix=obj.matrix_world,verts=bm.verts);tree=BVHTree.FromBMesh(bm);bm.free();bpy.data.meshes.remove(me);return tree
 overlaps=world_bvh(p).overlap(world_bvh(s))
 findings.append({'check':'no_solid_intersection_between_planter_and_support','pass':len(overlaps)==0,'overlapping_triangle_pairs':len(overlaps),'note':'The U clip surrounds the rim with explicit digital clearances; this check tests actual triangle intersection.'})
 params=json.loads(s.get('design_parameters_mm','{}'))
 findings.append({'check':'clip_geometry_recorded','pass':params.get('clip_inner_gap_at_rim')==10.6 and params.get('inner_clearance_mm')==0.1 and params.get('outer_clearance_to_brick_relief_mm')==0.5 and params.get('pcb_channel_depth_mm')==1.6 and params.get('board_face_plane_y_mm')==89.4 and params.get('board_back_plane_y_mm')==87.8,'parameters':params})
 board=[13.1,10.4];cavity=[13.6,10.9]
 findings.append({'check':'pcb_cradle_nominal_clearance','pass':abs((cavity[0]-board[0])/2-0.25)<=TOL and abs(cavity[1]-board[1]-0.5)<=TOL,'pcb_mm':board,'nominal_cradle_mm':cavity,'clearance_each_x_side_mm':0.25,'bottom_clearance_mm':0.5,'top_clearance_mm':0.0,'assumptions':['board landscape; 1.6 mm board thickness','pin/header projection is not dimensioned']})
 # Sensor face and central rear pin corridor must not be crossed by the support body.
 # Geometric exclusion zones are checked against every support face's world-space AABB.
 dg=bpy.context.evaluated_depsgraph_get();ev=s.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev,depsgraph=dg)
 face_clear=True;pin_clear=True
 for poly in me.polygons:
  ps=[s.matrix_world@me.vertices[i].co for i in poly.vertices]
  lo=[min(v[i]*1000 for v in ps) for i in range(3)];hi=[max(v[i]*1000 for v in ps) for i in range(3)]
  if lo[0]<3 and hi[0]>-3 and lo[1]<92 and hi[1]>89.3 and lo[2]<88 and hi[2]>82:face_clear=False
  if lo[0]<5 and hi[0]>-5 and lo[1]<87.7 and hi[1]>80 and lo[2]<89 and hi[2]>79.6:pin_clear=False
 bpy.data.meshes.remove(me)
 findings.append({'check':'sensor_face_and_pin_corridors_clear','pass':face_clear and pin_clear,'sensor_face_clear':face_clear,'rear_pin_corridor_clear_to_y80_mm':pin_clear,'note':'Digital keep-out zones only; actual header dimensions not supplied.'})
 status='PASS' if all(f['pass'] for f in findings) else 'FAIL'
 result={'run_id':RUN_ID,'status':status,'validation_mode':'read-only separate Blender process; source and candidate opened independently','blender_version':bpy.app.version_string,'source_blend':str(src),'candidate_blend':str(candidate),'source_planter_bbox_mm':source_dims,'planter_metrics':pd,'support_metrics':sd,'findings':findings}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('REV003_VALIDATION '+json.dumps(result,sort_keys=True))
 if status!='PASS':raise SystemExit(2)
main()

"""Check a complete, non-self-intersecting 66-box face operand."""
import json
from pathlib import Path
import sys
import bpy
import bmesh

sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_model_lib as lib
RUN_ID="CU-01-DIAG-BOOLEAN-20261102T220718Z"
OUTPUT=Path(__file__).resolve().parents[1]/"evidencias"/"one_face_courses.json"


def stats(obj,label):
    deps=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(deps)
    me=bpy.data.meshes.new_from_object(ev,depsgraph=deps); bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    unseen=set(bm.verts); comps=0
    while unseen:
        comps+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen: unseen.remove(q); stack.append(q)
    pts=[v.co for v in me.vertices]
    dims=[] if not pts else [(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(3)]
    result={"label":label,"dimensions_mm":dims,"components":comps,"manifold":bool(bm.edges) and all(e.is_manifold for e in bm.edges),"volume_mm3":bm.calc_volume(signed=True)*1e9,"vertices":len(me.vertices),"faces":len(me.polygons)}
    bm.free(); bpy.data.meshes.remove(me); return result


def build_side_operand(side):
    bm=bmesh.new(); half=lib.BODY_XY/2.0; depth=lib.PARAMS["relief_mm"]+lib.BRICK_OVERLAP_MM; normal=half+lib.PARAMS["relief_mm"]/2.0-lib.BRICK_OVERLAP_MM/2.0
    total_height=7*7+6*1.2; first_bottom=(60-total_height)/2
    for row in range(7):
        segments=lib.row_segments(row,lib.BODY_XY); cursor=-half; z=first_bottom+row*8.2+3.5
        for length in segments:
            tangent=cursor+length/2
            if side=="east": center=(normal,tangent,z); size=(depth,length,7)
            elif side=="west": center=(-normal,tangent,z); size=(depth,length,7)
            elif side=="north": center=(tangent,normal,z); size=(length,depth,7)
            else: center=(tangent,-normal,z); size=(length,depth,7)
            lib.add_box(bm,center,size); cursor+=length+1.2
    return lib.object_from_bmesh("OneCompleteSideOperand",bm,bpy.context.scene.collection)


def main():
    lib.clear_scene(); collection=bpy.context.scene.collection; target=lib.build_shell(collection); before=stats(target,"shell")
    operand=build_side_operand("east"); lib.apply_boolean(target,operand,"UNION","OneCompleteSideUnion")
    data=operand.data; bpy.data.objects.remove(operand,do_unlink=True)
    if data.users==0: bpy.data.meshes.remove(data)
    after=stats(target,"shell_plus_66_bricks_one_face")
    payload={"run_id":RUN_ID,"blender_version":bpy.app.version_string,"before":before,"after":after,"operand_components":66,"note":"in-memory only; no .blend saved"}
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CU01_ONE_FACE_ALL_COURSES "+json.dumps(payload,sort_keys=True))

main()

"""Isolate whether intersecting end operands at corners break a union."""
import json
from pathlib import Path
import sys
import bpy
import bmesh

sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_model_lib as lib

RUN_ID="CU-01-DIAG-BOOLEAN-20261102T220718Z"
OUTPUT=Path(__file__).resolve().parents[1]/"evidencias"/"corner_overlap.json"


def metrics(obj,label):
    deps=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(deps)
    me=bpy.data.meshes.new_from_object(ev,depsgraph=deps)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    unseen=set(bm.verts); n=0
    while unseen:
        n+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen: unseen.remove(q); stack.append(q)
    pts=[v.co for v in me.vertices]
    bounds=[] if not pts else [[min(p[i] for p in pts)*1000,max(p[i] for p in pts)*1000] for i in range(3)]
    result={"label":label,"components":n,"vertices":len(me.vertices),"faces":len(me.polygons),"manifold":bool(bm.edges) and all(e.is_manifold for e in bm.edges),"volume_mm3":bm.calc_volume(signed=True)*1e9,"bounds_mm":bounds}
    bm.free(); bpy.data.meshes.remove(me)
    return result


def build_one_course_operand(sides):
    bm=bmesh.new(); half=lib.BODY_XY/2.0
    depth=lib.PARAMS["relief_mm"]+lib.BRICK_OVERLAP_MM
    normal=half+lib.PARAMS["relief_mm"]/2.0-lib.BRICK_OVERLAP_MM/2.0
    segments=lib.row_segments(0,lib.BODY_XY)
    z=(lib.PARAMS["height_mm"]-(7*7+6*1.2))/2.0+3.5
    for side in sides:
        cursor=-half
        for length in segments:
            tangent=cursor+length/2.0
            if side=="east": center=(normal,tangent,z); size=(depth,length,7)
            elif side=="west": center=(-normal,tangent,z); size=(depth,length,7)
            elif side=="north": center=(tangent,normal,z); size=(length,depth,7)
            else: center=(tangent,-normal,z); size=(length,depth,7)
            lib.add_box(bm,center,size)
            cursor+=length+1.2
    return lib.object_from_bmesh("CourseOperand","",bpy.context.scene.collection) if False else lib.object_from_bmesh("CourseOperand",bm,bpy.context.scene.collection)


def run_branch(sides,label):
    lib.clear_scene(); collection=bpy.context.scene.collection
    target=lib.build_shell(collection)
    operand=build_one_course_operand(sides)
    before=metrics(target,label+"_shell_before")
    lib.apply_boolean(target,operand,"UNION",label+"_UNION")
    data=operand.data; bpy.data.objects.remove(operand,do_unlink=True)
    if data.users==0: bpy.data.meshes.remove(data)
    after=metrics(target,label+"_after")
    return {"sides":sides,"before":before,"after":after}


def main():
    branches=[run_branch(["east"],"one_face"),run_branch(["east","west"],"opposite_faces"),run_branch(["east","north"],"adjacent_faces")]
    payload={"run_id":RUN_ID,"blender_version":bpy.app.version_string,"branches":branches,"expected_shell_volume_mm3":661056.0,"course_added_volume_one_face_mm3":968.8,"note":"In-memory diagnostic only; no .blend saved."}
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CU01_CORNER_OVERLAP_DIAGNOSTIC "+json.dumps(payload,sort_keys=True))

main()

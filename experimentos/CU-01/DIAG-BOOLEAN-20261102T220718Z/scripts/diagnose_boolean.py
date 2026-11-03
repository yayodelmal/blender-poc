"""Read-only in-memory isolation of cavity and Boolean batch effects."""
import json
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_model_lib as lib

RUN_ID = "CU-01-DIAG-BOOLEAN-20261102T220718Z"
OUTPUT = Path(__file__).resolve().parents[1] / "evidencias" / "boolean_branches.json"


def components(bm):
    unseen=set(bm.verts); n=0
    while unseen:
        n += 1
        stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen:
                    unseen.remove(q); stack.append(q)
    return n


def stats(obj, label):
    deps=bpy.context.evaluated_depsgraph_get()
    ev=obj.evaluated_get(deps)
    mesh=bpy.data.meshes.new_from_object(ev,depsgraph=deps)
    bm=bmesh.new(); bm.from_mesh(mesh); bm.normal_update()
    pts=[obj.matrix_world@v.co for v in mesh.vertices]
    bounds=[] if not pts else [[min(p[i] for p in pts)*1000.0,max(p[i] for p in pts)*1000.0] for i in range(3)]
    result={"label":label,"vertices":len(mesh.vertices),"faces":len(mesh.polygons),"components":components(bm),"manifold":bool(bm.edges) and all(e.is_manifold for e in bm.edges),"volume_mm3":bm.calc_volume(signed=True)*1e9,"bounds_mm":bounds}
    bm.free(); bpy.data.meshes.remove(mesh)
    return result


def duplicate(source, name):
    obj=source.copy(); obj.data=source.data.copy(); obj.name=name
    bpy.context.scene.collection.objects.link(obj)
    return obj


def make_first_course():
    bm=bmesh.new()
    wall_half=lib.BODY_XY/2.0
    depth=lib.PARAMS["relief_mm"]+lib.BRICK_OVERLAP_MM
    normal_center=wall_half+lib.PARAMS["relief_mm"]/2.0-lib.BRICK_OVERLAP_MM/2.0
    row=0
    segments=lib.row_segments(row,lib.BODY_XY)
    cursor=-wall_half
    z_bottom=(lib.PARAMS["height_mm"]-(7*lib.PARAMS["brick_height_mm"]+6*lib.PARAMS["joint_mm"])) / 2.0
    z_center=z_bottom+lib.PARAMS["brick_height_mm"]/2.0
    for side in ("east","west","north","south"):
        cursor=-wall_half
        for length in segments:
            tangent=cursor+length/2.0
            if side=="east": center=(normal_center,tangent,z_center); size=(depth,length,lib.PARAMS["brick_height_mm"])
            elif side=="west": center=(-normal_center,tangent,z_center); size=(depth,length,lib.PARAMS["brick_height_mm"])
            elif side=="north": center=(tangent,normal_center,z_center); size=(length,depth,lib.PARAMS["brick_height_mm"])
            else: center=(tangent,-normal_center,z_center); size=(length,depth,lib.PARAMS["brick_height_mm"])
            lib.add_box(bm,center,size)
            cursor += length+lib.PARAMS["joint_mm"]
    return lib.object_from_bmesh("CU01_DebugFirstCourse",bm,bpy.context.scene.collection)


def union(target, operand, label):
    lib.apply_boolean(target,operand,"UNION",label)
    data=operand.data
    bpy.data.objects.remove(operand,do_unlink=True)
    if data.users==0: bpy.data.meshes.remove(data)


def main():
    lib.clear_scene()
    collection=bpy.context.scene.collection
    shell=lib.build_shell(collection)
    result=[stats(shell,"shell_after_difference")]

    one_target=duplicate(shell,"CU01_DebugOneCourseTarget")
    one_operand=make_first_course()
    union(one_target,one_operand,"Debug_OneCourse_Union")
    result.append(stats(one_target,"shell_plus_one_course_36_boxes"))

    all_target=duplicate(shell,"CU01_DebugFullTarget")
    all_operand,pattern=lib.build_bricks(collection)
    union(all_target,all_operand,"Debug_AllCourses_Union")
    result.append(stats(all_target,"shell_plus_all_courses_264_boxes"))

    payload={"run_id":RUN_ID,"blender_version":bpy.app.version_string,"branches":result,"pattern":pattern,"note":"No .blend was saved; all branches were measured in memory and in this diagnostic process."}
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CU01_BOOLEAN_DIAGNOSTIC "+json.dumps(payload,sort_keys=True))
    if any(not branch["manifold"] for branch in result):
        print("CU01_BOOLEAN_DIAGNOSTIC_NONMANIFOLD")


main()

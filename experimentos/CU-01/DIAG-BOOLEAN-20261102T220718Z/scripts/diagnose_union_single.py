"""Compare one-box Boolean UNION on hollow and solid targets, without saving."""
import json
from pathlib import Path
import sys
import bpy
import bmesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_model_lib as lib

RUN_ID="CU-01-DIAG-BOOLEAN-20261102T220718Z"
OUTPUT=Path(__file__).resolve().parents[1]/"evidencias"/"single_union.json"


def metrics(obj,label):
    deps=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(deps)
    me=bpy.data.meshes.new_from_object(ev,depsgraph=deps)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    pts=[v.co for v in me.vertices]
    bounds=[] if not pts else [[min(p[i] for p in pts)*1000,max(p[i] for p in pts)*1000] for i in range(3)]
    res={"label":label,"object":obj.name,"mesh_vertices":len(me.vertices),"mesh_faces":len(me.polygons),"bounds_mm":bounds,"volume_mm3":bm.calc_volume(signed=True)*1e9,"components":len({v for v in bm.verts})}
    bm.free(); bpy.data.meshes.remove(me)
    return res


def one_brick(collection):
    bm=bmesh.new()
    body_half=lib.BODY_XY/2
    normal=body_half+lib.PARAMS["relief_mm"]/2-lib.BRICK_OVERLAP_MM/2
    length=lib.row_segments(0,lib.BODY_XY)[0]
    z=(lib.PARAMS["height_mm"]-(7*7+6*1.2))/2+3.5
    tangent=-body_half+length/2
    lib.add_box(bm,(normal,tangent,z),(1.2,length,7.0))
    return lib.object_from_bmesh("OneBrickOperand",bm,collection)


def add_union_modifier(target,operand):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True); operand.select_set(False)
    bpy.context.view_layer.objects.active=target
    mod=target.modifiers.new("ProbeUnion","BOOLEAN")
    mod.operation="UNION"; mod.solver="EXACT"; mod.object=operand
    return mod


def main():
    lib.clear_scene(); collection=bpy.context.scene.collection
    hollow=lib.build_shell(collection)
    results=[metrics(hollow,"hollow_shell_before_union")]
    brick=one_brick(collection)
    results.append(metrics(brick,"one_brick_operand"))
    mod=add_union_modifier(hollow,brick)
    deps=bpy.context.evaluated_depsgraph_get(); bpy.context.view_layer.update()
    results.append(metrics(hollow,"hollow_shell_with_unapplied_union"))
    active=bpy.context.view_layer.objects.active
    apply_result=bpy.ops.object.modifier_apply(modifier=mod.name)
    results.append({"label":"modifier_apply_context","active_object":active.name if active else None,"apply_result":list(apply_result)})
    results.append(metrics(hollow,"hollow_shell_after_applied_union"))

    lib.clear_scene(); collection=bpy.context.scene.collection
    bm=bmesh.new(); lib.add_box(bm,(0,0,30),(148,148,60))
    plate=lib.object_from_bmesh("SolidPlateTarget",bm,collection)
    brick=one_brick(collection)
    mod=add_union_modifier(plate,brick); bpy.context.view_layer.update()
    results.append(metrics(plate,"solid_target_with_unapplied_union"))
    apply_result=bpy.ops.object.modifier_apply(modifier=mod.name)
    results.append({"label":"solid_modifier_apply_context","active_object":bpy.context.view_layer.objects.active.name,"apply_result":list(apply_result)})
    results.append(metrics(plate,"solid_target_after_applied_union"))
    payload={"run_id":RUN_ID,"blender_version":bpy.app.version_string,"observations":results}
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("CU01_SINGLE_UNION_DIAGNOSTIC "+json.dumps(payload,sort_keys=True))

main()

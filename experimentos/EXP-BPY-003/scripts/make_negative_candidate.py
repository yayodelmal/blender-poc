"""Create isolated controlled negative .blend copies; never edits source in place."""
import json
import os
import sys

import bpy
import bmesh
from mathutils import Vector

OBJECT_NAME = "EXP-BPY-003_ReliefPlate"
RUN_ID = "EXP-BPY-003-20261102T144300Z"


def main():
    if "--" not in sys.argv:
        raise RuntimeError("Expected JSON spec after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected exactly one JSON spec")
    spec = json.loads(args[0])
    output = os.path.abspath(spec["output_path"])
    if os.path.lexists(output):
        raise FileExistsError("Refusing overwrite: " + output)
    obj = bpy.data.objects.get(OBJECT_NAME)
    if obj is None:
        raise RuntimeError("Relief plate missing")
    kind = spec["kind"]
    if kind == "disconnected_brick":
        bm = bmesh.new()
        created = bmesh.ops.create_cube(bm, size=2.0)
        half = Vector((3.0, 2.5, 0.5)) * 0.001
        center = Vector((0.0, 0.0, 5.5)) * 0.001
        for v in created["verts"]:
            v.co.x = center.x + v.co.x * half.x
            v.co.y = center.y + v.co.y * half.y
            v.co.z = center.z + v.co.z * half.z
        mesh = bpy.data.meshes.new("NEGATIVE_DisconnectedBrick_Mesh")
        bm.to_mesh(mesh)
        bm.free()
        extra = bpy.data.objects.new("NEGATIVE_DisconnectedBrick", mesh)
        bpy.context.scene.collection.objects.link(extra)
        extra["negative_control"] = "floating brick: 0.5 mm above plate top"
    elif kind == "dimension_out_of_tolerance":
        for vertex in obj.data.vertices:
            vertex.co.x *= 80.05 / 80.0
        obj.data.update()
        obj["negative_control"] = "X dimension increased to 80.05 mm"
    else:
        raise ValueError("Unsupported negative kind")
    bpy.context.view_layer.update()
    result = bpy.ops.wm.save_as_mainfile(filepath=output, check_existing=False)
    if "FINISHED" not in result:
        raise RuntimeError("Could not save negative candidate")
    print("EXP_BPY_003_NEGATIVE " + json.dumps({"status": "PASS", "kind": kind, "source_file": spec["source_file"], "output_path": bpy.data.filepath, "objects": [x.name for x in bpy.context.scene.objects]}, sort_keys=True))


if __name__ == "__main__":
    main()

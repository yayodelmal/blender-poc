"""Create a new .blend copy with a useful initial viewport; preserve input file."""
import hashlib
import json
import os
import sys

import bpy
from mathutils import Vector

SOURCE_SHA256 = "09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b"
OBJECT_NAME = "EXP-BPY-003_ReliefPlate"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    if "--" not in sys.argv or len(sys.argv[sys.argv.index("--") + 1:]) != 1:
        raise RuntimeError("Expected one new output path after --")
    output = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
    source = os.path.abspath(bpy.data.filepath)
    if os.path.lexists(output):
        raise FileExistsError("Refusing to overwrite: " + output)
    observed_sha = sha256(source)
    if observed_sha != SOURCE_SHA256:
        raise RuntimeError("Source checksum differs from validated master; refusing copy")
    obj = bpy.data.objects.get(OBJECT_NAME)
    if obj is None or obj.type != "MESH":
        raise RuntimeError("Expected validated model is missing")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                view = area.spaces.active.region_3d
                view.view_location = Vector((0.0, 0.0, 0.0025))
                view.view_distance = 0.20
                view.view_perspective = "PERSP"
    saved = bpy.ops.wm.save_as_mainfile(filepath=output, check_existing=False)
    if "FINISHED" not in saved:
        raise RuntimeError("Could not save open-ready copy")
    print("EXP_BPY_003_OPEN_READY " + json.dumps({
        "status": "PASS",
        "source_path": source,
        "source_sha256_before": observed_sha,
        "saved_copy": bpy.data.filepath,
        "object": obj.name,
        "object_selected": obj.select_get(),
        "layout_view_distance_blender_units": 0.20,
        "view_location_m": [0.0, 0.0, 0.0025],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

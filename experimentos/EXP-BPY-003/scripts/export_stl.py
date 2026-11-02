"""Export selected validated relief geometry to STL with explicit scale and axes."""
import json
import os
import sys

import bpy

OBJECT_NAME = "EXP-BPY-003_ReliefPlate"


def main():
    if "--" not in sys.argv:
        raise RuntimeError("Expected JSON export specification after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected exactly one JSON specification")
    spec = json.loads(args[0])
    output = os.path.abspath(spec["output_path"])
    if os.path.lexists(output):
        raise FileExistsError("Refusing to overwrite STL: " + output)
    obj = bpy.data.objects.get(OBJECT_NAME)
    if obj is None:
        raise RuntimeError("Expected relief plate is missing")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    scale = float(spec["global_scale"])
    result = bpy.ops.wm.stl_export(
        filepath=output,
        check_existing=False,
        ascii_format=False,
        export_selected_objects=True,
        global_scale=scale,
        use_scene_unit=False,
        forward_axis="Y",
        up_axis="Z",
        apply_modifiers=True,
        evaluation_mode="DAG_EVAL_VIEWPORT",
    )
    if "FINISHED" not in result or not os.path.isfile(output) or os.path.getsize(output) == 0:
        raise RuntimeError("STL export failed or produced an empty file")
    print("EXP_BPY_003_STL_EXPORT " + json.dumps({"status": "PASS", "source_blend": bpy.data.filepath, "stl_path": output, "object": obj.name, "global_scale": scale, "use_scene_unit": False, "forward_axis": "Y", "up_axis": "Z", "selected_only": True, "result": list(result)}, sort_keys=True))


if __name__ == "__main__":
    main()

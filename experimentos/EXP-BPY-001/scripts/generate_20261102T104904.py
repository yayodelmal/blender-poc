"""Generate the isolated parametric cube for EXP-BPY-001."""
import json
import os
import sys

import bpy


RUN_ID = "EXP-BPY-001-20261102T104904-0300"
PARAMETERS_MM = {"x": 50.0, "y": 50.0, "z": 50.0}
OBJECT_NAME = "EXP-BPY-001_Cube_20261102T104904"


def output_path():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if not args:
        raise RuntimeError("Expected output .blend path after --")
    return os.path.abspath(args[0])


def main():
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Factory startup and this explicit clear make scene contents deterministic.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0  # one Blender unit equals one meter
    scene.unit_settings.length_unit = "MILLIMETERS"

    hx, hy, hz = (PARAMETERS_MM[key] / 2000.0 for key in ("x", "y", "z"))
    vertices = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
        (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    mesh = bpy.data.meshes.new(OBJECT_NAME + "_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(OBJECT_NAME, mesh)
    scene.collection.objects.link(obj)
    obj.location = (0.0, 0.0, 0.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    obj["experiment_id"] = RUN_ID
    obj["parameters_mm"] = json.dumps(PARAMETERS_MM, sort_keys=True)
    obj["parameter_units"] = "mm"
    obj["construction"] = "Centered mesh vertices derived from script PARAMETERS_MM"

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    result = bpy.ops.wm.save_as_mainfile(filepath=path, check_existing=False)
    if "FINISHED" not in result:
        raise RuntimeError("Blender did not report a successful save: " + repr(result))

    print("EXP_BPY_GENERATION " + json.dumps({
        "run_id": RUN_ID,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "bpy_available": True,
        "blend_path": bpy.data.filepath,
        "object_name": obj.name,
        "parameters_mm": PARAMETERS_MM,
        "scene_units": scene.unit_settings.system,
        "scene_scale_length": scene.unit_settings.scale_length,
        "object_scale": list(obj.scale),
        "save_result": sorted(result),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

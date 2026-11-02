"""Apply one parameter change to the existing mesh and save only to a new path."""
import json
import math
import os
import sys

import bpy


EXPECTED_OBJECT = "EXP-BPY-001_Cube_20261102T105936"
EXPECTED_MESH = EXPECTED_OBJECT + "_Mesh"
EXPECTED_EXPERIMENT_ID = "EXP-BPY-001-20261102T105936-0300"


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected JSON edit specification after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected exactly one JSON edit specification")
    return json.loads(args[0])


def dimensions_mm(obj):
    points = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
    mins = [min(point[i] for point in points) for i in range(3)]
    maxs = [max(point[i] for point in points) for i in range(3)]
    return [(maxs[i] - mins[i]) * 1000.0 for i in range(3)]


def main():
    spec = args_after_separator()
    output_path = os.path.abspath(spec["output_path"])
    if os.path.lexists(output_path):
        raise FileExistsError("Refusing to overwrite an existing candidate: " + output_path)
    if not bpy.data.filepath:
        raise RuntimeError("No input .blend is open")

    scene = bpy.context.scene
    if len(scene.objects) != 1:
        raise RuntimeError("Unexpected scene object count")
    obj = bpy.data.objects.get(EXPECTED_OBJECT)
    if obj is None or obj.type != "MESH" or obj.data.name != EXPECTED_MESH or obj.get("experiment_id") != EXPECTED_EXPERIMENT_ID:
        raise RuntimeError("Input object identity does not match EXP-BPY-001")
    if len(obj.modifiers) != 0 or obj.data.shape_keys is not None:
        raise RuntimeError("Refusing to edit a mesh with modifiers or shape keys")

    params = json.loads(obj.get("parameters_mm", "{}"))
    if params != spec["expected_current_parameters_mm"] or obj.get("parameter_units") != "mm":
        raise RuntimeError("Input parameter metadata does not match expected base state")
    current_dims = dimensions_mm(obj)
    axes = {"x": 0, "y": 1, "z": 2}
    axis = spec["axis"]
    if axis not in axes:
        raise ValueError("axis must be x, y, or z")
    axis_index = axes[axis]
    current_dimension = current_dims[axis_index]
    target_dimension = float(spec["target_mm"])
    if target_dimension <= 0.0 or current_dimension <= 0.0:
        raise ValueError("Dimensions must be positive")

    object_pointer_before = obj.as_pointer()
    mesh_pointer_before = obj.data.as_pointer()
    vertex_count_before = len(obj.data.vertices)
    mesh = obj.data
    local_values = [vertex.co[axis_index] for vertex in mesh.vertices]
    local_min = min(local_values)
    local_max = max(local_values)
    local_center = (local_min + local_max) / 2.0
    ratio = target_dimension / current_dimension
    for vertex in mesh.vertices:
        vertex.co[axis_index] = local_center + (vertex.co[axis_index] - local_center) * ratio
    mesh.update()

    params[axis] = target_dimension
    obj["parameters_mm"] = json.dumps(params, sort_keys=True)
    obj["revision_id"] = spec["revision_id"]
    obj["revision_base_sha256"] = spec["base_sha256"]
    obj["last_edit"] = "scaled existing mesh vertex coordinates along " + axis.upper() + " about geometric center"

    if obj.as_pointer() != object_pointer_before or obj.data.as_pointer() != mesh_pointer_before or len(mesh.vertices) != vertex_count_before:
        raise RuntimeError("Object or mesh datablock was replaced during edit")
    after_dims = dimensions_mm(obj)
    expected_after = [params["x"], params["y"], params["z"]]
    if any(abs(after_dims[i] - expected_after[i]) > 0.01 for i in range(3)):
        raise RuntimeError("Edited geometry does not match updated parameter values")
    if "FINISHED" not in bpy.ops.wm.save_as_mainfile(filepath=output_path, check_existing=False):
        raise RuntimeError("Blender did not confirm candidate save")

    print("EXP_BPY_002_EDIT " + json.dumps({
        "status": "PASS",
        "source_file": spec.get("source_file", ""),
        "saved_candidate": bpy.data.filepath,
        "revision_id": spec["revision_id"],
        "revision_base_sha256": spec["base_sha256"],
        "axis_changed": axis,
        "target_mm": target_dimension,
        "dimensions_before_mm": dict(zip(("x", "y", "z"), current_dims)),
        "dimensions_after_mm": dict(zip(("x", "y", "z"), after_dims)),
        "parameters_after_mm": params,
        "object_pointer_preserved": obj.as_pointer() == object_pointer_before,
        "mesh_pointer_preserved": obj.data.as_pointer() == mesh_pointer_before,
        "vertex_count_preserved": len(mesh.vertices) == vertex_count_before,
        "object_name": obj.name,
        "mesh_name": mesh.name,
        "python_version": sys.version.split()[0],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

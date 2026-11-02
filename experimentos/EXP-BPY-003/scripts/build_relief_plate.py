"""Build one editable brick-relief plate using an exact boolean union."""
import json
import math
import os
import sys

import bpy
import bmesh
from mathutils import Vector

RUN_ID = "EXP-BPY-003-20261102T144300Z"
PARAMETERS_MM = {
    "plate_width": 80.0,
    "plate_height": 60.0,
    "base_thickness": 4.0,
    "relief_height": 1.0,
    "brick_length": 18.0,
    "brick_height": 8.4,
    "joint": 1.2,
    "rows": 6,
    "row_pitch": 9.6,
    "brick_pitch_x": 19.2,
    "overlap_into_base": 0.5,
    "edge_margin": 0.6,
}
OBJECT_NAME = "EXP-BPY-003_ReliefPlate"


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected output .blend path after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected exactly one output path")
    return os.path.abspath(args[0])


def add_box(bm, center_mm, size_mm):
    # BMesh's `size` is the side length; size=2 gives unit half-extents for scaling below.
    result = bmesh.ops.create_cube(bm, size=2.0)
    # Blender's scene scale_length=1 stores coordinates in metres; convert inputs from mm.
    half = Vector(size_mm) * 0.0005
    center = Vector(center_mm) * 0.001
    for vert in result["verts"]:
        vert.co.x = center.x + vert.co.x * half.x
        vert.co.y = center.y + vert.co.y * half.y
        vert.co.z = center.z + vert.co.z * half.z
    return result["verts"]


def intervals_for_row(row_index):
    edge = PARAMETERS_MM["plate_width"] * 0.5 - PARAMETERS_MM["edge_margin"]
    length = PARAMETERS_MM["brick_length"]
    pitch = PARAMETERS_MM["brick_pitch_x"]
    phase = -0.5 * pitch if row_index % 2 else 0.0
    first_start = -0.5 * (4 * length + 3 * PARAMETERS_MM["joint"]) + phase
    intervals = []
    k = 0
    while first_start + k * pitch < edge:
        start = first_start + k * pitch
        end = start + length
        clipped_start, clipped_end = max(-edge, start), min(edge, end)
        # Keep clipped half-bricks printable; avoid tiny sliver fragments at the edge.
        if clipped_end - clipped_start >= PARAMETERS_MM["brick_length"] * 0.45:
            intervals.append((clipped_start, clipped_end))
        k += 1
    return intervals


def main():
    output_path = args_after_separator()
    if os.path.lexists(output_path):
        raise FileExistsError("Refusing to overwrite: " + output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    scene = bpy.context.scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = "MILLIMETERS"

    plate_bm = bmesh.new()
    base_dims = (PARAMETERS_MM["plate_width"], PARAMETERS_MM["plate_height"], PARAMETERS_MM["base_thickness"])
    add_box(plate_bm, (0.0, 0.0, base_dims[2] * 0.5), base_dims)
    base_mesh = bpy.data.meshes.new(OBJECT_NAME + "_Mesh")
    plate_bm.to_mesh(base_mesh)
    plate_bm.free()
    plate = bpy.data.objects.new(OBJECT_NAME, base_mesh)
    scene.collection.objects.link(plate)

    brick_bm = bmesh.new()
    brick_intervals = []
    rows = PARAMETERS_MM["rows"]
    pitch_y = PARAMETERS_MM["row_pitch"]
    brick_y = PARAMETERS_MM["brick_height"]
    total_span_y = rows * brick_y + (rows - 1) * PARAMETERS_MM["joint"]
    first_y = -total_span_y * 0.5
    for row in range(rows):
        y0 = first_y + row * pitch_y
        y1 = y0 + brick_y
        for x0, x1 in intervals_for_row(row):
            brick_intervals.append((x0, x1, y0, y1))
            add_box(
                brick_bm,
                ((x0 + x1) * 0.5, (y0 + y1) * 0.5, PARAMETERS_MM["base_thickness"] + PARAMETERS_MM["relief_height"] * 0.5 - PARAMETERS_MM["overlap_into_base"] * 0.5),
                (x1 - x0, y1 - y0, PARAMETERS_MM["relief_height"] + PARAMETERS_MM["overlap_into_base"]),
            )
    bricks_mesh = bpy.data.meshes.new("EXP-BPY-003_BrickOperands_Mesh")
    brick_bm.to_mesh(bricks_mesh)
    brick_bm.free()
    bricks_obj = bpy.data.objects.new("EXP-BPY-003_TemporaryBrickOperands", bricks_mesh)
    scene.collection.objects.link(bricks_obj)

    bpy.context.view_layer.objects.active = plate
    plate.select_set(True)
    bricks_obj.select_set(False)
    modifier = plate.modifiers.new("EXP003_ExactReliefUnion", "BOOLEAN")
    modifier.operation = "UNION"
    modifier.solver = "EXACT"
    modifier.object = bricks_obj
    result = bpy.ops.object.modifier_apply(modifier=modifier.name)
    if "FINISHED" not in result:
        raise RuntimeError("Exact boolean union did not finish")
    bpy.data.objects.remove(bricks_obj, do_unlink=True)
    bpy.data.meshes.remove(bricks_mesh)

    plate["experiment_id"] = RUN_ID
    plate["parameters_mm"] = json.dumps(PARAMETERS_MM, sort_keys=True)
    plate["parameter_units"] = "mm"
    plate["brick_count"] = len(brick_intervals)
    plate["editability_note"] = "Rebuild by rerunning this script; parameter values stored as metadata and are not reactive."
    plate["construction"] = "base mesh plus exact boolean union of overlapping brick solids"
    plate.data["expected_brick_count"] = len(brick_intervals)
    plate.data["pattern_id"] = "staggered_rectangular_bricks_v1"

    # Save a useful first-open view: the plate is 80 mm wide while Blender distances are metres.
    plate.select_set(True)
    bpy.context.view_layer.objects.active = plate
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                region_3d = area.spaces.active.region_3d
                region_3d.view_location = Vector((0.0, 0.0, 0.0025))
                region_3d.view_distance = 0.20
                region_3d.view_perspective = "PERSP"

    scene.render.resolution_percentage = 100
    bpy.context.view_layer.update()
    if os.path.lexists(output_path):
        raise FileExistsError("Refusing to overwrite: " + output_path)
    saved = bpy.ops.wm.save_as_mainfile(filepath=output_path, check_existing=False)
    if "FINISHED" not in saved:
        raise RuntimeError("Saving .blend did not finish")
    footprints = [(x1 - x0) * (y1 - y0) for x0, x1, y0, y1 in brick_intervals]
    print("EXP_BPY_003_BUILD " + json.dumps({
        "status": "PASS",
        "run_id": RUN_ID,
        "saved_path": bpy.data.filepath,
        "object_name": plate.name,
        "mesh_name": plate.data.name,
        "parameters_mm": PARAMETERS_MM,
        "brick_count": len(brick_intervals),
        "brick_footprint_area_mm2": sum(footprints),
        "objects_after_build": [obj.name for obj in scene.objects],
        "modifiers_after_build": len(plate.modifiers),
        "python": sys.version.split()[0],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

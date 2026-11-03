"""Build CU-01 revision 001 as a new, parameterized bpy reconstruction."""
import json
import os
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Euler, Vector

RUN_ID = "CU-01-REV-002-20261103T023400Z"
PARAMS = {
    "envelope_x_mm": 150.0,
    "envelope_y_mm": 150.0,
    "height_mm": 60.0,
    "wall_mm": 10.0,
    "base_mm": 4.0,
    "drainage_holes": 0,
    "brick_length_mm": 15.0,
    "brick_height_mm": 7.0,
    "joint_mm": 1.2,
    "relief_mm": 1.0,
    "layout": "alternating bond, fitted end pieces, all four walls",
    "corner_continuity": "relief courses meet at each square corner; shell is one connected solid",
    "validation_tolerance_mm": 0.01,
}
BODY_XY = PARAMS["envelope_x_mm"] - 2.0 * PARAMS["relief_mm"]
INNER_XY = BODY_XY - 2.0 * PARAMS["wall_mm"]
BRICK_OVERLAP_MM = 0.2
OBJECT_NAME = "CU01_Planter_REV002"


def parse_output():
    if "--" not in sys.argv:
        raise RuntimeError("expected output .blend path after --")
    args = sys.argv[sys.argv.index("--") + 1 :]
    if len(args) != 1:
        raise RuntimeError("expected exactly one output .blend path")
    return Path(args[0]).resolve()


def add_box(bm, center_mm, size_mm):
    geom = bmesh.ops.create_cube(bm, size=2.0)
    half = Vector(size_mm) / 2000.0
    center = Vector(center_mm) / 1000.0
    for vert in geom["verts"]:
        vert.co = center + Vector((vert.co.x * half.x, vert.co.y * half.y, vert.co.z * half.z))


def object_from_bmesh(name, bm, collection):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def apply_boolean(target, operand, operation, label):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    operand.select_set(False)
    bpy.context.view_layer.objects.active = target
    modifier = target.modifiers.new(label, "BOOLEAN")
    modifier.operation = operation
    modifier.solver = "EXACT"
    modifier.object = operand
    result = bpy.ops.object.modifier_apply(modifier=modifier.name)
    if "FINISHED" not in result:
        raise RuntimeError(f"Boolean {operation} did not finish: {result}")


def row_segments(row_index, wall_length_mm):
    # The two end units are fitted to keep 1.2 mm joints and carry the bond
    # to the wall corners. Interior units remain 15 mm long.
    if row_index % 2 == 0:
        interior_count = 7
    else:
        interior_count = 8
    gaps = interior_count + 1
    end_length = (wall_length_mm - interior_count * PARAMS["brick_length_mm"] - gaps * PARAMS["joint_mm"]) / 2.0
    return [end_length] + [PARAMS["brick_length_mm"]] * interior_count + [end_length]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = "MILLIMETERS"
    return scene


def build_shell(collection):
    bm = bmesh.new()
    add_box(bm, (0.0, 0.0, PARAMS["height_mm"] / 2.0), (BODY_XY, BODY_XY, PARAMS["height_mm"]))
    shell = object_from_bmesh("CU01_TemporaryShell", bm, collection)

    cutter_bm = bmesh.new()
    cutter_bottom = PARAMS["base_mm"]
    cutter_top = PARAMS["height_mm"] + 0.1
    add_box(
        cutter_bm,
        (0.0, 0.0, (cutter_bottom + cutter_top) / 2.0),
        (INNER_XY, INNER_XY, cutter_top - cutter_bottom),
    )
    cutter = object_from_bmesh("CU01_TemporaryCavityCutter", cutter_bm, collection)
    apply_boolean(shell, cutter, "DIFFERENCE", "CU01_OpenCavity_Exact")
    cutter_mesh = cutter.data
    bpy.data.objects.remove(cutter, do_unlink=True)
    if cutter_mesh.users == 0:
        bpy.data.meshes.remove(cutter_mesh)
    shell.name = OBJECT_NAME
    shell.data.name = "CU01_PlanterMesh_REV002"
    return shell


def build_bricks(collection, side_name):
    bm = bmesh.new()
    wall_half = BODY_XY / 2.0
    depth = PARAMS["relief_mm"] + BRICK_OVERLAP_MM
    normal_center = wall_half + PARAMS["relief_mm"] / 2.0 - BRICK_OVERLAP_MM / 2.0
    total_course_height = (
        7 * PARAMS["brick_height_mm"] + 6 * PARAMS["joint_mm"]
    )
    first_bottom = (PARAMS["height_mm"] - total_course_height) / 2.0
    counts = []
    end_lengths = []

    for row in range(7):
        segments = row_segments(row, BODY_XY)
        expected_length = BODY_XY - (len(segments) - 1) * PARAMS["joint_mm"]
        if abs(sum(segments) - expected_length) > 1e-9:
            raise RuntimeError(f"row {row} fitted segments do not close: {segments}")
        cursor = -wall_half
        z_bottom = first_bottom + row * (PARAMS["brick_height_mm"] + PARAMS["joint_mm"])
        z_center = z_bottom + PARAMS["brick_height_mm"] / 2.0
        counts.append(len(segments))
        end_lengths.append(segments[0])
        for side in (side_name,):
            cursor = -wall_half
            for segment_length in segments:
                tangent = cursor + segment_length / 2.0
                if side == "east":
                    center = (normal_center, tangent, z_center)
                    size = (depth, segment_length, PARAMS["brick_height_mm"])
                elif side == "west":
                    center = (-normal_center, tangent, z_center)
                    size = (depth, segment_length, PARAMS["brick_height_mm"])
                elif side == "north":
                    center = (tangent, normal_center, z_center)
                    size = (segment_length, depth, PARAMS["brick_height_mm"])
                else:
                    center = (tangent, -normal_center, z_center)
                    size = (segment_length, depth, PARAMS["brick_height_mm"])
                add_box(bm, center, size)
                cursor += segment_length + PARAMS["joint_mm"]
            if abs(cursor - wall_half - PARAMS["joint_mm"]) > 1e-8:
                raise RuntimeError(f"{side} row {row} does not reach the corner bounds")

    operands = object_from_bmesh("CU01_TemporaryBrickOperands", bm, collection)
    return operands, {"segments_per_course": counts, "end_piece_length_mm": end_lengths}


def prepare_view(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                region = area.spaces.active.region_3d
                region.view_location = (0.0, 0.0, 0.03)
                region.view_distance = 0.34
                region.view_rotation = Euler((0.95, 0.0, 0.78), "XYZ").to_quaternion()


def main():
    output = parse_output()
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    scene = clear_scene()
    collection = scene.collection
    obj = build_shell(collection)
    pattern = None
    union_sequence = ("east", "north", "west", "south")
    for side in union_sequence:
        operands, pattern = build_bricks(collection, side)
        apply_boolean(obj, operands, "UNION", f"CU01_{side}_ExactUnion")
        operand_mesh = operands.data
        bpy.data.objects.remove(operands, do_unlink=True)
        if operand_mesh.users == 0:
            bpy.data.meshes.remove(operand_mesh)
        print("CU01_FACE_UNION " + json.dumps({"side": side, "vertices": len(obj.data.vertices), "faces": len(obj.data.polygons)}, sort_keys=True))

    segment_count = sum(pattern["segments_per_course"]) * 4
    obj["case_id"] = "CU-01"
    obj["run_id"] = RUN_ID
    obj["strategy"] = "A_bpy_parameterized_full_rebuild"
    obj["parameters_mm"] = json.dumps(PARAMS, sort_keys=True)
    obj["derived_dimensions_mm"] = json.dumps(
        {
            "smooth_body_xy": BODY_XY,
            "inner_xy": INNER_XY,
            "inner_depth": PARAMS["height_mm"] - PARAMS["base_mm"],
            "nominal_brick_segments": segment_count,
            "course_end_piece_lengths_mm": pattern["end_piece_length_mm"],
        },
        sort_keys=True,
    )
    obj["pattern_units_by_course"] = json.dumps(pattern["segments_per_course"])
    obj["face_union_sequence"] = json.dumps(union_sequence)
    obj["modeling_note"] = (
        "Complete geometry regenerated from script parameters; not an in-place edit. "
        "End units are fitted at the corners to preserve 1.2 mm joints."
    )
    obj["physical_status"] = "digital model only; no STL or print"
    prepare_view(obj)
    result = bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    if "FINISHED" not in result:
        raise RuntimeError(f"save failed: {result}")
    print(
        "CU01_BUILD "
        + json.dumps(
            {
                "run_id": RUN_ID,
                "path": str(output),
                "parameters": PARAMS,
                "derived_dimensions_mm": {
                    "body_xy": BODY_XY,
                    "inner_xy": INNER_XY,
                    "inner_depth": PARAMS["height_mm"] - PARAMS["base_mm"],
                },
                "segments_per_course_per_side": pattern["segments_per_course"],
                "total_face_segments": segment_count,
                "strategy": "A_bpy_parameterized_full_rebuild",
            },
            sort_keys=True,
        )
    )


main()

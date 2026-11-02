"""Read-only topology and geometry validation for the EXP-BPY-003 plate."""
import hashlib
import json
import math
import sys

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

OBJECT_NAME = "EXP-BPY-003_ReliefPlate"
RUN_ID = "EXP-BPY-003-20261102T144300Z"
TOLERANCE_MM = 0.01


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected a JSON contract after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected one JSON contract")
    return json.loads(args[0])


def components(bm):
    unseen = set(bm.verts)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            v = stack.pop()
            for edge in v.link_edges:
                other = edge.other_vert(v)
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def bvh_nonadjacent_overlaps(bm):
    bm.faces.ensure_lookup_table()
    tree = BVHTree.FromBMesh(bm, epsilon=1e-9)
    pairs = tree.overlap(tree)
    found = set()
    for a, b in pairs:
        if a == b:
            continue
        fa, fb = bm.faces[a], bm.faces[b]
        if set(fa.verts).intersection(fb.verts):
            continue
        found.add(tuple(sorted((a, b))))
    return sorted(found)


def main():
    contract = args_after_separator()
    scene = bpy.context.scene
    all_objects = [obj for obj in scene.objects if obj.type == "MESH"]
    obj = bpy.data.objects.get(OBJECT_NAME)
    checks = []
    checks.append({"check": "expected_object", "pass": obj is not None, "observed_mesh_objects": [x.name for x in all_objects]})
    checks.append({"check": "only_one_mesh_object", "pass": len(all_objects) == 1, "expected": 1, "observed": len(all_objects)})
    if obj is None:
        result = {"run_id": RUN_ID, "status": "FAIL", "findings": checks, "opened_file": bpy.data.filepath}
        print("EXP_BPY_003_BLEND_VALIDATION " + json.dumps(result, sort_keys=True))
        raise RuntimeError("Expected relief object missing")

    params = json.loads(obj.get("parameters_mm", "{}"))
    expected_params = contract["expected_parameters_mm"]
    checks.append({"check": "parameters", "pass": params == expected_params and obj.get("parameter_units") == "mm", "expected": expected_params, "observed": params, "units": obj.get("parameter_units")})
    checks.append({"check": "identity", "pass": obj.get("experiment_id") == RUN_ID and obj.name == OBJECT_NAME, "observed": {"name": obj.name, "experiment_id": obj.get("experiment_id")}})
    checks.append({"check": "one_connected_mesh_object", "pass": len(all_objects) == 1, "observed": len(all_objects)})
    scene_units = scene.unit_settings
    unit_ok = scene_units.system == "METRIC" and abs(scene_units.scale_length - 1.0) < 1e-12 and scene_units.length_unit == "MILLIMETERS"
    checks.append({"check": "units", "pass": unit_ok, "observed": {"system": scene_units.system, "scale_length": scene_units.scale_length, "length_unit": scene_units.length_unit}})

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph, preserve_all_data_layers=True)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    coords = [obj.matrix_world @ v.co for v in mesh.vertices]
    mins = [min(v[i] for v in coords) for i in range(3)]
    maxs = [max(v[i] for v in coords) for i in range(3)]
    dims_mm = [(maxs[i] - mins[i]) * 1000 for i in range(3)]
    center_mm = [(maxs[i] + mins[i]) * 500 for i in range(3)]
    axes = ("x", "y", "z")
    expected_dims = contract["expected_dimensions_mm"]
    dim_deviation = {axes[i]: dims_mm[i] - expected_dims[axes[i]] for i in range(3)}
    dimensions_ok = all(abs(dim_deviation[a]) <= TOLERANCE_MM for a in axes)
    checks.append({"check": "evaluated_dimensions_mm", "pass": dimensions_ok, "expected": expected_dims, "observed": dict(zip(axes, dims_mm)), "deviation_mm": dim_deviation, "tolerance_mm": TOLERANCE_MM})
    center_ok = all(abs(x) <= TOLERANCE_MM for x in center_mm[:2]) and abs(center_mm[2] - expected_dims["z"] / 2) <= TOLERANCE_MM
    checks.append({"check": "center_and_base_plane_mm", "pass": center_ok, "expected_center_xy": [0, 0], "expected_min_z": 0, "observed_center_mm": center_mm, "observed_min_z_mm": mins[2] * 1000})

    comp_count = components(bm)
    global_component_count = comp_count
    other_component_details = []
    for other_obj in all_objects:
        if other_obj == obj:
            continue
        other_eval = other_obj.evaluated_get(depsgraph)
        other_mesh = bpy.data.meshes.new_from_object(other_eval, depsgraph=depsgraph)
        other_bm = bmesh.new()
        other_bm.from_mesh(other_mesh)
        other_count = components(other_bm)
        global_component_count += other_count
        other_component_details.append({"object": other_obj.name, "components": other_count})
        other_bm.free()
        bpy.data.meshes.remove(other_mesh)
    manifold = all(edge.is_manifold for edge in bm.edges)
    contiguous = all(edge.is_contiguous for edge in bm.edges if edge.is_manifold)
    degenerates = {
        "zero_or_tiny_edges": sum(edge.calc_length() <= 1e-9 for edge in bm.edges),
        "zero_or_tiny_faces": sum(face.calc_area() <= 1e-12 for face in bm.faces),
    }
    signed_volume_mm3 = bm.calc_volume(signed=True) * 1e9
    overlap_pairs = bvh_nonadjacent_overlaps(bm)
    checks.extend([
        {"check": "connected_components", "pass": global_component_count == 1, "expected": 1, "observed": global_component_count, "main_object_components": comp_count, "other_objects": other_component_details},
        {"check": "manifold_and_closed", "pass": manifold and len(bm.edges) > 0, "all_edges_manifold": manifold, "edge_count": len(bm.edges)},
        {"check": "consistent_face_orientation", "pass": contiguous and signed_volume_mm3 > 0, "all_manifold_edges_contiguous": contiguous, "signed_volume_mm3": signed_volume_mm3},
        {"check": "no_degenerate_edges_or_faces", "pass": degenerates["zero_or_tiny_edges"] == 0 and degenerates["zero_or_tiny_faces"] == 0, "observed": degenerates},
        {"check": "positive_volume", "pass": signed_volume_mm3 > 0, "observed_mm3": signed_volume_mm3},
        {"check": "nonadjacent_surface_overlap", "pass": len(overlap_pairs) == 0, "method": "BVHTree face overlap pairs excluding faces sharing vertices", "pair_count": len(overlap_pairs), "sample_pairs": overlap_pairs[:20]},
    ])

    z_top = expected_dims["z"] / 1000
    top_faces = [face for face in bm.faces if all(abs((obj.matrix_world @ v.co).z - z_top) <= 1e-7 for v in face.verts)]
    top_area_mm2 = sum(face.calc_area() for face in top_faces) * 1e6
    # Count disconnected islands of coplanar top faces using their shared edges.
    top_set = set(top_faces)
    top_components = 0
    unseen = set(top_faces)
    while unseen:
        top_components += 1
        stack = [unseen.pop()]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for linked in edge.link_faces:
                    if linked in unseen and linked in top_set:
                        unseen.remove(linked)
                        stack.append(linked)
    brick_count = int(obj.get("brick_count", -1))
    expected_top_area = float(contract["expected_brick_top_area_mm2"])
    checks.append({"check": "physical_relief_top_surfaces", "pass": top_components == brick_count and abs(top_area_mm2 - expected_top_area) <= 0.05, "expected_islands": brick_count, "observed_islands": top_components, "expected_top_area_mm2": expected_top_area, "observed_top_area_mm2": top_area_mm2, "max_relief_mm": dims_mm[2] - params["base_thickness"]})
    expected_volume = params["plate_width"] * params["plate_height"] * params["base_thickness"] + expected_top_area * params["relief_height"]
    checks.append({"check": "parameter_geometry_correspondence", "pass": int(obj.get("brick_count", -1)) == contract["expected_brick_count"] and abs(signed_volume_mm3 - expected_volume) <= 0.1, "expected_bricks": contract["expected_brick_count"], "observed_bricks": obj.get("brick_count"), "expected_volume_mm3": expected_volume, "observed_volume_mm3": signed_volume_mm3})
    checks.append({"check": "no_unapplied_modifiers", "pass": len(obj.modifiers) == 0, "observed": [m.name for m in obj.modifiers]})

    canonical = {
        "object": obj.name,
        "parameters": params,
        "dims_mm_rounded_6": [round(v, 6) for v in dims_mm],
        "center_mm_rounded_6": [round(v, 6) for v in center_mm],
        "top_area_mm2_rounded_6": round(top_area_mm2, 6),
        "components": global_component_count,
        "volume_mm3_rounded_6": round(signed_volume_mm3, 6),
    }
    semantic_sha = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "run_id": RUN_ID,
        "status": "PASS" if all(check["pass"] for check in checks) else "FAIL",
        "opened_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "object_count": len(all_objects),
        "dimensions_mm": dict(zip(axes, dims_mm)),
        "center_mm": center_mm,
        "parameters_mm": params,
        "brick_count": brick_count,
        "top_surface_islands": top_components,
        "top_area_mm2": top_area_mm2,
        "components": comp_count,
        "vertices": len(bm.verts),
        "edges": len(bm.edges),
        "faces": len(bm.faces),
        "signed_volume_mm3": signed_volume_mm3,
        "degenerates": degenerates,
        "nonadjacent_overlap_pairs": len(overlap_pairs),
        "semantic_state_sha256": semantic_sha,
        "findings": checks,
        "read_only": True,
    }
    bm.free()
    bpy.data.meshes.remove(mesh)
    print("EXP_BPY_003_BLEND_VALIDATION " + json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise RuntimeError("EXP-BPY-003 model validation failed")


if __name__ == "__main__":
    main()

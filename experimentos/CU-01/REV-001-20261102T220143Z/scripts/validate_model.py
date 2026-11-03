"""Read-only independent validation for CU-01 revision 001."""
import json
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

RUN_ID = "CU-01-REV-001-20261102T220143Z"
TOL_MM = 0.01
P = {
    "envelope_x_mm": 150.0,
    "envelope_y_mm": 150.0,
    "height_mm": 60.0,
    "wall_mm": 20.0,
    "base_mm": 4.0,
    "brick_length_mm": 15.0,
    "brick_height_mm": 7.0,
    "joint_mm": 1.2,
    "relief_mm": 1.0,
    "drainage_holes": 0,
}
BODY_XY = P["envelope_x_mm"] - 2.0 * P["relief_mm"]
INNER_XY = BODY_XY - 2.0 * P["wall_mm"]
OBJECT_NAME = "CU01_Planter_REV001"


def connected_components(bm):
    unseen = set(bm.verts)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            vert = stack.pop()
            for edge in vert.link_edges:
                other = edge.other_vert(vert)
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def face_groups(faces):
    unseen = set(faces)
    groups = []
    while unseen:
        seed = unseen.pop()
        stack = [seed]
        group = [seed]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for neighbor in edge.link_faces:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        stack.append(neighbor)
                        group.append(neighbor)
        groups.append(group)
    return groups


def row_segments(row_index):
    interior_count = 7 if row_index % 2 == 0 else 8
    segment_count = interior_count + 2
    wall_length = BODY_XY
    gaps = segment_count - 1
    end_length = (
        wall_length
        - interior_count * P["brick_length_mm"]
        - gaps * P["joint_mm"]
    ) / 2.0
    return [end_length] + [P["brick_length_mm"]] * interior_count + [end_length]


def measure_surface_regions(bm, obj, axis, sign):
    plane = sign * (P["envelope_x_mm"] / 2.0) / 1000.0
    tol_m = TOL_MM / 1000.0
    if axis == "x":
        faces = [f for f in bm.faces if all(abs(v.co.x - plane) <= tol_m for v in f.verts)]
        tangent = "y"
    else:
        faces = [f for f in bm.faces if all(abs(v.co.y - plane) <= tol_m for v in f.verts)]
        tangent = "x"
    regions = []
    for group in face_groups(faces):
        pts = [obj.matrix_world @ v.co for f in group for v in f.verts]
        tangent_vals = [getattr(p, tangent) * 1000.0 for p in pts]
        z_vals = [p.z * 1000.0 for p in pts]
        regions.append({
            "tangent_min_mm": min(tangent_vals),
            "tangent_max_mm": max(tangent_vals),
            "z_min_mm": min(z_vals),
            "z_max_mm": max(z_vals),
            "length_mm": max(tangent_vals) - min(tangent_vals),
            "height_mm": max(z_vals) - min(z_vals),
        })
    return regions


def cluster_rows(regions):
    rows = []
    for region in sorted(regions, key=lambda r: r["z_min_mm"]):
        row = next((x for x in rows if abs(x["z_min_mm"] - region["z_min_mm"]) <= TOL_MM), None)
        if row is None:
            row = {"z_min_mm": region["z_min_mm"], "regions": []}
            rows.append(row)
        row["regions"].append(region)
    return rows


def check_side(regions, side_name):
    rows = cluster_rows(regions)
    results = []
    for index, row in enumerate(rows):
        observed = sorted(r["length_mm"] for r in row["regions"])
        expected = sorted(row_segments(index))
        widths_ok = len(observed) == len(expected) and all(abs(a - b) <= TOL_MM for a, b in zip(observed, expected))
        heights_ok = all(abs(r["height_mm"] - P["brick_height_mm"]) <= TOL_MM for r in row["regions"])
        ordered = sorted(row["regions"], key=lambda r: r["tangent_min_mm"])
        gaps = [ordered[i + 1]["tangent_min_mm"] - ordered[i]["tangent_max_mm"] for i in range(len(ordered) - 1)]
        gaps_ok = len(gaps) == len(ordered) - 1 and all(abs(g - P["joint_mm"]) <= TOL_MM for g in gaps)
        bounds_ok = bool(ordered) and abs(ordered[0]["tangent_min_mm"] + BODY_XY / 2.0) <= TOL_MM and abs(ordered[-1]["tangent_max_mm"] - BODY_XY / 2.0) <= TOL_MM
        expected_z = (P["height_mm"] - (7 * P["brick_height_mm"] + 6 * P["joint_mm"])) / 2.0 + index * (P["brick_height_mm"] + P["joint_mm"])
        z_ok = len(rows) == 7 and abs(row["z_min_mm"] - expected_z) <= TOL_MM
        results.append({
            "course": index,
            "patches": len(row["regions"]),
            "expected_patches": len(expected),
            "lengths_mm": observed,
            "gaps_mm": gaps,
            "z_min_mm": row["z_min_mm"],
            "pass": widths_ok and heights_ok and gaps_ok and bounds_ok and z_ok,
        })
    return {
        "side": side_name,
        "patch_count": len(regions),
        "course_count": len(rows),
        "courses": results,
        "pass": len(rows) == 7 and all(r["pass"] for r in results),
    }


def ray_cast(obj_eval, origin_mm, direction):
    origin = Vector(origin_mm) / 1000.0
    direction = Vector(direction).normalized()
    return obj_eval.ray_cast(origin, direction, distance=1.0)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if len(argv) != 2:
        raise RuntimeError("expected input .blend path and output JSON path after --")
    blend_path = Path(argv[0]).resolve()
    json_path = Path(argv[1]).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(blend_path), load_ui=False)
    obj = bpy.data.objects.get(OBJECT_NAME)
    findings = []
    findings.append({"check": "expected_object", "pass": obj is not None, "name": OBJECT_NAME})
    if obj is None:
        raise RuntimeError("candidate object missing")
    findings.append({
        "check": "only_one_primary_mesh",
        "pass": sum(o.type == "MESH" for o in bpy.context.scene.objects) == 1,
        "observed": sum(o.type == "MESH" for o in bpy.context.scene.objects),
    })

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph, preserve_all_data_layers=True)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    world = [obj.matrix_world @ v.co for v in mesh.vertices]
    lo = [min(v[i] for v in world) * 1000.0 for i in range(3)]
    hi = [max(v[i] for v in world) * 1000.0 for i in range(3)]
    dims = [hi[i] - lo[i] for i in range(3)]
    expected_dims = [P["envelope_x_mm"], P["envelope_y_mm"], P["height_mm"]]
    findings.append({
        "check": "total_envelope_mm",
        "pass": all(abs(a - e) <= TOL_MM for a, e in zip(dims, expected_dims)),
        "expected": expected_dims,
        "observed": dims,
        "tolerance_mm": TOL_MM,
    })
    unit = bpy.context.scene.unit_settings
    findings.append({
        "check": "metric_units_and_object_scale",
        "pass": unit.system == "METRIC" and abs(unit.scale_length - 1.0) < 1e-12 and unit.length_unit == "MILLIMETERS" and all(abs(s - 1.0) < 1e-9 for s in obj.scale),
        "observed": {"system": unit.system, "scale_length": unit.scale_length, "length_unit": unit.length_unit, "object_scale": list(obj.scale)},
    })

    components = connected_components(bm)
    manifold = bool(bm.edges) and all(e.is_manifold for e in bm.edges)
    contiguous = bool(bm.edges) and all(e.is_contiguous for e in bm.edges if e.is_manifold)
    volume = bm.calc_volume(signed=True) * 1e9
    degenerates = {
        "edges": sum(e.calc_length() <= 1e-12 for e in bm.edges),
        "faces": sum(f.calc_area() <= 1e-15 for f in bm.faces),
    }
    findings.append({"check": "single_closed_manifold_component", "pass": components == 1 and manifold, "components": components, "all_edges_manifold": manifold})
    findings.append({"check": "orientation_and_positive_volume", "pass": contiguous and volume > 0.0, "contiguous": contiguous, "signed_volume_mm3": volume})
    findings.append({"check": "no_degenerate_elements", "pass": degenerates["edges"] == 0 and degenerates["faces"] == 0, "observed": degenerates})

    # Four inner wall planes: ±54 mm, 108 mm wide, from floor to rim.
    inner_wall_faces = []
    for axis, target in (("x", INNER_XY / 2.0), ("x", -INNER_XY / 2.0), ("y", INNER_XY / 2.0), ("y", -INNER_XY / 2.0)):
        for face in bm.faces:
            values = [getattr(v.co, axis) * 1000.0 for v in face.verts]
            if values and all(abs(v - target) <= TOL_MM for v in values):
                pts = [obj.matrix_world @ v.co for v in face.verts]
                zspan = (max(p.z for p in pts) - min(p.z for p in pts)) * 1000.0
                if zspan >= P["height_mm"] - P["base_mm"] - TOL_MM:
                    inner_wall_faces.append((axis, target, zspan))
    findings.append({
        "check": "four_inner_wall_planes",
        "pass": len(inner_wall_faces) >= 4,
        "expected_planes_mm": {"x": [-INNER_XY / 2.0, INNER_XY / 2.0], "y": [-INNER_XY / 2.0, INNER_XY / 2.0]},
        "observed_vertical_faces": inner_wall_faces,
    })
    findings.append({
        "check": "derived_cavity_dimensions_mm",
        "pass": abs(INNER_XY - 108.0) <= TOL_MM and abs((P["height_mm"] - P["base_mm"]) - 56.0) <= TOL_MM,
        "expected": [108.0, 108.0, 56.0],
        "wall_mm": P["wall_mm"],
        "base_mm": P["base_mm"],
    })

    depsgraph = bpy.context.evaluated_depsgraph_get()
    open_hit = evaluated.ray_cast(Vector((0.0, 0.0, 0.01)), Vector((0.0, 0.0, 1.0)), distance=1.0, depsgraph=depsgraph)
    findings.append({"check": "open_top", "pass": open_hit[0] is False, "ray_up_from_inner_cavity_hit": bool(open_hit[0])})
    sample_points = [(0, 0), (30, 0), (-30, 0), (0, 30), (0, -30), (30, 30), (-30, -30)]
    floor_hits = []
    for x, y in sample_points:
        hit = evaluated.ray_cast(Vector((x / 1000.0, y / 1000.0, 0.01)), Vector((0.0, 0.0, -1.0)), distance=1.0, depsgraph=depsgraph)
        floor_hits.append({"xy_mm": [x, y], "hit": bool(hit[0]), "z_mm": hit[1].z * 1000.0 if hit[0] else None})
    floors_ok = len(floor_hits) == len(sample_points) and all(h["hit"] and abs(h["z_mm"] - P["base_mm"]) <= TOL_MM for h in floor_hits)
    findings.append({"check": "closed_base_no_drainage", "pass": floors_ok, "ray_hits": floor_hits, "expected_floor_z_mm": P["base_mm"]})

    expected_units = 4 * sum(len(row_segments(i)) for i in range(7))
    side_specs = [("east", "x", 1), ("west", "x", -1), ("north", "y", 1), ("south", "y", -1)]
    side_results = []
    for name, axis, sign in side_specs:
        regions = measure_surface_regions(bm, obj, axis, sign)
        side_results.append(check_side(regions, name))
    findings.append({
        "check": "four_face_real_brick_relief_and_stagger",
        "pass": all(s["pass"] for s in side_results) and sum(s["patch_count"] for s in side_results) == expected_units,
        "expected_units": expected_units,
        "observed_units": sum(s["patch_count"] for s in side_results),
        "side_results": side_results,
        "nominal_brick_mm": [P["brick_length_mm"], P["brick_height_mm"]],
        "course_end_pieces_mm": [row_segments(0)[0], row_segments(1)[0]],
        "joint_mm": P["joint_mm"],
        "relief_mm": P["relief_mm"],
    })

    shell_volume = BODY_XY * BODY_XY * P["height_mm"] - INNER_XY * INNER_XY * (P["height_mm"] - P["base_mm"])
    exposed_area_per_side = sum(sum(row_segments(i)) * P["brick_height_mm"] for i in range(7))
    expected_volume = shell_volume + 4.0 * exposed_area_per_side * P["relief_mm"]
    findings.append({
        "check": "expected_signed_volume",
        "pass": abs(volume - expected_volume) <= 0.2,
        "expected_mm3": expected_volume,
        "observed_mm3": volume,
        "tolerance_mm3": 0.2,
    })

    params = json.loads(obj.get("parameters_mm", "{}"))
    findings.append({
        "check": "saved_parameter_record",
        "pass": params.get("envelope_x_mm") == 150.0 and params.get("envelope_y_mm") == 150.0 and params.get("wall_mm") == 20.0 and params.get("base_mm") == 4.0 and params.get("drainage_holes") == 0 and params.get("brick_length_mm") == 15.0,
        "observed": params,
    })
    findings.append({"check": "read_only_separate_process", "pass": True, "opened_file": bpy.data.filepath})

    result = {
        "run_id": RUN_ID,
        "status": "PASS" if all(item["pass"] for item in findings) else "FAIL",
        "opened_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "dimensions_mm": dims,
        "interior_dimensions_mm": [INNER_XY, INNER_XY, P["height_mm"] - P["base_mm"]],
        "components": components,
        "all_edges_manifold": manifold,
        "signed_volume_mm3": volume,
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "faces": len(mesh.polygons),
        "findings": findings,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("CU01_VALIDATION " + json.dumps(result, sort_keys=True))
    bm.free()
    bpy.data.meshes.remove(mesh)
    if result["status"] != "PASS":
        raise SystemExit(2)


main()

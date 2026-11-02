"""Import an STL in a fresh Blender process and validate bounds/topology/relief."""
import hashlib
import json
import math
import sys

import bpy
import bmesh

RUN_ID = "EXP-BPY-003-20261102T144300Z"
TOLERANCE_MM = 0.01


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected contract JSON after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected one contract")
    return json.loads(args[0])


def component_count(bm):
    unseen = set(bm.verts)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            v = stack.pop()
            for e in v.link_edges:
                other = e.other_vert(v)
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def main():
    contract = args_after_separator()
    before = set(bpy.context.scene.objects)
    imported = bpy.ops.wm.stl_import(
        filepath=contract["stl_path"],
        global_scale=float(contract["import_global_scale"]),
        use_scene_unit=False,
        forward_axis="Y",
        up_axis="Z",
        use_mesh_validate=True,
    )
    if "FINISHED" not in imported:
        raise RuntimeError("STL import operator failed")
    new_objects = [o for o in bpy.context.scene.objects if o not in before and o.type == "MESH"]
    checks = [{"check": "one_imported_mesh", "pass": len(new_objects) == 1, "observed": [o.name for o in new_objects]}]
    if not new_objects:
        print("EXP_BPY_003_STL_VALIDATION " + json.dumps({"status": "FAIL", "findings": checks}, sort_keys=True))
        raise RuntimeError("No mesh imported from STL")
    mesh_obj = new_objects[0]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ev = mesh_obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(ev, depsgraph=depsgraph)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    coords = [mesh_obj.matrix_world @ v.co for v in mesh.vertices]
    mins = [min(p[i] for p in coords) for i in range(3)]
    maxs = [max(p[i] for p in coords) for i in range(3)]
    dims = [(maxs[i] - mins[i]) * 1000 for i in range(3)]
    center = [(maxs[i] + mins[i]) * 500 for i in range(3)]
    axes = ("x", "y", "z")
    expected = contract["expected_dimensions_mm"]
    deviations = {axes[i]: dims[i] - expected[axes[i]] for i in range(3)}
    dim_ok = all(abs(deviations[a]) <= TOLERANCE_MM for a in axes)
    checks.append({"check": "dimensions_mm", "pass": dim_ok, "expected": expected, "observed": dict(zip(axes, dims)), "deviation_mm": deviations, "tolerance_mm": TOLERANCE_MM})
    comps = component_count(bm)
    manifold = all(e.is_manifold for e in bm.edges)
    contiguous = all(e.is_contiguous for e in bm.edges if e.is_manifold)
    transform3 = mesh_obj.matrix_world.to_3x3()
    volume_mm3 = bm.calc_volume(signed=True) * abs(transform3.determinant()) * 1e9
    tiny_edges = sum(e.calc_length() <= 1e-9 for e in bm.edges)
    tiny_faces = sum(f.calc_area() <= 1e-12 for f in bm.faces)
    checks.extend([
        {"check": "connected_components", "pass": comps == 1, "expected": 1, "observed": comps},
        {"check": "manifold", "pass": manifold, "all_edges_manifold": manifold},
        {"check": "consistent_normals_and_volume", "pass": contiguous and volume_mm3 > 0, "contiguous": contiguous, "signed_volume_mm3": volume_mm3},
        {"check": "nondegenerate", "pass": tiny_edges == 0 and tiny_faces == 0, "tiny_edges": tiny_edges, "tiny_faces": tiny_faces},
    ])
    top_z = maxs[2]
    top_faces = [f for f in bm.faces if all(abs((mesh_obj.matrix_world @ v.co).z - top_z) <= 1e-7 for v in f.verts)]
    unseen = set(top_faces)
    top_islands = 0
    top_set = set(top_faces)
    while unseen:
        top_islands += 1
        stack = [unseen.pop()]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for other in edge.link_faces:
                    if other in unseen and other in top_set:
                        unseen.remove(other)
                        stack.append(other)
    # STL import may keep numeric millimetres in local vertices and set object scale=0.001.
    # Apply world X/Y scale to local face areas before converting m² to mm².
    scale = mesh_obj.matrix_world.to_scale()
    top_area_mm2 = sum(f.calc_area() for f in top_faces) * abs(scale.x * scale.y) * 1e6
    expected_islands = int(contract["expected_top_islands"])
    expected_area = float(contract["expected_top_area_mm2"])
    relief_ok = top_islands == expected_islands and abs(top_area_mm2 - expected_area) <= 0.1
    checks.append({"check": "relief_preserved", "pass": relief_ok, "expected_top_islands": expected_islands, "observed_top_islands": top_islands, "expected_top_area_mm2": expected_area, "observed_top_area_mm2": top_area_mm2})
    center_ok = abs(center[0]) <= TOLERANCE_MM and abs(center[1]) <= TOLERANCE_MM and abs(mins[2] * 1000) <= TOLERANCE_MM
    checks.append({"check": "placement", "pass": center_ok, "center_mm": center, "min_z_mm": mins[2] * 1000})
    result = {
        "run_id": RUN_ID,
        "status": "PASS" if all(c["pass"] for c in checks) else "FAIL",
        "stl_path": contract["stl_path"],
        "import_global_scale": contract["import_global_scale"],
        "unit_convention": "STL numeric coordinates are mm; import scale 0.001 converts numeric mm to Blender metres",
        "blender_version": bpy.app.version_string,
        "dimensions_mm": dict(zip(axes, dims)),
        "center_mm": center,
        "vertices": len(bm.verts), "edges": len(bm.edges), "faces": len(bm.faces),
        "components": comps, "signed_volume_mm3": volume_mm3,
        "top_surface_islands": top_islands, "top_area_mm2": top_area_mm2,
        "findings": checks,
    }
    bm.free()
    bpy.data.meshes.remove(mesh)
    print("EXP_BPY_003_STL_VALIDATION " + json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise RuntimeError("Imported STL validation failed")


if __name__ == "__main__":
    main()

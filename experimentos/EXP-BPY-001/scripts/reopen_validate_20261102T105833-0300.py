"""Reopen and numerically validate an EXP-BPY-001 .blend in a fresh process."""
import json
import math
import os
import sys

import bpy
import bmesh


RUN_ID = "EXP-BPY-001-20261102T105833-0300"
OBJECT_NAME = "EXP-BPY-001_Cube_20261102T105833"
EXPECTED_MM = {"x": 50.0, "y": 50.0, "z": 50.0}
TOLERANCE_MM = 0.01


def main():
    if len(bpy.data.filepath) == 0:
        raise RuntimeError("No .blend file was opened by this process")
    scene = bpy.context.scene
    objects = list(scene.objects)
    findings = []
    findings.append({"check": "reopened_file", "pass": os.path.isfile(bpy.data.filepath), "observed": bpy.data.filepath})
    findings.append({"check": "exact_scene_object_count", "pass": len(objects) == 1, "expected": 1, "observed": len(objects)})
    obj = bpy.data.objects.get(OBJECT_NAME)
    findings.append({"check": "expected_object_exists", "pass": obj is not None, "expected": OBJECT_NAME, "observed": obj.name if obj else None})

    if obj is not None:
        params_raw = obj.get("parameters_mm", "")
        try:
            params = json.loads(params_raw)
        except Exception:
            params = None
        findings.append({"check": "parameters_preserved", "pass": params == EXPECTED_MM and obj.get("experiment_id") == RUN_ID and obj.get("parameter_units") == "mm", "expected": EXPECTED_MM, "observed": params, "experiment_id": obj.get("experiment_id"), "parameter_units": obj.get("parameter_units")})
        unit_ok = scene.unit_settings.system == "METRIC" and math.isclose(scene.unit_settings.scale_length, 1.0, abs_tol=1e-12)
        findings.append({"check": "units_documented", "pass": unit_ok, "expected": {"system": "METRIC", "scale_length": 1.0}, "observed": {"system": scene.unit_settings.system, "scale_length": scene.unit_settings.scale_length, "length_unit": scene.unit_settings.length_unit}})
        findings.append({"check": "centered_and_identity_transform", "pass": all(abs(v) <= 1e-9 for v in obj.location) and all(abs(v) <= 1e-9 for v in obj.rotation_euler) and all(abs(v - 1.0) <= 1e-9 for v in obj.scale), "expected": {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}, "observed": {"location": list(obj.location), "rotation": list(obj.rotation_euler), "scale": list(obj.scale)}})

        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated = obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated.to_mesh()
        try:
            coordinates = [evaluated.matrix_world @ vertex.co for vertex in evaluated_mesh.vertices]
            mins = [min(v[i] for v in coordinates) for i in range(3)]
            maxs = [max(v[i] for v in coordinates) for i in range(3)]
            center_mm = [(mins[i] + maxs[i]) * 500.0 for i in range(3)]
            dimensions_mm = [(maxs[i] - mins[i]) * 1000.0 for i in range(3)]
            axis_names = ("x", "y", "z")
            deviations = {axis_names[i]: dimensions_mm[i] - EXPECTED_MM[axis_names[i]] for i in range(3)}
            dims_ok = all(abs(deviations[axis]) <= TOLERANCE_MM for axis in axis_names)
            center_ok = all(abs(value) <= TOLERANCE_MM for value in center_mm)
            findings.append({"check": "evaluated_dimensions_mm", "pass": dims_ok, "expected": EXPECTED_MM, "observed": dict(zip(axis_names, dimensions_mm)), "deviation_mm": deviations, "tolerance_mm": TOLERANCE_MM})
            findings.append({"check": "evaluated_center_mm", "pass": center_ok, "expected": [0.0, 0.0, 0.0], "observed": center_mm, "tolerance_mm": TOLERANCE_MM})

            bm = bmesh.new()
            bm.from_mesh(evaluated_mesh)
            components = 0
            unseen = set(bm.verts)
            while unseen:
                components += 1
                stack = [unseen.pop()]
                while stack:
                    current = stack.pop()
                    for edge in current.link_edges:
                        other = edge.other_vert(current)
                        if other in unseen:
                            unseen.remove(other)
                            stack.append(other)
            topology = {"vertices": len(bm.verts), "edges": len(bm.edges), "faces": len(bm.faces), "components": components, "all_edges_manifold": all(edge.is_manifold for edge in bm.edges)}
            topology_ok = topology == {"vertices": 8, "edges": 12, "faces": 6, "components": 1, "all_edges_manifold": True}
            findings.append({"check": "evaluated_topology", "pass": topology_ok, "expected": {"vertices": 8, "edges": 12, "faces": 6, "components": 1, "all_edges_manifold": True}, "observed": topology})
            bm.free()
        finally:
            evaluated.to_mesh_clear()

    status = "PASS" if all(item["pass"] for item in findings) else "FAIL"
    result = {
        "run_id": RUN_ID,
        "status": status,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "bpy_available": True,
        "opened_blend": bpy.data.filepath,
        "scene_object_names": [item.name for item in objects],
        "tolerance_mm": TOLERANCE_MM,
        "findings": findings,
    }
    print("EXP_BPY_VALIDATION " + json.dumps(result, sort_keys=True))
    if status != "PASS":
        raise RuntimeError("One or more EXP-BPY-001 geometry checks failed; see findings above")


if __name__ == "__main__":
    main()

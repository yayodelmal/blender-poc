"""Read-only contract validator for EXP-BPY-002 .blend inputs."""
import hashlib
import json
import math
import sys

import bpy
import bmesh


EXPECTED_OBJECT = "EXP-BPY-001_Cube_20261102T105936"
EXPECTED_MESH = EXPECTED_OBJECT + "_Mesh"
EXPECTED_EXPERIMENT_ID = "EXP-BPY-001-20261102T105936-0300"
TOLERANCE_MM = 0.01


def contract_from_args():
    if "--" not in sys.argv:
        raise RuntimeError("A JSON validation contract is required after --")
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 1:
        raise RuntimeError("Expected exactly one JSON validation contract")
    return json.loads(args[0])


def topology_for(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
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
    result = {
        "vertices": len(bm.verts),
        "edges": len(bm.edges),
        "faces": len(bm.faces),
        "components": components,
        "all_edges_manifold": all(edge.is_manifold for edge in bm.edges),
    }
    bm.free()
    return result


def main():
    contract = contract_from_args()
    scene = bpy.context.scene
    objects = list(scene.objects)
    obj = bpy.data.objects.get(EXPECTED_OBJECT)
    findings = []

    findings.append({"check": "source_file_open", "pass": bool(bpy.data.filepath), "observed": bpy.data.filepath})
    findings.append({"check": "one_scene_object", "pass": len(objects) == 1, "expected": 1, "observed": len(objects)})
    findings.append({"check": "expected_object_exists", "pass": obj is not None, "expected": EXPECTED_OBJECT, "observed": [item.name for item in objects]})

    if obj is not None and obj.type == "MESH":
        mesh = obj.data
        raw = obj.get("parameters_mm", "")
        try:
            parameters = json.loads(raw)
        except Exception:
            parameters = None
        expected_params = contract["expected_parameters_mm"]
        params_ok = parameters == expected_params and obj.get("parameter_units") == "mm"
        findings.append({"check": "parameters", "pass": params_ok, "expected": expected_params, "observed": parameters, "units": obj.get("parameter_units")})

        revision_id = obj.get("revision_id")
        base_sha = obj.get("revision_base_sha256")
        findings.append({"check": "revision_metadata", "pass": revision_id == contract.get("expected_revision_id") and base_sha == contract.get("expected_revision_base_sha256"), "expected": {"revision_id": contract.get("expected_revision_id"), "revision_base_sha256": contract.get("expected_revision_base_sha256")}, "observed": {"revision_id": revision_id, "revision_base_sha256": base_sha}})

        identity_ok = obj.name == EXPECTED_OBJECT and mesh.name == EXPECTED_MESH and obj.get("experiment_id") == EXPECTED_EXPERIMENT_ID
        findings.append({"check": "identity_preserved", "pass": identity_ok, "expected": {"object": EXPECTED_OBJECT, "mesh": EXPECTED_MESH, "experiment_id": EXPECTED_EXPERIMENT_ID}, "observed": {"object": obj.name, "mesh": mesh.name, "experiment_id": obj.get("experiment_id")}})

        units = scene.unit_settings
        unit_ok = units.system == "METRIC" and math.isclose(units.scale_length, 1.0, rel_tol=0.0, abs_tol=1e-12) and units.length_unit == "MILLIMETERS"
        findings.append({"check": "units", "pass": unit_ok, "expected": {"system": "METRIC", "scale_length": 1.0, "length_unit": "MILLIMETERS"}, "observed": {"system": units.system, "scale_length": units.scale_length, "length_unit": units.length_unit}})

        coords = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
        if coords:
            mins = [min(coord[i] for coord in coords) for i in range(3)]
            maxs = [max(coord[i] for coord in coords) for i in range(3)]
            dims = [(maxs[i] - mins[i]) * 1000.0 for i in range(3)]
            center = [(maxs[i] + mins[i]) * 500.0 for i in range(3)]
        else:
            dims = [float("nan")] * 3
            center = [float("nan")] * 3
        axes = ("x", "y", "z")
        expected_dims = contract["expected_dimensions_mm"]
        deviations = {axes[i]: dims[i] - expected_dims[axes[i]] for i in range(3)}
        dims_ok = all(math.isfinite(deviations[axis]) and abs(deviations[axis]) <= TOLERANCE_MM for axis in axes)
        findings.append({"check": "dimensions_mm", "pass": dims_ok, "expected": expected_dims, "observed": dict(zip(axes, dims)), "deviation_mm": deviations, "tolerance_mm": TOLERANCE_MM})

        center_ok = all(math.isfinite(value) and abs(value) <= TOLERANCE_MM for value in center)
        findings.append({"check": "center_mm", "pass": center_ok, "expected": [0.0, 0.0, 0.0], "observed": center, "tolerance_mm": TOLERANCE_MM})
        transform_ok = all(abs(value) <= 1e-9 for value in obj.location) and all(abs(value) <= 1e-9 for value in obj.rotation_euler) and all(abs(value - 1.0) <= 1e-9 for value in obj.scale)
        findings.append({"check": "object_transform", "pass": transform_ok, "expected": {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}, "observed": {"location": list(obj.location), "rotation": list(obj.rotation_euler), "scale": list(obj.scale)}})

        topology = topology_for(mesh)
        expected_topology = {"vertices": 8, "edges": 12, "faces": 6, "components": 1, "all_edges_manifold": True}
        findings.append({"check": "topology", "pass": topology == expected_topology, "expected": expected_topology, "observed": topology})
        findings.append({"check": "no_modifiers_or_shape_keys", "pass": len(obj.modifiers) == 0 and mesh.shape_keys is None, "expected": {"modifier_count": 0, "shape_keys": False}, "observed": {"modifier_count": len(obj.modifiers), "shape_keys": mesh.shape_keys is not None}})

        geometry_points = sorted([[round(float((obj.matrix_world @ vertex.co)[i]) * 1000.0, 9) for i in range(3)] for vertex in mesh.vertices])
        canonical = {
            "object": obj.name,
            "mesh": mesh.name,
            "experiment_id": obj.get("experiment_id"),
            "revision_id": revision_id,
            "revision_base_sha256": base_sha,
            "parameters_mm": parameters,
            "units": {"system": units.system, "scale_length": units.scale_length, "length_unit": units.length_unit},
            "transform": {"location": list(obj.location), "rotation": list(obj.rotation_euler), "scale": list(obj.scale)},
            "points_mm_rounded_9": geometry_points,
            "topology": topology,
        }
        canonical_sha = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    else:
        parameters = None
        dims = [float("nan")] * 3
        center = [float("nan")] * 3
        topology = None
        canonical_sha = None

    result = {
        "run_id": "EXP-BPY-002-20261102T112024-0300",
        "label": contract.get("label"),
        "status": "PASS" if findings and all(item["pass"] for item in findings) else "FAIL",
        "opened_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "dimensions_mm": dict(zip(("x", "y", "z"), dims)),
        "center_mm": center,
        "parameters_mm": parameters,
        "topology": topology,
        "canonical_state_sha256": canonical_sha,
        "scene_objects": [{"name": item.name, "type": item.type} for item in objects],
        "text_datablocks": [text.name for text in bpy.data.texts],
        "findings": findings,
        "read_only": True,
    }
    print("EXP_BPY_002_VALIDATION " + json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise RuntimeError("EXP-BPY-002 contract validation failed")


if __name__ == "__main__":
    main()

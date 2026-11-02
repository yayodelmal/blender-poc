"""Read-only semantic inspection for an isolated copy of the EXP-BPY-001 blend."""
import json
import math
import sys

import bpy
import bmesh


EXPECTED_NAME = "EXP-BPY-001_Cube_20261102T105936"
EXPECTED_MESH_NAME = EXPECTED_NAME + "_Mesh"
EXPECTED_RUN_ID = "EXP-BPY-001-20261102T105936-0300"
EXPECTED_MM = {"x": 50.0, "y": 50.0, "z": 50.0}
TOLERANCE_MM = 0.01


def main():
    scene = bpy.context.scene
    objects = list(scene.objects)
    obj = bpy.data.objects.get(EXPECTED_NAME)
    findings = []
    findings.append({"check": "expected_object_present", "pass": obj is not None, "expected": EXPECTED_NAME, "observed": [o.name for o in objects]})
    findings.append({"check": "scene_object_count", "pass": len(objects) == 1, "expected": 1, "observed": len(objects)})

    details = {}
    if obj is not None and obj.type == "MESH":
        mesh = obj.data
        raw_params = obj.get("parameters_mm", "")
        try:
            params = json.loads(raw_params)
        except Exception:
            params = None
        details = {
            "object_name": obj.name,
            "mesh_name": mesh.name,
            "object_type": obj.type,
            "experiment_id": obj.get("experiment_id"),
            "parameter_units": obj.get("parameter_units"),
            "parameters_mm": params,
            "construction": obj.get("construction"),
            "location": list(obj.location),
            "rotation_euler": list(obj.rotation_euler),
            "scale": list(obj.scale),
            "modifiers": [{"name": m.name, "type": m.type} for m in obj.modifiers],
            "shape_keys_present": mesh.shape_keys is not None,
            "custom_property_names": sorted(k for k in obj.keys() if not k.startswith("_") ),
        }

        identity_ok = obj.name == EXPECTED_NAME and mesh.name == EXPECTED_MESH_NAME and obj.get("experiment_id") == EXPECTED_RUN_ID
        findings.append({"check": "identity_fingerprint", "pass": identity_ok, "expected": {"object": EXPECTED_NAME, "mesh": EXPECTED_MESH_NAME, "experiment_id": EXPECTED_RUN_ID}, "observed": {"object": obj.name, "mesh": mesh.name, "experiment_id": obj.get("experiment_id")}})
        findings.append({"check": "parameters_metadata", "pass": params == EXPECTED_MM and obj.get("parameter_units") == "mm", "expected": {"parameters_mm": EXPECTED_MM, "units": "mm"}, "observed": {"parameters_mm": params, "units": obj.get("parameter_units")}})
        unit_ok = scene.unit_settings.system == "METRIC" and math.isclose(scene.unit_settings.scale_length, 1.0, rel_tol=0.0, abs_tol=1e-12) and scene.unit_settings.length_unit == "MILLIMETERS"
        findings.append({"check": "units", "pass": unit_ok, "expected": {"system": "METRIC", "scale_length": 1.0, "length_unit": "MILLIMETERS"}, "observed": {"system": scene.unit_settings.system, "scale_length": scene.unit_settings.scale_length, "length_unit": scene.unit_settings.length_unit}})

        coordinates = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
        mins = [min(v[i] for v in coordinates) for i in range(3)] if coordinates else [float("nan")] * 3
        maxs = [max(v[i] for v in coordinates) for i in range(3)] if coordinates else [float("nan")] * 3
        axis_names = ("x", "y", "z")
        dimensions_mm = [(maxs[i] - mins[i]) * 1000.0 for i in range(3)]
        center_mm = [(maxs[i] + mins[i]) * 500.0 for i in range(3)]
        deviations = {axis_names[i]: dimensions_mm[i] - EXPECTED_MM[axis_names[i]] for i in range(3)}
        dimensions_ok = all(abs(deviations[axis]) <= TOLERANCE_MM for axis in axis_names)
        center_ok = all(math.isfinite(v) and abs(v) <= TOLERANCE_MM for v in center_mm)
        findings.append({"check": "mesh_dimensions_mm", "pass": dimensions_ok, "expected": EXPECTED_MM, "observed": dict(zip(axis_names, dimensions_mm)), "deviation_mm": deviations, "tolerance_mm": TOLERANCE_MM, "method": "base mesh vertices transformed by object matrix; no modifiers are present"})
        findings.append({"check": "geometric_center_mm", "pass": center_ok, "expected": [0.0, 0.0, 0.0], "observed": center_mm, "tolerance_mm": TOLERANCE_MM})
        transform_ok = all(abs(v) <= 1e-9 for v in obj.location) and all(abs(v) <= 1e-9 for v in obj.rotation_euler) and all(abs(v - 1.0) <= 1e-9 for v in obj.scale)
        findings.append({"check": "object_transform", "pass": transform_ok, "expected": {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}, "observed": {"location": list(obj.location), "rotation": list(obj.rotation_euler), "scale": list(obj.scale)}})

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
        topology = {"vertices": len(bm.verts), "edges": len(bm.edges), "faces": len(bm.faces), "components": components, "all_edges_manifold": all(edge.is_manifold for edge in bm.edges)}
        topology_ok = topology == {"vertices": 8, "edges": 12, "faces": 6, "components": 1, "all_edges_manifold": True}
        bm.free()
        findings.append({"check": "topology", "pass": topology_ok, "expected": {"vertices": 8, "edges": 12, "faces": 6, "components": 1, "all_edges_manifold": True}, "observed": topology})
        findings.append({"check": "no_unexpected_geometry_processors", "pass": len(obj.modifiers) == 0 and mesh.shape_keys is None, "expected": {"modifiers": 0, "shape_keys": False}, "observed": {"modifiers": details["modifiers"], "shape_keys_present": details["shape_keys_present"]}})
    else:
        findings.append({"check": "object_is_mesh", "pass": False, "observed_type": obj.type if obj else None})

    texts = [{"name": text.name, "length": len(text.as_string())} for text in bpy.data.texts]
    drivers = []
    for datablock in list(bpy.data.objects) + list(bpy.data.meshes) + list(bpy.data.scenes):
        animation = getattr(datablock, "animation_data", None)
        if animation:
            for driver in animation.drivers:
                drivers.append({"owner": datablock.name, "data_path": driver.data_path, "expression": driver.driver.expression})
    result = {
        "status": "PASS" if findings and all(item["pass"] for item in findings) else "FAIL",
        "opened_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "python_version": sys.version.split()[0],
        "scene_objects": [{"name": o.name, "type": o.type} for o in objects],
        "object_details": details,
        "text_datablocks": texts,
        "drivers": drivers,
        "findings": findings,
        "read_only_notice": "No Blender save operator or file-writing API was invoked by this script.",
    }
    print("INC_BPY_SEMANTIC_READONLY " + json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise RuntimeError("Read-only semantic checks failed; see findings")


if __name__ == "__main__":
    main()

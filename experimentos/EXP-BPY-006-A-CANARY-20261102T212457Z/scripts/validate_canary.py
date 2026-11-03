"""Independent, read-only validator for the A-parameter canary candidate."""
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh

RUN_ID = 'EXP-BPY-006-A-CANARY-20261102T212457Z'
OBJECT_NAME = 'EXP-BPY-006_ReliefPlate'
TOL_MM = 0.01
VOLUME_TOL_MM3 = 0.01
EXPECTED = {
    'width_mm': 80.0, 'height_mm': 60.0, 'base_mm': 4.0, 'relief_mm': 1.0,
    'brick_x_mm': 14.8, 'brick_y_mm': 7.0, 'joint_mm': 1.2,
    'pitch_x_mm': 16.0, 'pitch_y_mm': 8.2,
    'rows': 6, 'columns_even': 5, 'columns_odd': 4,
}
BASELINE = {
    **EXPECTED,
    'brick_x_mm': 15.0,
    'pitch_x_mm': 16.2,
}


def connected_components(bm):
    unseen = set(bm.verts)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            for edge in vertex.link_edges:
                other = edge.other_vert(vertex)
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def face_regions(faces):
    unseen = set(faces)
    regions = []
    while unseen:
        first = unseen.pop()
        stack = [first]
        group = [first]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for neighbor in edge.link_faces:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        stack.append(neighbor)
                        group.append(neighbor)
        regions.append(group)
    return regions


def region_record(region, obj):
    coords = [obj.matrix_world @ vertex.co for face in region for vertex in face.verts]
    xs = [point.x * 1000.0 for point in coords]
    ys = [point.y * 1000.0 for point in coords]
    zs = [point.z * 1000.0 for point in coords]
    area = sum(face.calc_area() for face in region) * 1e6
    return {
        'min_x_mm': min(xs), 'max_x_mm': max(xs),
        'min_y_mm': min(ys), 'max_y_mm': max(ys),
        'center_x_mm': (min(xs) + max(xs)) / 2.0,
        'center_y_mm': (min(ys) + max(ys)) / 2.0,
        'center_z_mm': sum(zs) / len(zs),
        'width_x_mm': max(xs) - min(xs),
        'width_y_mm': max(ys) - min(ys),
        'top_area_mm2': area,
    }


def cluster_rows(regions):
    groups = []
    for region in sorted(regions, key=lambda item: item['center_y_mm']):
        if not groups or abs(region['center_y_mm'] - groups[-1][0]['center_y_mm']) > TOL_MM:
            groups.append([region])
        else:
            groups[-1].append(region)
    return groups


def main():
    trailing = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if len(trailing) != 2:
        raise RuntimeError('expected candidate .blend path and evidence JSON path')
    blend_path = Path(trailing[0]).resolve()
    evidence_path = Path(trailing[1]).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(blend_path), load_ui=False)

    scene = bpy.context.scene
    obj = bpy.data.objects.get(OBJECT_NAME)
    findings = []

    def add(check, passed, **details):
        findings.append({'check': check, 'pass': bool(passed), **details})

    add('target_object_present', obj is not None, object_name=OBJECT_NAME)
    if obj is None:
        raise RuntimeError('target mesh object missing; evidence cannot be completed')

    recorded_parameters = json.loads(obj.get('parameters_mm', '{}'))
    add('canary_parameters_recorded', recorded_parameters == EXPECTED,
        expected=EXPECTED, observed=recorded_parameters)
    add('only_authorized_parameters_changed_vs_baseline',
        all(recorded_parameters.get(k) == v for k, v in BASELINE.items()
            if k not in ('brick_x_mm', 'pitch_x_mm'))
        and recorded_parameters.get('brick_x_mm') == 14.8
        and recorded_parameters.get('pitch_x_mm') == 16.0,
        baseline=BASELINE, observed=recorded_parameters)

    unit = scene.unit_settings
    units_ok = (unit.system == 'METRIC' and abs(unit.scale_length - 1.0) < 1e-12
                and unit.length_unit == 'MILLIMETERS')
    add('units_and_object_scale', units_ok and all(abs(v - 1.0) < 1e-9 for v in obj.scale),
        units={'system': unit.system, 'scale_length': unit.scale_length,
               'length_unit': unit.length_unit, 'object_scale': list(obj.scale)})

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph,
                                           preserve_all_data_layers=True)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    world_coords = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
    mins = [min(point[i] for point in world_coords) * 1000.0 for i in range(3)]
    maxs = [max(point[i] for point in world_coords) * 1000.0 for i in range(3)]
    dims = [maxs[i] - mins[i] for i in range(3)]
    add('evaluated_outer_envelope_mm',
        all(abs(dims[i] - target) <= TOL_MM for i, target in enumerate((80.0, 60.0, 5.0))),
        expected=[80.0, 60.0, 5.0], observed=dims, tolerance_mm=TOL_MM)

    bottom = [point for point in world_coords if abs(point.z * 1000.0) <= TOL_MM / 10]
    bottom_x = max(point.x for point in bottom) * 1000.0 - min(point.x for point in bottom) * 1000.0
    bottom_y = max(point.y for point in bottom) * 1000.0 - min(point.y for point in bottom) * 1000.0
    base_top_vertices = [vertex for vertex in bm.verts
                         if abs((obj.matrix_world @ vertex.co).z * 1000.0 - 4.0) <= TOL_MM / 10]
    base_ok = (abs(bottom_x - 80.0) <= TOL_MM and abs(bottom_y - 60.0) <= TOL_MM
               and abs(mins[2]) <= TOL_MM and bool(base_top_vertices))
    add('base_80x60x4_mm', base_ok,
        underside_dimensions_mm=[bottom_x, bottom_y], min_z_mm=mins[2],
        base_top_at_z4_vertex_count=len(base_top_vertices), tolerance_mm=TOL_MM)

    top_faces = [face for face in bm.faces
                 if all(abs((obj.matrix_world @ vertex.co).z * 1000.0 - maxs[2]) <= TOL_MM / 10
                        for vertex in face.verts)]
    regions = [region_record(group, obj) for group in face_regions(top_faces)]
    dimensions_ok = (len(regions) == 27 and all(
        abs(region['width_x_mm'] - 14.8) <= TOL_MM
        and abs(region['width_y_mm'] - 7.0) <= TOL_MM for region in regions))
    changed_from_baseline = (len(regions) == 27 and all(
        abs(region['width_x_mm'] - 15.0) > TOL_MM for region in regions))
    rows = cluster_rows(regions)
    row_counts = [len(row) for row in rows]
    x_gaps = []
    for row in rows:
        ordered = sorted(row, key=lambda item: item['center_x_mm'])
        for left, right in zip(ordered, ordered[1:]):
            x_gaps.append(right['min_x_mm'] - left['max_x_mm'])
    y_gaps = []
    for lower, upper in zip(rows, rows[1:]):
        y_gaps.append(min(item['min_y_mm'] for item in upper)
                      - max(item['max_y_mm'] for item in lower))
    spacing_ok = (len(rows) == 6 and row_counts == [5, 4, 5, 4, 5, 4]
                  and len(x_gaps) == 21 and len(y_gaps) == 5
                  and all(abs(gap - 1.2) <= TOL_MM for gap in x_gaps + y_gaps))
    add('27_physical_relief_regions_and_canary_dimensions', dimensions_ok and changed_from_baseline,
        expected_count=27, observed_top_regions=len(regions), expected_brick_mm=[14.8, 7.0],
        regions=regions, baseline_brick_x_mm=15.0, changed_from_baseline=changed_from_baseline,
        tolerance_mm=TOL_MM)
    add('pattern_spacing_x_y_mm', spacing_ok, expected_gap_mm=1.2,
        observed_x_gaps_mm=x_gaps, observed_y_gaps_mm=y_gaps,
        row_counts=row_counts, tolerance_mm=TOL_MM)

    components = connected_components(bm)
    manifold = bool(bm.edges) and all(edge.is_manifold for edge in bm.edges)
    contiguous = bool(bm.edges) and all(edge.is_contiguous for edge in bm.edges)
    volume_mm3 = bm.calc_volume(signed=True) * 1e9
    expected_volume = (80.0 * 60.0 * 4.0) + (27 * 14.8 * 7.0 * 1.0)
    add('single_closed_manifold_component', components == 1 and manifold,
        components=components, all_edges_manifold=manifold, all_edges_contiguous=contiguous)
    add('positive_volume_expected_from_canary_parameters',
        volume_mm3 > 0 and abs(volume_mm3 - expected_volume) <= VOLUME_TOL_MM3,
        expected_formula_mm3='80*60*4 + 27*14.8*7*1 = 21997.2',
        expected_volume_mm3=expected_volume, observed_volume_mm3=volume_mm3,
        tolerance_mm3=VOLUME_TOL_MM3)
    degenerate_edges = sum(edge.calc_length() <= 1e-12 for edge in bm.edges)
    degenerate_faces = sum(face.calc_area() <= 1e-15 for face in bm.faces)
    add('no_degenerate_elements', degenerate_edges == 0 and degenerate_faces == 0,
        degenerate_edges=degenerate_edges, degenerate_faces=degenerate_faces)

    status = 'PASS' if all(item['pass'] for item in findings) else 'FAIL'
    result = {
        'run_id': RUN_ID, 'status': status, 'opened_file': str(blend_path),
        'validation_mode': 'independent_read_only_no_blend_save',
        'blender_version': bpy.app.version_string, 'blender_build_hash': bpy.app.build_hash.decode('ascii', errors='replace'),
        'python_version': sys.version.split()[0], 'object': obj.name,
        'parameters_mm': recorded_parameters, 'dimensions_mm': dims,
        'base_dimensions_mm': [bottom_x, bottom_y, 4.0],
        'brick_count': len(regions), 'brick_regions': regions,
        'row_counts': row_counts, 'x_gaps_mm': x_gaps, 'y_gaps_mm': y_gaps,
        'components': components, 'all_edges_manifold': manifold,
        'all_edges_contiguous': contiguous, 'volume_mm3': volume_mm3,
        'expected_volume_mm3': expected_volume,
        'vertices': len(bm.verts), 'edges': len(bm.edges), 'faces': len(bm.faces),
        'findings': findings,
    }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print('CANARY_VALIDATION ' + json.dumps(result, sort_keys=True))
    bm.free()
    bpy.data.meshes.remove(mesh)
    if status != 'PASS':
        raise RuntimeError('canary validation failed; preserve evidence and stop')


main()

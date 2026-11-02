"""Read-only preflight and topology-region inventory for an EXP-BPY-006 source copy."""
import json
import sys

import bpy
import bmesh

OBJECT_NAME = 'EXP-BPY-003_ReliefPlate'
EXPECTED_PARAMS = {
    'base_thickness': 4.0,
    'brick_height': 8.4,
    'brick_length': 18.0,
    'brick_pitch_x': 19.2,
    'edge_margin': 0.6,
    'joint': 1.2,
    'overlap_into_base': 0.5,
    'plate_height': 60.0,
    'plate_width': 80.0,
    'relief_height': 1.0,
    'row_pitch': 9.6,
    'rows': 6,
}
EPS = 1e-7


def connected_face_groups(faces):
    unseen = set(faces)
    groups = []
    while unseen:
        seed = unseen.pop()
        group = {seed}
        stack = [seed]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for other in edge.link_faces:
                    if other in unseen:
                        unseen.remove(other)
                        group.add(other)
                        stack.append(other)
        groups.append(group)
    return groups


def components(bm):
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


def main():
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    obj = bpy.data.objects.get(OBJECT_NAME)
    checks = []
    checks.append({'check': 'source_file_opened', 'pass': bool(bpy.data.filepath), 'path': bpy.data.filepath})
    checks.append({'check': 'one_expected_mesh', 'pass': obj is not None and len(meshes) == 1,
                   'mesh_objects': [item.name for item in meshes]})
    if obj is None:
        raise RuntimeError('Expected source object not found')
    params = json.loads(obj.get('parameters_mm', '{}'))
    checks.append({'check': 'initial_parameters', 'pass': params == EXPECTED_PARAMS,
                   'expected': EXPECTED_PARAMS, 'observed': params})
    units = bpy.context.scene.unit_settings
    checks.append({'check': 'metric_units', 'pass': units.system == 'METRIC' and
                   units.scale_length == 1 and units.length_unit == 'MILLIMETERS',
                   'observed': {'system': units.system, 'scale_length': units.scale_length,
                                'length_unit': units.length_unit}})

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph, preserve_all_data_layers=True)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    world = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
    mins = [min(p[i] for p in world) for i in range(3)]
    maxs = [max(p[i] for p in world) for i in range(3)]
    dims = [(maxs[i] - mins[i]) * 1000 for i in range(3)]
    center = [(maxs[i] + mins[i]) * 500 for i in range(3)]
    expected = [80.0, 60.0, 5.0]
    checks.append({'check': 'evaluated_dimensions', 'pass': all(abs(a-b) <= 0.01 for a,b in zip(dims, expected)),
                   'expected_mm': expected, 'observed_mm': dims, 'tolerance_mm': 0.01})
    checks.append({'check': 'base_plane', 'pass': abs(mins[2] * 1000) <= 0.01 and abs(params['base_thickness'] - 4) <= 0.01,
                   'min_z_mm': mins[2]*1000, 'base_thickness_mm': params['base_thickness']})
    top_faces = [face for face in bm.faces if all(abs((obj.matrix_world @ v.co).z - maxs[2]) <= EPS for v in face.verts)]
    top_groups = connected_face_groups(top_faces)
    top_regions = []
    for group in top_groups:
        verts = {v for face in group for v in face.verts}
        points = [obj.matrix_world @ v.co for v in verts]
        top_regions.append({
            'face_count': len(group), 'vertex_count': len(verts),
            'bounds_mm': [[min(p[i] for p in points)*1000, max(p[i] for p in points)*1000] for i in range(3)],
            'center_xy_mm': [sum((min(p[i] for p in points)+max(p[i] for p in points))*500 for _ in [0])/1 for i in range(2)],
        })
    # Face-connected surfaces at/above the base top plane are inventoried to assess whether
    # each raised feature can be isolated without altering the saved source.
    raised_faces = [face for face in bm.faces if min((obj.matrix_world @ v.co).z for v in face.verts) >= params['base_thickness']/1000 - EPS]
    raised_groups = connected_face_groups(raised_faces)
    manifold = all(edge.is_manifold for edge in bm.edges)
    result = {
        'run_id': 'EXP-BPY-006-20261102T175526Z', 'source': bpy.data.filepath,
        'blender': bpy.app.version_string, 'python': sys.version.split()[0],
        'object_name': obj.name, 'mesh_name': obj.data.name,
        'object_pointer': obj.as_pointer(), 'mesh_pointer': obj.data.as_pointer(),
        'parameters_mm': params, 'dimensions_mm': dims, 'center_mm': center,
        'top_face_island_count': len(top_groups), 'top_regions': top_regions,
        'raised_surface_face_group_count_including_base_contacts': len(raised_groups),
        'topology': {'vertices': len(bm.verts), 'edges': len(bm.edges), 'faces': len(bm.faces),
                     'components': components(bm), 'all_edges_manifold': manifold,
                     'contiguous_normals': all(e.is_contiguous for e in bm.edges if e.is_manifold),
                     'signed_volume_mm3': bm.calc_volume(signed=True)*1e9,
                     'modifier_names': [m.name for m in obj.modifiers]},
        'checks': checks,
        'read_only': True,
    }
    print('EXP_BPY_006_SOURCE_INSPECTION ' + json.dumps(result, sort_keys=True))
    bm.free()
    bpy.data.meshes.remove(mesh)
    if not all(item['pass'] for item in checks):
        raise RuntimeError('Source preflight failed')


if __name__ == '__main__':
    main()

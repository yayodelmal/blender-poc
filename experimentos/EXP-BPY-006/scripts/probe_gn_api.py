import bpy
g=bpy.data.node_groups.new('probe','GeometryNodeTree')
for typ in ('GeometryNodeMeshBoolean','GeometryNodeMeshGrid','GeometryNodeMeshCube'):
 n=g.nodes.new(typ)
 if typ=='GeometryNodeMeshBoolean': n.operation='UNION'
 print('NODE_SOCKET_PROBE',typ,'INPUTS',[(s.name,s.identifier,s.type,s.is_multi_input) for s in n.inputs],'OUTPUTS',[(s.name,s.identifier,s.type) for s in n.outputs])

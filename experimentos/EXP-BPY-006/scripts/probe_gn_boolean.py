import bpy,bmesh,json
s=bpy.context.scene; bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
ob=bpy.data.objects.new('Probe',bpy.data.meshes.new('carrier')); s.collection.objects.link(ob)
g=bpy.data.node_groups.new('ProbeBoolean','GeometryNodeTree'); g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry'); g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
base=g.nodes.new('GeometryNodeMeshCube'); base.inputs['Size'].default_value=(.08,.06,.004)
trans=g.nodes.new('GeometryNodeTransform'); trans.inputs['Translation'].default_value=(0,0,.002); g.links.new(base.outputs['Mesh'],trans.inputs['Geometry'])
br=g.nodes.new('GeometryNodeMeshCube'); br.inputs['Size'].default_value=(.015,.007,.0012)
bt=g.nodes.new('GeometryNodeTransform'); bt.inputs['Translation'].default_value=(0,0,.0044); g.links.new(br.outputs['Mesh'],bt.inputs['Geometry'])
bo=g.nodes.new('GeometryNodeMeshBoolean'); bo.operation='UNION'; g.links.new(bt.outputs['Geometry'],bo.inputs[0]); g.links.new(trans.outputs['Geometry'],bo.inputs[1])
out=g.nodes.new('NodeGroupOutput'); g.links.new(bo.outputs['Mesh'],out.inputs['Geometry'])
m=ob.modifiers.new('gn','NODES'); m.node_group=g; bpy.context.view_layer.update(); d=bpy.context.evaluated_depsgraph_get(); e=ob.evaluated_get(d); me=bpy.data.meshes.new_from_object(e,depsgraph=d)
bm=bmesh.new(); bm.from_mesh(me); un=set(bm.verts); c=0
while un:
 c+=1; stack=[un.pop()]
 while stack:
  v=stack.pop()
  for ed in v.link_edges:
   u=ed.other_vert(v)
   if u in un: un.remove(u); stack.append(u)
ps=[v.co for v in me.vertices]; dims=[(max(p[i] for p in ps)-min(p[i] for p in ps))*1000 for i in range(3)]
print('GN_BOOLEAN_PROBE',json.dumps({'operation':bo.operation,'dims_mm':dims,'components':c,'vertices':len(me.vertices),'faces':len(me.polygons),'links':[(x.from_node.type,x.to_node.type,x.to_socket.name) for x in g.links]},sort_keys=True))

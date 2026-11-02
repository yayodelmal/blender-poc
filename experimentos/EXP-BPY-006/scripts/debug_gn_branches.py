"""Read candidate GN graph, temporarily expose branches in memory, never save."""
import sys,json,bpy

path=sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.open_mainfile(filepath=path,load_ui=False)
obj=bpy.data.objects['EXP-BPY-006_ReliefPlate']; ng=next(m.node_group for m in obj.modifiers if m.type=='NODES')
out=next(n for n in ng.nodes if n.type=='GROUP_OUTPUT')
for label in ('Base desde Z=0','Ladrillos sobre base','Unión booleana'):
 node=next(n for n in ng.nodes if n.label==label)
 for link in list(ng.links):
  if link.to_node==out: ng.links.remove(link)
 source=node.outputs.get('Geometry') or node.outputs.get('Mesh')
 ng.links.new(source,out.inputs['Geometry'])
 bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dg); me=bpy.data.meshes.new_from_object(ev,depsgraph=dg)
 if me.vertices:
  ps=[obj.matrix_world@v.co for v in me.vertices]; dims=[(max(p[i] for p in ps)-min(p[i] for p in ps))*1000 for i in range(3)]; lo=[min(p[i] for p in ps)*1000 for i in range(3)]
 else: dims=[];lo=[]
 print('GN_BRANCH',json.dumps({'branch':label,'dims_mm':dims,'min_mm':lo,'vertices':len(me.vertices),'faces':len(me.polygons)},sort_keys=True))
 bpy.data.meshes.remove(me)
print('GN_LINKS',json.dumps([{'from':x.from_node.label or x.from_node.name,'out':x.from_socket.name,'to':x.to_node.label or x.to_node.name,'in':x.to_socket.name} for x in ng.links],sort_keys=True))

"""Build one multi-input UNION variant; verify effective link order before save."""
import json,os,sys,bpy
RUN='EXP-BPY-006-GN-MULTIORDER-20261102T211540Z'; ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API=os.path.join(ROOT,'evidencias','api_order_preflight.json')
def socket_order(sock): return [link.from_node.label.replace('Input ','') for link in sock.links]
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=2: raise RuntimeError('Expected VARIANT OUTPUT')
    variant,out=sys.argv[sys.argv.index('--')+1:]; out=os.path.abspath(out)
    if variant not in ('A_BEFORE_B','B_BEFORE_A'): raise RuntimeError('Unknown variant')
    if os.path.exists(out): raise FileExistsError(out)
    with open(API,encoding='utf-8') as f: api=json.load(f)
    if not api.get('preflight_pass'): raise RuntimeError('API link-order preflight did not pass')
    desired=['A','B'] if variant=='A_BEFORE_B' else ['B','A']
    creation=next((x['creation_sequence'] for x in api['link_order_tests'].values() if [e['node'] for e in x['effective_order']]==desired),None)
    if creation is None: raise RuntimeError('No tested creation sequence yields requested order')
    scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1.0; scene.unit_settings.length_unit='MILLIMETERS'
    carrier=bpy.data.meshes.new('GN_MULTIORDER_EmptyCarrier'); obj=bpy.data.objects.new('GN_MULTIORDER_Result',carrier); scene.collection.objects.link(obj)
    obj['run_id']=RUN; obj['variant']=variant; obj['expected_multi_input_order']=json.dumps(desired)
    group=bpy.data.node_groups.new('GN_MULTIORDER_'+variant,'GeometryNodeTree'); group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    def node(kind,label):
        n=group.nodes.new(kind); n.label=label; return n
    boolean=node('GeometryNodeMeshBoolean','Boolean UNION'); boolean.operation='UNION'
    multis=[(i,s) for i,s in enumerate(boolean.inputs) if s.enabled and s.type=='GEOMETRY' and s.is_multi_input]
    geo=[s for s in boolean.outputs if s.enabled and s.type=='GEOMETRY']
    disabled_mesh1=[s for s in boolean.inputs if s.name=='Mesh 1' and s.type=='GEOMETRY' and not s.enabled]
    if len(multis)!=1 or len(geo)!=1 or len(disabled_mesh1)!=1: raise RuntimeError('Live Boolean socket identity differs from API preflight')
    socket=multis[0][1]
    if (socket.name,socket.identifier)!=(api['resolved_multi_input']['name'],api['resolved_multi_input']['identifier']) or (geo[0].name,geo[0].identifier)!=(api['resolved_geometry_output']['name'],api['resolved_geometry_output']['identifier']): raise RuntimeError('Live Boolean sockets differ from preflight inventory')
    cubes={}; transforms={}
    for label,x in [('A',.005),('B',.0148)]:
        cube=node('GeometryNodeMeshCube','Cube '+label); cube.inputs['Size'].default_value=(.01,.01,.01); cubes[label]=cube
        trans=node('GeometryNodeTransform','Input '+label); trans.inputs['Translation'].default_value=(x,.005,.005); group.links.new(cube.outputs['Mesh'],trans.inputs['Geometry']); transforms[label]=trans
    # The creation sequence is selected from this run's measured preflight mapping.
    link_ids={}
    for label in creation:
        link=group.links.new(transforms[label].outputs['Geometry'],socket)
        link_ids[label]=getattr(link,'multi_input_sort_id',None)
    actual=socket_order(socket)
    print('GN_MULTIORDER_LINK_CHECK '+json.dumps({'variant':variant,'expected_order':desired,'creation_sequence':creation,'observed_order':actual,'read_only_sort_ids':link_ids},sort_keys=True))
    if actual!=desired: raise RuntimeError('Effective multi-input order mismatch; refusing to save candidate')
    if len(disabled_mesh1[0].links)!=0: raise RuntimeError('Unexpected link connected to disabled Mesh 1')
    output=node('NodeGroupOutput','Union output'); group.links.new(boolean.outputs[geo[0].identifier],output.inputs['Geometry'])
    mod=obj.modifiers.new('GN_MULTIORDER_UNION','NODES'); mod.node_group=group
    obj.select_set(True); bpy.context.view_layer.objects.active=obj
    os.makedirs(os.path.dirname(out),exist_ok=True); save_result=bpy.ops.wm.save_as_mainfile(filepath=out,check_existing=False)
    if 'FINISHED' not in save_result: raise RuntimeError('Save failed')
    result={'run_id':RUN,'variant':variant,'artifact':out,'blender_version':bpy.app.version_string,'operation':'UNION','resolved_multi_input':{'name':socket.name,'identifier':socket.identifier},'resolved_output':{'name':geo[0].name,'identifier':geo[0].identifier},'expected_order':desired,'creation_sequence':creation,'observed_order':actual,'read_only_sort_ids':link_ids,'input_A':{'dimensions_mm':[10,10,10],'center_mm':[5,5,5]},'input_B':{'dimensions_mm':[10,10,10],'center_mm':[14.8,5,5]},'overlap_x_mm':.2,'expected_union':{'dimensions_mm':[19.8,10,10],'volume_mm3':1980}}
    print('GN_MULTIORDER_BUILD '+json.dumps(result,sort_keys=True))
main()

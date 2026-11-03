"""Inspect Boolean sockets and prove multi-input link order can be inverted."""
import json,os,sys,bpy
RUN='EXP-BPY-006-GN-MULTI-20261102T210408Z'
def snapshot(socket):
    return [{'from_node':l.from_node.label or l.from_node.name,'from_socket':l.from_socket.name,'sort_id':getattr(l,'multi_input_sort_id',None)} for l in socket.links]
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=1: raise RuntimeError('Expected inventory output path')
    path=os.path.abspath(sys.argv[sys.argv.index('--')+1]); tree=bpy.data.node_groups.new('GN_MULTI_API_INSPECTION','GeometryNodeTree')
    boolean=tree.nodes.new('GeometryNodeMeshBoolean'); boolean.operation='UNION'
    ins=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled,'multi_input':s.is_multi_input} for i,s in enumerate(boolean.inputs)]
    outs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled} for i,s in enumerate(boolean.outputs)]
    multis=[(i,s) for i,s in enumerate(boolean.inputs) if s.enabled and s.type=='GEOMETRY' and s.is_multi_input]
    geo_out=[s for s in boolean.outputs if s.enabled and s.type=='GEOMETRY']
    # Test API ordering only: links are formed, inspected, and removed; no geometry is evaluated or saved.
    a=tree.nodes.new('GeometryNodeMeshCube'); a.label='TEST_A'
    b=tree.nodes.new('GeometryNodeMeshCube'); b.label='TEST_B'
    order_ab=order_ba=[]; socket_index=None
    if len(multis)==1 and len(geo_out)==1:
        socket_index,multi=multis[0]
        tree.links.new(a.outputs['Mesh'],multi); tree.links.new(b.outputs['Mesh'],multi); order_ab=snapshot(multi)
        for link in list(multi.links): tree.links.remove(link)
        tree.links.new(b.outputs['Mesh'],multi); tree.links.new(a.outputs['Mesh'],multi); order_ba=snapshot(multi)
    resolved={'name':geo_out[0].name,'identifier':geo_out[0].identifier,'type':geo_out[0].type} if len(geo_out)==1 else None
    sequence_ab=[x['from_node'] for x in order_ab]; sequence_ba=[x['from_node'] for x in order_ba]
    ok=len(multis)==1 and len(geo_out)==1 and sequence_ab==['TEST_A','TEST_B'] and sequence_ba==['TEST_B','TEST_A']
    result={'run_id':RUN,'blender_version':bpy.app.version_string,'operation':'UNION','inputs':ins,'outputs':outs,'active_geometry_multi_input_candidates':len(multis),'multi_input_index':socket_index,'multi_input_name':multis[0][1].name if len(multis)==1 else None,'geometry_output_candidates':len(geo_out),'resolved_geometry_output':resolved,'test_link_order_A_then_B':order_ab,'test_link_order_B_then_A':order_ba,'order_inversion_observed':sequence_ab==['TEST_A','TEST_B'] and sequence_ba==['TEST_B','TEST_A'],'api_unambiguous':len(multis)==1 and len(geo_out)==1 and ok,'geometry_evaluated':False}
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'x',encoding='utf-8') as f: json.dump(result,f,indent=2); f.write('\n')
    print('GN_MULTI_API '+json.dumps(result,sort_keys=True))
    if not result['api_unambiguous']: raise SystemExit(2)
main()

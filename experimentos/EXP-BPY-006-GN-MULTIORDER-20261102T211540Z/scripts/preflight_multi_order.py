"""Inspect Boolean sockets and the effective order for both link creation sequences."""
import json,os,sys,traceback,bpy
RUN='EXP-BPY-006-GN-MULTIORDER-20261102T211540Z'
def order(socket):
    return [{'node':link.from_node.label,'sort_id':getattr(link,'multi_input_sort_id',None)} for link in socket.links]
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=1: raise RuntimeError('Expected API inventory output path')
    path=os.path.abspath(sys.argv[sys.argv.index('--')+1]); result={'run_id':RUN,'blender_version':bpy.app.version_string,'geometry_evaluated':False,'multi_input_sort_id_assigned':False}
    try:
        tree=bpy.data.node_groups.new('GN_MULTIORDER_PREFLIGHT','GeometryNodeTree'); boolean=tree.nodes.new('GeometryNodeMeshBoolean'); boolean.operation='UNION'
        inputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled,'multi_input':s.is_multi_input} for i,s in enumerate(boolean.inputs)]
        outputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled} for i,s in enumerate(boolean.outputs)]
        multi=[(i,s) for i,s in enumerate(boolean.inputs) if s.enabled and s.type=='GEOMETRY' and s.is_multi_input]
        out=[s for s in boolean.outputs if s.enabled and s.type=='GEOMETRY']
        mesh1=[s for s in boolean.inputs if s.name=='Mesh 1' and s.type=='GEOMETRY' and not s.enabled]
        result.update({'operation':'UNION','inputs':inputs,'outputs':outputs,'active_geometry_multi_input_count':len(multi),'resolved_multi_input':{'index':multi[0][0],'name':multi[0][1].name,'identifier':multi[0][1].identifier} if len(multi)==1 else None,'disabled_mesh1_count':len(mesh1),'enabled_geometry_output_count':len(out),'resolved_geometry_output':{'name':out[0].name,'identifier':out[0].identifier} if len(out)==1 else None})
        if len(multi)!=1 or len(out)!=1 or len(mesh1)!=1: raise RuntimeError('Socket identity is ambiguous or does not match expected API')
        sock=multi[0][1]; a=tree.nodes.new('GeometryNodeMeshCube'); a.label='A'; b=tree.nodes.new('GeometryNodeMeshCube'); b.label='B'
        link_orders={}
        for creation,label in [(('A','B'),'create_A_then_B'),(('B','A'),'create_B_then_A')]:
            for link in list(sock.links): tree.links.remove(link)
            nodes={'A':a,'B':b}
            for key in creation: tree.links.new(nodes[key].outputs['Mesh'],sock)
            link_orders[label]={'creation_sequence':creation,'effective_order':order(sock)}
        eff1=[x['node'] for x in link_orders['create_A_then_B']['effective_order']]
        eff2=[x['node'] for x in link_orders['create_B_then_A']['effective_order']]
        both_orders={tuple(eff1),tuple(eff2)}=={('A','B'),('B','A')}
        result.update({'link_order_tests':link_orders,'both_effective_orders_observed':both_orders,'preflight_pass':both_orders and all(len(v['effective_order'])==2 for v in link_orders.values())})
        if not result['preflight_pass']: raise RuntimeError('Creation sequences did not yield both opposite, verifiable effective orders')
    except Exception as exc: result.update({'preflight_pass':False,'error':repr(exc),'traceback':traceback.format_exc()})
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'x',encoding='utf-8') as f: json.dump(result,f,indent=2); f.write('\n')
    print('GN_MULTIORDER_PREFLIGHT '+json.dumps(result,sort_keys=True))
    if not result.get('preflight_pass'): raise SystemExit(2)
main()

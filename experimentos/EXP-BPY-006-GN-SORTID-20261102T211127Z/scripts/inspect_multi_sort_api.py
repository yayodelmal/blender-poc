"""Preflight Boolean sockets and explicit multi_input_sort_id behavior; no geometry eval/save."""
import json,os,sys,traceback,bpy
RUN='EXP-BPY-006-GN-SORTID-20261102T211127Z'
def read_order(sock):
    return [{'node':link.from_node.label,'sort_id':link.multi_input_sort_id} for link in sock.links]
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=1: raise RuntimeError('Expected API inventory JSON path')
    path=os.path.abspath(sys.argv[sys.argv.index('--')+1]); result={'run_id':RUN,'blender_version':bpy.app.version_string,'geometry_evaluated':False}
    try:
        tree=bpy.data.node_groups.new('GN_SORTID_API_PROBE','GeometryNodeTree'); boolean=tree.nodes.new('GeometryNodeMeshBoolean'); boolean.operation='UNION'
        inputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled,'multi_input':s.is_multi_input} for i,s in enumerate(boolean.inputs)]
        outputs=[{'index':i,'name':s.name,'identifier':s.identifier,'type':s.type,'enabled':s.enabled} for i,s in enumerate(boolean.outputs)]
        multi=[(i,s) for i,s in enumerate(boolean.inputs) if s.enabled and s.type=='GEOMETRY' and s.is_multi_input]
        geo=[s for s in boolean.outputs if s.enabled and s.type=='GEOMETRY']
        result.update({'operation':'UNION','inputs':inputs,'outputs':outputs,'active_geometry_multi_input_candidates':len(multi),'geometry_output_candidates':len(geo),'resolved_multi_input':{'index':multi[0][0],'name':multi[0][1].name,'identifier':multi[0][1].identifier} if len(multi)==1 else None,'resolved_geometry_output':{'name':geo[0].name,'identifier':geo[0].identifier} if len(geo)==1 else None})
        if len(multi)!=1 or len(geo)!=1: raise RuntimeError('Socket identity ambiguous')
        disabled_mesh1=[s for s in boolean.inputs if s.name=='Mesh 1' and s.type=='GEOMETRY' and not s.enabled]
        if len(disabled_mesh1)!=1: raise RuntimeError('Mesh 1 not uniquely identified as disabled')
        sock=multi[0][1]; a=tree.nodes.new('GeometryNodeMeshCube'); a.label='A'; b=tree.nodes.new('GeometryNodeMeshCube'); b.label='B'
        link_a=tree.links.new(a.outputs['Mesh'],sock); link_b=tree.links.new(b.outputs['Mesh'],sock)
        assignments=[]
        for label,sort_id in [('A',1),('B',0)]:
            link=link_a if label=='A' else link_b; link.multi_input_sort_id=sort_id
            assignments.append({'node':label,'assigned_sort_id':sort_id,'read_back_sort_id':link.multi_input_sort_id})
        tree.update_tag(); order_ab=read_order(sock)
        link_a.multi_input_sort_id=0; link_b.multi_input_sort_id=1
        tree.update_tag(); order_ba=read_order(sock)
        ok=order_ab==[{'node':'A','sort_id':1},{'node':'B','sort_id':0}] and order_ba==[{'node':'B','sort_id':1},{'node':'A','sort_id':0}] and all(x['assigned_sort_id']==x['read_back_sort_id'] for x in assignments)
        result.update({'sort_id_property_available':True,'assignments_A_before_B':assignments,'observed_order_A_before_B':order_ab,'observed_order_B_before_A':order_ba,'explicit_ordering_verified':ok,'preflight_pass':ok})
        if not ok: raise RuntimeError('Explicit sort IDs did not create both exact socket link orders')
    except Exception as exc:
        result.update({'preflight_pass':False,'error':repr(exc),'traceback':traceback.format_exc()})
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'x',encoding='utf-8') as f: json.dump(result,f,indent=2); f.write('\n')
    print('GN_SORTID_API '+json.dumps(result,sort_keys=True))
    if not result.get('preflight_pass'): raise SystemExit(2)
main()

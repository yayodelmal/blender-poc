"""Read-only independent validation of saved multi-input Boolean variants."""
import json,os,sys,bpy,bmesh
RUN='EXP-BPY-006-GN-MULTIORDER-20261102T211540Z'; TOL_MM=.01; TOL_VOL=.1
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); API=os.path.join(ROOT,'evidencias','api_order_preflight.json')
def components(bm):
    unseen=set(bm.verts); total=0
    while unseen:
        total+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen: unseen.remove(q); stack.append(q)
    return total
def measure(obj,label):
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dg); me=bpy.data.meshes.new_from_object(ev,depsgraph=dg,preserve_all_data_layers=True)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update(); pts=[obj.matrix_world@v.co for v in me.vertices]
    dims=[(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(3)] if pts else []
    center=[(max(p[i] for p in pts)+min(p[i] for p in pts))*500 for i in range(3)] if pts else []
    volume=bm.calc_volume(signed=True)*1e9 if bm.faces else 0.0
    result={'label':label,'dimensions_mm':dims,'center_mm':center,'signed_volume_mm3':volume,'components':components(bm) if bm.verts else 0,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'all_edges_manifold':bool(bm.edges) and all(e.is_manifold for e in bm.edges),'all_manifold_edges_contiguous':bool(bm.edges) and all(e.is_contiguous for e in bm.edges if e.is_manifold),'degenerate_edges':sum(e.calc_length()<=1e-12 for e in bm.edges),'degenerate_faces':sum(f.calc_area()<=1e-15 for f in bm.faces)}
    bm.free(); bpy.data.meshes.remove(me); return result
def close(a,b,tol=TOL_MM): return len(a)==len(b) and all(abs(x-y)<=tol for x,y in zip(a,b))
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=2: raise RuntimeError('Expected BLEND RESULT_JSON')
    blend,result_path=sys.argv[sys.argv.index('--')+1:]; blend=os.path.abspath(blend); result_path=os.path.abspath(result_path)
    if os.path.exists(result_path): raise FileExistsError(result_path)
    with open(API,encoding='utf-8') as f: api=json.load(f)
    if not api.get('preflight_pass'): raise RuntimeError('API preflight failed; refusing validation')
    bpy.ops.wm.open_mainfile(filepath=blend,load_ui=False)
    obj=bpy.data.objects.get('GN_MULTIORDER_Result')
    if obj is None: raise RuntimeError('Opened file lacks expected result object')
    mod=next((m for m in obj.modifiers if m.type=='NODES' and m.node_group),None)
    if mod is None: raise RuntimeError('Opened file lacks Geometry Nodes modifier')
    group=mod.node_group; boolean=next((n for n in group.nodes if n.label=='Boolean UNION'),None); out=next((n for n in group.nodes if n.type=='GROUP_OUTPUT'),None)
    if boolean is None or out is None: raise RuntimeError('Boolean node or Group Output missing')
    # Resolve both sockets unambiguously before any geometry evaluation.
    multis=[(i,s) for i,s in enumerate(boolean.inputs) if s.enabled and s.type=='GEOMETRY' and s.is_multi_input]
    outs=[s for s in boolean.outputs if s.enabled and s.type=='GEOMETRY']
    mesh1=[s for s in boolean.inputs if s.name=='Mesh 1' and s.type=='GEOMETRY' and not s.enabled]
    if len(multis)!=1 or len(outs)!=1 or len(mesh1)!=1: raise RuntimeError('Live socket resolution ambiguous; refusing geometry evaluation')
    sock=multis[0][1]; geometry_out=outs[0]
    if (sock.name,sock.identifier)!=(api['resolved_multi_input']['name'],api['resolved_multi_input']['identifier']) or (geometry_out.name,geometry_out.identifier)!=(api['resolved_geometry_output']['name'],api['resolved_geometry_output']['identifier']): raise RuntimeError('Live sockets differ from this run API inventory')
    variant=obj.get('variant'); expected=['A','B'] if variant=='A_BEFORE_B' else ['B','A']
    actual=[l.from_node.label.replace('Input ','') for l in sock.links]
    mesh1_unlinked=len(mesh1[0].links)==0
    a=next((n for n in group.nodes if n.label=='Input A'),None); b=next((n for n in group.nodes if n.label=='Input B'),None)
    if a is None or b is None: raise RuntimeError('Input transform nodes missing')
    checks=[{'check':'resolved_sockets_before_evaluation','pass':True,'multi_input':{'name':sock.name,'identifier':sock.identifier},'geometry_output':{'name':geometry_out.name,'identifier':geometry_out.identifier}},{'check':'saved_effective_link_order','pass':actual==expected,'expected':expected,'observed':actual,'read_only_sort_ids':[getattr(l,'multi_input_sort_id',None) for l in sock.links]},{'check':'disabled_Mesh1_unlinked','pass':mesh1_unlinked,'link_count':len(mesh1[0].links)}]
    def expose(node):
        for link in list(group.links):
            if link.to_node==out: group.links.remove(link)
        group.links.new(node.outputs['Geometry'],out.inputs['Geometry'])
    expose(a); ma=measure(obj,'input_A'); expose(b); mb=measure(obj,'input_B')
    def input_pass(m,center): return close(m['dimensions_mm'],[10,10,10]) and close(m['center_mm'],center) and abs(m['signed_volume_mm3']-1000)<=TOL_VOL and m['components']==1 and m['all_edges_manifold'] and m['degenerate_edges']==0 and m['degenerate_faces']==0
    checks += [{'check':'input_A','pass':input_pass(ma,[5,5,5]),'expected':{'dimensions_mm':[10,10,10],'center_mm':[5,5,5],'volume_mm3':1000},'observed':ma},{'check':'input_B','pass':input_pass(mb,[14.8,5,5]),'expected':{'dimensions_mm':[10,10,10],'center_mm':[14.8,5,5],'volume_mm3':1000},'observed':mb}]
    for link in list(group.links):
        if link.to_node==out: group.links.remove(link)
    group.links.new(boolean.outputs[geometry_out.identifier],out.inputs['Geometry'])
    union=measure(obj,'union')
    union_ok=close(union['dimensions_mm'],[19.8,10,10]) and abs(union['signed_volume_mm3']-1980)<=TOL_VOL and union['components']==1 and union['all_edges_manifold'] and union['all_manifold_edges_contiguous'] and union['signed_volume_mm3']>0 and union['degenerate_edges']==0 and union['degenerate_faces']==0
    checks.append({'check':'union_contract','pass':union_ok,'expected':{'dimensions_mm':[19.8,10,10],'volume_mm3':1980,'components':1,'closed_manifold':True,'degenerates':0},'observed':union})
    result={'run_id':RUN,'variant':variant,'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','opened_blend':blend,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'read_only_file':True,'no_save_called':True,'expected_link_order':expected,'observed_link_order':actual,'input_A':ma,'input_B':mb,'union':union,'checks':checks}
    os.makedirs(os.path.dirname(result_path),exist_ok=True)
    with open(result_path,'x',encoding='utf-8') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print('GN_MULTIORDER_VALIDATION '+json.dumps(result,sort_keys=True))
    if result['status']!='PASS': raise SystemExit(2)
main()

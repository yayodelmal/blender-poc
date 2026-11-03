"""Read-only independent validation of the two Boolean inputs and union output."""
import json,os,sys,bpy,bmesh

RUN='EXP-BPY-006-GN-DIAG-20261102T190420Z'; TOL_MM=.01; TOL_VOL=.1
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_PATH=os.path.join(ROOT,'evidencias','api_socket_inventory.json')
def components(bm):
    unseen=set(bm.verts); count=0
    while unseen:
        count+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen: unseen.remove(q); stack.append(q)
    return count
def measure(obj,label):
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dg)
    me=bpy.data.meshes.new_from_object(ev,depsgraph=dg,preserve_all_data_layers=True)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    pts=[obj.matrix_world@v.co for v in me.vertices]
    dims=[(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(3)] if pts else []
    center=[(max(p[i] for p in pts)+min(p[i] for p in pts))*500 for i in range(3)] if pts else []
    signed=bm.calc_volume(signed=True)*1e9 if bm.faces else 0.0
    result={'label':label,'dimensions_mm':dims,'center_mm':center,'signed_volume_mm3':signed,'components':components(bm) if bm.verts else 0,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'all_edges_manifold':bool(bm.edges) and all(e.is_manifold for e in bm.edges),'all_manifold_edges_contiguous':bool(bm.edges) and all(e.is_contiguous for e in bm.edges if e.is_manifold),'degenerate_edges':sum(e.calc_length()<=1e-12 for e in bm.edges),'degenerate_faces':sum(f.calc_area()<=1e-15 for f in bm.faces)}
    bm.free(); bpy.data.meshes.remove(me); return result
def close(a,b,tol=TOL_MM): return len(a)==len(b) and all(abs(x-y)<=tol for x,y in zip(a,b))
def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=2: raise RuntimeError('Expected BLEND VALIDATION_JSON after --')
    blend,out=sys.argv[sys.argv.index('--')+1:]; blend=os.path.abspath(blend); out=os.path.abspath(out)
    if os.path.exists(out): raise FileExistsError(out)
    with open(API_PATH,encoding='utf-8') as f: api=json.load(f)
    if not api.get('resolution_unambiguous'): raise RuntimeError('Recorded API output is not unambiguous; refusing geometry evaluation')
    bpy.ops.wm.open_mainfile(filepath=blend,load_ui=False)
    obj=bpy.data.objects.get('GN_DIAG_Result')
    if obj is None: raise RuntimeError('Candidate open succeeded but result object is absent')
    mod=next((m for m in obj.modifiers if m.type=='NODES' and m.node_group),None)
    if mod is None: raise RuntimeError('Candidate has no Geometry Nodes modifier')
    group=mod.node_group; boolean=next((n for n in group.nodes if n.label=='Boolean UNION under test'),None); output=next((n for n in group.nodes if n.type=='GROUP_OUTPUT'),None)
    if boolean is None or output is None: raise RuntimeError('Required Boolean or Group Output node missing')
    # Resolve the live node output by type and compare against the pre-build inventory before any evaluation.
    candidates=[s for s in boolean.outputs if s.type=='GEOMETRY' and s.enabled]
    resolved=candidates[0] if len(candidates)==1 else None
    if resolved is None: raise RuntimeError('Live Boolean geometry output is ambiguous or absent; refusing evaluation')
    if (resolved.name,resolved.identifier)!=(api['resolved_geometry_output']['name'],api['resolved_geometry_output']['identifier']): raise RuntimeError('Live Boolean geometry output differs from inspected API; refusing evaluation')
    # Verify saved input wiring and order before modifying only the in-memory graph for branch inspection.
    a=next(n for n in group.nodes if n.label=='Position A'); b=next(n for n in group.nodes if n.label=='Position B offset 9.8mm')
    s1=boolean.inputs[0].links[0].from_node.label if len(boolean.inputs[0].links)==1 else None
    s2=boolean.inputs[1].links[0].from_node.label if len(boolean.inputs[1].links)==1 else None
    variant=obj.get('variant'); expected=('Position A','Position B offset 9.8mm') if variant=='A_FIRST' else ('Position B offset 9.8mm','Position A')
    checks=[{'check':'geometry_output_resolved_before_evaluation','pass':True,'observed':{'name':resolved.name,'identifier':resolved.identifier,'type':resolved.type},'api_inventory':api['resolved_geometry_output']},{'check':'saved_input_order','pass':(s1,s2)==expected,'expected':expected,'observed':(s1,s2)}]
    def expose(source):
        for link in list(group.links):
            if link.to_node==output: group.links.remove(link)
        group.links.new(source.outputs['Geometry'],output.inputs['Geometry'])
    input_a=expose(a); ma=measure(obj,'input_A')
    input_b=expose(b); mb=measure(obj,'input_B')
    def input_ok(m,c): return close(m['dimensions_mm'],[10,10,10]) and close(m['center_mm'],c) and abs(m['signed_volume_mm3']-1000)<=TOL_VOL and m['components']==1 and m['all_edges_manifold'] and m['degenerate_edges']==0 and m['degenerate_faces']==0
    checks += [{'check':'input_A_individual','pass':input_ok(ma,[5,5,5]),'expected':{'dimensions_mm':[10,10,10],'center_mm':[5,5,5],'volume_mm3':1000,'components':1,'manifold':True},'observed':ma},{'check':'input_B_individual','pass':input_ok(mb,[14.8,5,5]),'expected':{'dimensions_mm':[10,10,10],'center_mm':[14.8,5,5],'volume_mm3':1000,'components':1,'manifold':True},'observed':mb}]
    # Restore precisely the saved Boolean output route in memory, then evaluate. Do not save the opened file.
    for link in list(group.links):
        if link.to_node==output: group.links.remove(link)
    group.links.new(boolean.outputs[resolved.identifier],output.inputs['Geometry'])
    union=measure(obj,'union')
    union_ok=close(union['dimensions_mm'],[19.8,10,10]) and abs(union['signed_volume_mm3']-1980)<=TOL_VOL and union['components']==1 and union['all_edges_manifold'] and union['all_manifold_edges_contiguous'] and union['signed_volume_mm3']>0 and union['degenerate_edges']==0 and union['degenerate_faces']==0
    checks.append({'check':'union_contract','pass':union_ok,'expected':{'dimensions_mm':[19.8,10,10],'volume_mm3':1980,'components':1,'closed_manifold':True,'degenerates':0},'observed':union})
    result={'run_id':RUN,'variant':variant,'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','opened_blend':blend,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'read_only_blend':True,'no_save_called':True,'input_A':ma,'input_B':mb,'union':union,'checks':checks}
    os.makedirs(os.path.dirname(out),exist_ok=True)
    with open(out,'x',encoding='utf-8') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print('GN_DIAG_VALIDATION '+json.dumps(result,sort_keys=True))
    if result['status']!='PASS': raise SystemExit(2)
main()

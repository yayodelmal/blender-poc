"""Independently inspect both individual GN inputs and the persisted union result."""
import json,sys,bpy,bmesh

TOL_MM=.01; VOL_TOL=.1
def components(bm):
    unseen=set(bm.verts); count=0
    while unseen:
        count+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                u=e.other_vert(v)
                if u in unseen: unseen.remove(u); stack.append(u)
    return count
def evaluate(obj,label):
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(dg)
    me=bpy.data.meshes.new_from_object(ev,depsgraph=dg,preserve_all_data_layers=True)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    pts=[obj.matrix_world@v.co for v in me.vertices]
    dims=[(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(3)] if pts else []
    mins=[min(p[i] for p in pts)*1000 for i in range(3)] if pts else []
    centers=[(min(p[i] for p in pts)+max(p[i] for p in pts))*500 for i in range(3)] if pts else []
    volume=bm.calc_volume(signed=True)*1e9
    comp=components(bm) if bm.verts else 0
    manifold=bool(bm.edges) and all(e.is_manifold for e in bm.edges)
    contiguous=bool(bm.edges) and all(e.is_contiguous for e in bm.edges if e.is_manifold)
    result={'label':label,'dimensions_mm':dims,'min_mm':mins,'center_mm':centers,'volume_mm3':volume,'components':comp,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'all_edges_manifold':manifold,'consistent_orientation':contiguous,'signed_volume_positive':volume>0}
    bm.free(); bpy.data.meshes.remove(me)
    return result
def near(actual,expected,tol=TOL_MM): return len(actual)==len(expected) and all(abs(a-b)<=tol for a,b in zip(actual,expected))
def main():
    if '--' not in sys.argv: raise RuntimeError('Expected .blend path after --')
    path=sys.argv[sys.argv.index('--')+1]; bpy.ops.wm.open_mainfile(filepath=path,load_ui=False)
    obj=bpy.data.objects.get('GN_DIAG_Result'); checks=[]
    if not obj: raise RuntimeError('Result object missing')
    mod=next((m for m in obj.modifiers if m.type=='NODES' and m.node_group),None)
    if not mod: raise RuntimeError('Geometry Nodes modifier missing')
    group=mod.node_group; variant=obj.get('variant'); boolean=next(n for n in group.nodes if n.label=='Union under test'); out=next(n for n in group.nodes if n.type=='GROUP_OUTPUT')
    transform_a=next(n for n in group.nodes if n.label=='Position A'); transform_b=next(n for n in group.nodes if n.label=='Position B with 0.2mm overlap')
    # Confirm the input order actually persisted in this .blend.
    source1=boolean.inputs[0].links[0].from_node.label if boolean.inputs[0].is_linked else None
    source2=boolean.inputs[1].links[0].from_node.label if boolean.inputs[1].is_linked else None
    expected_order=('Position A','Position B with 0.2mm overlap') if variant=='A_FIRST' else ('Position B with 0.2mm overlap','Position A')
    order_ok=(source1,source2)==expected_order
    checks.append({'check':'persisted_boolean_input_order','pass':order_ok,'expected':expected_order,'observed':(source1,source2)})
    # Temporarily redirect only the in-memory graph output to inspect each input.
    def expose(source):
        for link in list(group.links):
            if link.to_node==out: group.links.remove(link)
        group.links.new(source.outputs['Geometry'],out.inputs['Geometry'])
    inputs={}
    for key,node in [('A',transform_a),('B',transform_b)]:
        expose(node); inputs[key]=evaluate(obj,'input_'+key)
    checks.append({'check':'input_A_individually_expected','pass':near(inputs['A']['dimensions_mm'],[10,10,10]) and near(inputs['A']['center_mm'],[5,5,5]) and abs(inputs['A']['volume_mm3']-1000)<=VOL_TOL and inputs['A']['components']==1 and inputs['A']['all_edges_manifold'],'observed':inputs['A']})
    checks.append({'check':'input_B_individually_expected','pass':near(inputs['B']['dimensions_mm'],[10,10,10]) and near(inputs['B']['center_mm'],[14.8,5,5]) and abs(inputs['B']['volume_mm3']-1000)<=VOL_TOL and inputs['B']['components']==1 and inputs['B']['all_edges_manifold'],'observed':inputs['B']})
    # Restore the saved union wiring in memory and evaluate without saving the file.
    expose(boolean); final=evaluate(obj,'union')
    union_ok=near(final['dimensions_mm'],[19.8,10,10]) and abs(final['volume_mm3']-1980)<=VOL_TOL and final['components']==1 and final['all_edges_manifold'] and final['consistent_orientation'] and final['signed_volume_positive']
    checks.append({'check':'union_dimensions_volume_connected_closed_manifold','pass':union_ok,'expected':{'dimensions_mm':[19.8,10,10],'volume_mm3':1980,'components':1,'all_edges_manifold':True},'observed':final,'volume_tolerance_mm3':VOL_TOL})
    result={'run_id':obj.get('diagnostic_run_id'),'variant':variant,'opened_file':bpy.data.filepath,'blender_version':bpy.app.version_string,'python_version':__import__('sys').version.split()[0],'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks,'read_only_file':True,'graph_rewired_in_memory_for_input_checks':True,'saved_file_not_modified':True}
    print('GN_DIAG_VALIDATION '+json.dumps(result,sort_keys=True))
    if result['status']!='PASS': raise SystemExit(2)
main()

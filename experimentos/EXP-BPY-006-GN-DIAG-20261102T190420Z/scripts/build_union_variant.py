"""Build one minimal GeometryNodeMeshBoolean UNION order variant."""
import json,os,sys,bpy

RUN='EXP-BPY-006-GN-DIAG-20261102T190420Z'
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_PATH=os.path.join(ROOT,'evidencias','api_socket_inventory.json')
def main():
    if '--' not in sys.argv: raise RuntimeError('Expected VARIANT OUTPUT after --')
    args=sys.argv[sys.argv.index('--')+1:]
    if len(args)!=2 or args[0] not in ('A_FIRST','B_FIRST'): raise RuntimeError('Expected A_FIRST|B_FIRST OUTPUT')
    variant,out=args; out=os.path.abspath(out)
    if os.path.exists(out): raise FileExistsError(out)
    with open(API_PATH,encoding='utf-8') as f: api=json.load(f)
    if not api.get('resolution_unambiguous') or api.get('resolved_geometry_output',{}).get('type')!='GEOMETRY': raise RuntimeError('Prior API inventory does not prove one geometry output')
    scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1.0; scene.unit_settings.length_unit='MILLIMETERS'
    mesh=bpy.data.meshes.new('GN_DIAG_EmptyCarrier'); obj=bpy.data.objects.new('GN_DIAG_Result',mesh); scene.collection.objects.link(obj)
    obj['diagnostic_run_id']=RUN; obj['variant']=variant; obj['overlap_mm']=0.2
    group=bpy.data.node_groups.new('GN_DIAG_Union_'+variant,'GeometryNodeTree')
    group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    def node(kind,label):
        n=group.nodes.new(kind); n.label=label; return n
    # A bounds X=[0,10]mm; B bounds X=[9.8,19.8]mm. Both span Y,Z=[0,10]mm.
    cube_a=node('GeometryNodeMeshCube','Input A 10mm cube'); cube_a.inputs['Size'].default_value=(.01,.01,.01)
    pos_a=node('GeometryNodeTransform','Position A'); pos_a.inputs['Translation'].default_value=(.005,.005,.005); group.links.new(cube_a.outputs['Mesh'],pos_a.inputs['Geometry'])
    cube_b=node('GeometryNodeMeshCube','Input B 10mm cube'); cube_b.inputs['Size'].default_value=(.01,.01,.01)
    pos_b=node('GeometryNodeTransform','Position B offset 9.8mm'); pos_b.inputs['Translation'].default_value=(.0148,.005,.005); group.links.new(cube_b.outputs['Mesh'],pos_b.inputs['Geometry'])
    boolean=node('GeometryNodeMeshBoolean','Boolean UNION under test'); boolean.operation='UNION'
    resolved=[s for s in boolean.outputs if s.type=='GEOMETRY' and s.enabled]
    if len(resolved)!=1 or resolved[0].identifier!=api['resolved_geometry_output']['identifier'] or resolved[0].name!=api['resolved_geometry_output']['name']:
        raise RuntimeError('Geometry output changed or is ambiguous relative to recorded API inventory')
    first,second=(pos_a,pos_b) if variant=='A_FIRST' else (pos_b,pos_a)
    group.links.new(first.outputs['Geometry'],boolean.inputs[0]); group.links.new(second.outputs['Geometry'],boolean.inputs[1])
    output=node('NodeGroupOutput','Boolean geometry result'); group.links.new(boolean.outputs[resolved[0].identifier],output.inputs['Geometry'])
    modifier=obj.modifiers.new('GN_DIAG_Union','NODES'); modifier.node_group=group
    obj.select_set(True); bpy.context.view_layer.objects.active=obj
    os.makedirs(os.path.dirname(out),exist_ok=True)
    result=bpy.ops.wm.save_as_mainfile(filepath=out,check_existing=False)
    if 'FINISHED' not in result: raise RuntimeError('Saving candidate failed')
    rec={'run_id':RUN,'variant':variant,'artifact':out,'blender_version':bpy.app.version_string,'operation':'UNION','resolved_output':{'name':resolved[0].name,'identifier':resolved[0].identifier,'type':resolved[0].type},'inputs':{'Mesh 1':first.label,'Mesh':second.label},'input_A':{'dimensions_mm':[10,10,10],'center_mm':[5,5,5],'volume_mm3':1000},'input_B':{'dimensions_mm':[10,10,10],'center_mm':[14.8,5,5],'volume_mm3':1000},'overlap_x_mm':.2,'expected_union':{'dimensions_mm':[19.8,10,10],'volume_mm3':1980,'components':1,'manifold':True}}
    print('GN_DIAG_BUILD '+json.dumps(rec,sort_keys=True))
main()

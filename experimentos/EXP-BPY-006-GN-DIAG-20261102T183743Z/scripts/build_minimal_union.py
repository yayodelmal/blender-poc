"""Build one of two minimal, reversed Geometry Nodes union inputs."""
import json,os,sys,bpy

RUN='EXP-BPY-006-GN-DIAG-20261102T183743Z'
def main():
    if '--' not in sys.argv: raise RuntimeError('Expected VARIANT OUTPUT after --')
    args=sys.argv[sys.argv.index('--')+1:]
    if len(args)!=2 or args[0] not in ('A_FIRST','B_FIRST'): raise RuntimeError('Expected A_FIRST|B_FIRST and output path')
    variant,out=args; out=os.path.abspath(out)
    if os.path.exists(out): raise FileExistsError(out)
    scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1.0; scene.unit_settings.length_unit='MILLIMETERS'
    # Input A bounds x=[0,10] mm. Input B bounds x=[9.8,19.8] mm.
    # They overlap by exactly 0.2 mm; expected union is 19.8x10x10 mm, 1980 mm^3.
    mesh=bpy.data.meshes.new('GN_DIAG_EmptyCarrier'); obj=bpy.data.objects.new('GN_DIAG_Result',mesh); scene.collection.objects.link(obj)
    obj['diagnostic_run_id']=RUN; obj['variant']=variant; obj['overlap_mm']=0.2
    group=bpy.data.node_groups.new('GN_DIAG_Union_'+variant,'GeometryNodeTree')
    group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    def node(typ,label):
        n=group.nodes.new(typ); n.label=label; return n
    a=node('GeometryNodeMeshCube','Input A: 10mm cube'); a.inputs['Size'].default_value=(.01,.01,.01)
    ta=node('GeometryNodeTransform','Position A'); ta.inputs['Translation'].default_value=(.005,.005,.005); group.links.new(a.outputs['Mesh'],ta.inputs['Geometry'])
    b=node('GeometryNodeMeshCube','Input B: 10mm cube'); b.inputs['Size'].default_value=(.01,.01,.01)
    tb=node('GeometryNodeTransform','Position B with 0.2mm overlap'); tb.inputs['Translation'].default_value=(.0148,.005,.005); group.links.new(b.outputs['Mesh'],tb.inputs['Geometry'])
    boolean=node('GeometryNodeMeshBoolean','Union under test'); boolean.operation='UNION'
    first,second=(ta,tb) if variant=='A_FIRST' else (tb,ta)
    group.links.new(first.outputs['Geometry'],boolean.inputs[0]); group.links.new(second.outputs['Geometry'],boolean.inputs[1])
    output=node('NodeGroupOutput','Result'); group.links.new(boolean.outputs['Mesh'],output.inputs['Geometry'])
    modifier=obj.modifiers.new('GN_DIAG_MinimalUnion','NODES'); modifier.node_group=group
    obj.select_set(True); bpy.context.view_layer.objects.active=obj
    os.makedirs(os.path.dirname(out),exist_ok=True)
    result=bpy.ops.wm.save_as_mainfile(filepath=out,check_existing=False)
    if 'FINISHED' not in result: raise RuntimeError('Unable to save diagnostic blend')
    print('GN_DIAG_BUILD '+json.dumps({'run_id':RUN,'variant':variant,'artifact':out,'input_a':{'dimensions_mm':[10,10,10],'center_mm':[5,5,5]},'input_b':{'dimensions_mm':[10,10,10],'center_mm':[14.8,5,5]},'overlap_mm':.2,'expected_union_dimensions_mm':[19.8,10,10],'expected_union_volume_mm3':1980,'boolean_mesh1':first.label,'boolean_mesh2':second.label},sort_keys=True))

main()

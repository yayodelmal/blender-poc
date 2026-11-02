"""Independent, read-only validation of an EXP-BPY-006 .blend candidate."""
import json, math, sys
import bpy, bmesh

TOL=.01; EXPECT={'x':80.0,'y':60.0,'z':5.0}; OBJ='EXP-BPY-006_ReliefPlate'
P={'width_mm':80.0,'height_mm':60.0,'base_mm':4.0,'relief_mm':1.0,'brick_x_mm':15.0,'brick_y_mm':7.0,'joint_mm':1.2,'pitch_x_mm':16.2,'pitch_y_mm':8.2,'rows':6,'columns_even':5,'columns_odd':4}

def comps(bm):
    unseen=set(bm.verts); n=0
    while unseen:
        n+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                q=e.other_vert(v)
                if q in unseen: unseen.remove(q); stack.append(q)
    return n

def islands(faces):
    unseen=set(faces); result=[]
    while unseen:
        seed=unseen.pop(); stack=[seed]; group=[seed]
        while stack:
            f=stack.pop()
            for e in f.edges:
                for q in e.link_faces:
                    if q in unseen: unseen.remove(q); stack.append(q); group.append(q)
        result.append(group)
    return result

def main():
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:])!=1: raise RuntimeError('expected .blend path after --')
    path=sys.argv[sys.argv.index('--')+1:][0]
    bpy.ops.wm.open_mainfile(filepath=path, load_ui=False)
    s=bpy.context.scene; obj=bpy.data.objects.get(OBJ); checks=[]
    checks.append({'check':'expected_object','pass':obj is not None})
    meshes=[o for o in s.objects if o.type=='MESH' and o.get('role')!='boolean_operand']
    checks.append({'check':'single_primary_mesh_object','pass':len(meshes)==1,'observed':len(meshes)})
    if obj is None: raise RuntimeError('expected object missing')
    if obj.scale.length==0: raise RuntimeError('zero object scale')
    deps=bpy.context.evaluated_depsgraph_get(); ev=obj.evaluated_get(deps); me=bpy.data.meshes.new_from_object(ev,depsgraph=deps,preserve_all_data_layers=True)
    bm=bmesh.new(); bm.from_mesh(me); bm.normal_update()
    co=[obj.matrix_world@v.co for v in me.vertices]; lo=[min(v[i] for v in co)*1000 for i in range(3)]; hi=[max(v[i] for v in co)*1000 for i in range(3)]; dims=[hi[i]-lo[i] for i in range(3)]
    dev=[dims[i]-EXPECT['xyz'[i]] for i in range(3)]
    checks.append({'check':'evaluated_envelope_mm','pass':all(abs(x)<=TOL for x in dev),'expected':[80,60,5],'observed':dims,'deviation':dev,'tolerance':TOL})
    unit=s.unit_settings
    checks.append({'check':'units_and_scale','pass':unit.system=='METRIC' and abs(unit.scale_length-1)<1e-12 and unit.length_unit=='MILLIMETERS' and all(abs(x-1)<1e-9 for x in obj.scale),'observed':{'system':unit.system,'scale_length':unit.scale_length,'length_unit':unit.length_unit,'object_scale':list(obj.scale)}})
    checks.append({'check':'base_plane_and_thickness','pass':abs(lo[2])<=TOL and any(abs(v.co.z*1000-4.0)<=TOL for v in bm.verts) and abs((hi[2]-4.0)-1.0)<=TOL,'observed':{'min_z_mm':lo[2],'max_z_mm':hi[2],'base_top_vertex_present':any(abs(v.co.z*1000-4)<=TOL for v in bm.verts)}})
    count=comps(bm); manifold=bool(bm.edges) and all(e.is_manifold for e in bm.edges); contiguous=all(e.is_contiguous for e in bm.edges if e.is_manifold); vol=bm.calc_volume(signed=True)*1e9
    degen={'edges':sum(e.calc_length()<=1e-12 for e in bm.edges),'faces':sum(f.calc_area()<=1e-15 for f in bm.faces)}
    checks += [{'check':'connected_closed_solid','pass':count==1 and manifold,'components':count,'all_edges_manifold':manifold}, {'check':'orientation_and_volume','pass':contiguous and vol>0,'contiguous':contiguous,'signed_volume_mm3':vol}, {'check':'no_degenerate_elements','pass':degen['edges']==0 and degen['faces']==0,'observed':degen}]
    top=[f for f in bm.faces if all(abs((obj.matrix_world@v.co).z*1000-hi[2])<=TOL/10 for v in f.verts)]
    regs=islands(top); regions=[]
    for reg in regs:
        pts=[obj.matrix_world@v.co for f in reg for v in f.verts]
        xyz=list(zip(*[(p.x*1000,p.y*1000,p.z*1000) for p in pts]))
        regions.append({'dx_mm':max(xyz[0])-min(xyz[0]),'dy_mm':max(xyz[1])-min(xyz[1]),'area_mm2':sum(f.calc_area() for f in reg)*1e6})
    pattern_ok=len(regions)==27 and all(abs(r['dx_mm']-15)<=TOL and abs(r['dy_mm']-7)<=TOL for r in regions)
    checks.append({'check':'physical_brick_relief','pass':pattern_ok,'expected_bricks':27,'observed_top_islands':len(regions),'regions':regions,'max_z_mm':hi[2]})
    params_ok=False; parameter_record={}
    if obj.get('strategy')=='A_bpy_parameterized_full_rebuild':
        parameter_record=json.loads(obj.get('parameters_mm','{}')); params_ok=parameter_record==P
    elif obj.get('strategy')=='B_geometry_nodes':
        mod=next((m for m in obj.modifiers if m.type=='NODES' and m.node_group),None)
        if mod:
            group=mod.node_group
            required=['Relieve (m)','Ladrillo X (m)','Ladrillo Y (m)','Paso X (m)','Paso Y (m)']
            interfaces=[i for i in group.interface.items_tree if getattr(i,'in_out',None)=='INPUT' and i.name!='Geometry']
            parameter_record={i.name:i.default_value for i in interfaces}
            group_input=next((n for n in group.nodes if n.type=='GROUP_INPUT'),None)
            params_ok=all(any(i.name==n for i in interfaces) for n in required) and group_input is not None and all(group_input.outputs.get(n) is not None and group_input.outputs[n].is_linked for n in required) and len(group.nodes)>0 and any(m.type=='BOOLEAN' and m.object is not None and m.object.get('role')=='boolean_operand' for m in obj.modifiers)
            parameter_record['construction_base_mm']=json.loads(obj.get('construction_base_dimensions_mm','{}'))
    checks.append({'check':'persistent_editable_parameters','pass':params_ok,'strategy':obj.get('strategy'),'observed':parameter_record,'modifier_count':len(obj.modifiers)})
    if obj.get('strategy')=='A_bpy_parameterized_full_rebuild': checks.append({'check':'strategy_identity','pass':obj.name==OBJ and obj.get('experiment_id')=='EXP-BPY-006-20261102T175526Z','interpretation':'parameters plus rebuild script; full regeneration, not in-place'})
    checks.append({'check':'read_only_validation_process','pass':True,'opened_file':bpy.data.filepath})
    res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','opened_file':bpy.data.filepath,'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'object':obj.name,'strategy':obj.get('strategy'),'dimensions_mm':dims,'center_mm':[(lo[i]+hi[i])/2 for i in range(3)],'components':count,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'volume_mm3':vol,'findings':checks}
    print('EXP_BPY_006_VALIDATION '+json.dumps(res,sort_keys=True))
    bm.free(); bpy.data.meshes.remove(me)
    if res['status']!='PASS': raise RuntimeError('candidate validation failed')

main()

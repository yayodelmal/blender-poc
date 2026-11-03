import bpy, bmesh, hashlib, json, sys
from pathlib import Path
args=sys.argv[sys.argv.index("--")+1:]
if len(args)!=3: raise RuntimeError("expected source blend, candidate blend, output json")
src,candidate,out=map(lambda x:str(Path(x).resolve()),args)
def signature(obj):
    data={"vertices":[tuple(round(float(c),9) for c in v.co) for v in obj.data.vertices],"polygons":[tuple(int(i) for i in p.vertices) for p in obj.data.polygons]}
    return hashlib.sha256(json.dumps(data,separators=(",",":"),sort_keys=True).encode()).hexdigest()
def components(bm):
    unseen=set(bm.verts); n=0
    while unseen:
        n+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in unseen: unseen.remove(other); stack.append(other)
    return n
bpy.ops.wm.open_mainfile(filepath=src,load_ui=False); source=bpy.data.objects.get("CU01_Planter_REV002")
if source is None: raise RuntimeError("source object missing")
sig_src=signature(source)
bpy.ops.wm.open_mainfile(filepath=candidate,load_ui=False); obj=bpy.data.objects.get("CU01_Planter_REV002")
if obj is None: raise RuntimeError("candidate object missing")
sig_out=signature(obj); mesh=obj.data; bm=bmesh.new(); bm.from_mesh(mesh); bm.normal_update()
comps=components(bm); manifold=bool(bm.edges) and all(e.is_manifold for e in bm.edges)
coords=[obj.matrix_world@v.co for v in mesh.vertices]; dims=[(max(v[i] for v in coords)-min(v[i] for v in coords))*1000 for i in range(3)]
mat=mesh.materials[0] if len(mesh.materials)==1 else None; nodes=mat.node_tree.nodes if mat and mat.use_nodes else []
voro=next((n for n in nodes if n.type=="TEX_VORONOI"),None); ramps=[n for n in nodes if n.type=="VALTORGB"]; bsdf=next((n for n in nodes if n.type=="BSDF_PRINCIPLED"),None)
outnode=next((n for n in nodes if n.type=="OUTPUT_MATERIAL"),None)
linked=bool(voro and bsdf and outnode and any(l.from_node==voro for l in mat.node_tree.links) and any(l.from_node==bsdf and l.to_node==outnode for l in mat.node_tree.links))
checks={"same_geometry_fingerprint":sig_src==sig_out,"envelope_150x150x60_mm":all(abs(a-b)<=0.01 for a,b in zip(dims,[150,150,60])),"single_closed_manifold":comps==1 and manifold,"one_procedural_marble_material":mat is not None and voro is not None and len(ramps)>=2 and linked,"white_base_and_rough_finish":bool(bsdf) and all(abs(float(c)-1.0)<1e-6 for c in bsdf.inputs["Base Color"].default_value) and abs(float(bsdf.inputs["Roughness"].default_value)-0.8)<1e-6,"finish_marker":obj.get("finish_variant")=="white_black_gray_pla_marbled"}
result={"run_id":"CU-01-COLOR-PLA-MARBLE-20261103T024738Z","status":"PASS" if all(checks.values()) else "FAIL","opened_file":bpy.data.filepath,"source":src,"dimensions_mm":dims,"components":comps,"manifold":manifold,"geometry_sha256_source":sig_src,"geometry_sha256_candidate":sig_out,"material":{"name":mat.name if mat else None,"voronoi_scale":float(voro.inputs["Scale"].default_value) if voro else None,"black_gray_palette":bool(ramps),"roughness":float(bsdf.inputs["Roughness"].default_value) if bsdf else None},"checks":checks}
Path(out).parent.mkdir(parents=True,exist_ok=True); Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print("MARBLE_VALIDATION "+json.dumps(result,sort_keys=True)); bm.free()
if result["status"]!="PASS": raise SystemExit(2)

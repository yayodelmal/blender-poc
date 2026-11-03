import bpy, bmesh, hashlib, json, sys
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index("--")+1:]
if len(args)!=3: raise RuntimeError("expected source blend, candidate blend, output json")
src,candidate,out=map(lambda x:str(Path(x).resolve()),args)
def count_components(bm):
    unseen=set(bm.verts); count=0
    while unseen:
        count+=1; stack=[unseen.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in unseen: unseen.remove(other); stack.append(other)
    return count
def fingerprint(obj):
    m=obj.data
    payload={"vertices":[tuple(round(float(c),9) for c in v.co) for v in m.vertices],"polygons":[tuple(int(i) for i in p.vertices) for p in m.polygons]}
    return hashlib.sha256(json.dumps(payload,separators=(",",":"),sort_keys=True).encode()).hexdigest(),payload
bpy.ops.wm.open_mainfile(filepath=src,load_ui=False)
src_obj=bpy.data.objects.get("CU01_Planter_REV002")
if src_obj is None: raise RuntimeError("source REV-002 object missing")
sig_source,topology_source=fingerprint(src_obj)
bpy.ops.wm.open_mainfile(filepath=candidate,load_ui=False)
obj=bpy.data.objects.get("CU01_Planter_REV002")
if obj is None: raise RuntimeError("white candidate object missing")
sig_candidate,topology_candidate=fingerprint(obj)
mesh=obj.data; bm=bmesh.new(); bm.from_mesh(mesh); bm.normal_update()
coords=[obj.matrix_world@v.co for v in mesh.vertices]
dims=[(max(v[i] for v in coords)-min(v[i] for v in coords))*1000 for i in range(3)]
manifold=bool(bm.edges) and all(e.is_manifold for e in bm.edges)
components=count_components(bm)
materials=[m for m in mesh.materials if m is not None]
mat=materials[0] if len(materials)==1 else None
bsdf=next((n for n in mat.node_tree.nodes if n.type=="BSDF_PRINCIPLED"),None) if mat and mat.use_nodes else None
color=list(bsdf.inputs["Base Color"].default_value) if bsdf else None
white=bool(color) and all(abs(color[i]-1.0)<1e-9 for i in range(4)) and abs(bsdf.inputs["Roughness"].default_value-0.8)<1e-6
checks={"same_geometry_fingerprint":sig_source==sig_candidate,"envelope_150x150x60_mm":all(abs(a-b)<=0.01 for a,b in zip(dims,[150,150,60])),"single_closed_manifold":manifold and components==1,"one_white_matte_material":white,"finish_marker":obj.get("finish_variant")=="white_matte"}
result={"run_id":"CU-01-COLOR-WHITE-20261103T024347Z","status":"PASS" if all(checks.values()) else "FAIL","opened_file":bpy.data.filepath,"source":src,"dimensions_mm":dims,"geometry_sha256_source":sig_source,"geometry_sha256_candidate":sig_candidate,"components":components,"material":{"name":mat.name if mat else None,"base_color":color,"roughness":bsdf.inputs["Roughness"].default_value if bsdf else None},"checks":checks}
Path(out).parent.mkdir(parents=True,exist_ok=True); Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print("WHITE_VALIDATION "+json.dumps(result,sort_keys=True)); bm.free()
if result["status"]!="PASS": raise SystemExit(2)

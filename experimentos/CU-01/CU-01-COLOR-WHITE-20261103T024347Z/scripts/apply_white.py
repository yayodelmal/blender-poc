import bpy, json, sys
from pathlib import Path
args=sys.argv[sys.argv.index("--")+1:]
if len(args)!=2: raise RuntimeError("expected source and destination blend paths")
src,dst=map(lambda x:str(Path(x).resolve()),args)
bpy.ops.wm.open_mainfile(filepath=src,load_ui=True)
obj=bpy.data.objects.get("CU01_Planter_REV002")
if obj is None or obj.type!="MESH": raise RuntimeError("REV-002 mesh not found")
mat=bpy.data.materials.get("CU01_White_Matte") or bpy.data.materials.new("CU01_White_Matte")
mat.diffuse_color=(1.0,1.0,1.0,1.0); mat.use_nodes=True
bsdf=next((n for n in mat.node_tree.nodes if n.type=="BSDF_PRINCIPLED"),None)
if bsdf is None: raise RuntimeError("Principled BSDF not found")
bsdf.inputs["Base Color"].default_value=(1.0,1.0,1.0,1.0); bsdf.inputs["Roughness"].default_value=0.8; bsdf.inputs["Metallic"].default_value=0.0
obj.data.materials.clear(); obj.data.materials.append(mat)
obj["finish_variant"]="white_matte"; obj["finish_note"]="Appearance-only variant of CU-01 REV-002; geometry unchanged."
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=="VIEW_3D":
            area.spaces.active.shading.color_type="MATERIAL"
            area.spaces.active.shading.type="MATERIAL"
Path(dst).parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=dst,check_existing=False)
print("WHITE_VARIANT "+json.dumps({"source":src,"output":dst,"object":obj.name,"material":mat.name,"base_color":[1,1,1,1],"roughness":0.8}))

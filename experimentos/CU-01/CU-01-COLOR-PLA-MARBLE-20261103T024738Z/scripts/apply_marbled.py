import bpy, json, sys
from pathlib import Path
args=sys.argv[sys.argv.index("--")+1:]
if len(args)!=2: raise RuntimeError("expected source and destination blend paths")
src,dst=map(lambda x:str(Path(x).resolve()),args)
bpy.ops.wm.open_mainfile(filepath=src,load_ui=True)
obj=bpy.data.objects.get("CU01_Planter_REV002")
if obj is None or obj.type!="MESH": raise RuntimeError("REV-002 mesh not found")
mat=bpy.data.materials.new("CU01_PLA_Marble_White_Black_Gray")
mat.diffuse_color=(0.93,0.93,0.93,1.0); mat.use_nodes=True
nodes=mat.node_tree.nodes; links=mat.node_tree.links; nodes.clear()
out=nodes.new("ShaderNodeOutputMaterial"); out.location=(700,80)
bsdf=nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location=(450,80)
bsdf.inputs["Base Color"].default_value=(1.0,1.0,1.0,1.0)
bsdf.inputs["Roughness"].default_value=0.8
bsdf.inputs["Metallic"].default_value=0.0
links.new(bsdf.outputs["BSDF"],out.inputs["Surface"])
tex=nodes.new("ShaderNodeTexCoord"); tex.location=(-900,100)
voro=nodes.new("ShaderNodeTexVoronoi"); voro.location=(-650,100); voro.feature="F1"; voro.distance="EUCLIDEAN"
voro.inputs["Scale"].default_value=1000.0; voro.inputs["Randomness"].default_value=1.0
links.new(tex.outputs["Object"],voro.inputs["Vector"])
rgbbw=nodes.new("ShaderNodeRGBToBW"); rgbbw.location=(-430,-220); links.new(voro.outputs["Color"],rgbbw.inputs["Color"])
palette=nodes.new("ShaderNodeValToRGB"); palette.location=(-180,-220)
palette.color_ramp.elements.remove(palette.color_ramp.elements[1])
e=palette.color_ramp.elements[0]; e.position=0.0; e.color=(0.005,0.005,0.005,1.0)
for pos,col in ((0.30,(0.025,0.025,0.025,1.0)),(0.55,(0.12,0.12,0.12,1.0)),(0.80,(0.32,0.32,0.32,1.0)),(1.0,(0.48,0.48,0.48,1.0))):
    el=palette.color_ramp.elements.new(pos); el.color=col
links.new(rgbbw.outputs["Val"],palette.inputs["Fac"])
mask=nodes.new("ShaderNodeValToRGB"); mask.location=(-180,160)
mask.color_ramp.interpolation="EASE"
mask.color_ramp.elements[0].position=0.0; mask.color_ramp.elements[0].color=(1,1,1,1)
mask.color_ramp.elements[1].position=0.27; mask.color_ramp.elements[1].color=(0,0,0,1)
el=mask.color_ramp.elements.new(0.20); el.color=(1,1,1,1)
links.new(voro.outputs["Distance"],mask.inputs["Fac"])
mix=nodes.new("ShaderNodeMixRGB"); mix.location=(180,120); mix.blend_type="MIX"; mix.inputs["Color1"].default_value=(1,1,1,1)
links.new(mask.outputs["Color"],mix.inputs["Fac"]); links.new(palette.outputs["Color"],mix.inputs["Color2"]); links.new(mix.outputs["Color"],bsdf.inputs["Base Color"])
obj.data.materials.clear(); obj.data.materials.append(mat)
obj["finish_variant"]="white_black_gray_pla_marbled"; obj["finish_note"]="Procedural subtle black and gray flecks; appearance-only, geometry inherited from REV-002."
obj["speckle_scale_per_meter"]=1000.0; obj["speckle_radius_threshold"]=0.20; obj["speckle_outer_threshold"]=0.27
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=="VIEW_3D":
            area.spaces.active.shading.color_type="MATERIAL"; area.spaces.active.shading.type="MATERIAL"
Path(dst).parent.mkdir(parents=True,exist_ok=True); bpy.ops.wm.save_as_mainfile(filepath=dst,check_existing=False)
print("MARBLE_VARIANT "+json.dumps({"source":src,"output":dst,"material":mat.name,"base":"white","flecks":["black","gray"],"roughness":0.8,"voronoi_scale":1000.0,"distance_threshold":[0.20,0.27]}))

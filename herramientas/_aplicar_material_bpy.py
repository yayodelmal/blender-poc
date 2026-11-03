"""Parte bpy de aplicar_material.py. Se ejecuta dentro de Blender, no directamente."""
import bpy, hashlib, json, sys
from pathlib import Path

src, dst, color_json, rugosidad, objeto, nombre_mat = sys.argv[sys.argv.index("--") + 1:]
color, rugosidad = json.loads(color_json), float(rugosidad)


def huella(objs):
    payload = [(o.name, [tuple(round(float(c), 9) for c in v.co) for v in o.data.vertices],
                [tuple(int(i) for i in p.vertices) for p in o.data.polygons]) for o in objs]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


bpy.ops.wm.open_mainfile(filepath=src, load_ui=True)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if objeto:
    meshes = [o for o in meshes if o.name == objeto]
if len(meshes) != 1:
    raise RuntimeError(f"se esperaba 1 objeto mesh y hay {len(meshes)}: {[o.name for o in meshes]}; usar --objeto")
obj = meshes[0]
nombre_obj = obj.name
antes = huella([obj])

mat = bpy.data.materials.get(nombre_mat) or bpy.data.materials.new(nombre_mat)
mat.diffuse_color = color
mat.use_nodes = True
bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
if bsdf is None:
    raise RuntimeError("Principled BSDF no encontrado")
bsdf.inputs["Base Color"].default_value = color
bsdf.inputs["Roughness"].default_value = rugosidad
bsdf.inputs["Metallic"].default_value = 0.0
obj.data.materials.clear()
obj.data.materials.append(mat)
obj["finish_variant"] = nombre_mat
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.shading.type = "MATERIAL"

despues = huella([obj])
if antes != despues:
    raise RuntimeError("la geometría cambió al aplicar el material")
Path(dst).parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=dst, check_existing=False)

# Reabrir lo guardado y comprobar material y geometría (mismo proceso, sin segunda pasada).
bpy.ops.wm.open_mainfile(filepath=dst, load_ui=False)
chk = bpy.data.objects[nombre_obj]
m = chk.data.materials[0] if len(chk.data.materials) == 1 else None
b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m else None
ok = (huella([chk]) == antes and b is not None
      and all(abs(b.inputs["Base Color"].default_value[i] - color[i]) < 1e-5 for i in range(4))
      and abs(b.inputs["Roughness"].default_value - rugosidad) < 1e-5)
if not ok:
    raise RuntimeError("la verificación del archivo guardado falló")
print("VARIANTE " + json.dumps({"geometria_sha256": antes, "objetos": [nombre_obj]}))

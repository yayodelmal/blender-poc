"""Material procedural Hyper PLA Marmol para modelos Blender del proyecto.

El patrón replica el material ajustado en Blender: fondo blanco, motas oscuras
negras/grises con Voronoi en coordenadas Object y acabado visual del Principled
BSDF. La función solo modifica materiales del objeto; no cambia su geometría.
"""

MATERIAL_NAME = "Hyper_PLA_Marmol"
MATERIAL_VERSION = 1

# Ajustes capturados de la escena visual aprobada en Blender.
DIFFUSE_COLOR = (0.93, 0.93, 0.93, 1.0)
BASE_COLOR = (1.0, 1.0, 1.0, 1.0)
METALLIC = 0.6692306995391846
ROUGHNESS = 0.5
IOR = 82.39999389648438
VORONOI_SCALE = 1000.0
VORONOI_RANDOMNESS = 1.0
MASK_WHITE_END = 0.20
MASK_BLACK_START = 0.27

_PALETTE = (
    (0.00, (0.005, 0.005, 0.005, 1.0)),
    (0.30, (0.025, 0.025, 0.025, 1.0)),
    (0.55, (0.120, 0.120, 0.120, 1.0)),
    (0.80, (0.320, 0.320, 0.320, 1.0)),
    (1.00, (0.480, 0.480, 0.480, 1.0)),
)


def crear_material(nombre=MATERIAL_NAME):
    """Crea o recupera el material Hyper PLA Marmol en la sesión Blender."""
    import bpy

    existing = bpy.data.materials.get(nombre)
    if existing is not None and existing.get("hyper_pla_marmol_version") == MATERIAL_VERSION:
        return existing

    material = bpy.data.materials.new(nombre)
    material.diffuse_color = DIFFUSE_COLOR
    material.use_nodes = True
    material["hyper_pla_marmol_version"] = MATERIAL_VERSION
    material["hyper_pla_marmol_voronoi_scale"] = VORONOI_SCALE
    material["hyper_pla_marmol_mask"] = [MASK_WHITE_END, MASK_BLACK_START]

    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.name = "Hyper PLA Marmol Output"
    output.location = (700, 80)

    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.name = "Hyper PLA Marmol Surface"
    principled.location = (450, 80)
    principled.inputs["Base Color"].default_value = BASE_COLOR
    principled.inputs["Metallic"].default_value = METALLIC
    principled.inputs["Roughness"].default_value = ROUGHNESS
    principled.inputs["IOR"].default_value = IOR
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    coordinates = nodes.new("ShaderNodeTexCoord")
    coordinates.name = "Hyper PLA Marmol Object Coordinates"
    coordinates.location = (-900, 100)

    voronoi = nodes.new("ShaderNodeTexVoronoi")
    voronoi.name = "Hyper PLA Marmol Flecks"
    voronoi.location = (-650, 100)
    voronoi.feature = "F1"
    voronoi.distance = "EUCLIDEAN"
    voronoi.inputs["Scale"].default_value = VORONOI_SCALE
    voronoi.inputs["Randomness"].default_value = VORONOI_RANDOMNESS
    links.new(coordinates.outputs["Object"], voronoi.inputs["Vector"])

    rgb_to_bw = nodes.new("ShaderNodeRGBToBW")
    rgb_to_bw.name = "Fleck Shade Variation"
    rgb_to_bw.location = (-430, -220)
    links.new(voronoi.outputs["Color"], rgb_to_bw.inputs["Color"])

    palette = nodes.new("ShaderNodeValToRGB")
    palette.name = "Black and Gray Fleck Palette"
    palette.location = (-180, -220)
    palette.color_ramp.interpolation = "LINEAR"
    first, last = palette.color_ramp.elements
    first.position, first.color = _PALETTE[0]
    last.position, last.color = _PALETTE[-1]
    for position, color in _PALETTE[1:-1]:
        element = palette.color_ramp.elements.new(position)
        element.color = color
    links.new(rgb_to_bw.outputs["Val"], palette.inputs["Fac"])

    mask = nodes.new("ShaderNodeValToRGB")
    mask.name = "Fleck Shape Mask"
    mask.location = (-180, 160)
    mask.color_ramp.interpolation = "EASE"
    mask_start, mask_end = mask.color_ramp.elements
    mask_start.position, mask_start.color = 0.0, (1.0, 1.0, 1.0, 1.0)
    mask_end.position, mask_end.color = MASK_BLACK_START, (0.0, 0.0, 0.0, 1.0)
    mask_white = mask.color_ramp.elements.new(MASK_WHITE_END)
    mask_white.color = (1.0, 1.0, 1.0, 1.0)
    links.new(voronoi.outputs["Distance"], mask.inputs["Fac"])

    mix = nodes.new("ShaderNodeMixRGB")
    mix.name = "White Base with Marble Flecks"
    mix.location = (180, 120)
    mix.blend_type = "MIX"
    mix.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
    links.new(mask.outputs["Color"], mix.inputs["Fac"])
    links.new(palette.outputs["Color"], mix.inputs["Color2"])
    links.new(mix.outputs["Color"], principled.inputs["Base Color"])

    return material


def aplicar_material(obj, material=None, reemplazar=True, previsualizar=True):
    """Aplica Hyper PLA Marmol a un objeto malla, sin cambiar su geometría.

    Args:
        obj: objeto Blender con datos que admitan ranuras de material.
        material: material opcional; si se omite, se crea/recupera el predeterminado.
        reemplazar: quita materiales anteriores del objeto antes de asignar el nuevo.
        previsualizar: configura las vistas 3D abiertas para mostrar el material.

    Returns:
        El material aplicado.
    """
    import bpy

    if obj is None or obj.type != "MESH" or not hasattr(obj.data, "materials"):
        raise TypeError("Hyper PLA Marmol requiere un objeto Blender de tipo MESH")

    material = material or crear_material()
    slots = obj.data.materials
    if reemplazar:
        slots.clear()
    if material.name not in {slot.name for slot in slots if slot is not None}:
        slots.append(material)

    obj["acabado_por_defecto"] = "hyper_pla_marmol"
    obj["acabado_por_defecto_version"] = MATERIAL_VERSION

    if previsualizar:
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == "VIEW_3D":
                    area.spaces.active.shading.color_type = "MATERIAL"
                    area.spaces.active.shading.type = "MATERIAL"

    return material


# Nombre explícito para llamadas desde nuevos generadores.
aplicar_material_por_defecto = aplicar_material

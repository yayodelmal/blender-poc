import bpy, json, sys
result = {"blender": bpy.app.version_string, "python": sys.version.split()[0], "ops": {}}
for name in ("stl_export", "stl_import"):
    op = getattr(bpy.ops.wm, name, None)
    if op is None:
        result["ops"][name] = None
    else:
        props = []
        for p in op.get_rna_type().properties:
            if p.identifier == "rna_type":
                continue
            item = {"identifier": p.identifier, "type": p.type}
            if hasattr(p, "default"):
                item["default"] = str(p.default)
            if p.type == "ENUM":
                item["enum_items"] = [entry.identifier for entry in p.enum_items]
            props.append(item)
        result["ops"][name] = props
print("EXP_BPY_003_STL_API " + json.dumps(result, sort_keys=True))

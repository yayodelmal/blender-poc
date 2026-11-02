import bpy, json, sys
obj = bpy.data.objects.get('EXP-BPY-003_ReliefPlate')
views=[]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D' and area.spaces.active.type == 'VIEW_3D':
            space=area.spaces.active
            rv=space.region_3d
            views.append({'screen':screen.name,'area_size':[area.width,area.height], 'view_distance':rv.view_distance, 'view_location':list(rv.view_location), 'view_perspective':rv.view_perspective, 'view_rotation':[rv.view_rotation.w,rv.view_rotation.x,rv.view_rotation.y,rv.view_rotation.z], 'lens':space.lens})
result={
 'filepath':bpy.data.filepath,
 'objects':[(o.name,o.type, list(o.dimensions), list(o.location), list(o.scale),o.hide_viewport,o.hide_get(),o.hide_render) for o in bpy.context.scene.objects],
 'object_exists':obj is not None,
 'object_collections':[c.name for c in obj.users_collection] if obj else [],
 'scene_camera':bpy.context.scene.camera.name if bpy.context.scene.camera else None,
 'view_layers':[(vl.name,[(o.name,o.hide_get()) for o in vl.objects]) for vl in bpy.context.scene.view_layers],
 'view_3d':views,
}
print('EXP_BPY_003_VIEW_DIAG '+json.dumps(result,sort_keys=True))

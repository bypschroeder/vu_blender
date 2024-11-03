import bpy

def bake_cloth_simulation(shirt_obj, start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    bpy.context.view_layer.objects.active = shirt_obj
    bpy.ops.object.select_all(action="DESELECT")
    shirt_obj.select_set(True)

    if (bpy.context.object.mode != "OBJECT"):
        bpy.ops.object.mode_set(mode="OBJECT")

    print("Baking the cloth-simulation")
    bpy.ops.ptcache.bake_all(bake=True)
    print("Baking done")
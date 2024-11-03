import bpy

def export_to_obj(filepath):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        if obj.type == "MESH" or obj.type == "ARMATURE":
            obj.select_set(True)

    bpy.ops.wm.obj_export(filepath=filepath)

def export_to_fbx(filepath):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        if obj.type == "MESH" or obj.type == "ARMATURE":
            obj.select_set(True)

    bpy.ops.export_scene.fbx(filepath=filepath)

def export_to_glb(filepath):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        if obj.type == "MESH" or obj.type == "ARMATURE":
            obj.select_set(True)

    bpy.ops.export_scene.gltf(filepath=filepath)
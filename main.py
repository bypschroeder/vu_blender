import bpy
import math
import os
import random

def clear_scene():
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        if collection.name == "Collection":
            bpy.data.collections.remove(collection)

def add_camera(location, rotation):
    bpy.ops.object.camera_add(location=location)

    camera = bpy.context.object

    r = tuple(math.radians(angle) for angle in rotation)

    camera.rotation_euler = r

    return camera

def add_light(rotation):
    bpy.ops.object.light_add(type='SUN', radius=10, location=(0, 0, 0))

    light = bpy.context.object

    r = tuple(math.radians(angle) for angle in rotation)

    light.rotation_euler = r

def import_smplx_model(gender='neutral'):
    if gender not in ['neutral', 'male', 'female']:
        raise ValueError("Invalid gender")
    
    if "smplx_blender_addon" not in bpy.context.preferences.addons:
        print("No SMPL-X addon found")
        return

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_gender = gender
    bpy.ops.scene.smplx_add_gender()
    # bpy.ops.object.smplx_set_poseshapes()
    # bpy.ops.object.smplx_set_handpose()

    # TODO: Height und Weight ändern sich, wenn man die Pose ändert
    # bpy.data.window_managers["WinMan"].smplx_tool.smplx_height = height
    # bpy.data.window_managers["WinMan"].smplx_tool.smplx_weight = weight

    bpy.ops.object.smplx_random_shape()

    human_mesh = bpy.data.objects.get(f"SMPLX-mesh-{gender}")
    human_mesh.modifiers.new(name="Collision", type="COLLISION")

    armature = bpy.data.objects.get(f"SMPLX-{gender}")
    armature.scale[0] = 10
    armature.scale[1] = 10
    armature.scale[2] = 10

    bpy.ops.object.select_all(action='DESELECT')

def load_smplx_pose(path):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.smplx_load_pose(filepath=path)

def set_keyframe_at_frame(armature):
    armature = bpy.data.objects.get(armature)

    if armature is None or armature.type != 'ARMATURE':
        print("Armature not found")
        return
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="SELECT")

    bpy.ops.anim.keyframe_insert_by_name(type="LocRotScale")

    bpy.ops.object.posemode_toggle()

def append_object(filepath, object_name):
    with bpy.data.libraries.load(filepath=filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    
    obj = bpy.data.objects.get(object_name)

    if obj:
        bpy.context.collection.objects.link(obj)
        obj.select_set(True)

        obj.location = (0, -0.9, -1.6) # Weight und Height
        # obj.location = (0, -1.5, 0) # Pose

        print(f"{object_name} was appended")
    else:
        print(f"{object_name} could not be found")

    return obj

def append_random_shirt(directory):
    blend_files = [f for f in os.listdir(directory) if f.endswith('.blend')]

    if not blend_files:
        print("No blend files found")
        return None
    
    selected_file = random.choice(blend_files)

    blend_path = os.path.join(directory, selected_file)

    object_name = os.path.splitext(selected_file)[0]

    return append_object(blend_path, object_name)

def append_random_pants(directory):
    blend_files = [f for f in os.listdir(directory) if f.endswith('.blend')]

    if not blend_files:
        print("No blend files found")
        return None
    
    selected_file = random.choice(blend_files)

    blend_path = os.path.join(directory, selected_file)

    object_name = os.path.splitext(selected_file)[0]

    return append_object(blend_path, object_name)

def add_cloth_modifier(shirt_obj):
    if not any(mod.type == 'CLOTH' for mod in shirt_obj.modifiers):
        cloth_modifier = shirt_obj.modifiers.new(name="Cloth", type='CLOTH')
        
        cloth_modifier.settings.quality = 24
        cloth_modifier.settings.mass = 0.3  
        cloth_modifier.settings.air_damping = 1
        
        cloth_modifier.settings.tension_stiffness = 15
        cloth_modifier.settings.compression_stiffness = 15
        cloth_modifier.settings.shear_stiffness = 15
        cloth_modifier.settings.bending_stiffness = 0.5

        cloth_modifier.settings.use_sewing_springs = True
        cloth_modifier.settings.sewing_force_max = 5
        
        cloth_modifier.collision_settings.collision_quality = 8
        cloth_modifier.collision_settings.use_self_collision = True

        cloth_modifier.point_cache.frame_start = 1
        cloth_modifier.point_cache.frame_end = 50

        print("cloth-modifier was added")
    else:
        print(f"{shirt_obj.name} already has a cloth-modifier")

def add_weld_modifier(shirt_obj):
    if not any(mod.type == "WELD" for mod in shirt_obj.modifiers):
        weld_modifier = shirt_obj.modifiers.new(name="Weld", type="WELD")

        weld_modifier.mode = "CONNECTED"
        weld_modifier.loose_edges = True
        weld_modifier.merge_threshold = 0.18

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

def render_image(camera, output_path):
    bpy.context.scene.camera = camera

    bpy.context.scene.frame_set(50)

    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGBA"

    bpy.context.scene.render.film_transparent = True

    bpy.ops.render.render(write_still=True)

    print("Rendered image to", output_path)


# Loop for rendering multiple images
for i in range(3):
    clear_scene()

    camera = add_camera(location=(0, -60, -3), rotation=(90, 0, 0))
    add_light(rotation=(90, 0, 0))

    gender = "male" if i % 2 == 0 else "female"
    import_smplx_model(gender=gender)
    # bpy.context.scene.frame_set(20)
    # set_keyframe_at_frame("SMPLX-male")

    # bpy.context.scene.frame_set(40)
    # load_smplx_pose("./smpl/models/smplx/rp_aneko_posed_009_0_0.pkl")
    # set_keyframe_at_frame("SMPLX-male")


    shirt = append_random_shirt("D:/Projects/vu_blender/clothes/shirts/")
    # pants = append_random_pants("D:/Projects/vu_blender/clothes/pants/")

    if shirt:
        add_cloth_modifier(shirt)
        add_weld_modifier(shirt)

        # bake_cloth_simulation(shirt, start_frame=1, end_frame=50)

    # if pants:
    #     add_cloth_modifier(pants)
    #     add_weld_modifier(pants)

        # bake_cloth_simulation(pants, start_frame=1, end_frame=50)

    bake_cloth_simulation(shirt, start_frame=1, end_frame=50)

    render_image(camera, f"D:/Projects/vu_blender/output_images/{i}.png")

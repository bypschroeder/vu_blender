import bpy
import random
import os

from _helpers.path import get_relative_path

def import_smplx_model(gender="neutral"):
    if gender not in ['neutral', 'male', 'female']:
        raise ValueError("Invalid gender")
    
    if "smplx_blender_addon"not in bpy.context.preferences.addons:
        raise ValueError("Please install smplx addon") 
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_gender = gender
    bpy.ops.scene.smplx_add_gender()

    bpy.ops.object.select_all(action='DESELECT')
    armature = bpy.data.objects.get(f"SMPLX-{gender}")
    armature.select_set(True)

    bpy.context.view_layer.objects.active = armature
    
    armature.scale = (10, 10, 10) 

def load_pose(path):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.smplx_load_pose(filepath=path)

def set_height_weight(height, weight, gender):
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_height = height
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_weight = weight

    bpy.ops.object.select_all(action="DESELECT")
    mesh = bpy.data.objects.get(f"SMPLX-mesh-{gender}")
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    
    bpy.ops.object.smplx_measurements_to_shape()
    bpy.ops.object.smplx_snap_ground_plane()

def get_random_gender():
    genders = ["neutral", "male", "female"]

    return random.choice(genders)

def get_random_height(gender):
    if gender == "female":
        return random.triangular(1.4, 1.75, 2.0)
    else:
        return random.uniform(1.5, 2.2)

def get_random_weight(height):
    mean_weight = 22 * (height ** 2)
    std_dev = 5

    weight = random.gauss(mean_weight, std_dev)

    weight = max(40.0, min(weight, 110.0))

    return weight

def get_random_pose(folder_path):
    pkl_files = [file for file in os.listdir(folder_path) if file.endswith(".pkl")]

    if not pkl_files:
        raise ValueError("No pose files found")
    
    random_pkl_file = random.choice(pkl_files)

    return os.path.join(folder_path, random_pkl_file)

# TODO: überarbeiten
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

def keyframe_armature_location(armature):
    armature = bpy.data.objects.get(armature)

    if armature is None or armature.type != 'ARMATURE':
        print("Armature not found")
        return
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    bpy.ops.anim.keyframe_insert_by_name(type="Location")

def keyframe_all_shape_keys(mesh_name):
    mesh = bpy.data.objects.get(mesh_name)

    if not mesh:
        print(f"Mesh {mesh_name} not found")
        return
    
    if not mesh.data.shape_keys:
        print(f"Mesh {mesh_name} has no shape keys")
        return
    
    for shape_key in mesh.data.shape_keys.key_blocks:
        shape_key.keyframe_insert(data_path="value", frame=bpy.context.scene.frame_current)

def add_collision_modifier(mesh_name):
    mesh = bpy.data.objects.get(mesh_name)

    if not mesh:
        print(f"Mesh {mesh_name} not found")
        return
    
    mesh.modifiers.new(name="Collision", type="COLLISION")
    mesh.collision.thickness_inner = 0.001
    mesh.collision.thickness_outer = 0.001

def create_random_smplx_model(randomize_pose="true"):
    gender = "male" # get_random_gender()
    height = get_random_height(gender)
    weight = get_random_weight(height)

    import_smplx_model(gender)
    bpy.ops.object.smplx_snap_ground_plane()

    bpy.context.scene.frame_set(10)
    set_keyframe_at_frame(f"SMPLX-{gender}")
    keyframe_armature_location(f"SMPLX-{gender}")
    bpy.ops.anim.keyframe_insert_by_name(type="Location")
    keyframe_all_shape_keys(f"SMPLX-mesh-{gender}")
    
    bpy.context.scene.frame_set(40)
    if randomize_pose:
        load_pose(get_random_pose(get_relative_path("/smpl/models/smplx/")))
    set_keyframe_at_frame(f"SMPLX-{gender}")

    set_height_weight(height, weight, gender)
    keyframe_armature_location(f"SMPLX-{gender}")
    keyframe_all_shape_keys(f"SMPLX-mesh-{gender}")

    add_collision_modifier(f"SMPLX-mesh-{gender}")

    return gender, height, weight
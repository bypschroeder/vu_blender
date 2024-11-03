import bpy
import os
import sys

def add_subdirs_to_sys_path(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == "__pycache__":
            continue  
        sys.path.append(dirpath)

script_dir = os.path.dirname(os.path.abspath(__file__))
add_subdirs_to_sys_path(script_dir)

from config.config_loader import load_config
from _helpers.scene import clear_scene, add_camera, add_light
from _helpers.export import export_to_obj, export_to_fbx, export_to_glb
from _helpers.path import get_relative_path
from _helpers.bake import bake_cloth_simulation
from _helpers.render import render_image
from smpl.import_smpl import create_random_smplx_model
from clothing.append_clothing import append_random_top, append_random_bottom, append_random_shoes

config = load_config()

# Loop for rendering multiple images
for i in range(1):
    # Create scene
    clear_scene()
    if config.scene.place_camera:
        if config.scene.randomize_camera:
            camera = add_camera((0, 0, 0), (0, 0, 0))
        else:
            camera = add_camera((0, -60, 10), (90, 0, 0))
    if config.scene.place_light:
        if config.scene.randomize_light:
            light = add_light((0, 0, 0))
        else:
            light = add_light((90, 0, 0))
    if config.scene.add_floor:
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
        floor = bpy.context.object
        floor.scale = (10, 10, 10)
        floor.modifiers.new(name="Solidify", type="SOLIDIFY")
        floor.modifiers["Solidify"].thickness = 0.1
        floor.modifiers["Solidify"].offset = 0.1
    if config.scene.add_background:
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
        background = bpy.context.object
        background.scale = (10, 10, 10)

    # Create human
    create_random_smplx_model(randomize_pose=config.human.randomize_pose)

    # Add clothing
    if config.clothing.add_top:
        append_random_top()
    
    if config.clothing.add_bottom:
        append_random_bottom()

    if config.clothing.add_shoes:
        append_random_shoes()

    # Bake cloth simulation
    bake_cloth_simulation()

    # Export
    if config.export.export_obj:
        export_to_obj(get_relative_path(f"/output/export_obj/{i}.obj")) # change export path to config
    
    if config.export.export_fbx:
        export_to_fbx(get_relative_path(f"/output/export_fbx/{i}.fbx")) # change export path to config
    
    if config.export.export_glb:
        export_to_glb(get_relative_path(f"/output/export_glb/{i}.glb")) # change export path to config

    # Render
    render_image(camera, get_relative_path(f"/output/render_images/{i}.png")) # change export path to config
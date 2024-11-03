import bpy
import os
import random

from _helpers.path import get_relative_path
from clothing.modifiers import set_cloth_material

clothing_material_map = {
    "t-shirt": "cotton",
    "jeans": "denim",
    "hoodie": "wool"
}

def append_object(filepath, object_name):
    with bpy.data.libraries.load(filepath=filepath, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
    
    obj = bpy.data.objects.get(object_name)

    if obj:
        bpy.context.collection.objects.link(obj)
        obj.select_set(True)

        print(f"{object_name} was appended")
    else:
        print(f"{object_name} could not be found")

    return obj

def get_random_blend_file(folder_path):
    blend_files = [f for f in os.listdir(folder_path) if f.endswith('.blend')]

    if not blend_files:
        print("No blend files found")
        return None
    
    return os.path.join(folder_path, random.choice(blend_files))

def get_object_name_from_filepath(filepath):
    filename_with_extension = os.path.basename(filepath)

    object_name = os.path.splitext(filename_with_extension)

    return object_name[0]

def append_random_top():
    top_path = get_random_blend_file(get_relative_path("/clothing/models/tops/shirts/"))

    if top_path:
        top_obj = append_object(top_path, get_object_name_from_filepath(top_path))
        top_base_name = top_obj.name.split("_", 1)[-1]
        if top_base_name in clothing_material_map:
            set_cloth_material(top_obj, clothing_material_map[top_base_name])

def append_random_bottom():
    bottom_path = get_random_blend_file(get_relative_path("/clothing/models/bottoms/pants/"))

    if bottom_path:
        bottom_obj = append_object(bottom_path, get_object_name_from_filepath(bottom_path))
        bottom_base_name = bottom_obj.name.split("_", 1)[-1]
        if bottom_base_name in clothing_material_map:
            set_cloth_material(bottom_obj, clothing_material_map[bottom_base_name])

def append_random_shoes():
    print("TODO")

# def assemble_random_outfit():
#     top_path = get_random_blend_file(get_relative_path("/clothing/models/shirts/"))
#     bottom_path = get_random_blend_file(get_relative_path("/clothing/models/pants/"))

#     if top_path:
#         top_obj = append_object(top_path, get_object_name_from_filepath(top_path))
#         top_base_name = top_obj.name.split("_", 1)[-1]
#         if top_base_name in clothing_material_map:
#             set_cloth_material(top_obj, clothing_material_map[top_base_name])
    
#     if bottom_path:
#         bottom_obj = append_object(bottom_path, get_object_name_from_filepath(bottom_path))
#         bottom_base_name = bottom_obj.name.split("_", 1)[-1]
#         if bottom_base_name in clothing_material_map:
#             set_cloth_material(bottom_obj, clothing_material_map[bottom_base_name])

#     return bottom_obj, bottom_obj


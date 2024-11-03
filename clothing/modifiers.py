def set_cloth_material(obj, material_type="default"):
    cloth_modifier = obj.modifiers.get("Cloth")

    if not cloth_modifier:
        cloth_modifier = obj.modifiers.new(name="Cloth", type='CLOTH')

    cloth_settings = cloth_modifier.settings

    add_smooth_modifier(obj)

    if material_type == "cotton":
        cloth_settings.quality = 12
        cloth_settings.mass = 0.3
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 22.5
        cloth_settings.compression_stiffness = 22.5
        cloth_settings.shear_stiffness = 22.5
        cloth_settings.bending_stiffness = 0.510

        cloth_settings.tension_damping = 5
        cloth_settings.compression_damping = 5
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.350

        cloth_settings.collision_quality = 8
        cloth_settings.use_self_collision = True
        cloth_settings.collision_settings.self_distance_min = 0.001
    elif material_type == "denim":
        cloth_settings.quality = 12
        cloth_settings.mass = 1.0
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 18
        cloth_settings.compression_stiffness = 18
        cloth_settings.shear_stiffness = 18
        cloth_settings.bending_stiffness = 2.507

        cloth_settings.tension_damping = 5
        cloth_settings.compression_damping = 5
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.007

        cloth_settings.collision_quality = 8
        cloth_settings.use_self_collision = True
        cloth_settings.collision_settings.self_distance_min = 0.001
    elif material_type == "wool":
        cloth_settings.quality = 12
        cloth_settings.mass = 0.1
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 1.35
        cloth_settings.compression_stiffness = 1.35
        cloth_settings.shear_stiffness = 1.35
        cloth_settings.bending_stiffness = 1.508

        cloth_settings.tension_damping = 5
        cloth_settings.compression_damping = 5
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.210

        cloth_settings.collision_quality = 8
        cloth_settings.use_self_collision = True
        cloth_settings.collision_settings.self_distance_min = 0.001
    elif material_type == "silk":
        cloth_settings.quality = 12
    elif material_type == "linen":
        cloth_settings.quality = 12
    elif material_type == "default":
        cloth_settings.quality = 12
        cloth_settings.mass = 0.5
        cloth_settings.air_damping = 1

        cloth_settings.tension_stiffness = 22.5
        cloth_settings.compression_stiffness = 22.5
        cloth_settings.shear_stiffness = 22.5
        cloth_settings.bending_stiffness = 5.005

        cloth_settings.tension_damping = 5
        cloth_settings.compression_damping = 5
        cloth_settings.shear_damping = 5
        cloth_settings.bending_damping = 0.007

        cloth_settings.collision_quality = 8
        cloth_settings.use_self_collision = True
        cloth_settings.collision_settings.self_distance_min = 0.001    
    else:
        print("Material type not found")

def add_smooth_modifier(obj):
    smooth_modifier = obj.modifiers.new(name="Smooth", type="SMOOTH")

    smooth_modifier.factor = 0.6
    smooth_modifier.iterations = 2
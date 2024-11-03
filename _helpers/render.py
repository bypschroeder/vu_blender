import bpy

def render_image(camera, output_path):
    bpy.context.scene.camera = camera

    bpy.context.scene.frame_set(bpy.context.scene.frame_end)

    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGBA"

    bpy.context.scene.render.film_transparent = True

    bpy.ops.render.render(write_still=True)

    print("Rendered image to", output_path)
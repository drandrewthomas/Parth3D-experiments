import bpy

# Set the renderer to Eevee
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Set the image format to an 8-bit PNG with alpha channel
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.image_settings.color_depth = '8'

# Set the size of the image to render
bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480

# Tell Blender to render the background transparent
bpy.context.scene.render.film_transparent = True

# We save the file in the same place as the blender file
fname = bpy.path.abspath("//") + "backgroundtest.png"

# Render our image of the scene through the default camera
bpy.context.scene.render.filepath = fname
bpy.ops.render.render(write_still=True)

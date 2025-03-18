import bpy; print("Available addons:"); print([addon.module for addon in bpy.context.preferences.addons])

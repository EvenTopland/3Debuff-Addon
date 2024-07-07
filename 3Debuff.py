bl_info = {
    "name": "3Debuff",
    "blender": (4, 1, 1),
    "category": "Object",
}

import bpy
import random

def move_objects():
    for obj in bpy.data.objects:
        obj.location.x += random.uniform(-3, 3)
        obj.location.y += random.uniform(-3, 3)
        obj.location.z += random.uniform(-3, 3)
    return 120  # Run every 2 minutes

def delete_random_object():
    if bpy.data.objects:
        obj = random.choice(bpy.data.objects)
        bpy.data.objects.remove(obj)
    return 300  # Run every 5 minutes

def rotate_objects():
    for obj in bpy.data.objects:
        obj.rotation_euler.x += random.uniform(-0.4, 0.4)
        obj.rotation_euler.y += random.uniform(-0.4, 0.4)
        obj.rotation_euler.z += random.uniform(-0.4, 0.4)
    return 120  # Run every 2 minutes

def shutdown_blender():
    delay_seconds = random.randint(60, 300)
    bpy.app.timers.register(bpy.ops.wm.quit_blender, first_interval=delay_seconds)

def change_light_colors():
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            obj.data.color = (random.random(), random.random(), random.random())
    return 300  # Run every 5 minutes

def add_random_modifier():
    modifiers = [
        "ARRAY", "BEVEL", "MIRROR", "REMESH", "SCREW", "SKIN", "SOLIDIFY", 
        "SUBSURF", "WIREFRAME", "DISPLACE", "SIMPLE_DEFORM", "WAVE"
    ]
    
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    
    if mesh_objects:
        obj = random.choice(mesh_objects)
        mod_type = random.choice(modifiers)
        obj.modifiers.new(name=mod_type, type=mod_type)
    return 300  # Run every 5 minutes

def disable_undo():
    keyconfig = bpy.context.window_manager.keyconfigs.active
    for keymap in keyconfig.keymaps:
        for kmi in keymap.keymap_items:
            if kmi.idname == 'ed.undo':
                keymap.keymap_items.remove(kmi)

def disable_delete_button():
    keyconfig = bpy.context.window_manager.keyconfigs.active
    
    for keymap_name in ['Object Mode', 'Mesh']:
        keymap = keyconfig.keymaps.get(keymap_name)
        if keymap:
            for kmi in keymap.keymap_items:
                if kmi.type in {'X', 'DEL'}:
                    keymap.keymap_items.remove(kmi)

ui_scale = 0.5
scale_direction = 1

def change_ui_scale():
    global ui_scale, scale_direction
    ui_scale += 0.1 * scale_direction
    if ui_scale >= 2.0:
        scale_direction = -1
    elif ui_scale <= 0.5:
        scale_direction = 1
    bpy.context.preferences.view.ui_scale = ui_scale
    return 5  # Run every 5 seconds

class OBJECT_OT_move_objects(bpy.types.Operator):
    bl_idname = "object.move_objects"
    bl_label = "Move Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(move_objects)
        return {'FINISHED'}

class OBJECT_OT_delete_random_object(bpy.types.Operator):
    bl_idname = "object.delete_random_object"
    bl_label = "Delete Random Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(delete_random_object)
        return {'FINISHED'}

class OBJECT_OT_rotate_objects(bpy.types.Operator):
    bl_idname = "object.rotate_objects"
    bl_label = "Rotate Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(rotate_objects)
        return {'FINISHED'}

class OBJECT_OT_shutdown_blender(bpy.types.Operator):
    bl_idname = "object.shutdown_blender"
    bl_label = "Shutdown Blender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        shutdown_blender()
        return {'FINISHED'}

class OBJECT_OT_random_light_color(bpy.types.Operator):
    bl_idname = "object.random_light_color"
    bl_label = "Randomize Light Colors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(change_light_colors)
        return {'FINISHED'}

class OBJECT_OT_add_random_modifier(bpy.types.Operator):
    bl_idname = "object.add_random_modifier"
    bl_label = "Add Random Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(add_random_modifier)
        return {'FINISHED'}

class OBJECT_OT_disable_undo(bpy.types.Operator):
    bl_idname = "object.disable_undo"
    bl_label = "Disable Undo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        disable_undo()
        return {'FINISHED'}

class OBJECT_OT_disable_delete_button(bpy.types.Operator):
    bl_idname = "object.disable_delete_button"
    bl_label = "Disable Delete Button"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        disable_delete_button()
        return {'FINISHED'}

class OBJECT_OT_change_scale(bpy.types.Operator):
    bl_idname = "ui.change_scale"
    bl_label = "Change UI Scale Periodically"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.timers.register(change_ui_scale)
        return {'FINISHED'}

class VIEW3D_PT_chaos_panel(bpy.types.Panel):
    bl_label = "3Debuff Panel"
    bl_idname = "VIEW3D_PT_chaos_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '3Debuff'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.move_objects", text="Move Objects Every 2min")
        layout.operator("object.delete_random_object", text="Delete Random Object Every 5min")
        layout.operator("object.rotate_objects", text="Rotate Objects Every 2min")
        layout.operator("object.add_random_modifier", text="Add Random Modifier Every 5min")
        layout.operator("object.shutdown_blender", text="Random shutdown timer")
        layout.operator("object.disable_undo", text="Disable Undo")
        layout.operator("object.disable_delete_button", text="Disable Delete Button")
        layout.operator("ui.change_scale", text="Change UI Scale Periodically")
        layout.operator("object.random_light_color", text="Randomize Light Colors every 5min")

def register():
    bpy.utils.register_class(OBJECT_OT_move_objects)
    bpy.utils.register_class(OBJECT_OT_delete_random_object)
    bpy.utils.register_class(OBJECT_OT_rotate_objects)
    bpy.utils.register_class(OBJECT_OT_shutdown_blender)
    bpy.utils.register_class(OBJECT_OT_add_random_modifier)
    bpy.utils.register_class(OBJECT_OT_disable_undo)
    bpy.utils.register_class(OBJECT_OT_disable_delete_button)
    bpy.utils.register_class(OBJECT_OT_change_scale)
    bpy.utils.register_class(OBJECT_OT_random_light_color)
    bpy.utils.register_class(VIEW3D_PT_chaos_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_move_objects)
    bpy.utils.unregister_class(OBJECT_OT_delete_random_object)
    bpy.utils.unregister_class(OBJECT_OT_rotate_objects)
    bpy.utils.unregister_class(OBJECT_OT_shutdown_blender)
    bpy.utils.unregister_class(OBJECT_OT_add_random_modifier)
    bpy.utils.unregister_class(OBJECT_OT_disable_undo)
    bpy.utils.unregister_class(OBJECT_OT_disable_delete_button)
    bpy.utils.unregister_class(OBJECT_OT_change_scale)
    bpy.utils.unregister_class(OBJECT_OT_random_light_color)
    bpy.utils.unregister_class(VIEW3D_PT_chaos_panel)

if __name__ == "__main__":
    register()
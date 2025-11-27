bl_info = {
    "name": "Updater test NEW OBJECT",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > My Tools",
    "description": "Adds a custom mesh object",
    "category": "Object",
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatVectorProperty, BoolProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

# Import updater - make sure this module exists in your addon
from . import addon_updater_ops

def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# NUEVO: Panel para la interfaz lateral
class VIEW3D_PT_my_custom_panel(Panel):
    bl_label = "My Custom Tools"
    bl_idname = "VIEW3D_PT_my_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Tools"  # Esto crea una pestaña nueva en el sidebar

    def draw(self, context):
        layout = self.layout
        
        # Título
        layout.label(text="Add Custom Objects")
        
        # Botón principal
        row = layout.row()
        row.operator("mesh.add_object", text="Add Custom Mesh", icon='MESH_PLANE')
        
        # Configuración de escala
        box = layout.box()
        box.label(text="Scale Settings:")
        
        # Aquí podrías añadir propiedades configurables
        # box.prop(context.scene, "my_scale_property")...
        
        # Información
        layout.separator()
        layout.label(text="Check preferences for updates")


class DemoPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )

    updater_interval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_interval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
    )
    updater_interval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_interval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout
        addon_updater_ops.update_settings_ui(self, context, layout)


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Custom Object",  # Texto más descriptivo
        icon='PLUGIN')


def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


addon_keymaps = []


def register():
    # Register the updater first
    addon_updater_ops.register(bl_info)

    # Register classes
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(VIEW3D_PT_my_custom_panel)  # NUEVO: Registrar el panel
    bpy.utils.register_class(DemoPreferences)
    
    # Register manual map and UI
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    # Unregister in reverse order
    
    # Unregister UI and manual
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    
    # Unregister classes
    bpy.utils.unregister_class(DemoPreferences)
    bpy.utils.unregister_class(VIEW3D_PT_my_custom_panel)  # NUEVO: Desregistrar el panel
    bpy.utils.unregister_class(OBJECT_OT_add_object)

    # Unregister the updater last
    addon_updater_ops.unregister()


if __name__ == "__main__":
    register()
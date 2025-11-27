import bpy
from bpy.types import Panel


class VIEW3D_PT_random_vertex_colors(Panel):
    bl_label = "Random Vertex Colors"
    bl_idname = "VIEW3D_PT_random_vertex_colors"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            layout.label(text="Selecciona un objeto mesh")
            return

        # Botón principal
        col = layout.column(align=True)
        col.operator("mesh.random_vertex_colors", 
                    text="Randomizar Vertex Colors", 
                    icon='COLOR')

        # Configuración de colores
        box = layout.box()
        box.label(text="Configuración de Colores:", icon='PALETTE')
        
        # Acceder a las propiedades del operador
        op_props = bpy.ops.mesh.random_vertex_colors.get_rna_type().properties
        
        row = box.row(align=True)
        row.prop(op_props["color_min"], "default", text="Color Mínimo")
        row.prop(op_props["color_max"], "default", text="Color Máximo")

        # Información del objeto
        box = layout.box()
        box.label(text="Información del Objeto:", icon='INFO')
        
        if obj.data.vertex_colors:
            box.label(text=f"Vertex Colors: {len(obj.data.vertex_colors.active.data)}")
        else:
            box.label(text="Vertex Colors: No creados")


classes = [
    VIEW3D_PT_random_vertex_colors,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
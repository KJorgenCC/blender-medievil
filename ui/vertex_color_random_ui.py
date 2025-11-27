import bpy

class UI_PT_VertexColorRandom(bpy.types.Panel):
    bl_label = "Vertex Color Random"
    bl_idname = "UI_PT_vertex_color_random"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.vertex_color_random")

def register():
    bpy.utils.register_class(UI_PT_VertexColorRandom)

def unregister():
    bpy.utils.unregister_class(UI_PT_VertexColorRandom)
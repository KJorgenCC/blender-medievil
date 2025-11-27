import bpy
import random

class OPS_VertexColorRandom(bpy.types.Operator):
    bl_idname = "object.vertex_color_random"
    bl_label = "Random Vertex Colors"
    bl_description = "Randomize vertex colors for selected object"
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}
        
        mesh = obj.data
        if not mesh.vertex_colors:
            mesh.vertex_colors.new()
        
        color_layer = mesh.vertex_colors.active.data
        
        for poly in mesh.polygons:
            for idx in poly.loop_indices:
                color_layer[idx].color = (
                    random.random(),
                    random.random(),
                    random.random(),
                    1.0
                )
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OPS_VertexColorRandom)

def unregister():
    bpy.utils.unregister_class(OPS_VertexColorRandom)
import bpy
import bmesh
import random
from bpy.types import Operator
from bpy.props import FloatVectorProperty


class MESH_OT_random_vertex_colors(Operator):
    bl_idname = "mesh.random_vertex_colors"
    bl_label = "Random Vertex Colors"
    bl_description = "Aplica colores aleatorios a los vértices del mesh seleccionado"
    bl_options = {'REGISTER', 'UNDO'}

    color_min: FloatVectorProperty(
        name="Color Mínimo",
        subtype='COLOR',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=1.0,
        description="Color mínimo para la generación aleatoria"
    )

    color_max: FloatVectorProperty(
        name="Color Máximo",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        description="Color máximo para la generación aleatoria"
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH' and obj.mode == 'OBJECT')

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data

        # Crear vertex color layer si no existe
        if not mesh.vertex_colors:
            mesh.vertex_colors.new()
            self.report({'INFO'}, "Vertex color layer creado")

        vertex_colors = mesh.vertex_colors.active.data

        # Asignar colores aleatorios a cada vértice
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                # Generar color aleatorio dentro del rango especificado
                r = random.uniform(self.color_min[0], self.color_max[0])
                g = random.uniform(self.color_min[1], self.color_max[1])
                b = random.uniform(self.color_min[2], self.color_max[2])
                
                vertex_colors[loop_index].color = (r, g, b, 1.0)

        # Actualizar la malla
        mesh.update()
        self.report({'INFO'}, f"Vertex colors randomizados para {obj.name}")
        return {'FINISHED'}


classes = [
    MESH_OT_random_vertex_colors,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
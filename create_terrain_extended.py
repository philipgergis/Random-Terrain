bl_info = {
    "name": "Extended Terrain",
    "author": "Philip Gergis",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Extended Terrain Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
import random


def add_object(self, context):

    # spawn plane
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    obj = bpy.context.object
    me = obj.data

    # Code taken from https://docs.blender.org/api/current/bmesh.html

    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    # set random see
    random.seed(self.seed)
    
    # Modify the BMesh, can do anything here...
    
    d = self.d
    for i in range(self.iterations):
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
        for v in bm.verts:
            v.co.z += random.uniform(-d, d)
        d *= self.s
    
    for v in bm.verts:
        if(self.sharp):
            v.co.z = -abs(v.co.z)
        else:
            if(v.co.z >= self.max):
                v.co.z = self.max
            elif(v.co.z <= self.min):
                v.co.z = self.min
        
    
        
        

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()  # free and prevent further access


class OBJECT_OT_add_object(Operator):
    """Create a new Extended Terrain Object"""
    bl_idname = "mesh.add_terrain_extended"
    bl_label = "Add extended terrain"
    bl_options = {'REGISTER', 'UNDO'}
    
    d: FloatProperty(
        name="d",
        default=1.0,
        min=0.1,
        max=3.0,
        step=1
    )
    
    s: FloatProperty(
        name="s",
        default=0.5,
        min=0.01,
        max=1.0,
        step=1
    )
    
    iterations: IntProperty(
        name="iterations",
        default=5,
        min=2,
        max=9,
    )
    
    seed: IntProperty(
        name="seed",
        default=0,
    )
    
    min: FloatProperty(
        name="min",
        default=0.0,
        min=-10.0,
        max=0.0,
        step=1,
    )
    
    max: FloatProperty(
        name="max",
        default=0.45,
        min=0.0,
        max=10.0,
        step=1,
    )
    
    sharp: BoolProperty(
        name="sharp",
        default=False,
    )

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Extended Terrain",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()

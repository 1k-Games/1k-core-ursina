import warnings 

from print_tricks import pt
from ursina import * 

from math import radians




from panda3d.core import Camera

from ursina import *

class CustomEntity(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def use_camera_pip(self, cam_parent=None, position=Vec3(0,0,0), rotation=Vec3(0,0,0), resolution=(512, 512)):
        if hasattr(self, 'pip_display_region'):
            self.ursina_window.removeDisplayRegion(self.pip_display_region)
            self.camera_2.removeNode()

        ## Ursina's main display region
        self.main_display_region = app.camNode.getDisplayRegion(0)
        self.ursina_window = self.main_display_region.getWindow()

        ## Create a texture buffer at the specified resolution
        self.texture_buffer = self.ursina_window.makeTextureBuffer("Texture Buffer", resolution[0], resolution[1])

        ## secondary display region & camera
        self.camera_node_2 = Camera('CameraNode2')
        self.camera_2 = scene.attachNewNode(self.camera_node_2)
        self.camera_2.node().getLens(0).setFar(11333)

        if cam_parent is not None:
            self.camera_2.reparent_to(cam_parent)
        else:
            self.camera_2.reparent_to(camera)

        self.camera_2.setPos(position)
        self.camera_2.setHpr(rotation)

        ## Create a new display region and set its camera to the camera of the buffer
        self.pip_display_region = self.ursina_window.makeDisplayRegion(0.1, 0.9, 0.1, 0.9)
        self.pip_display_region.setCamera(self.camera_2)
        self.pip_display_region.setSort(22)


app = Ursina()

entity = CustomEntity()
entity.use_camera_pip()

Entity(model = 'plane', collider = 'box', color = color.red, scale = (100, 1, 100), position = (0, -1, 0))
Entity(model='cube', color=color.blue, scale=(1, 1, 1))
EditorCamera()

app.run()











path_vertices = [Vec3(-0.005, -0.005, -0.005), Vec3(0.005, -0.005, -0.005), Vec3(0.005, 0.005, -0.005), Vec3(-0.005, 0.005, -0.005), Vec3(-0.005, -0.005, 0.005), Vec3(0.005, -0.005, 0.005), Vec3(0.005,
0.005, 0.005), Vec3(-0.005, 0.005, 0.005), Vec3(-0.005, -0.005, -0.005), Vec3(0.005, -0.005, -0.005), Vec3(0.005, 0.005, -0.005), Vec3(-0.005, 0.005, -0.005), Vec3(-0.005, -0.005, 0.005),
Vec3(0.005, -0.005, 0.005), Vec3(0.005, 0.005, 0.005), Vec3(-0.005, 0.005, 0.005), Vec3(-0.005, 0.106964, 0.0264391), Vec3(0.005, 0.106964, 0.0264391), Vec3(0.005, 0.116964, 0.0264391),
Vec3(-0.005, 0.116964, 0.0264391), Vec3(-0.005, 0.106964, 0.0364391), Vec3(0.005, 0.106964, 0.0364391), Vec3(0.005, 0.116964, 0.0364391), Vec3(-0.005, 0.116964, 0.0364391), Vec3(-0.005,
0.217521, 0.12036), Vec3(0.005, 0.217521, 0.12036), Vec3(0.005, 0.227521, 0.12036), Vec3(-0.005, 0.227521, 0.12036), Vec3(-0.005, 0.217521, 0.13036), Vec3(0.005, 0.217521, 0.13036),
Vec3(0.005, 0.227521, 0.13036), Vec3(-0.005, 0.227521, 0.13036), Vec3(-0.005, 0.325279, 0.275583), Vec3(0.005, 0.325279, 0.275583), Vec3(0.005, 0.335279, 0.275583), Vec3(-0.005, 0.335279,
0.275583), Vec3(-0.005, 0.325279, 0.285583), Vec3(0.005, 0.325279, 0.285583), Vec3(0.005, 0.335279, 0.285583), Vec3(-0.005, 0.335279, 0.285583), Vec3(-0.005, 0.527032, 0.761379),
Vec3(0.005, 0.527032, 0.761379), Vec3(0.005, 0.537032, 0.761379), Vec3(-0.005, 0.537032, 0.761379), Vec3(-0.005, 0.527032, 0.771379), Vec3(0.005, 0.527032, 0.771379), Vec3(0.005, 0.537032,
0.771379), Vec3(-0.005, 0.537032, 0.771379), Vec3(-0.005, 0.61849, 1.08584), Vec3(0.005, 0.61849, 1.08584), Vec3(0.005, 0.62849, 1.08584), Vec3(-0.005, 0.62849, 1.08584), Vec3(-0.005,
0.61849, 1.09584), Vec3(0.005, 0.61849, 1.09584), Vec3(0.005, 0.62849, 1.09584), Vec3(-0.005, 0.62849, 1.09584), Vec3(-0.005, 0.702107, 1.45947), Vec3(0.005, 0.702107, 1.45947),
Vec3(0.005, 0.712107, 1.45947), Vec3(-0.005, 0.712107, 1.45947), Vec3(-0.005, 0.702107, 1.46947), Vec3(0.005, 0.702107, 1.46947), Vec3(0.005, 0.712107, 1.46947), Vec3(-0.005, 0.712107,
1.46947), Vec3(-0.005, 0.841724, 2.33484), Vec3(0.005, 0.841724, 2.33484), Vec3(0.005, 0.851724, 2.33484), Vec3(-0.005, 0.851724, 2.33484), Vec3(-0.005, 0.841724, 2.34484), Vec3(0.005,
0.841724, 2.34484), Vec3(0.005, 0.851724, 2.34484), Vec3(-0.005, 0.851724, 2.34484), Vec3(-0.005, 0.895969, 2.82558), Vec3(0.005, 0.895969, 2.82558), Vec3(0.005, 0.905969, 2.82558),
Vec3(-0.005, 0.905969, 2.82558), Vec3(-0.005, 0.895969, 2.83558), Vec3(0.005, 0.895969, 2.83558), Vec3(0.005, 0.905969, 2.83558), Vec3(-0.005, 0.905969, 2.83558), Vec3(-0.005, 0.938883,
3.3436), Vec3(0.005, 0.938883, 3.3436), Vec3(0.005, 0.948883, 3.3436), Vec3(-0.005, 0.948883, 3.3436), Vec3(-0.005, 0.938883, 3.3536), Vec3(0.005, 0.938883, 3.3536), Vec3(0.005, 0.948883,
3.3536), Vec3(-0.005, 0.948883, 3.3536), Vec3(-0.005, 0.988712, 4.43518), Vec3(0.005, 0.988712, 4.43518), Vec3(0.005, 0.998712, 4.43518), Vec3(-0.005, 0.998712, 4.43518), Vec3(-0.005,
0.988712, 4.44518), Vec3(0.005, 0.988712, 4.44518), Vec3(0.005, 0.998712, 4.44518), Vec3(-0.005, 0.998712, 4.44518), Vec3(-0.005, 0.995, 4.995), Vec3(0.005, 0.995, 4.995), Vec3(0.005,
1.005, 4.995), Vec3(-0.005, 1.005, 4.995), Vec3(-0.005, 0.995, 5.005), Vec3(0.005, 0.995, 5.005), Vec3(0.005, 1.005, 5.005), Vec3(-0.005, 1.005, 5.005), Vec3(-0.005, 0.988712, 5.55482),
Vec3(0.005, 0.988712, 5.55482), Vec3(0.005, 0.998712, 5.55482), Vec3(-0.005, 0.998712, 5.55482), Vec3(-0.005, 0.988712, 5.56482), Vec3(0.005, 0.988712, 5.56482), Vec3(0.005, 0.998712,
5.56482), Vec3(-0.005, 0.998712, 5.56482), Vec3(-0.005, 0.938883, 6.6464), Vec3(0.005, 0.938883, 6.6464), Vec3(0.005, 0.948883, 6.6464), Vec3(-0.005, 0.948883, 6.6464), Vec3(-0.005,
0.938883, 6.6564), Vec3(0.005, 0.938883, 6.6564), Vec3(0.005, 0.948883, 6.6564), Vec3(-0.005, 0.948883, 6.6564), Vec3(-0.005, 0.895969, 7.16442), Vec3(0.005, 0.895969, 7.16442),
Vec3(0.005, 0.905969, 7.16442), Vec3(-0.005, 0.905969, 7.16442), Vec3(-0.005, 0.895969, 7.17442), Vec3(0.005, 0.895969, 7.17442), Vec3(0.005, 0.905969, 7.17442), Vec3(-0.005, 0.905969,
7.17442), Vec3(-0.005, 0.841724, 7.65516), Vec3(0.005, 0.841724, 7.65516), Vec3(0.005, 0.851724, 7.65516), Vec3(-0.005, 0.851724, 7.65516), Vec3(-0.005, 0.841724, 7.66516), Vec3(0.005,
0.841724, 7.66516), Vec3(0.005, 0.851724, 7.66516), Vec3(-0.005, 0.851724, 7.66516), Vec3(-0.005, 0.702107, 8.53053), Vec3(0.005, 0.702107, 8.53053), Vec3(0.005, 0.712107, 8.53053),
Vec3(-0.005, 0.712107, 8.53053), Vec3(-0.005, 0.702107, 8.54053), Vec3(0.005, 0.702107, 8.54053), Vec3(0.005, 0.712107, 8.54053), Vec3(-0.005, 0.712107, 8.54053), Vec3(-0.005, 0.61849,
8.90416), Vec3(0.005, 0.61849, 8.90416), Vec3(0.005, 0.62849, 8.90416), Vec3(-0.005, 0.62849, 8.90416), Vec3(-0.005, 0.61849, 8.91416), Vec3(0.005, 0.61849, 8.91416), Vec3(0.005, 0.62849,
8.91416), Vec3(-0.005, 0.62849, 8.91416), Vec3(-0.005, 0.527032, 9.22862), Vec3(0.005, 0.527032, 9.22862), Vec3(0.005, 0.537032, 9.22862), Vec3(-0.005, 0.537032, 9.22862), Vec3(-0.005,
0.527032, 9.23862), Vec3(0.005, 0.527032, 9.23862), Vec3(0.005, 0.537032, 9.23862), Vec3(-0.005, 0.537032, 9.23862), Vec3(-0.005, 0.325279, 9.71442), Vec3(0.005, 0.325279, 9.71442),
Vec3(0.005, 0.335279, 9.71442), Vec3(-0.005, 0.335279, 9.71442), Vec3(-0.005, 0.325279, 9.72442), Vec3(0.005, 0.325279, 9.72442), Vec3(0.005, 0.335279, 9.72442), Vec3(-0.005, 0.335279,
9.72442), Vec3(-0.005, 0.217521, 9.86964), Vec3(0.005, 0.217521, 9.86964), Vec3(0.005, 0.227521, 9.86964), Vec3(-0.005, 0.227521, 9.86964), Vec3(-0.005, 0.217521, 9.87964), Vec3(0.005,
0.217521, 9.87964), Vec3(0.005, 0.227521, 9.87964), Vec3(-0.005, 0.227521, 9.87964), Vec3(-0.005, -0.005, 9.995), Vec3(0.005, -0.005, 9.995), Vec3(0.005, 0.005, 9.995), Vec3(-0.005, 0.005,
9.995), Vec3(-0.005, -0.005, 10.005), Vec3(0.005, -0.005, 10.005), Vec3(0.005, 0.005, 10.005), Vec3(-0.005, 0.005, 10.005)]





# from panda3d.core import NodePath, GeomEnums, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomNode
# from panda3d.core import Shader
# from ursina import Entity, application

# app=Ursina()
# from panda3d.core import NodePath, GeomEnums, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomNode, TransformState, Mat4
# from panda3d.core import Shader
# from ursina import Entity, application

# def create_instance(entity):
#     if hasattr(entity, 'model') and entity.model:
#         # Convert Ursina's model to Panda3D's NodePath
#         node_path = NodePath(entity.model)

#         # Create a new format that includes an instance index.
#         format = GeomVertexFormat(GeomVertexFormat.get_v3n3cpt2())
#         array_format = format.get_array(0)
#         array_format.set_instancing(True)
#         format = GeomVertexFormat.register_format(format)

#         # Create a new GeomVertexData with the new format.
#         vdata = GeomVertexData(node_path.node().get_geom(0).get_vertex_data())
#         vdata.set_format(format)

#         # Create a new Geom with the new GeomVertexData.
#         geom = Geom(vdata)
#         geom.add_primitive(node_path.node().get_geom(0).get_primitive(0))

#         # Create a new GeomNode with the new Geom.
#         geom_node = GeomNode('geom_node')
#         geom_node.add_geom(geom)

#         # Replace the original node with the new GeomNode.
#         node_path.node().remove_all_geoms()
#         node_path.node().add_child(geom_node)

#         # Set the instance count
#         instance_count = 10
#         node_path.setInstanceCount(instance_count)

#         # Create transformation matrices for each instance
#         transforms = []
#         for i in range(instance_count):
#             mat = Mat4.translate_mat(i * 2, 0, 0)  # Change the multiplier for different spacing
#             transforms.append(TransformState.make_mat(mat))

#         # Set the instance transforms
#         geom_node.set_instance_transforms(transforms)

#         # Convert back to Ursina's Entity
#         entity.model = Entity(model=node_path, parent=application.scene)

#     return entity

# e = Entity(model='cube', color=color.red, z=-10)
# create_instance(e)
# EditorCamera()

# app.run()















import os

from ursina import *

app=Ursina()


##############
# setup textures, etc. 
##############
# e = Animation('sparks3.gif')
anitex = Entity(model='cube', texture=None, y=2)
directory = "C:\\.PythonProjects\\EnergyGame\\EG\\all_bilities\\combilities\\sparks\\"
frames = [load_texture(os.path.join(directory, file)) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
frame_index = 0 
pt(frames)

file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
pt(f"File paths: {file_paths}")
frames = [load_texture(file_path) for file_path in file_paths]

test_image_path = os.path.join(directory, "sparks_6.png")  # replace with an actual file name
pt(load_texture(test_image_path))
pt(test_image_path)

##############
# setup mesh points
##############
vertices = [Vec3(random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1)) for _ in range(25)]
mesh_ent = Entity(model=Mesh(vertices=vertices, mode='point', thickness=.25))

##############
# update textures
##############
def update():
    ...
    frame_index = (frame_index + 1) % len(frames)  # Update the frame index        ...
    anitex.texture = frames[frame_index]
    mesh_ent.texture = frames[frame_index]
    pt(anitex.texture, frame_index)
    pt.ex()


EditorCamera()
app.run()




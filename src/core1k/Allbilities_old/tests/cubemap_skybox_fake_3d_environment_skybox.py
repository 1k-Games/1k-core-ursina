'''Currently Failing. 

The goal is to create that 6-photos from all directions and apply to skybox idea for
high resolution, crazy graphics whenever you are stationary. But I thought maybe I 
could achieve that through the cubemap concepts. But it doesn't appear to be working
at all. '''


from ursina import *
from panda3d.core import TextureStage, TexGenAttrib

app = Ursina()

# Create entities
main_cube = Entity(model="cube", collider="mesh", color=color.red, texture="white_cube")
large_cube = Entity(model="cube", scale=10, position=(5, 1, 17), texture="white_cube")
camera_cube = Entity(model="cube", position=camera.position)

# Create a task to create the cube map after the first frame
def create_cube_map(task):
    base.saveCubeMap('skybox_map#.jpg', size=1024)
    skybox = Sky()
    skybox.texture = loader.loadCubeMap('skybox_map#.jpg')
    return task.done  # This ends the task after it's run once

# Schedule the task to run after the first frame
taskMgr.doMethodLater(0, create_cube_map, 'Create Cube Map')

EditorCamera()
app.run()
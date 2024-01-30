# Import necessary modules
from ursina import *
from panda3d.core import TextureStage
from panda3d.core import TexGenAttrib
from panda3d.core import Camera, MouseWatcher

# Initialize Ursina application
app = Ursina()
window.vsync = False  # Disable vertical sync

# Create entities
main_cube = Entity(model="cube", collider="mesh", color=color.red, texture="white_cube")
large_cube = Entity(model="cube", scale=10, position=(5, 1, 17), texture="white_cube")
camera_cube = Entity(model="cube", position=camera.position)
Sky()

# Create cube maps for entities
base.saveCubeMap('sphere_map#.jpg', size=512)  # Save a cube map image
camera_cube.model.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)  # Set texture generation
camera_cube.model.setTexture(loader.loadCubeMap("sphere_map#.jpg"), 1)  # Load the cube map

original_camera_position = camera.position

# Set the camera position to the main_cube's position and save a cube map image
camera.position = main_cube.position
base.saveCubeMap("cube_map_img#.jpg", size=512)

# Set texture generation and load the cube map for the 'main_cube' entity
large_cube.model.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyeCubeMap)
large_cube.model.setTexture(loader.loadCubeMap("cube_map_img#.jpg"), 1)

# Restore the original camera position
camera.position = original_camera_position

EditorCamera()


app.run()


from print_tricks import pt
from ursina import *
from panda3d.core import Camera, MouseWatcher

app = Ursina()
camera.fov=90
pt(camera.fov)
pt(app.camLens.getFov())
window.vsync = False  # Disable vertical sync

main_cube = Entity(model="cube", collider="mesh", color=color.red, texture="white_cube")
large_cube = Entity(model="cube", scale=10, position=(5, 1, 17), texture="white_cube")
camera_cube = Entity(model="cube", position=camera.position)
Sky()


# Create secondary render node and display regions
# scene_node_2 = scene.attachNewNode("sceneNode2")
right_display_region = app.camNode.getDisplayRegion(0)
right_display_region.setDimensions(0.1, 1, 0, 1)
window = right_display_region.getWindow()
left_display_region = window.makeDisplayRegion(0.4, 0.6, 0.8, 1)

# Create secondary camera
camera_node_2 = Camera('CameraNode2')
camera_2 = scene.attachNewNode(camera_node_2)

# Set the secondary camera's position and rotation
camera_2.setPos(camera.getPos() + Vec3(-1, -22, 1))
camera_2.setHpr(Vec3(11,33,0))
camera_2.reparent_to(camera)


# Set the camera for the display region 'left_display_region' to the secondary camera
left_display_region.setCamera(camera_2)


# Create a new mouse watcher and attach it to the parent of the base mouse watcher
custom_mouse_watcher = MouseWatcher()
app.mouseWatcher.getParent().attachNewNode(custom_mouse_watcher)

# Set t
# he FOV of the secondary camera to match the main camera
main_camera_fov = app.camLens.getFov()
camera_2_fov = camera_node_2.getLens().getFov()
pt(main_camera_fov, camera_2_fov)
# camera_node_2.getLens().setFov(main_camera_fov)

# Initialize EditorCamera
EditorCamera()

aspect_ratio = window.size[0] / window.size[1]  # Get the aspect ratio of the window
pt(aspect_ratio)
fov = app.camLens.getFov()  # Get the current field of view
new_fov = (fov[0], fov[0] / aspect_ratio)  # Calculate the new field of view
pt(fov, new_fov)
app.camLens.setFov(new_fov)  # Set the new field of view
# Run the Ursina application
app.run()







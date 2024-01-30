from print_tricks import pt
from ursina import *
from panda3d.core import Camera

app = Ursina()

main_cube = Entity(model="cube", collider="mesh", color=color.red, texture="white_cube")
Sky()


## Ursina's main display region. 
main_display_region = app.camNode.getDisplayRegion(0)
main_display_region.setDimensions(0, 1, 0, 1)
window = main_display_region.getWindow()

## secondary display region & camera
camera_node_2 = Camera('camera node 2')
camera_2 = scene.attachNewNode(camera_node_2)

left_display_region = window.makeDisplayRegion(0.4, 0.6, 0.75, 0.95)
left_display_region.setCamera(camera_2)

camera_2.setPos(camera.getPos() + Vec3(-1, -22, 1))
camera_2.setHpr(Vec3(11,33,0))
camera_2.reparent_to(camera)

EditorCamera()

app.run()







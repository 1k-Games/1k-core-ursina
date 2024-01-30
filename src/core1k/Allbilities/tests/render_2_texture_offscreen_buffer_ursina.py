from print_tricks import pt
from ursina import *

app = Ursina()
mirror_camera_pos = (0, 0, 0)
debug_camera_position = False

mirror_buffer = app.win.makeTextureBuffer("mirror buffer", 512, 512)
mirror_render = NodePath("mirror render")
mirror_render.reparentTo(scene)

mirror_camera = app.makeCamera(mirror_buffer)
mirror_camera.node().getLens().setFov(90)
mirror_camera.reparentTo(mirror_render)
mirror_camera.setPos(mirror_camera_pos)
mirror_camera.lookAt(0, 0, -4)

sky = Sky()
sky.reparentTo(mirror_render)
sphere = Entity(model='sphere', color=color.red, texture='brick',
                position=mirror_camera_pos + (0, 0, -4),
                parent=mirror_render
                )
sphere.animate_rotation((330, 440, 550), duration=4, loop=True, curve=curve.linear)

mirror = Entity(model='quad', scale=10, position=(0, 0, 0))
mirror.texture = Texture(mirror_buffer.getTexture())


if debug_camera_position == True:
    mirror_cam_visual = app.loader.loadModel('models/box')
    mirror_cam_visual.setPos(mirror_camera_pos)
    mirror_cam_visual.reparentTo(scene)
    
EditorCamera(position=(-2, 3, -10), rotation=(11,22,0))

app.run()
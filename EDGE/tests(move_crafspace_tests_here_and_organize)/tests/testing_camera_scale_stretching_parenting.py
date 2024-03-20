

#########################
# sucess
# Any combo of parents & positions
# 
#########################
from ursina import *
app = Ursina()
camera.fov = 100

square_cube = Entity(scale=3, model='cube', z=10, color=color.red)
stretched   = Entity(scale=(1,333,1), model='sphere', z=20, color=color.blue)
Sphere      = Entity(scale=1, model='sphere', z=41, color=color.yellow)
cam_mount   = Entity(scale=1, world_scale=1, model=Cone())

camera.world_position = stretched.world_position
camera.parent = scene
camera.look_at(square_cube)

# Save the rotation and scale
rotation = camera.rotation
scale = camera.world_scale

# Set the parent to stretched and apply the saved rotation and scale
camera.parent = stretched
camera.rotation = rotation
camera.world_scale = scale

app.run()


#########################
# sucCess
# Any combo of parents & positions
# 
#########################
from ursina import *
app = Ursina()

square_cube = Entity(scale=(1,1,1), model='cube', z=-10, color=color.red)
stretched   = Entity(scale=(1,3,1), model='sphere', color=color.blue)
cam_mount   = Entity(scale=1, world_scale=1)
camera.parent = cam_mount
cam_mount.parent = stretched
cam_mount.world_position=stretched.world_position
# camera.world_scale = 1

EditorCamera()
app.run()


#########################
# Success
# Camera.parent = Stretched, 
# Got rid of world_scale!!!
#########################
from ursina import *
app = Ursina()

square_cube = Entity(scale=(1,1,1), model='cube', z=-10, color=color.red)
stretched   = Entity(scale=(1,3,1), model='sphere', color=color.blue)
cam_mount   = Entity(scale=1, world_scale=1)
camera.parent = stretched
# camera.world_scale = 1

EditorCamera()
app.run()

#########################
# FAILS
# Camera.parent = Stretched 
#
#########################
from ursina import *
app = Ursina()

square_cube = Entity(scale=(1,1,1), model='cube', z=-10, color=color.red)
stretched   = Entity(scale=(1,3,1), model='sphere', color=color.blue)
cam_mount = Entity(scale=1, world_scale=1)
camera.parent = stretched
camera.world_scale = 1

EditorCamera()
app.run()





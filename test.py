from ursina import *


class RotatingEntity(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = 100

    def update(self):
        if held_keys['right mouse down']:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity
            self.rotation_x += mouse.velocity[1] * self.mouse_sensitivity


app = Ursina()

rotating_entity = RotatingEntity(model='cube', color=color.orange, scale=(1, 1, 1))

app.run()


from ursina import *

app = Ursina()

# Create a draggable entity
entity = Draggable()
entity.model = 'cube'
entity.texture = 'white_cube'
entity.scale = Vec3(1,1,1)

def update():
    
    ## Rotations
    if held_keys['right mouse down']:
        
        entity.rotation_y += mouse.velocity[0] * 20
        entity.rotation_x += mouse.velocity[1] * 20
        
    if held_keys['middle mouse down']:
        entity.rotation_z += mouse.velocity[0] * 20
        
    if held_keys['w']:
        entity.rotation_x += time.dt * 100
    if held_keys['s']:
        entity.rotation_x -= time.dt * 100
    if held_keys['a']:
        entity.rotation_y += time.dt * 100
    if held_keys['d']:
        entity.rotation_y-= time.dt * 100
    if held_keys['e']:
        entity.rotation_z += time.dt * 100
    if held_keys['q']:
        entity.rotation_z -= time.dt * 100

    ## Scale
    if held_keys['up arrow']:
        entity.scale += Vec3(time.dt, time.dt, time.dt)
    if held_keys['down arrow']:
        entity.scale -= Vec3(time.dt, time.dt, time.dt)
        
    ## Texture Scale

app.run()
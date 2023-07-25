from ursina import *

class ThirdPersonController(Entity):
    def __init__(self, height=2, speed=2, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.speed = speed

        self.model = "cube"
        self.color = color.red

        camera.parent = self
        camera.fov = 90
        camera.y = 1.25
        camera.z = -3.25

    def update(self):
        self.rotation_y += ((held_keys['d'] - held_keys['a']) or held_keys['gamepad left stick x'])

        self.direction = Vec3(
            self.forward * ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
            ).normalized()
        move_amount = self.direction * time.dt * self.speed
        self.position += move_amount

        

    def input(self, key):
        ...
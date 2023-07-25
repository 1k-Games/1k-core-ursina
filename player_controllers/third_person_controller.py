from ursina import *

class ThirdPersonController(Entity):
    def __init__(self, height=2, speed=2, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.speed = speed

        self.model = "cube"
        self.color = color.red

        self.mouse_sensitivity = Vec2(40, 40)

        camera.parent = self
        camera.fov = 90
        camera.y = 1.25
        camera.z = -3.25

        mouse.locked = True

    def update(self):
        direction = ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
        rotation = ((held_keys['d'] - held_keys['a']) or held_keys['gamepad left stick x'])
        
        self.rotation_y += rotation
        self.direction = Vec3(
            self.forward * direction
            ).normalized()
        move_amount = self.direction * time.dt * self.speed
        self.position += move_amount

        if held_keys['right mouse']:
            camera.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        if not held_keys['right mouse'] and self.direction != self.forward:
            camera.rotation = lerp(camera.rotation, self.forward, 1 * time.dt)

    def input(self, key):
        ...



if __name__ == '__main__':
    app = Ursina()
    ThirdPersonController()
    Entity(model='cube', x=3, z=2)
    Sky()
    app.run()
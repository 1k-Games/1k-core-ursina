from ursina import *

class FreeCameraController(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera_pivot = Entity(parent=self)
        self.mouse_sensitivity = Vec2(40, 40)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90

        mouse.locked = True
    
    def input(self, key):
        if key == 'tab':
            mouse.locked = not mouse.locked

            if mouse.locked:
                mouse.position = Vec3(0,0,0)

    def update(self):
        if mouse.locked:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

            self.direction = Vec3(
                self.forward * ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
                + self.right * ((held_keys['d'] - held_keys['a']) or held_keys['gamepad left stick x'])
                ).normalized()

            self.position += self.direction * time.dt

            if held_keys['q']:
                self.y += time.dt

            if held_keys['e']:
                self.y -= time.dt

if __name__ == '__main__':
    app = Ursina()
    Sky()

    FreeCameraController()
    Entity(model='cube', color=color.blue, scale=(1,1,1), x=3, y=0, z=3)

    app.run()
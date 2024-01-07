from ursina import *

class SideScrollingFreeController(Entity):
    def __init__(self):
        super().__init__()

        self.mouse_sensitivity = Vec2(20, 20)
        camera.parent = self

        self.mouse_position = mouse.position

    # TODO: "Lock" mouse but allow for infinite scrolling 
    #       if it hits edge of screen and stops, this resets the
    def update(self):
        if held_keys['right mouse']:
            self.x += mouse.velocity[0] * self.mouse_sensitivity[0]

    def input(self, key):
        if key == 'right mouse down':
            self.mouse_position = mouse.position
            mouse.visible = False

        if key == 'right mouse up':
            mouse.position = self.mouse_position
            mouse.visible = True


if __name__ == '__main__':
    app = Ursina( 
        size=(1200,800), 
        vsync=False
    )

    Entity(model='cube', z=3, x=0.5)
    SideScrollingFreeController()

    app.run()


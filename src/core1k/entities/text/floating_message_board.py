from ursina import *

class FloatingMessageBoard(Entity):
    def __init__(self, text='Placeholder Text!', panel_color=color.white, alpha=1, font_scale=2, text_origin=(0, 0), **kwargs):
        super().__init__(**kwargs)

        panel = Entity(model='quad', color=panel_color, alpha=alpha, scale=self.scale, rotation=self.rotation, position=self.position)
        text  = Text(parent=panel, text=text, color=panel_color.invert(), z=-0.1, origin=text_origin, scale=font_scale)

# TODO: Include a way to move around
if __name__ == '__main__':
    app=Ursina(size=(1200, 800), fullscreen=False)
    board = FloatingMessageBoard(text='Hello', panel_color=color.white, alpha=1, font_scale=5)
    board.z = 15

    camera.z = -5

    app.run()
from print_tricks import pt
from ursina import *
from game_manager import GameManager

app = Ursina(
    size=(1280, 720),
    # borderless=False,
    # fullscreen=True,
    # development_mode=False
    )
window.position=(360,0)

GameManager(app)

app.run()



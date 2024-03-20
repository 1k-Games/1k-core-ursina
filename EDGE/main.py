from print_tricks import pt
from ursina import *
from zac.zac import zac
if __name__ == "__main__":
    app = Ursina()

    game_menu = GameMenu() 

    EditorCamera()

    app.run()
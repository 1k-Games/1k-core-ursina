from print_tricks import pt
# pt.easy_imports('main.py')

from ursina import *
from engine.zac.zac import Zac

if __name__ == "__main__":
    app = Ursina()

    Zac() 

    EditorCamera()

    app.run()
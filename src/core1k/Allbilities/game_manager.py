from ursina import *
from print_tricks import pt

print('-----------Game Manager-----------')
class GameManager(Entity):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.ignore_paused = True
        
        import test_combilities 
        
        test_combilities.test_combilities(app)


    def update(self):
        ...

    def input(self, key):
        ...
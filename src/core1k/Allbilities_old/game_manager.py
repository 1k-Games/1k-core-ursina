from ursina import *
from print_tricks import pt
from levels import testing_range_city as testing_range
import test_combilities 

print('-----------Game Manager-----------')
class GameManager(Entity):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.ignore_paused = True
        
        level = testing_range.BuildLevel()
        test_combilities.test_combilities(app, level)    
        
    def update(self):
        ...

    def input(self, key):
        ...
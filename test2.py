
from ursina import *

from print_tricks import pt 

class PauseMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pt('---init---')
        cb = Entity(model='cube', parent=self)
        self.enabled = False
    def on_enable(self):
        pt('---on enable---')
    def on_disable(self):
        pt('---on disable---')


    
class Dev_Pause_Menu(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pause_menu = PauseMenu(add_to_scene_entities=False, enabled=False)
        
    def input(self, key):
        if key == 'escape':
            self.pause_menu.enabled = not self.pause_menu.enabled
            
if __name__ == '__main__':
    app = Ursina(size=(1920,1080))
    Dev_Pause_Menu()
    app.run()
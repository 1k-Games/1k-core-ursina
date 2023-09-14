from print_tricks import pt

from ursina import *

class Second(Entity):
    def __init__(self, **kwargs):
        super().__init__(add_to_scene_entities=False, **kwargs)
        
        print('---init---')
        
    def on_enable(self):
        print('---on enable---')
        print()
    def on_disable(self):
        print('---on disable---- ')

class First(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.second = Second(
            enabled=False
        )


app=Ursina(size=(1920,1080))

First()
# print(scene.entities)
app.run()





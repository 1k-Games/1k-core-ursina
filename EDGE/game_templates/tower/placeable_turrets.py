from print_tricks import pt
pt.easy_imports('main.py')

from ursina import *

from engine.aura.aura import Aura
from engine.ai.enemy import enemies

'''
    - Aura's that use CCAUS devices

    '''
pt.c('placeable_turrets.py')


from ursina import *
from engine.ai.enemy import Enemy_2d


class Placeable_Turret(Entity):
    def __init__(self, name='', aura=None, position=Vec3(0,0,0), **kwargs):
        super().__init__(position=position, model="cube", color=color.blue, **kwargs)
        # self.ccaus = CCAUS(range=5)
        # self.range = self.ccaus.range
        
        if aura:
            self.position = aura.position
        else:
            self.aura = Aura(name=name)
            self.aura.add_entity(self)

    def update(self):
        # Assuming a global list of enemies for simplicity
        global enemies
        self.detect_and_fire(self.position, enemies)
        
    
    def detect_and_fire(self, position, enemies):
        for enemy in enemies:
            if distance(position, enemy.position) <= self.range:
                print(f"Firing at {enemy}")
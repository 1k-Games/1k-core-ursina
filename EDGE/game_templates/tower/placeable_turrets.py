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
        self.range = 2
        self.ai_reaction_time = 0.33 ## The ai's reaction time. 
        self.ai_last_trigger_time = 0.0
        
        if aura:
            self.position = aura.position
        else:
            self.aura = Aura(name=name)
            self.aura.add_entity(self)
            
        

    def update(self):
        if time.time() - self.ai_last_trigger_time >= self.ai_reaction_time:
            global enemies
            self.detect_and_fire(self.position, enemies)
            
            self.ai_last_trigger_time = time.time()

    def detect_and_fire(self, position, enemies):
        for enemy in enemies:
            if distance(position, enemy.position) <= self.range:
                print(f"Firing at {enemy.name}")
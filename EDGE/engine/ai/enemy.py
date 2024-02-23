from print_tricks import pt
pt.easy_imports('main.py')

from ursina import *
from ursina import curve

from engine.aura.aura import Aura

enemies = []


class Enemy_2d(Entity):
    def __init__(self, name='', aura: Aura=None, start_position=Vec3(0,0,0), **kwargs):
        super().__init__(model="cube", color=color.red, scale=1, visible=False, position=start_position, **kwargs)
        
        ###################################
        ## AURA Integration
        ###################################
        if aura:
            self.position = aura.position
        else:
            self.aura = Aura(name=name)
            self.aura.add_entity(self)
            
    def go(self, pos, duration):
        self.animate('position', pos, duration=duration, curve=curve.linear)

    def move(self, world_positions):
        if len(world_positions) < 3:
            print("Need at least 3 points to move between averages.")
            return

        self.position = world_positions[0]
        self.visible = True
        counter = 0
        duration = 0.04

        for i in range(1, len(world_positions) - 1):
            avg_position = (world_positions[i-1] + world_positions[i] + world_positions[i+1]) / 3
            counter += duration
            invoke(self.go, avg_position, duration=duration, delay=counter)


# enemy = Entity(model="cube", color=color.red, scale=1, visible = False)

# def go(enemy, pos, duration):
#     enemy.animate('position', pos, duration=duration, curve=curve.linear)
#     # pt(pos)
    
# def move(world_positions):
#     if len(world_positions) < 3:  # Ensure there are at least 3 points
#         print("Need at least 3 points to move between averages.")
#         return

#     enemy.position = world_positions[0]  # Start at the first position
#     enemy.visible = True
#     counter = 0
#     duration = 0.04

#     # Start from the second position since we're averaging with the previous and next
#     for i in range(1, len(world_positions) - 1):
#         # Calculate the average of the previous, current, and next positions
#         avg_position = (world_positions[i-1] + world_positions[i] + world_positions[i+1]) / 3
#         counter += duration
#         invoke(go, enemy, avg_position, duration=duration, delay=counter)



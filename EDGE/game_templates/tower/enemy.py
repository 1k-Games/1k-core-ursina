from print_tricks import pt
from ursina import *
from ursina import curve

path = []

enemy = Entity(model="sphere", color=color.red, scale=2, visible = False)

def go(enemy, pos, duration):
    enemy.animate('position', pos, duration=duration, curve=curve.linear)
    pt(pos)
    
def move(world_positions):
    pt(world_positions)
    enemy.position = world_positions[0]
    enemy.visible = True
    counter = 0
    duration = 0.7
    for position in world_positions:
        counter += duration
        invoke(go, enemy, position, duration=duration, delay=counter)



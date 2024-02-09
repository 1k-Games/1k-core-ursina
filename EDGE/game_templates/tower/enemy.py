from ursina import *
from ursina import curve

path = []

enemy = Entity(model="sphere", color=color.red, scale=.5, visible = False)

def go(enemy, pos, duration):
    enemy.animate('position', (pos[0], .1, pos[2]), duration=duration, curve = curve.linear)

def move(path_locations_ordered):
    enemy.position = path_locations_ordered[0]
    enemy.visible = True
    counter = 0
    for location in path_locations_ordered:
        invoke(go, enemy, location, duration=2, delay=counter)
        counter += 2



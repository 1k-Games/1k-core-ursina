from ursina import *
from ursina import curve

path = []

enemy = Entity(model="sphere", color=color.red, scale=.5, visible = False)

def go(enemy, pos, delay):
    enemy.animate('position', (pos[0], .1, pos[2]), duration = 2, curve = curve.linear)

def move(path):
    enemy.position = path[0].position
    enemy.visible = True
    counter = 0
    for cube in path:
        invoke(go, enemy, cube.position, counter, delay = counter)
        counter += 2



from ursina import *
from random import randint

app = Ursina()

player = Entity(model='cube', color=color.white, scale=(1, 1, 1), position=(0, 0, 0))
camera.parent = player
camera.position = (0, 0, -10)

def reset_scene():
    player.position = (0, 0, 0)
    for entity in scene.entities:
        if entity != player:
            entity.position = (randint(-10, 10), randint(-10, 10), randint(-10, 10))

def update():
    player.position += held_keys['w'] * time.dt * Vec3(0, 0, 1)
    player.rotation_y += held_keys['a'] * time.dt * -100
    player.rotation_y += held_keys['d'] * time.dt * 100

    if player.position > 20:
        reset_scene()

for i in range(10):
    Entity(model='sphere', color=color.random_color(), scale=(1, 1, 1), position=(randint(-10, 10), randint(-10, 10), randint(-10, 10)))

app.run()


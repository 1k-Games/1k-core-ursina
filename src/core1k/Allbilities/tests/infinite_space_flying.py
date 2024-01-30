import time
from ursina import *
from print_tricks import pt
app = Ursina()

# Load spaceship model and texture
spaceship = Entity(model='cube', texture='white_cube', scale=(1, 0.5, 2))

# Set up basic controls for movement
def input(key):
    if key == 'w':
        spaceship.z += 100
    elif key == 's':
        spaceship.z -= 100
    elif key == 'a':
        spaceship.x -= 100
    elif key == 'd':
        spaceship.x += 100
    elif key == 'space':
        spaceship.y += 100
    elif key == 'left shift' or key == 'right shift':
        spaceship.y -= 100

global start_time
start_time = time.time()
def update():
    global start_time
    if time.time() - start_time > 1:
        start_time = time.time()
        pt(spaceship.position, spaceship.world_position)

# Create a simple skybox and ground
sky = Sky()
ground = Entity(model='plane', scale=(100, 1, 100), texture='white_cube', color=color.green)

app.run()

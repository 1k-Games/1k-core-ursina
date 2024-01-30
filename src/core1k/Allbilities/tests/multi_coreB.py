from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from multiprocessing import Process, Queue
import time

app = Ursina()

# Create a ground plane
ground = Entity(model='plane', scale=(100, 1, 100), texture='white_cube', collider='box')
ground.texture_scale = (50, 50)

# Create a target cube
cube = Entity(model='cube', position=(5, 1, 5), texture='white_cube', collider='box')
cube.model.generate()
# Create a first-person controller
player = FirstPersonController()

# Function to move the target cube
def move_cube(cube_queue, player_queue):
    while True:
        cube_position = cube_queue.get()
        player_position = player_queue.get()
        cube.x = cube_position[0]
        cube.z = cube_position[1]
        player.x = player_position[0]
        player.z = player_position[1]
        time.sleep(0.01)

# Create queues for communication
cube_queue = Queue()
player_queue = Queue()

# Create a process to move the target cube
cube_process = Process(target=move_cube, args=(cube_queue, player_queue))
cube_process.start()

def update():
    cube_queue.put((cube.x + 0.01, cube.z + 0.01))
    player_queue.put((player.x, player.z))

# Run the game
app.run()

# Terminate the cube process when the game ends
cube_process.terminate()
cube_process.join()
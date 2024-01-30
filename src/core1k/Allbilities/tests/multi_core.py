from multiprocessing import Process, Queue
from ursina import *
import time
from print_tricks import pt 
def player_process(queue_to_ground, queue_from_ground):
    player = Entity(model='cube', color=color.orange, scale_y=2)

    while True:
        # player.x += held_keys['d'] * .1
        # player.x -= held_keys['a'] * .1
        player.x += .1 * time.dt
        print('python: player.x: ', player.x)
        queue_to_ground.put(player.position)
        if not queue_from_ground.empty():
            ground_vertices = queue_from_ground.get()
            print(f'inside_player_process: Ground vertices: {ground_vertices}')

        time.sleep(1)

def ground_process(queue_from_player, queue_to_ground):
    ground = Entity(model='plane', color=color.magenta, z=-.1, y=-3, origin=(0, .5), scale=(50, 1, 10), collider='box')
    # print(ground.model.vertices)
    # print(type(ground.model.vertices))
    # print(ground.model)
    # pt(ground.model.vertices)

    inc = 1
    while True:
        ground.model.vertices[0] += Vec3(0.5, 0, 0.5) * time.dt
        g = ground.model.vertices
        print('python: ground', ground.model.vertices)
        if not queue_from_player.empty():
            player_position = queue_from_player.get()
            print(f'inside_ground_process: player position: {player_position}')

        queue_to_ground.put(ground.model.vertices)
        time.sleep(1)

if __name__ == '__main__':
    queue_to_ground = Queue()
    queue_from_ground = Queue()

    player_p = Process(target=player_process, args=(queue_to_ground, queue_from_ground))
    ground_p = Process(target=ground_process, args=(queue_to_ground, queue_from_ground))

    player_p.start()
    ground_p.start()

    player_p.join()
    ground_p.join()
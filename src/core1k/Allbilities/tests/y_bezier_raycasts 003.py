''' bezier raycasts 002'''
'''TODO in here, (then place in abilities_working_on.py and then abilities.py):
- Get boomerang (dash point) to be at maximum_length when activated but not touching anything
- Set distance of dash point to interception point (just like placing the boomerang at the hit point, we are also making the visual dash_arc stop/calculate at that same position as where the boomerang lands)
- How to allow dash to curve so we can jump on top of surfaces above us? 
    - Create some new walls to test the curving and the hit detection/distance. 

'''
from ursina import *
from panda3d import core
from print_tricks import pt
from mp_linecast import linecast
app = Ursina()

player_scale = 7
length = 100
player = Entity(model = 'cube', color = color.yellow, scale = player_scale)

bezier = curve.CubicBezier(0,0,0,1)
verts = [Vec3(bezier.calculate(i/30), 0, i/30) for i in range(31)]
dash_arc = Entity(
    model=Mesh(vertices=verts, mode='line', thickness=5.5),
    color = color.yellow, visible = False,
    parent = player,
    scale = length / player_scale,
    # scale = length,
    )

wall = Entity(model = 'cube', scale = (2, 10, 55), position = (44, 0, 3), collider = 'box')
wall2 = duplicate(wall, position = (63, 0, 15))

boomerang = Entity(model='cube', color=color.orange, 
    # parent = player,
    # scale=(.5, .5, .5),
    scale=(4, 4, 4),
    # position = (-9,-9,-9),
    position = verts[-1] * length / player_scale,
    )
def ray(origin, destination):
    dash_ray = linecast(
    origin, destination,
    ignore = [player, boomerang, dash_arc, camera, ],
    debug = True
    )
    return dash_ray

global counter; counter = 0
global hit_once; hit_once = False
global dash_ray2; dash_ray2 = None
def start_ray():
    global counter
    global hit_once
    global dash_ray2

    nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[2])
    nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[8])
    nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
    nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])

    if counter == 0:
        dash_ray = ray(player.world_position, nvA)
        counter +=1
    elif counter == 1:
        dash_ray = ray(nvA, nvB)
        counter += 1
    elif counter == 2:
        dash_ray = ray(nvB, nvC)
        counter += 1
    elif counter == 3:
        dash_ray = ray(nvC, nvD)
        counter = 0

    if dash_ray.world_point is not None:
        # pt(1, boomerang.world_position, dash_ray.world_point)
        dash_ray2 = dash_ray
        # pt(1, dash_ray2)
        hit_once = True 
    if counter == 3:
        if hit_once:
            dash_arc.color = color.blue
            dash_dest = dash_ray.world_point
            # pt(2, boomerang.world_position, dash_ray2.world_point)
            boomerang.visible = True
            boomerang.world_position = dash_ray2.world_point
            hit_once = False 
            
        elif hit_once == False:
            dash_arc.color = color.red
            boomerang



def update():
    if held_keys['space']:
        dash_arc.visible = True
        start_ray()
    else:
        dash_arc.visible = False

def input(key):

    if key == 'space up':
        boomerang.visible = False
    if key == 'o':
        wall.z += 1
        pt(wall.position)
    if key == 'l':
        wall.z -= 1
        pt(wall.position)
    if key == 'i':
        wall.x += 1
        pt(wall.position)
    if key == 'k':
        wall.x -= 1
        pt(wall.position)
    if key == 'w':
        player.z +=2
    if key == 's':
        player.z -= 2
    if key == 'a': 
        player.x -= 2
    if key == 'd':
        player.x += 2
    if key == 'left arrow':
        player.rotation_y -= 2
    if key == 'right arrow':
        player.rotation_y += 2
    if key == 'page up':
        player.rotation_x += 2
    if key == 'page down':
        player.rotation_x -= 2

    if key == 'up arrow':
        player.rotation_z += 2
    if key == 'down arrow':
        player.rotation_z -= 2


EditorCamera(position = (100, 725, 100), rotation = (90, 0, 0), move_speed = 1000)
app.run()
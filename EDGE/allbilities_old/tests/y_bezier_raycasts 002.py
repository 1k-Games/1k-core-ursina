from ursina import *
from panda3d import getRelativePoint
from print_tricks import pt
from mp_linecast import linecast
app = Ursina()

player_scale = 7
default_length = 100
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

wall = Entity(
    model = 'cube', scale = (2, 10, 55),
    position = (44, 0, 3),
    collider = 'box')

boomerang = Entity(model='cube', color=color.azure, 
    scale=(.5, .5, .5),
    parent = player,
    # position = (-9,-9,-9),
    position = verts[-1] * length / player_scale,
    )

def start_ray(origin, destination):
    # global dash_arc
    # global counter
    # hit = False
    dash_ray = linecast(
        origin, destination,
        ignore = [player, boomerang, dash_arc, camera, ],
        debug = True
        )
    
    if dash_ray.hit:
        pt('hit')
        # hit = True
        return dash_ray, True
    else:
        hit = False
        return dash_ray, False

global counter; counter = 0
global hit_once; hit_once = False
def update():
    global counter
    global hit_once
    
    if held_keys['space']:    
        nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[2])
        nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[8])
        nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
        nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])
        
        if counter == 0:
            # dash_ray, was_hit = start_ray(player.world_position, nv[2] * length + pw)
            dash_ray, was_hit = start_ray(player.world_position, nvA)
            counter +=1
        elif counter == 1:
            # dash_ray, was_hit = start_ray(nv[2] * length + pw , nv[8] * length + pw)
            dash_ray, was_hit = start_ray(nvA, nvB)
            counter += 1
        elif counter == 2:
            # dash_ray, was_hit = start_ray(nv[8] * length + pw , nv[18] * length + pw)
            dash_ray, was_hit = start_ray(nvB, nvC)
            counter += 1
        elif counter == 3:
            # dash_ray, was_hit = start_ray(nv[18] * length + pw ,  nv[-1] * length + pw)
            # dash_ray, was_hit = start_ray(nvC, boomerang.model.world_position)
            dash_ray, was_hit = start_ray(nvC, nvD)
            counter = 0
        
        if was_hit == True:
            hit_once = True 
            
        if counter == 3:
            if hit_once:
                dash_arc.color = color.blue
                dash_dest = dash_ray.world_point
                boomerang.position = dash_ray.world_point
                hit_once = False 
            elif hit_once == False:
                dash_arc.color = color.red
        
    if held_keys['1']:
        dash_arc.visible = True 
    else:
        dash_arc.visible = False

def input(key):

    if key == 'space up':
        boomerang.position = player.position
        dash_arc.color = color.yellow
    if key == 'r':
        boomerang.position = (0,0,0)
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

        # this_verts = dash_arc.model.vertices
        # pt(this_verts)
        # gg = dash_arc.getRelativePoint(scene, dash_arc.model.vertices[-1])
        # pt(gg)

    if key == 'up arrow':
        player.rotation_z += 2
    if key == 'down arrow':
        player.rotation_z -= 2


EditorCamera(position = (100, 725, 100), rotation = (90, 0, 0), move_speed = 1000)
app.run()
''' bezier raycasts 003'''
'''TODO in here, (then place in abilities_working_on.py and then abilities.py):
- How to allow dash to curve so we can jump on top of surfaces above us? 
    - Create some new walls to test the curving and the hit detection/distance. 
- Hyperdash alternative verion, hyperdash style:
    - ray cast aimed above player pointer (helps to obscure that this in't actually an arc, but is faked)
    - If hit wall, shoot raycast down. Hit position is jump position. 
    - if not hit wall, but hits max range for that gun angle, do same as above (shoot ray down etc)
- Turn this into a class, so it's easier for me to integrate it into the abilities. 
- Separate out the arc that controls thing from the visual arc. 
    (Right now, I have the visual real arc that controls the rays. The problem is when I shrink the arc,
    it screws up the other calculations.)
    - So I need to make the real arc stay the same size, and it can only
    be visual when debugging. 
    - Visual arc changes size when the rays get the interception point. 
- Set distance of dash point to interception point (just like placing the boomerang at the hit point, we are also making the visual dash_arc stop/calculate at that same position as where the boomerang lands)
- Make a perfectly accurate final collision ray point:
    - If any of the main rays hit, Take the closest vertice on the main arc that is closest to this ray hit point, and actually place the boomerang on that point!!!
    - It prob makes sense to convert the hit point vertice to a relative point in relation to the dash arc or player... That way we are only converting one thing, and then can easily take that point and do a distance check against all of the points of the arc to see which is closest to it.
    - Extended: when find the point it should be at, cast a raycast on the previous point, the the next main point (so it's like a last, final raycast to confirm)
    - Alt: make a new ray cast that is cast just behind where the point hit, instead of calculating at all?

- REDO THEORY:
    Goals:
        - project an arc into the world at __ length. 
        - Arc changes length & end point dynamically based on what it contacts. 
        - You move to the contact point.
        
    Debate How to:
        - If I parent to player, and have it generate point from player perspective, 
        then I don't have to re-calculate the size of the dash everytime it doesn't hit something. 
        - BUT... I have to regenerate points anyways, literally everytime it'll contact anything else
            AND, it'll take more resources to convert. 
        
    How to: conclusion:
        - Generate ARC in real-world coordinates
        - Get the coordinate of the player and make that the first point. 
        - Get the coordinate of max length or the coordinate of the hit point, and make that the end point. Boom. 
'''
import math
from ursina import *
from panda3d import core
from print_tricks import pt
from mp_linecast import linecast
app = Ursina()

temp_delete_object = Entity(model = 'sphere', color = color.black, 
    scale = 6, position = (-10, -10, -10))

player_scale = 7
length = 100
player = Entity(model = 'cube', color = color.yellow, scale = player_scale)

bezier = curve.CubicBezier(0,0,1,0)
verts = [Vec3(bezier.calculate(i/30), 0, i/30) for i in range(31)]
# pt(verts)
verts2 = []
for count, vert in enumerate(verts):
    # i = verts[i]
    x = vert[0] * 14
    z = vert[2] * 14
    xyz = Vec3(x, vert[1], z)
    verts2.append(xyz)
verts = verts2 
# pt(verts)
dash_arc = Entity(
    model=Mesh(vertices=verts, mode='line', thickness=2),
    color = color.yellow, visible = True,
    parent = player,
    # scale = length / player_scale,
    # scale = 1
    )
dash_arc_visual = Entity(
    model=Mesh(vertices=verts2, mode='line', thickness=5.5),
    color = color.orange, visible = False,
    parent = player,
    # scale = length / player_scale,
    # scale = 1
    )

wall = Entity(model = 'cube', position = (44, 0, 43), scale = (2, 10, 55), collider = 'box')
wall2 = duplicate(wall, position = (63, 0, 66))

boomerang = Entity(model='cube', color=color.orange, 
    scale=(4, 4, 4),
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
global dash_ray_saved; dash_ray_saved = None

def start_ray(a, b, c):
    global counter
    global hit_once
    global dash_ray_saved

    # For bezier 0,0,0,1
    # nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[2])
    # nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[8])
    # nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
    # nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])
    
    # For bezier 0,0,1,0
    # nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[12])
    # nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
    # nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[27])
    # nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])
    
    # for dynamically changing postions (bezier 0,0,1,0)
    nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[a])
    nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[b])
    nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[c])
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
        counter += 1
        
    # No hits during all of the ray casts
    if counter == 4 and dash_ray.world_point is None:
        boomerang.world_position = nvD
        dash_arc_visual.color = color.red
        # dash_arc_visual.scale = length / player_scale
        if len(dash_arc_visual.model.vertices) < 31:
            dash_arc_visual.model.vertices = verts
            dash_arc_visual.model.generate()
        counter = 0

    # A hit just occured in whatever dash_ray was just sent
    if dash_ray.world_point is not None:
        boomerang.visible = True
        boomerang.world_position = dash_ray.world_point
        arc_close_points(dash_ray)
        dash_arc_visual.color = color.blue
        counter = 0


def arc_close_points(dash_ray):
    ## find the point in the vertices list that's closest to the hit point
    # localized_hit_point = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[a])
    # localized_hit_point = scene.getRelativePoint(dash_arc, dash_ray.world_point)
    localized_hit_point = dash_arc.getRelativePoint(scene, dash_ray.world_point)
    
    pt(
        dash_ray.world_point,
        localized_hit_point
        )
    temp_delete_object.world_position = localized_hit_point
    
    n=15
    
    # Make a new list of vertices cut off at the right point. Generate. 
    cut_verts = verts[:-n or None]
    dash_arc_visual.model.vertices = cut_verts
    dash_arc_visual.model.generate()
    
def start_ray_old(a, b, c):
    global counter
    global hit_once
    global dash_ray_saved

    # For bezier 0,0,0,1
    # nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[2])
    # nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[8])
    # nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
    # nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])
    
    # For bezier 0,0,1,0
    # nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[12])
    # nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[18])
    # nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[27])
    # nvD = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[-1])
    
    # for dynamically changing postions (bezier 0,0,1,0)
    nvA = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[a])
    nvB = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[b])
    nvC = scene.getRelativePoint(dash_arc, dash_arc.model.vertices[c])
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
        counter += 1
        
    # No hits during all of the ray casts
    if counter == 4 and dash_ray.world_point is None:
        boomerang.world_position = nvD
        dash_arc_visual.color = color.red
        # dash_arc_visual.scale = length / player_scale
        if len(dash_arc_visual.model.vertices) < 31:
            dash_arc_visual.model.vertices = verts
            dash_arc_visual.model.generate()
        counter = 0

    # A hit just occured in whatever dash_ray was just sent
    if dash_ray.world_point is not None:
        boomerang.visible = True
        boomerang.world_position = dash_ray.world_point
        arc_close_points(dash_ray)
        dash_arc_visual.color = color.blue
        counter = 0


global a; a = 10
global b; b = 20
global c; c = 27
def update():
    global a; global b; global c
    if held_keys['space']:
        start_ray(a, b, c)
    elif held_keys['v']:
        start_ray_old(a, b, c)

def input(key):
    global a; global b; global c
    if key == 'space' or key == 'v':
        dash_arc_visual.visible = True
        boomerang.visible = True
    if key == 'space up' or key == 'v up':
        boomerang.visible = False
        dash_arc_visual.visible = False
    
    if key == '1':
        a -= 1
    if key == '2':
        a += 1
    if key == '3':
        b -= 1
    if key == '4':
        b += 1
    if key == '5':
        c -= 1
    if key == '6':
        c += 1
    if key == 'o':
        wall.z += 8
        pt(wall.position)
    if key == 'l':
        wall.z -= 8
        pt(wall.position)
    if key == 'i':
        wall.x += 8
        pt(wall.position)
    if key == 'k':
        wall.x -= 8
        pt(wall.position)
    if key == 'w':
        player.z += 8
    if key == 's':
        player.z -= 8
    if key == 'a': 
        player.x -= 8
    if key == 'd':
        player.x += 8
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

    # pt(a, b, c)

EditorCamera(position = (55, 725, 55), rotation = (90, 0, 0), move_speed = 1000)
app.run()
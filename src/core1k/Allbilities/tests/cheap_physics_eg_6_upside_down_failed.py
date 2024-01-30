import threading
import time
import gc 
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
print(parent_dir)
print(os.getcwd())
sys.path.append(parent_dir)

from ursina import *
from ursina.shaders import lit_with_shadows_shader
# from ursina.prefabs.first_person_controller import FirstPersonController
from local_axis_first_person_controller import FirstPersonController
# from local_axis_entity import L_Entity
from print_tricks import pt

# from KahmVasTopos.KahmVasTopos import KVT

app = Ursina(vsync=False, size=(1280,720))
Entity.default_shader = lit_with_shadows_shader
global dir_light
dir_light = DirectionalLight()
dir_light.look_at(Vec3(1,-1,-1))
physics_entities = []
static_entities = []
static_ent_locations = []
static_ent_loc_set = set()
walls = []

center_parent = Entity()
class Cent(Entity):
    '''Entity subclass that is parented to the Center Entity by default. '''
    def __init__(self, parent=center_parent, **kwargs):
        super().__init__(parent=parent, **kwargs)

upside_down_scene = Entity(rotation_y=180)
ground = Entity(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
player = FirstPersonController()
ground.parent=upside_down_scene
player.parent = upside_down_scene
physics_parent = Cent()
statics_parent = Cent()
transfer_parent = Cent()

walls.append(ground)
global block_color
block_color = color.blue

def get_inst(my_class):
    all_objects = gc.get_objects()
    my_classes = []
    for obj in all_objects:
        if isinstance(obj, my_class):
            my_classes.append(obj)
    return my_classes
def check_distance(player, center):
    pt.h()
    while True:
        distance = (player.position - center).length()
        pt(ground.world_rotation)
        if distance > 2:
            pt(player.position)
        time.sleep(1)

# Create a separate thread to check the distance
thread = threading.Thread(target=check_distance, args=(player, (0,0,0)), daemon=True).start()

def stop(ent):
    ent.velocity = Vec3(0,0,0)
# camera.world_parent = upside_down_scene
def spawn_block():
    global block_color
    e = Cent(model='cube', 
            velocity=Vec3(0), 
            position=player.position+Vec3(0,1.5,0)+(camera.forward*5), 
            collider='box',
            parent = physics_parent, 
            color = block_color,
            )
    e.velocity = (camera.forward *4 + Vec3(0,1.5,0)) * 10
    physics_entities.append(e)
def input(key):
    global block_color
    # if key == 'left mouse down':
    #     spawn_block()
    if key == 'j':
        combined_statics = statics_parent.combine()
        pt(combined_statics)
    if key == 'k':
        pt(static_ent_locations)
        pt(static_ent_loc_set)
    if key == 'z':
        if block_color == color.blue:
            block_color = color.yellow
        elif block_color == color.yellow:
            block_color = color.blue
    if key == 'l':
        global dir_light
        # pt(dir_light)
        pt(dir_light.enabled)
        dir_light.disable()
        dir_light.remove()
        # dir_light.enabled = False
        # dir_light.shadows = False 
        pt(dir_light.enabled)
        
last_key_press_time = 0
def update():
    z = upside_down_scene.position.z - 1 * time.dt
    upside_down_scene.rotate((0, 0, z))
    
    global last_key_press_time
    current_time = time.time()
    if held_keys['left mouse'] and current_time - last_key_press_time >= 0.1:
        spawn_block()
        last_key_press_time = current_time
    for e in physics_entities:
        if e.intersects():
            # stop(e)
            e.velocity = Vec3(0,0,0)
            physics_entities.remove(e)
            e.parent = statics_parent
            static_entities.append(e)
            static_ent_locations.append(e.position)
            ex = int(round(e.position.x))
            ey = int(round(e.position.y))
            ez = int(round(e.position.z))
            static_ent_loc_set.add((ex, ey, ez))
            
            
        e.velocity = lerp(e.velocity, Vec3(0), time.dt)
        e.velocity += Vec3(0,-1,0) * time.dt * 5
        e.position += (e.velocity + Vec3(0,-4,0)) * time.dt
        
        # pt(e.velocity, e.position)

    p_round_pos = (int(round(player.position.x)), 
                    int(round(player.position.y)), 
                    int(round(player.position.z))
                    )

    # expanded_area_set = surrounding_coords(p_round_pos, 2)
    # if expanded_area_set.intersection(static_ent_loc_set):
    #     pt('yup')
    
Sky()
app.run()

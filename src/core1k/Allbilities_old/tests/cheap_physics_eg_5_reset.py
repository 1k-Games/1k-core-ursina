import threading
import time
import gc 

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

from print_tricks import pt

app = Ursina(vsync=False, size=(1280,720))
Entity.default_shader = lit_with_shadows_shader
global dir_light
dir_light = DirectionalLight()
dir_light.look_at(Vec3(1,-1,-1))
pt(dir_light)
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

ground = Cent(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
player = FirstPersonController()
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
        if distance > 2:
            cent_instances = get_inst(Cent)
            pt(cent_instances)
            pt(player.position)
            pt(center_parent.position)
            center_parent.position = player.position
            pt(center_parent.position)
            center_parent.position = (0,0,0)
            pt(center_parent.position)
            pt(player.position)
            pt.ex()
        time.sleep(1)



# Create a separate thread to check the distance
thread = threading.Thread(target=check_distance, args=(player, (0,0,0))).start()
def surrounding_coords(coord, max_dist):
    sc = {(x, y, z) for x in range(coord[0] - max_dist, coord[0] + max_dist + 1)
        for y in range(coord[1] - max_dist, coord[1] + max_dist + 1)
        for z in range(coord[2] - max_dist, coord[2] + max_dist + 1)}
    return sc
def stop(ent):
    ent.velocity = Vec3(0,0,0)
def spawn_block():
    global block_color
    e = Cent(model='cube', 
            velocity=Vec3(0), 
            position=player.position+Vec3(0,1.5,0)+(player.forward*5), 
            collider='box',
            parent = physics_parent, 
            color = block_color,
            )
    e.velocity = (camera.forward *4 + Vec3(0,1.5,0)) * 10
    physics_entities.append(e)
    
    
combined_statics_parent = None
def input(key):
    global block_color
    global combined_statics_parent
    
    if key == 'u':
        statics_parent.enabled = not statics_parent.enabled

    if key == 'j':
        if combined_statics_parent is None:
            # Make a copy of statics_parent and combine it
            combined_statics_parent = duplicate(statics_parent)
            combined_statics_parent.combine()
            statics_parent.enabled = False
        else:
            # Switch back to the original entities
            combined_statics_parent.enabled = False
            statics_parent.enabled = True
            combined_statics_parent = None

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

    expanded_area_set = surrounding_coords(p_round_pos, 2)
    if expanded_area_set.intersection(static_ent_loc_set):
        pt('yup')
    
Sky()
app.run()

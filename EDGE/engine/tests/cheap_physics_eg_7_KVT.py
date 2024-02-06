import time
import gc 
#
from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
# from ursina.shaders import fxaa_shader
# camera.shader = fxaa_shader

from print_tricks import pt
# pt()
# pt.ex()

sys.path.append("..")
# from ..kahm_vas_topos.kahm_vas_topos import KVT
Entity.default_shader = lit_with_shadows_shader
global dir_light
# dir_light = DirectionalLight()
# dir_light.look_at(Vec3(1,-1,-1))
# pt(dir_light)
physics_entities = []
## TODO: when their forward momentum has reached 0, then parent them to the active moving entity. 
    ## alternate who is moving and who is not (just like my reset-grid concept)
    ## if there are too many independent entities on the field at once, rapidly increase their slow-down rate so they reach 0 much faster. 
moving_group1 = Entity()
moving_group2 = Entity()
moving_g_active = Entity()

static_entities = []
static_ent_locations = []
static_ent_loc_set = set()

center_parent = Entity()
ground_parent = Entity()
class Cent(Entity):
    '''Entity subclass that is parented to the Center Entity by default. '''
    def __init__(self, parent=center_parent, **kwargs):
        super().__init__(parent=parent, **kwargs)

def get_instances(my_class):
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
            cent_instances = get_instances(Cent)
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


def generate_positions(num_positions):
    positions = []
    layer = 0
    step = 6561

    while len(positions) < num_positions:
        if layer == 0:
            positions.append((0, 0, 0))
        else:
            for i in range(-layer, layer + 1):
                if i == -layer or i == layer:
                    for j in range(-layer, layer + 1):
                        positions.append((i * step, 0, j * step))
                else:
                    positions.append((i * step, 0, -layer * step))
                    positions.append((i * step, 0, layer * step))
        layer += 1

    return positions[:num_positions]

def gen_ground(num_positions):
    # Initial ground
    # ground = Cent(model='plane', scale=6561, texture='KVT_grid_8192_black', texture_scale=(.801, .801), collider='box')
    ground = Cent(model='plane',
        scale=6561, 
        # texture='KVT_grid_8192_black_192mb.dds', ## DDS didn't work 
        texture='KVT_grid_8192_black.png', 
        texture_scale=(.801, .801), 
        collider='box', 
        parent=ground_parent)
    # Surrounding positions
    positions = generate_positions(num_positions)
    # pt(positions)
    # Loop through the surrounding positions
    for position in positions:
        # Duplicate the ground object at the position
        ground = duplicate(ground, position=Vec3(*position))
    
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
    if key == ']':
        new_y = player.position.y + 1000.
        player.position = Vec3(player.position.x, new_y, player.position.z)
    if key == '[':
        player.position = Vec3(player.position.x, 3., player.position.z)

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
    # player_kvt = kvt.update_kvt_for_ent(player)
    # print(player_kvt)



if __name__ == '__main__':

    app = Ursina(vsync=False, size=(1280,720))
    # kvt = KVT()
    
    gen_ground(64)

    s=Sky(scale=Vec3(200000,200000,200000))
    pt(s.scale)
    # player = FirstPersonController()
    # player = Entity()
    player = EditorCamera(
        position=(0,8000,0),
        move_speed = 1000,
        zoom_speed = 10,
        rotation = (77, 45, 0)
                    )
    camera.clip_plane_near = .1
    camera.clip_plane_far = 300000
    camera.fov = 105
    physics_parent = Cent()
    statics_parent = Cent()
    transfer_parent = Cent()

    global block_color
    block_color = color.blue

    app.run()

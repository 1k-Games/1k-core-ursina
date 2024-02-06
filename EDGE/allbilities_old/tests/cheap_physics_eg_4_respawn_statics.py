from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

from print_tricks import pt

app = Ursina(vsync=False, size=(1280,720))

physics_entities = []
static_entities = []
static_ent_locations = []
static_ent_loc_set = set()
walls = []

Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
player = FirstPersonController()
physics_parent = Entity()
statics_parent = Entity()

walls.append(ground)
global block_color
block_color = color.blue

def surrounding_coords(coord, max_dist):
    sc = {(x, y, z) for x in range(coord[0] - max_dist, coord[0] + max_dist + 1)
        for y in range(coord[1] - max_dist, coord[1] + max_dist + 1)
        for z in range(coord[2] - max_dist, coord[2] + max_dist + 1)}
    return sc
def stop(ent):
    ent.velocity = Vec3(0,0,0)
def spawn_block():
    global block_color
    e = Entity(model='cube', 
            velocity=Vec3(0), 
            position=player.position+Vec3(0,1.5,0)+player.forward, 
            collider='box',
            parent = physics_parent, 
            color = block_color,
            )
    e.velocity = (camera.forward *4 + Vec3(0,1.5,0)) * 10
    physics_entities.append(e)
def input(key):
    global block_color
    if key == 'left mouse down':
        spawn_block()
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
last_key_press_time = 0
def update():
    global last_key_press_time
    current_time = time.time()
    if held_keys['r'] and held_keys['left mouse'] and current_time - last_key_press_time >= 0.1:
        last_key_press_time = current_time
        spawn_block()
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

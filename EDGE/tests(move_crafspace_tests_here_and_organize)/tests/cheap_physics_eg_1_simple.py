from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

from print_tricks import pt

app = Ursina(vsync=False, size=(1280,720))

physics_entities = []
static_entities = []
static_ent_locations = []
walls = []

Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
player = FirstPersonController()
physics_parent = Entity()

walls.append(ground)

def stop(ent):
    ent.velocity = Vec3(0,0,0)

def input(key):
    if key == 'left mouse down':
        e = Entity(model='cube', color=color.azure, 
                    velocity=Vec3(0), position=player.position+Vec3(0,1.5,0)+player.forward, 
                    collider='box',
                    parent = physics_parent,
                    )
        e.velocity = (camera.forward *4 + Vec3(0,1.5,0)) * 10
        physics_entities.append(e)
    if key == 'j':
        combined_statics = physics_parent.combine()
        pt(combined_statics)

def update():
    for e in physics_entities:
        if e.intersects():
            # stop(e)
            e.velocity = Vec3(0,0,0)
            physics_entities.remove(e)
            static_entities.append(e)
        e.velocity = lerp(e.velocity, Vec3(0), time.dt)
        e.velocity += Vec3(0,-1,0) * time.dt * 5
        e.position += (e.velocity + Vec3(0,-4,0)) * time.dt
        
        # pt(e.velocity, e.position)


Sky()
app.run()

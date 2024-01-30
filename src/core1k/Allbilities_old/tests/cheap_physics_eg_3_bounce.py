from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

from print_tricks import pt

app = Ursina(vsync=False, size=(1280,720))

physics_entities = []
static_entities = []
walls = []

Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
player = FirstPersonController()
physics_parent = Entity()

walls.append(ground)
global bouncing
bouncing = False 

def stop(ent):
    ent.velocity = Vec3(0,0,0)
def bounce(ent):
    e = ent
    global bouncing
    pt(2, e.velocity, e.position)
    ex = e.velocity.x
    ey = e.velocity.y
    ez = e.velocity.z
    e.velocity = Vec3(ex, -ey, ez)
    e.position += (e.velocity + Vec3(0,1,0))
    pt('bounce')
    pt(3, ent.velocity, e.position)
    bouncing = True
    # pt.ex()
def input(key):
    if key == 'left mouse down':
        e = Entity(model='cube', color=color.azure, 
                    velocity=Vec3(0), position=player.position+Vec3(0,1.5,0)+player.forward, 
                    collider='box',
                    parent = physics_parent,
                    )
        e.velocity = (camera.forward *4 + Vec3(0,1.5,0)) * 10
        physics_entities.append(e)
    # if key =='right mouse down':
    #     e2 = duplicate(e)
    #     e2.velocity = e2.velocity *-1
    if key == 'j':
        combined_statics = physics_parent.combine()
        pt(combined_statics)

def update():
    global bouncing
    for e in physics_entities:
        if e.intersects():
            # e.velocity = Vec3(0,0,0)
            if bouncing != True:
                bounce(e)
            # stop(e)
            continue

        e.velocity = lerp(e.velocity, Vec3(0), time.dt)
        e.velocity += Vec3(0,-1,0) * time.dt * 5
        e.position += (e.velocity + Vec3(0,-4,0)) * time.dt
        
        pt(e.velocity, e.position)


Sky()
app.run()

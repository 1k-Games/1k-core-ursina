from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math

app = Ursina()

# Create terrain
terrain = Entity(model='plane', scale=320, texture='white_cube', texture_scale=Vec2(32), collider='box')
terrain.scale = Vec3(50)
terrain.position = Vec3(0, 0, 0)

# Create floating objects
floating_object = Entity(model='cube', texture='white_cube', collider='box')
floating_object.position = Vec3(10, 2, 0)

# Create a first-person controller
first_person_controller = FirstPersonController(camera_offset=Vec3(0, 2, 5))

# Custom light entity
custom_light = Entity(model='cube', texture='white_cube', collider='box', position=(0, 50, -10))
custom_light.scale = Vec3(50)

def is_in_shadow(object_entity, custom_light_entity):
    ray_origin = object_entity.position
    ray_direction = custom_light_entity.position - ray_origin
    ray_direction.normalize()
    ray_direction.z += 10
    ray_end = ray_origin + ray_direction * 10

    hit_info = raycast(ray_origin, ray_end, ignore=['custom_light'])
    return hit_info.entity == custom_light_entity

def update_shadow_color():
    for entity in app.find_all('Entity'):
        if entity != custom_light:
            if is_in_shadow(entity, custom_light):
                entity.color = color.rgba(0, 0, 0, 0.5)
            else:
                entity.color = color.white

def input(key):
    if key =='u':
        update_shadow_color()
    if key == 'i':
        is_in_shadow(floating_object, custom_light)
app.run()

''' Originaly obtained online I believe. Was just the inner and outer cubes and the file was named "matrix_rain.py"
    '''
# Matrix digital rain
from ursina import *

def update():
    # for entity in cubes:
    #     entity.rotation_y += time.dt * 5                # Rotate all the cubes every time update is called

    global offset, offset2
    offset = offset + time.dt * -0.3                     # Add a small number to this variable
    offset2 = offset2 + time.dt * -0.4                   # Add a value to this variable, but different to the first one

    setattr(cubeA, "texture_offset", (0, offset))  # Assign as a texture offset
    setattr(cubeA2, "texture_offset", (0, offset2))  

    setattr(sphereA, "texture_offset", (0, offset))  # Assign as a texture offset
    setattr(sphereA2, "texture_offset", (0, offset2))

    setattr(sphereB, "texture_offset", (0, offset))  # Assign as a texture offset
    setattr(sphereB2, "texture_offset", (0, offset2))

    setattr(sphereC, "texture_offset", (0, offset))  # Assign as a texture offset
    setattr(sphereC2, "texture_offset", (0, offset2))    

    setattr(sphereD, "texture_offset", (0, offset))  # Assign as a texture offset
    setattr(sphereD2, "texture_offset", (0, offset2))
    
    cubeA.rotation_y += time.dt * 1                # Rotate all the cubes every time update is called
    cubeA2.rotation_y += time.dt * 1                # Rotate all the cubes every time update is called
    
app=Ursina()
def gen_cubesA():
    cubesA=[]
    cubeA = Entity(model='cube', scale=(7,5,6), texture="white_noise_delete.jpg", world_position = (-12,0,0))
    # cube = Entity(model='cube', scale=(7,5,6), texture="from_matrix_rain/digit_rain_1bit.png")
    cubeA2 = Entity(model='cube', color=color.rgba(255,255,255,128), scale=(7.5,5.5,6.5),
                texture="white_noise_delete.jpg", world_position = (-12,0,0))
                #    texture="from_matrix_rain/digit_rain_1bit.png")

    cubesA.append(cubeA)                                  # Add the cube to the list
    cubesA.append(cubeA2)
    
    return cubeA, cubeA2, cubesA
cubeA, cubeA2, cubesA = gen_cubesA()

def gen_spheresA():
    spheres=[]
    sphereA = Entity(model='sphere', scale=(7,5,6), texture="white_noise_delete.jpg", world_position = (0,0,0))
    sphereA2 = Entity(model='sphere', color=color.rgba(255,255,255,128), scale=(7.5,5.5,6.5),
                texture="white_noise_delete.jpg", world_position = (0,0,0))
                #    texture="from_matrix_rain/digit_rain_1bit.png")

    spheres.append(sphereA)                                  # Add the sphere to the list
    spheres.append(sphereA2)

    return sphereA, sphereA2
sphereA, sphereA2 = gen_spheresA()

def gen_spheresB():
    spheres=[]
    sphereB = Entity(model='sphere', scale=(7,5,6), texture="white_noise_delete.png", world_position = (0,11,0), rotation=(-90,0,0))
    sphereB2 = Entity(model='sphere', color=color.rgba(255,255,255,128), scale=(7.5,5.5,6.5),
                texture="white_noise_delete.jpg", world_position = (0,11,0), rotation=(-90,0,0))
                #    texture="from_matrix_rain/digit_rain_1bit.png")

    spheres.append(sphereB)                                  # Add the sphere to the list
    spheres.append(sphereB2)

    return sphereB, sphereB2
sphereB, sphereB2 = gen_spheresB()

def gen_spheresC():
    spheres=[]
    sphereC = Entity(model='sphere', scale=(7,5,6), texture="white_noise_delete.jpg", world_position = (9,11,0), rotation=(90,0,0))
    sphereC2 = Entity(model='sphere', color=color.rgba(255,255,255,128), scale=(7.5,5.5,6.5),
                texture="white_noise_delete.jpg", world_position = (9,11,0), rotation=(90,0,0))
                #    texture="from_matrix_rain/digit_rain_1bit.png")

    spheres.append(sphereC)                                  # Add the sphere to the list
    spheres.append(sphereC2)

    return sphereC, sphereC2
sphereC, sphereC2 = gen_spheresC()

def gen_spheresD():
    spheres=[]
    sphereD = Entity(model='sky_dome', scale=(4,4,4), texture="white_noise_delete.jpg", world_position = (9,0,0))
    sphereD2 = Entity(model='sky_dome', color=color.rgba(255,255,255,128), scale=(4.5,4.5,4.5),
                texture="white_noise_delete.jpg", world_position = (9,0,0))
                #    texture="from_matrix_rain/digit_rain_1bit.png")

    spheres.append(sphereD)                                  # Add the sphere to the list
    spheres.append(sphereD2)

    return sphereD, sphereD2
sphereD, sphereD2 = gen_spheresD()
    
offset = 0
offset2 = 0


#### Controllers, Cameras, App Run
nowController = EditorCamera(move_speed=15)
nowController.y = 4
nowController.rotation_x = 0
camera.clip_plane_far = 100000
camera.fov = 85 

app.run()

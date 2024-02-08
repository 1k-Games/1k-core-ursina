from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from enemy import *

Entity.default_shader = bls

cubes = []
highlighted_cubes = []
targets = []

def input(key):
    global highlighted_cubes
    if key == "right mouse down":
    
        if mouse.world_point == None:
            return
        
        for cube in grounds:
            if distance_xz(cube, mouse.world_point) < .5:
                cube.color = color.gray
                if cube in highlighted_cubes:
                    highlighted_cubes.remove(cube)
                    break

    if key == "space":
        print(cam.position)
        print(cam.rotation)

    if key == "x":
        move(targets)
                
def on_click_cube(cube):
    global cubes

    if len(cubes) == 1:
        cube.color = color.orange
        cubes.append(cube)

        start_cube, end_cube = tuple(cubes)

        find_path(start_cube, end_cube)
        mark_path(highlighted_cubes)
        
        cubes.clear() # ilk seçimi çıkar
    else:
        cube.color = color.orange
        cubes.append(cube)

def find_path(start, end):
    global highlighted_cubes
    
    if check_width(start, end):
        print_on_screen("Lütfen aynı x veya z düzlemi seçiniz.", scale=2, position=(-.5,0))
        return 
    
    if highlighted_cubes and start not in highlighted_cubes:
        print_on_screen("Start position must be in green path", scale=2, position=(-.5,0))
        return
    
    for cube in grounds:
        if is_between(start, end, cube) or is_between(end, start, cube):                    
            highlighted_cubes.append(cube)
        else:
            cube.color = color.gray

    # put first cube in targets list
    if not targets:
        targets.append(start)

    # put end cubes in targets list
    if end not in targets:
        targets.append(end)
    

def check_width(start, end):
    if abs(start.x - end.x) > 0 and abs(start.z - end.z) > 0:
        return True
        

def is_between(a, b, c):
    # Check if point 'c' is between points 'a' and 'b' along both axes
    x_between = min(a.x, b.x) <= c.x <= max(a.x, b.x)
    z_between = min(a.z, b.z) <= c.z <= max(a.z, b.z)
    return x_between and z_between

def mark_path(path):
    for cube in path:
        cube.color = color.lime


app = Ursina()

Sky(texture = "sky_sunset")

grounds = []

cube_parent = Entity()
# Create ground cubes
for x in range(20):
    for z in range(20):
        cube = Entity(name='cube', parent=cube_parent, model='cube', position=(x, -0.5, z), color=color.gray, texture="white_cube")
        cube.collider = 'box'
        cube.on_click = lambda x=cube: on_click_cube(x)
        grounds.append(cube)




# cam settings
cam = EditorCamera()
cam.position = Vec3(10.4199, 13.6906, -4)
cam.rotation = Vec3(50.9669, -1.30302, 0)

app.run()

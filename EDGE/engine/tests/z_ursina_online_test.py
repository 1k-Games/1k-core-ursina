from ursina import *
import math
from ursina.prefabs.first_person_controller import FirstPersonController
from print_tricks import pt

app = Ursina()
box = Entity(model='cube', position = (4, 2, 13))
player = FirstPersonController()
ground = Entity(model='plane', scale=(100,1,100), color=color.yellow, texture='white_cube', texture_scale=(100,100), collider='box')
my_line = Entity(model=Mesh(vertices=[(0,0,0), (0,0,0)], mode='line', thickness = 5),
    # parent=player
    )

def update():
    curve1 = getattr(curve, 'out_circ')
    curve_points = [Vec3(curve1((i / 31)), (i / 31), (i / 31)) for i in range(32)]
    
    # dist = distance(box, player)
    # px = player.x
    # py = player.y
    # pz = player.z
    # curve_points = [(curve1(px), py, pz)]
    
    # for i in range(32):
    #     pp = i * player.x
    #     x = pp * dist / 29
    #     curve_points.append((curve1(x), x, x))
    # pt(curve_points)
    # bx = box.x
    # by = box.y
    # bz = box.z
    # curve_points.append(Vec3(curve1(bx), by, bz))
    # curve_points.insert(0, player.world_position)
    # curve_points.append(box.world_position)
    
    my_line.model.vertices = curve_points
    my_line.model.generate()


# c = curve.CubicBezier(0, .5, 1, .5)
# print('-----------', c.calculate(.23))
    
# e = Entity()
# e.animate_y(1, curve=curve.in_expo)

# e2 = Entity(x=1.5)
# e2.animate_y(1, curve=curve.CubicBezier(0,.7,1,.3))
app.run()

from ursina import *
import math
from ursina.prefabs.first_person_controller import FirstPersonController
from print_tricks import pt  

app = Ursina()
box = Entity(model='cube', position = (4, 2, 10))
player = FirstPersonController()
ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
my_line = Entity(model=Mesh(vertices=[(0,0,0), (0,0,0)], mode='line', thickness = 5))

def update():
    # step = lambda i: math.distance(self.player.position, self.eCord_position)
    tot_dist = int(round(math.dist(player.position, box.position), 0))
    # print(tot_dist)
    step = tot_dist / 100
    x = player.x
    y = player.y
    z = player.z
    curve1 = getattr(curve, 'out_circ')
    # curve_points = [Vec3(curve1(i / (tot_dist-1)), i/ (tot_dist-1), i*step) for i in range(tot_dist)]
    # curve_points = [Vec3(curve1((i+1) / (tot_dist-1))*x, (i+1)/ (tot_dist-1)*y, (i+1)*z) for i in range(tot_dist)]
    curve_points = [(x,y,z)]
    pt(curve_points)
    pt(player.position)
    for i in range (tot_dist):
        cx = curve1((i+1*x) / (tot_dist - 1))
        cy = (i+1*y) / (tot_dist - 1)
        cz = (i+1*z) / (tot_dist - 1)
        curve_points.append((cx, cy, cz))
    # pt('===start', curve_points)
    # pt(curve_points)
    # curve_points.insert(0, player.position)
    curve_points.append(box.position)
    pt('end', curve_points)

    my_line.model.vertices = curve_points
    my_line.model.generate()

app.run()
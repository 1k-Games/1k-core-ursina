from ursina import *
import math
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
box = Entity(model='cube', position = (4, 2, 10))
player = FirstPersonController()
ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
my_line = Entity(model=Mesh(vertices=[(0,0,0), (0,0,0)], mode='line', thickness = 5))

def update():
    # tot_dist = int(round(math.dist(player.position, box.position)))
    tot_dist = 320
    curve1 = getattr(curve, 'out_circ')
    curve_points = [Vec3(curve1(i / (tot_dist-1)), i/ (tot_dist-1), i/ (tot_dist-1)) for i in range(tot_dist)]
    curve_points.insert(0, player.position)
    curve_points.append(box.position)

    my_line.model.vertices = curve_points
    my_line.model.generate()

app.run()
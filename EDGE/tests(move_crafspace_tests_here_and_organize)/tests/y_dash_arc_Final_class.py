''' Final Class version: 

    How to: conclusion:
        - Generate ARC in real-world coordinates
        - Get the coordinate of the player and make that the first point. 
        - Get the coordinate of max length or the coordinate of the hit point, and make that the end point. Boom. 
'''
import math
from ursina import *
from print_tricks import pt
from mp_linecast import linecast

class DashArc(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_scale = 7
        self.length = 100
        self.player = Entity(model = 'cube', color = color.yellow, scale = self.player_scale)
        self.aa=0.5
        self.bb=1
        self.cc=1
        self.dd=0.5
        # self.bezier = curve.CubicBezier(0,0,1,0)
        self.bezier = curve.CubicBezier(self.aa, self.bb, self.cc, self.dd)
        self.verts = [Vec3(self.bezier.calculate(i/30), 0, i/30) for i in range(31)]
        self.verts2 = [Vec3(vert[0] * 14, vert[1], vert[2] * 14) for vert in self.verts]
        self.verts = self.verts2
        self.dash_arc = Entity(
            model=Mesh(vertices=self.verts, mode='line', thickness=2),
            color = color.yellow, visible = True,
            parent = self.player,
        )
        self.dash_arc_visual = Entity(
            model=Mesh(vertices=self.verts2, mode='line', thickness=5.5),
            color = color.orange, visible = False,
            parent = self.player,
        )
        self.wall = Entity(model = 'cube', position = (44, 0, 43), scale = (2, 10, 55), collider = 'box')
        self.wall2 = duplicate(self.wall, position = (63, 0, 66))
        self.end_point = Entity(model='cube', color=color.orange, 
            scale=(4, 4, 4),
            position = self.verts[-1] * self.length / self.player_scale,
        )
        self.counter = 0
        self.hit_once = False
        self.dash_ray_saved = None
        self.a = 10
        self.b = 20
        self.c = 27

    def ray(self, origin, destination):
        dash_ray = linecast(
        origin, destination,
        ignore = [self.player, self.end_point, self.dash_arc, camera, ],
        debug = True
        )
        return dash_ray

    def start_ray(self):
        total_vertices = len(self.dash_arc.model.vertices)
        resolution = 8  # or any other value you want to set
        indices = [int(i * total_vertices / resolution) for i in range(1, resolution)]
        indices.append(-1)  # Ensure the last vertex is included

        vertices = [self.player.world_position] + [scene.getRelativePoint(self.dash_arc, self.dash_arc.model.vertices[i]) for i in indices]

        for i in range(resolution):
            if self.counter == i:
                dash_ray = self.ray(vertices[i], vertices[i+1])
                if dash_ray.world_point is not None:
                    self.end_point.visible = True
                    self.end_point.world_position = dash_ray.world_point
                    self.arc_close_points(dash_ray)
                    self.dash_arc_visual.color = color.blue
                    self.counter = 0
                    break
                self.counter += 1

        if self.counter == resolution:
            self.counter = 0
            self.end_point.world_position = vertices[-1]
            self.dash_arc_visual.color = color.red
            if len(self.dash_arc_visual.model.vertices) < 31:
                self.dash_arc_visual.model.vertices = self.verts
                self.dash_arc_visual.model.generate()
                
                
    def arc_close_points(self, dash_ray):
        localized_hit_point = self.dash_arc.getRelativePoint(scene, dash_ray.world_point)
        pt(
            dash_ray.world_point,
            localized_hit_point
            )    
        n=15
        cut_verts = self.verts[:-n or None]
        self.dash_arc_visual.model.vertices = cut_verts
        self.dash_arc_visual.model.generate()

    def update(self):
        if held_keys['space']:
            self.start_ray()

    def input(self, key):
        if key == 'space' or key == 'v':
            self.dash_arc_visual.visible = True
            self.end_point.visible = True
        if key == 'space up' or key == 'v up':
            self.end_point.visible = False
            self.dash_arc_visual.visible = False
        # if key == '1':
        #     self.a -= 1
        # if key == '2':
        #     self.a += 1
        # if key == '3':
        #     self.b -= 1
        # if key == '4':
        #     self.b += 1
        # if key == '5':
        #     self.c -= 1
        # if key == '6':
        #     self.c += 1
        if key == 'o':
            self.wall.z += 8
            pt(self.wall.position)
        if key == 'l':
            self.wall.z -= 8
            pt(self.wall.position)
        if key == 'i':
            self.wall.x += 8
            pt(self.wall.position)
        if key == 'k':
            self.wall.x -= 8
            pt(self.wall.position)
        if key == 'w':
            self.player.z += 8
        if key == 's':
            self.player.z -= 8
        if key == 'a': 
            self.player.x -= 8
        if key == 'd':
            self.player.x += 8
        if key == 'left arrow':
            self.player.rotation_y -= 2
        if key == 'right arrow':
            self.player.rotation_y += 2
        if key == 'page up':
            self.player.rotation_x += 2
        if key == 'page down':
            self.player.rotation_x -= 2
        if key == 'up arrow':
            self.player.rotation_z += 2
        if key == 'down arrow':
            self.player.rotation_z -= 2
        

        if key == '1':
            self.aa+=.05
            print(self.aa)
        if key == '2':
            self.aa-=.05
            print(self.aa)
        if key == '3':
            self.bb+=.05
            print(self.bb)
        if key == '4':
            self.bb-=.05
            print(self.bb)
        if key == '5':
            self.cc+=.05
            print(self.cc)
        if key == '6':
            self.cc-=.05
            print(self.cc)
        if key == '7':
            self.dd+=.05
            print(self.dd)
        if key == '8':
            self.dd-=.05
            print(self.dd)
        self.bezier = curve.CubicBezier(self.aa,self.bb,self.cc,self.dd)
        self.verts = [Vec3(self.bezier.calculate(i/30), 0, i/30) for i in range(31)]
        self.verts2 = [Vec3(vert[0] * 14, vert[1], vert[2] * 14) for vert in self.verts]
        self.dash_arc.model.vertices = self.verts
        self.dash_arc.model.generate()
        self.dash_arc_visual.model.vertices = self.verts2
        self.dash_arc_visual.model.generate()


if __name__ == "__main__":
    app = Ursina(size=(1920,1080))
    dash_arc = DashArc()
    EditorCamera(position = (55, 725, 55), rotation = (90, 0, 0), move_speed = 1000)
    app.run()
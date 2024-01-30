''' self.bezier raycasts 003'''
'''TODO in here, (then place in abilities_working_on.py and then abilities.py):

- ARC Idea 1:
    - How to allow dash to curve so we can jump on top of surfaces above us? 
        - Create some new walls to test the curving and the hit detection/distance. 
    - Separate out the arc that controls thing from the visual arc. 
        (Right now, I have the visual real arc that controls the rays. The problem is when I shrink the arc,
        it screws up the other calculations.)
        - So I need to make the real arc stay the same size, and it can only
        be visual when debugging. 
        - Visual arc changes size when the rays get the interception point. 
    - Set distance of dash point to interception point (just like placing the self.boomerang at the hit point, we are also making the visual self.dash_arc stop/calculate at that same position as where the self.boomerang lands)
    - Make a perfectly accurate final collision ray point:
        - If any of the main rays hit, Take the closest vertice on the main arc that is closest to this ray hit point, and actually place the self.boomerang on that point!!!
        - It prob makes sense to convert the hit point vertice to a relative point in relation to the dash arc or self.player... That way we are only converting one thing, and then can easily take that point and do a distance check against all of the points of the arc to see which is closest to it.
        - Extended: when find the point it should be at, cast a raycast on the previous point, the the next main point (so it's like a last, final raycast to confirm)
        - Alt: make a new ray cast that is cast just behind where the point hit, instead of calculating at all?

- ARC Idea 2:
    Goals:
        - project an arc into the world at __ self.length. 
        - Arc changes self.length & end point dynamically based on what it contacts. 
        - You move to the contact point.
        
    Debate How to:
        - If I parent to self.player, and have it generate point from self.player perspective, 
        then I don't have to re-calculate the size of the dash everytime it doesn't hit something. 
        - BUT... I have to regenerate points anyways, literally everytime it'll contact anything else
            AND, it'll take more resources to convert. 
        
    How to: conclusion:
        - Generate ARC in real-world coordinates
        - Get the coordinate of the self.player and make that the first point. 
        - Get the coordinate of max self.length or the coordinate of the hit point, and make that the end point. Boom. 
            - The max self.length will be easily calculated by having a self.player-target out in the world that is parented to the self.player. 
            - We convert this targets position to real world coords
            - We tell arc to generate in the world at self.player, and end at target position. 
            - if we hit something, target position = hit point. 

- ARC idea 3: Hyperdash:
    - Hyperdash alternative verion, hyperdash style:
        - ray cast aimed above self.player pointer (helps to obscure that this in't actually an arc, but is faked)
        - If hit self.wall, shoot raycast down. Hit position is jump position. 
        - if not hit self.wall, but hits max range for that gun angle, do same as above (shoot ray down etc)

- ARC idea 4: Circle/Loop/ring mesh:
(See discord for more information)

'''



import math
from panda3d import core
from ursina import *
from print_tricks import pt
# from abilities import Ability
from mp_linecast import linecast
app = Ursina()


class Dash_Draft(Entity):
    def __init__(self, enabled = True):
        super().__init__(
            # player, 
            enabled
        )
        self.counter = 0
        self.pointA = 10
        self.pointB = 20
        self.pointC = 27
        
        self.create_map_test_objects()

    def update(self):
        
        if held_keys['space']:
            self.start_ray(self.pointA, self.pointB, self.pointC)
        elif held_keys['v']:
            self.start_ray_old(self.pointA, self.pointB, self.pointC)

        ## update main arc position
        ## we use this to calculate the collision rays etc. 
        self.verts = self.get_curved_verts(self.player.world_x, self.player.world_z, 
            self.dash_target.world_x, self.dash_target.world_z, 31)
        self.dash_arc.model.vertices = self.verts
        self.dash_arc.model.generate()

    def input(self, key):
        if key == 'space' or key == 'v':
            self.dash_arc_visual.visible = True
            self.boomerang.visible = True
            # pt(fsaf)
        if key == 'space up' or key == 'v up':
            self.boomerang.visible = False
            self.dash_arc_visual.visible = False
        
        if key == '1':
            self.pointA -= 1
        if key == '2':
            self.pointA += 1
        if key == '3':
            self.pointB -= 1
        if key == '4':
            self.pointB += 1
        if key == '5':
            self.pointC -= 1
        if key == '6':
            self.pointC += 1
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

        # pt(a, b, c)

    def create_map_test_objects(self):
        
        self.temp_delete_object = Entity(model = 'sphere', color = color.black, 
            scale = 6, position = (-10, -10, -10))

        self.player_scale = 7
        self.length = 100
        self.player = Entity(model = 'cube', color = color.yellow, scale = self.player_scale,
            position = (2,0,2))
        self.dash_target = Entity(model = 'cube', color = color.green, 
            position = (15, 0, 15), 
            parent = self.player,)
        
        self.verts = self.get_curved_verts(self.player.world_x, self.player.world_z, 
            self.dash_target.world_x, self.dash_target.world_z, 31)

        # pt(self.verts)
        pt(self.dash_target.x, self.dash_target.z, self.dash_target.position, self.dash_target.world_position)

        self.dash_arc = Entity(
            model=Mesh(vertices= self.verts, mode='line', thickness=2),
            color = color.yellow, visible = True,
            # parent = self.player,
            # scale = 1 / self.player_scale,
            # scale = 1
            )
        self.dash_arc_visual = Entity(
            model=Mesh(vertices= self.verts, mode='line', thickness=5.5),
            color = color.orange, visible = False,
            # parent = self.player,
            # scale = self.length / self.player_scale,
            # scale = 1
            )

        self.wall = Entity(model = 'cube', position = (44, 0, 43), scale = (2, 10, 55), collider = 'box')
        self.wall2 = duplicate(self.wall, position = (63, 0, 66))

        self.boomerang = Entity(model='cube', color=color.orange, 
            scale=(4, 4, 4),
            position = self.verts[-1] * self.length / self.player_scale,
            )

        return

    def get_curved_verts(self, start_x, start_z, end_x, end_z, num_points):
        
        ## I made all of these local, for faster calulcations. 
        ## I created this forumula through experimentation. 
        
        
        
        # self.bezier = curve.CubicBezier(0,0,15,0)
        # self.verts = [Vec3(self.bezier.calculate(i/30), 0, i/30) for i in range(31)]
        # pt(self.verts)
        # pt.ex()
        
        verts = []
        num = num_points - 1 

        bezier = curve.CubicBezier(0,0,1,0)
        for i in range(int(num_points)):
            # bb = f'---{start_x} {start_x/(i/num)} {start_x*(i/num)} {start_x/(num/i)} {start_x*(num/i)}'
            bezX = bezier.calculate((i/num))

            # if i is 0:
            #     x = start_x
            #     y = 0
            #     z = start_z
            # else:
            x = (bezX * end_x) + (start_x*((num-i)/num))
            y = 0
            z = ((i/num) * end_z) + (start_z*((num-i)/num))
            verts.append(Vec3(x,y,z))
        # pt.ex()
        # for i in range(int(num_points/2)):
        #     bezX = bezier.calculate((i/num/2))
        #     x = (bezX * end_x) + start_x
        #     y = 0
        #     z = ((i/num/2) * end_z) + start_z
        #     verts.append(Vec3(x,y,z))
            
        # for i in range(int(num_points/2)):
        #     bezX = bezier.calculate((i/num/2))
        #     z = (bezX * end_x) + start_x
        #     y = 0
        #     x = ((i/num/2) * end_z) + start_z
        #     verts.append(Vec3(x,y,z))
            
        return verts   
    
        ## commented version:::
        # # We have to calculate with 1 less than the range
        # num = num_points - 1 
        # for i in range(num_points):
        #     ## calc the curve on a scale from 0-1
        #     bezX = bezier.calculate((i/num))
        #     ## multiply the result by the ending X position that we want in world space, add the starting position (the player's hand)
        #     x = (bezX * end_x) + start_x
        #     y = 0
        #     ## i/num = scale from 0-1 and goes hand-in-hand with the bezier.calculate i/num
        #     ## Then we multiply by our desired Z in world space, and add our starting Z location (player's hand). 
        #     z = ((i/num) * end_z) + start_z
        #     verts.append(Vec3(x,y,z))
            
        ## old method, 0-1 range only:
        # self.verts = [Vec3(self.bezier.calculate(i/30), 0, i/30) for i in range(31)]

    def ray(self, origin, destination):
        self.dash_ray = linecast(
        origin, destination,
        ignore = [self.player, self.boomerang, self.dash_arc, camera, ],
        debug = True
        )
        return self.dash_ray

    def start_ray(self, a, b, c):
        
        # for dynamically changing postions (self.bezier 0,0,1,0)
        nvA = scene.getRelativePoint(self.dash_arc, self.dash_arc.model.vertices[a])
        nvB = scene.getRelativePoint(self.dash_arc, self.dash_arc.model.vertices[b])
        nvC = scene.getRelativePoint(self.dash_arc, self.dash_arc.model.vertices[c])
        nvD = scene.getRelativePoint(self.dash_arc, self.dash_arc.model.vertices[-1])
        
        if self.counter == 0:
            self.dash_ray = self.ray(self.player.world_position, nvA)
            self.counter +=1
        elif self.counter == 1:
            self.dash_ray = self.ray(nvA, nvB)
            self.counter += 1
        elif self.counter == 2:
            self.dash_ray = self.ray(nvB, nvC)
            self.counter += 1
        elif self.counter == 3:
            self.dash_ray = self.ray(nvC, nvD)
            self.counter += 1
            
        # No hits during all of the ray casts
        if self.counter == 4 and self.dash_ray.world_point is None:
            self.boomerang.world_position = nvD
            self.dash_arc_visual.color = color.red
            # self.dash_arc_visual.scale = self.length / self.player_scale
            # if len(self.dash_arc_visual.model.vertices) < 31:
            #     self.dash_arc_visual.model.vertices = self.verts
            #     self.dash_arc_visual.model.generate()
            self.verts = self.get_curved_verts(self.player.world_x, self.player.world_z, 
                self.dash_target.world_x, self.dash_target.world_z, 31)
            self.dash_arc_visual.model.vertices = self.verts
            self.dash_arc_visual.model.generate()
            self.counter = 0
            
            pt(self.verts, self.player.world_x, self.player.world_z, 
            self.dash_target.world_x, self.dash_target.world_z,)

        # A hit just occured in whatever self.dash_ray was just sent
        if self.dash_ray.world_point is not None:
            self.boomerang.visible = True
            self.boomerang.world_position = self.dash_ray.world_point
            self.dash_arc_visual.color = color.blue
            self.verts = self.get_curved_verts(self.player.world_x, self.player.world_z, 
                self.dash_ray.world_point.x, self.dash_ray.world_point.z, 31)
            self.dash_arc_visual.model.vertices = self.verts
            self.dash_arc_visual.model.generate()
            self.counter = 0

    def arc_close_points(self, dash_ray):
        localized_hit_point = self.dash_arc.getRelativePoint(scene, self.dash_ray.world_point)
    

dash_draft = Dash_Draft()
EditorCamera(position = (55, 725, 55), rotation = (90, 0, 0), move_speed = 1000)
app.run()
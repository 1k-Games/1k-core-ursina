from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)

from ursina import *
from core1k.base_entities.trigger_base_entity import TriggerBaseEntity

class FirstPersonShooterController(Entity):
    def __init__(self, level, fov=90, enabled=True, **kwargs):
        self.level = level
        self.reticle = Entity(parent=camera.ui, model='quad', color=color.green, scale=.024, rotation_z=45, texture='default-reticle.png', enabled=enabled)
        self.camera_pivot = Entity()
        self.camera_fov = fov
        
        super().__init__(**kwargs)
        
        # pt.c('------- FPS Controller --------')
        # pt(self.world_position, self.position, self.world_rotation, self.rotation)
        
        self.speed = 11
        self.sprint_speed = self.speed * 1.6
        self.height = 2
        
        self.camera_pivot.parent = self
        self.camera_pivot.y = self.height

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = self.camera_fov

        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, TriggerBaseEntity]
        
        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y

    def on_enable(self):
        # pt('FPS ENABLED')
        mouse.locked = True
        self.reticle.enabled = True
        self.setup_camera()
        
    def on_disable(self):
        # pt('FPS DISABLED')
        self.reticle.enabled = False
        # pt(mouse.locked, self.reticle.enabled)
        
    def setup_camera(self):
        
        # pt(1, '-fps-',  self.camera_pivot.parent, camera.parent, 
        #     camera.world_position, self.camera_pivot.world_position)
        
        camera.fov = self.camera_fov
        camera.position = self.camera_pivot.position 
        camera.rotation = self.camera_pivot.rotation
        camera.parent = self.camera_pivot
        
        # pt(2, '-fps-',  self.camera_pivot.parent, camera.parent, 
        #     camera.world_position, self.camera_pivot.world_position)
    def update(self):
        # pt('-------------- third person controller ---------')
        
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)
        
        self.direction = Vec3(
            self.forward * ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
            + self.right * ((held_keys['d'] - held_keys['a']) or held_keys['gamepad left stick x'])
            ).normalized()
            
        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        
        if held_keys['left shift']:
            move_amount = self.direction * time.dt * self.sprint_speed
        else: 
            move_amount = self.direction * time.dt * self.speed
            
        if not feet_ray.hit and not head_ray.hit:
            
            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # pt()
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity
            
            pt(self.height, self.y, ray.hit, ray.distance)
            pt.c(ray.entity)
            if pt.r(loops=3):
                pt.ex()
        # hv = self.level.terrain.model.height_values
        # self.y = self.true_y(self.world_position, self.level)
        # pt('_______', self.y)
        # self.y = terraincast(self.world_position, self.level.terrain, hv)
        # pt(self.y)
        
    def true_y(self, p_pos, level):
        terrain = level.terrain
        w = level.w 
        h = level.h
        x = int(p_pos.x/(terrain.scale_x/w) + w/2)
        z = int(p_pos.z/(terrain.scale_z/h) + h/2)
        i = (z*(w)) + x
        # pt(p_pos, x, z, i)

        true_x, true_z = int(x/7), int(z/7)
        # pt(true_x, true_z)
        y1 = terrain.model.height_values[x][z]
        # pt(y1)
        y2 = terrain.model.height_values[true_x][true_z]
        # pt(y2)
        difx = abs(p_pos.x) - abs(x)
        dify = abs(p_pos.z) - abs(z)
        pt(p_pos, x, z, true_x, true_z, difx, dify)

        if pt.r(seconds=2):
            pt.ex()

    def input(self, key):
        if key == 'space':
            self.jump()

        if key == 'left control' or key == 'c':
            self.crouch()
            
        if key == 'left control up' or key == 'c up':
            self.stand_up()
            
        if key == 'p':
            pt(self.height, self.jump_height, self.y)

    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def crouch(self):
        self.height /= 2
        
    def stand_up(self):
        self.height *= 2
        
    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        self.air_time = 0
        self.grounded = True





if __name__ == '__main__':
    window.vsync = False
    app = Ursina(size=(1920,1080))
    # Sky(color=color.gray)
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    player = FirstPersonShooterController(y=2, origin_y=-.5, level=Entity())
    player.y=1
    player.gun = None


    gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box', scale=(.2,.2,1))
    def get_gun():
        gun.parent = camera
        gun.position = Vec3(.5,0,.5)
        player.gun = gun
    gun.on_click = get_gun

    gun_2 = duplicate(gun, z=7, x=8)
    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
    # hill = Entity(model='sphere', position=(20,-10,10), scale=(25,25,25), collider='sphere', color=color.green)
    # hill = Entity(model='sphere', position=(20,-0,10), scale=(25,25,25), collider='mesh', color=color.green)
    # from ursina.shaders import basic_lighting_shader
    # for e in scene.entities:
    #     e.shader = basic_lighting_shader

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)
    def input(key):
        if key == 'left mouse down' and player.gun:
            gun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    # player.add_script(NoclipMode())
    app.run()

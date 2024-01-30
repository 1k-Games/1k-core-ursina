from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)

from math import atan2
from ursina import *

from characters.target_types import EnergyBeing
from eg_globals import EG_Globals



class FR_Hybrid_Controller(EnergyBeing):
    def __init__(self,
        fov=90,
        starting_cam_pos='first',
        cam_height=2,
        enabled=True,
        **kwargs):
        
        # pt(cam_height)
        # pt(starting_cam_pos)
        # self.y = self.character.scale_y/2

        self.reticle = Entity(parent=camera.ui, model='quad', scale=.005, rotation_z=45, texture='default-reticle.png', enabled=enabled)
        
        self.camera_fov = fov
        self.starting_cam_pos = starting_cam_pos
        
        self.cam_mount_main_ent = Entity(model='cube', color=Color(1,0,0,0.6),
                                    scale=1, world_scale=1,
                                    )
        self.cam_mount_main_default_pos = Vec3(0, cam_height, .1)
        
        self.cam_dist = 20
        
        self.middle_mouse_held = False  # Add this line
        self.core = Entity() ## placeholder for when setup_camera() is first called. 

        self._active = True
        
        super().__init__(**kwargs)
        # pt.c('------- FR Hybrid Controller --------')
        
        self.cam_mount_main_ent.parent = self
        
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos
        
        
        
        self.char_half_height = self.character.scale_y / 2
        
        self.traverse_target = scene
        
        self.ignore_list = [self]
        self.add_children_to_ignore_list(self)
        # print('ignore: ', self.ignore_list)
            
        self.speed = 6
        self.sprint_speed = self.speed * 1.6


        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 0
        self.grounded = False
        self.jump_height = 4.5
        self.jump_up_duration = .5
        self.fall_after = .35
        self.jumping = False
        self.air_time = 0
        
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+self.cam_mount_main_ent.position, 
            self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y
        
        self.setup_initial_camera(self.starting_cam_pos)
        
    def setup_initial_camera(self, cam_position):
        camera.fov = self.camera_fov
        camera.position = self.cam_mount_main_ent.position 
        camera.rotation = self.cam_mount_main_ent.rotation
        camera.parent = self.cam_mount_main_ent
        # camera.world_position = self.cam_mount_main_ent.world_position
        
        
        # camera.fov = self.camera_fov
        # camera.position = self.camera_pivot.position 
        # camera.rotation = self.camera_pivot.rotation
        # camera.parent = self.camera_pivot
        
        # self.cam_mount_main_ent.world_position = self.cam_mount_main_default_pos
        
        self.setup_camera(cam_position) 
        
    def setup_first_person_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos
        self.cam_mount_main_ent.world_rotation = self.world_rotation
        
    def setup_front_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(0, 0, self.cam_dist)
        self.cam_mount_main_ent.rotation = Vec3(0, 180, 0)
        
    def setup_left_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(-self.cam_dist, 0, 0)
        self.cam_mount_main_ent.rotation = Vec3(0, 90, 0)

    def setup_right_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(self.cam_dist, 0, 0)
        self.cam_mount_main_ent.rotation = Vec3(0, -90, 0)

    def setup_top_down_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(0, self.cam_dist, 0)
        self.cam_mount_main_ent.rotation = Vec3(90, 0, 0)

    def setup_high_back_view(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(0, self.cam_dist / 2, -self.cam_dist)
        self.cam_mount_main_ent.rotation = Vec3(22.5, 0, 0)

    def setup_third_person_view(self):
        self.cam_mount_main_ent.parent = self.core 
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos + Vec3(0, 0, -self.cam_dist*2)

        # self.cam_mount_main_ent.world_rotation = self.world_rotation
    
    def setup_camera(self, cam_position):


        # self.core.rotation = (0,0,0)
        # self.cam_mount_main_ent.world_position = (0,0,0)
        # camera.world_rotation = self.cam_mount_main_ent.world_rotation
        
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos
        self.cam_mount_main_ent.parent = self

        self.starting_cam_pos = cam_position
        if cam_position == 'first':
            self.setup_first_person_view()
        elif cam_position == 'front':
            self.setup_front_view()
        elif cam_position == 'left':
            self.setup_left_view()
        elif cam_position == 'right':
            self.setup_right_view()
        elif cam_position == 'top':
            self.setup_top_down_view()
        elif cam_position == 'back':
            self.setup_high_back_view()
        elif cam_position == 'third':
            self.setup_third_person_view()
            
        
    def add_children_to_ignore_list(self, entity):
        for child in entity.children:
            self.ignore_list.append(child)
            self.add_children_to_ignore_list(child)
            

    def update(self):
        if not self.active:
            return

        
        if self.middle_mouse_held:
            self.core.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
            self.core.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.core.rotation_x = clamp(self.core.rotation_x, -90, 90)
        else:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
            self.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.rotation_x = clamp(self.rotation_x, -90, 90)
        
        self.direction = Vec3(
            self.forward * ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
            + self.right * ((held_keys['d'] - held_keys['a']) or held_keys['gamepad left stick x'])
            ).normalized()
        
        
        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0, self.character.y, 0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        
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
            
        if self.gravity:
            ray = raycast(self.world_position+(0,self.char_half_height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)
            
            if ray.distance <= self.character.scale_y + .1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                # if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                #     self.y = ray.world_point[1]
                return
            else:
                self.grounded = False
                
            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity
    
    def input(self, key):
        if not self.active:
            return

            
        if key == '1':
            self.gravity = 1
            
        if key == 'u':
            pt(self.world_position, self.character.world_position)
        if key == 'space':
            self.jump()
            
        if key == 'left control' or key == 'c':
            self.crouch()
            
        if key == 'left control up' or key == 'c up':
            self.stand_up()
            
        if key == 'p':
            pt(self.camera_height, self.jump_height, self.y)
            
        if key == 'insert':
            self.setup_camera('first')
        elif key == 'delete':
            self.setup_camera('front')
        elif key == 'home':
            self.setup_camera('left')
        elif key == 'end':
            self.setup_camera('right')
        elif key == 'page up':
            self.setup_camera('top')
        elif key == 'page down':
            self.setup_camera('back')
            
        elif key == 'middle mouse down':
            pt.c('down')
            # self.cam_mount_main_ent.position = self.cam_mount_main_default_pos
            self.setup_camera('third')
            # self.original_parent = self.cam_mount_main_ent.parent
            self.middle_mouse_held = True 
            
        elif key == 'middle mouse up':
            # pt.c('up')
            # pt(self.cam_mount_main_ent.world_position, self.cam_mount_main_ent.position, self.cam_mount_main_ent.world_scale, self.cam_mount_main_ent.scale, camera.world_position, camera.position)
            
            
            # pt(self.cam_mount_main_ent.world_position, self.cam_mount_main_ent.position, self.cam_mount_main_ent.world_scale, self.cam_mount_main_ent.scale, camera.world_position, camera.position)
            self.middle_mouse_held = False 
            
            
        
    def on_enable(self):
        ...
        self.active = True
        # mouse.locked = True
        # self.setup_initial_camera(self.starting_cam_pos)

    def on_disable(self):
        try:
            self.reticle.enabled = False
            
            
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value
        if self._active:
            self.on_activate()
        else:
            self.on_deactivate()
            
    def on_activate(self):
        mouse.locked = True
        self.reticle.enabled = True
        self.setup_initial_camera(self.starting_cam_pos)
        
    def on_deactivate(self):
        self.reticle.enabled = False
        
    def jump(self):
        if not self.grounded:
            return
        
        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)
        
    def crouch(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos[1] / 2
        
    def stand_up(self):
        self.cam_mount_main_ent.position = self.cam_mount_main_default_pos[1]
        
    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False
        
    def land(self):
        self.air_time = 0
        self.grounded = True


class Player(FR_Hybrid_Controller):
    def __init__(self, **kwargs):
        super().__init__(
            color=EG_Globals.ent_colors['player_color'],
            shield_part_double_sided=False,
            **kwargs)
    
        self.setup_inner_colored_shield()
        self.setup_inner_hit_effects_shield()
        



    @every(0.015) ## 15 ms between color changes. Just for the player on this pc.  
    def update_inner_colored_shield(self):
        index = min(self.shield.shield_health // 100, 10)
        color = EG_Globals.SHIELD_COLORS()[int(index)]
        self.inner_colored_shield.color = color 
        self.reticle.color = color 
        
    def setup_inner_hit_effects_shield(self):
        ...
        
    def setup_inner_colored_shield(self):
        self.inner_colored_shield = Entity(name='inner_colored_shield',
            parent=camera,
            model='quad',
            world_scale=2.15,
            z=.5,
            # texture='player_inner_shields_color',
            texture='player_inner_shields_color_hard_white',
            alpha=.88,
            shader=None,
        )
        
        #######################
        ## self.core 3d world version
        ## Interesting idea, but I actually see 0 benefits. 
        #######################
        # self.inner_colored_shield = Entity(name='inner_colored_shield',
        #     parent=self.core,
        #     model='sphere_normals_inverted',
        #     y=self.cam_mount_main_default_pos, ## line it up with eyes
        #     world_scale=3.5,
        #     texture='player_inner_shields_color2',
        #     color=color.cyan,
        #     shader=None,
        # )
        
if __name__ == '__main__':
    window.vsync = False
    app = Ursina()

    ground = Entity(model='plane', scale=(200,1,200), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    # player = Player(y=2, origin_y=-.5, level=Entity())
    player = Player(cam_height=.47)
    # player.y = 3
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


    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    app.run()

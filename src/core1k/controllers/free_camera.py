from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)
# from ursina import Entity, camera, destroy, held_keys, mouse, curve, lerp, clamp, time, Vec2, Vec3, slerp
from ursina import *

class FreeCamera(Entity):
    
    def __init__(self,
            controls_center=None,
            free_target=None,
            free_target_offset = (0,0,10),
            **kwargs
        ):
        camera.free_cam_pos = camera.position
        self.controls_center = controls_center
        self.free_target = free_target
        self.free_target_offset = free_target_offset
        
        super().__init__(name='free_camera', eternal=False)
        
        pt.c('------- FreeCamera --------')
        pt(self.world_position, self.position, self.world_rotation, self.rotation)
        
        
        self.rotation_speed = 200
        self.pan_speed = Vec2(5, 5)
        self.move_speed = 10
        self.zoom_speed = 1.25
        self.zoom_smoothing = 8
        self.rotate_around_mouse_hit = False
        
        self.smoothing_helper = Entity(add_to_scene_entities=False)
        self.rotation_smoothing = 0
        self.look_at = self.smoothing_helper.look_at
        self.look_at_2d = self.smoothing_helper.look_at_2d
        self.rotate_key = 'right mouse'
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.start_position = self.position
        self.perspective_fov = camera.fov
        self.orthographic_fov = camera.fov
        # self.on_destroy = self.on_disable
        self.hotkeys = {'toggle_orthographic':'shift+p', 'focus':'f', 'reset_center':'shift+f'}
        
    def on_enable(self):
        # pt('free cam ENABLE')
        
        # if self.free_target:
            # self.free_target.parent = self
            
        # camera.org_parent = camera.parent
        # camera.org_position = camera.position
        # camera.org_rotation = camera.rotation
        camera.parent = self
        # camera.position = camera.free_cam_pos
        # camera.rotation = (0,0,0)
        self.goal_z = camera.z
        self.goal_fov = camera.fov
        
    def on_disable(self):
        ...
        # if self.free_target:
        #     self.free_target.position = self.position
            # self.free_target.parent = 
            
        # camera.free_cam_pos = camera.position
        # camera.parent = camera.org_parent
        # camera.position = camera.org_position
        # camera.rotation = camera.org_rotation
        
    # def on_destroy(self):
    #     destroy(self.smoothing_helper)
    def change_targets(self):
        if self.controls_center:
            hit_info = mouse.hovered_entity if not mouse.locked else raycast(
                camera.position, camera.forward).entity
            
            if hit_info:
                self.controls_center.cycle_through_active_controllers()
    ...
        
    def input(self, key):
        combined_key = ''.join(e+'+' for e in ('control', 'shift', 'alt') if held_keys[e] and not e == key) + key
        
        if combined_key == self.hotkeys['toggle_orthographic']:
            if not camera.orthographic:
                self.orthographic_fov = camera.fov
                camera.fov = self.perspective_fov
            else:
                self.perspective_fov = camera.fov
                camera.fov = self.orthographic_fov

            camera.orthographic = not camera.orthographic
            
        elif combined_key == self.hotkeys['reset_center']:
            self.animate_position(self.start_position, duration=.1, curve=curve.linear)
            
        elif combined_key == self.hotkeys['focus'] and mouse.world_point:
            self.animate_position(mouse.world_point, duration=.1, curve=curve.linear)
            
        elif key == 'scroll up':
            if not camera.orthographic:
                goal_position = self.world_position
                # if mouse.hovered_entity and not mouse.hovered_entity.has_ancestor(camera):
                #     goal_position = mouse.world_point

                self.world_position = lerp(self.world_position, goal_position, self.zoom_speed * time.dt * 10)
                self.goal_z += self.zoom_speed * (abs(self.goal_z)*.1)
            else:
                self.goal_fov -= self.zoom_speed * (abs(self.goal_fov)*.1)
                self.goal_fov = clamp(self.goal_fov, 1, 200)
                
        elif key == 'scroll down':
            if not camera.orthographic:
                # camera.world_position += camera.back * self.zoom_speed * 100 * time.dt * (abs(camera.z)*.1)
                self.goal_z -= self.zoom_speed * (abs(self.goal_z)*.1)
            else:
                self.goal_fov += self.zoom_speed * (abs(self.goal_fov)*.1)
                self.goal_fov = clamp(self.goal_fov, 1, 200)
                
        elif key == 'right mouse down' or key == 'middle mouse down':
            if mouse.hovered_entity and self.rotate_around_mouse_hit:
                org_pos = camera.world_position
                self.world_position = mouse.world_point
                camera.world_position = org_pos
        
        if key == 'left mouse down':
            self.change_targets()
            
    def update(self):
        # pt.t('free camera')
        
        # self.free_target.position = camera.position * self.forward *-2
        # offset = self.forward * self.free_target_offset
        # self.free_target.position = self.position + offset
    
        if held_keys['gamepad right stick y'] or held_keys['gamepad right stick x']:
            self.smoothing_helper.rotation_x -= held_keys['gamepad right stick y'] * self.rotation_speed / 100
            self.smoothing_helper.rotation_y += held_keys['gamepad right stick x'] * self.rotation_speed / 100

        elif held_keys[self.rotate_key]:
            self.smoothing_helper.rotation_x -= mouse.velocity[1] * self.rotation_speed
            self.smoothing_helper.rotation_y += mouse.velocity[0] * self.rotation_speed

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            + self.up    * (held_keys['e'] - held_keys['q'])
            ).normalized()

        self.position += self.direction * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

        if self.goal_z < 0:
            self.goal_z += held_keys['w'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
        else:
            self.position += camera.forward * held_keys['w'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

        self.goal_z -= held_keys['s'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

        if mouse.middle:
            if not camera.orthographic:
                zoom_compensation = -self.goal_z * .1
            else:
                zoom_compensation = camera.orthographic * camera.fov * .2

            self.position -= camera.right * mouse.velocity[0] * self.pan_speed[0] * zoom_compensation
            self.position -= camera.up * mouse.velocity[1] * self.pan_speed[1] * zoom_compensation

        if not camera.orthographic:
            camera.z = lerp(camera.z, self.goal_z, time.dt*self.zoom_smoothing)
        else:
            camera.fov = lerp(camera.fov, self.goal_fov, time.dt*self.zoom_smoothing)

        if self.rotation_smoothing == 0:
            self.rotation = self.smoothing_helper.rotation
        else:
            self.quaternion = slerp(self.quaternion, self.smoothing_helper.quaternion, time.dt*self.rotation_smoothing)
            camera.world_rotation_z = 0

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, 'smoothing_helper') and name in ('rotation', 'rotation_x', 'rotation_y', 'rotation_z'):
            setattr(self.smoothing_helper, name, value)

if __name__ == '__main__':
    # window.vsync = False
    from ursina import Ursina, Sky, load_model, color, Text, window
    from src.core1k.controllers.first_person_shooter_controller import FirstPersonShooterController
    app = Ursina(size=(1920,1080), vsync=False)
    '''
    Simple camera for debugging.
    Hold right click and move the mouse to rotate around point.
    '''

    sky = Sky()
    e = Entity(model=load_model('cube', use_deepcopy=True), color=color.white, collider='box')
    e.model.colorize()


    ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=(32,32), collider='box')
    box = Entity(model='cube', collider='box', texture='white_cube', scale=(10,2,2), position=(2,1,5), color=color.light_gray)
    
    player = FirstPersonShooterController(model='cube', y=1, enabled=False, level=ground)
    fc = FreeCamera(y=2)
    # fc.enabled = False
    rotation_info = Text(position=window.top_left)

    def update():
        rotation_info.text = str(int(fc.rotation_y)) + '\n' + str(int(fc.rotation_x))


    def input(key):
        if key == 'tab':    # press tab to toggle edit/play mode
            fc.enabled = not fc.enabled
            player.enabled = not player.enabled


    app.run()

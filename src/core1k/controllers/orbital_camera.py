from print_tricks import pt 
from ursina import *

class OrbitalCamera(Entity):
    def __init__(self, 
            controls_center=None, 
            speed=25, 
            *args, **kwargs
        ):
        
        self.active = True  
        
        super().__init__(*args, **kwargs)
        
        # pt.c('------- Orbital Camera --------')
        # pt(self.world_position, self.position, self.world_rotation, self.rotation)
        
        self.controls_center = controls_center
        self.target = camera.ui ##NOTE Setting this to something that I know will always be
                                #### 000. This is for the initial target when you load up the 
                                #### camera with no target yet selected. This saves creating/destroying
                                #### another entity or various other methods. 
        self.distance = 3
        
        self.speed = speed
        self.base_speed = speed  # Save the base speed for resetting
        self.shift_speed = self.base_speed * 6
        self.scroll_speed = self.base_speed / 15
        self.shift_scroll_speed = self.scroll_speed * 6
        self.shift_hold_time = 0  # Variable to keep track of how long shift has been held
        
        self.rotation_speed = 88
        self.mouse_sensitivity = Vec2(40, 40)
        
    def change_targets(self):
        hit_info = mouse.hovered_entity
        if hit_info:
            self.target = hit_info
            # self.position = self.target.world_position + self.forward * -self.distance
            self.distance = (self.world_position - hit_info.world_position).length()
            
        else:
            
            self.target = None
            # pt.ci('else')
            if self.controls_center is not None:
                self.controls_center.cycle_through_active_controllers()
                
    def on_enable(self):
        camera.position = self.position
        camera.world_position = self.world_position
        camera.parent = self
        mouse.locked = False
        camera.fov = 90
        # pt(camera.fov)
    
    
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
        camera.position = self.position
        camera.world_position = self.world_position
        camera.parent = self
        mouse.locked = False
        camera.fov = 90
        
    def on_deactivate(self):
        ...        
    def input(self, key):
        if not self.active: 
            return 


        import math
        # if key == 'left mouse down':
        #     self.change_targets()
            
        if key == 'scroll up':
            if held_keys['left shift']:
                self.distance -= self.shift_scroll_speed
            else:
                self.distance -= self.scroll_speed
        if key == 'scroll down':
            if held_keys['left shift']:
                self.distance += self.shift_scroll_speed
            else:
                self.distance += self.scroll_speed
            
        if key == 'f' and self.target:
            if self.target.model:
                bounding_box = self.target.bounds.size
                x, y, z = bounding_box
                orig_window_x, orig_window_y = window.size
                window_aspect_ratio = orig_window_x / orig_window_y
                bounding_box_aspect_ratio = max(x, y, z)
                
                fov_adjustment = 40.0 / camera.fov # Adjust this constant as needed
                
                self.distance = bounding_box_aspect_ratio * window_aspect_ratio **2 * fov_adjustment
                # pt(camera.fov, x,y,z, orig_window_x, orig_window_y, window_aspect_ratio, bounding_box_aspect_ratio, self.distance)
                
    def update(self):
        if not self.active: 
            return 


        # pt.t('orbital camera')
        if self.target:
            if held_keys['shift']:
                self.speed = self.shift_speed
            else:
                self.speed = self.base_speed  # Reset speed to base speed
                
            if held_keys['right mouse']:
                self.rotation_y += mouse.velocity[0] * self.rotation_speed
                self.rotation_x -= mouse.velocity[1] * self.rotation_speed
                
            if held_keys['e']:
                self.rotation_x -= self.rotation_speed * time.dt * 2
            if held_keys['q']:
                self.rotation_x += self.rotation_speed * time.dt * 2
            if held_keys['a']:
                self.rotation_y += self.rotation_speed * time.dt * 2
            if held_keys['d']:
                self.rotation_y -= self.rotation_speed * time.dt * 2
                
            # self.position = target_position + self.forward * -self.distance
            self.world_position = self.target.world_position + self.forward * -self.distance
            
            if held_keys['w']:
                self.distance -= time.dt * self.speed
            if held_keys['s']:
                self.distance += time.dt * self.speed
                
            # Prevent the camera from going past the target
            if self.distance <= 0:
                self.distance = 0.025



if __name__ == "__main__":
    app = Ursina(size=(1920,1080))
    
    ball = Entity(model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(model='sphere', collider='box', scale=(1,3,1))
    box = Entity(model='cube', collider='box', position=(2, 0, 0))
    
    # cam = EditorCamera()
    cam = OrbitalCamera(
        free_target=Entity(),
        )
    
    app.run()
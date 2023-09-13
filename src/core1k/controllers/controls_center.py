from print_tricks import pt
# pt.easy_imports()

from ursina import *

from core1k.controllers.orbital_camera import OrbitalCamera
from core1k.controllers.free_camera import FreeCamera

class ControlsCenter(Entity):
    def __init__(self, speed=25, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.free_target_base_pos = self.forward * 11
        self.free_target = Entity(
            name='free_target',
            model='cube',
            position=self.free_target_base_pos,
            rotation=(90,0,0),
            color=color.red,
            scale=.03,
            # billboard=True,
            # double_sided=True,
            collider='box',
        )
        
        self.orbital_camera = OrbitalCamera(
            controls_center=self,
            free_target=self.free_target, 
            speed=speed, 
        )
        self.free_camera = FreeCamera(
            free_target=self.free_target
        )
        self.orbital_camera.enabled = False

        # self.free_target.parent = self.free_camera
        self.free_target.parent = camera
    def change_cameras(self):
        # pt('---------- change cameras - -----------')
        info = mouse.hovered_entity
        if info:
            if info.name == self.free_target.name:
                pt.t()
                # self.free_target.parent = None 
                self.free_target.parent = self.free_camera
            self.orbital_camera.enabled = True
            self.orbital_camera.target = info

            self.orbital_camera.position = self.free_camera.position
            self.orbital_camera.rotation = self.free_camera.rotation
            self.free_camera.enabled = False
        else: 
            if self.orbital_camera.enabled:
                self.free_camera.position = self.orbital_camera.position
                self.free_camera.rotation = self.orbital_camera.rotation
                
            self.orbital_camera.target = None
            self.orbital_camera.enabled = False

            self.free_target.parent = camera
            self.free_camera.enabled = True

    def input(self, key):
        if self.orbital_camera.enabled:
            return
        if key == 'left mouse down':
            self.change_cameras()


if __name__ == "__main__":
    app = Ursina(size=(1920,1080))
    
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1))
    box = Entity(name='box', model='cube', collider='box', position=(2, 0, 0))
    
    # cam = FreeCamera()
    # cam = OrbitalCamera()
    cam = ControlsCenter()
    
    app.run()
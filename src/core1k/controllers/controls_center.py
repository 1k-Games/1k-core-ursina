from print_tricks import pt 
from ursina import *
from orbital_camera import OrbitalCamera
from free_camera import FreeCamera

class ControlsCenter(Entity):
    def __init__(self, speed=25, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.orbit_camera = OrbitalCamera(developer_camera=self, speed=speed)
        self.editor_camera = FreeCamera()
        self.orbit_camera.enabled = False

    def change_cameras(self):
        info = mouse.hovered_entity
        if info:
            self.orbit_camera.enabled = True
            self.orbit_camera.target = info

            self.orbit_camera.position = self.editor_camera.position
            self.orbit_camera.rotation = self.editor_camera.rotation
            self.editor_camera.enabled = False
        else: 
            self.orbit_camera.target = None
            self.orbit_camera.enabled = False

            self.editor_camera.position = self.orbit_camera.position
            self.editor_camera.rotation = self.orbit_camera.rotation
            self.editor_camera.enabled = True

    def input(self, key):
        if self.orbit_camera.enabled:
            return
        if key == 'left mouse down':
            self.change_cameras()


if __name__ == "__main__":
    app = Ursina(size=(1920,1080))
    
    ball = Entity(model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(model='sphere', collider='box', scale=(1,3,1))
    box = Entity(model='cube', collider='box', position=(2, 0, 0))
    
    # cam = FreeCamera()
    # cam = OrbitalCamera()
    cam = ControlsCenter()
    
    app.run()
from print_tricks import pt
pt.easy_testing()
pt.easy_imports()

from ursina import *

from core1k.controllers.orbital_camera import OrbitalCamera
from core1k.controllers.free_camera import FreeCamera

class ControlsCenter(Entity):
    def __init__(self, dev_pause_menu=None, game_pause_menu=None, player=None, speed=25, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.dev_pause_menu = dev_pause_menu
        self.game_pause_menu = game_pause_menu
        if self.dev_pause_menu:
            self.dev_pause_menu.enabled = False
        if self.game_pause_menu:
            self.game_pause_menu.enabled = False
        
        if application.development_mode:
            self.setup_editor_cameras(speed, self.position, self.rotation)

    def setup_editor_cameras(self, speed, position, rotation):
        
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
        self.free_camera = FreeCamera(position=position, rotation=rotation,
            free_target=self.free_target
        )
        self.orbital_camera.enabled = False

        # self.free_target.parent = self.free_camera
        self.free_target.parent = camera
        
    def input(self, key):
        
        if key == 'f1':
            pt('down')
        if key =='f1':
            pt(key)
            if dev_pause_menu:
                game_pause_menu.enabled = False
                dev_pause_menu.enabled = True
            else:
                pt('No dev pause menu')
        
        if self.orbital_camera.enabled:
            return
        if key == 'left mouse down':
            self.change_editor_cameras()
        
    def change_editor_cameras(self):
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


if __name__ == "__main__":
    from src.core1k.controllers.orbital_camera import OrbitalCamera
    from src.core1k.controllers.free_camera import FreeCamera
    from src.core1k.controllers.first_person_shooter_controller import FirstPersonShooterController
    from src.core1k.dev_tools.dev_pause_menu import Dev_Pause_Menu
    from src.core1k.dev_tools.game_pause_menu_template import GamePauseMenuTemplate
    
    app = Ursina(size=(1920,1080))
    
    player = FirstPersonShooterController(level=Entity())
    dev_pause_menu = Dev_Pause_Menu()
    game_pause_menu = GamePauseMenuTemplate()
    
    ground = Entity(model='plane', position=(0,-5,0), scale=(100,1,100), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(parent=ground, model='cube', position=(0,1.5,0), world_scale=(1,3,10), rotation_y=45, collider='box', texture='white_cube')
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1))
    box = Entity(name='box', model='cube', collider='box', position=(2, 0, 0))
    
    # cam = FreeCamera()
    # cam = OrbitalCamera()
    cc = ControlsCenter(
        # dev_pause_menu=dev_pause_menu, 
        game_pause_menu=game_pause_menu,
        player=player,
        position=(),
    )
    
    app.run()
    
    '''
    - f1: Dev Pause Menu
    - f2 up: Swap between player & editor cameras from their own last positions
    - f3 up: swap between player & editor cameras from the current camera position.
    
    f2/f3 down: display a tiny menu that shows altnertavite player controllers/camera names
      and the number you can press to activate that one instead. 
        - So you can swap between a 3rd person, first person, new fps, 6dof etc. 
    
    - escape: game pause menu. 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
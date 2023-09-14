from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)

from ursina import *

if __name__ != '__main__':
    from core1k.controllers.orbital_camera import OrbitalCamera
    from core1k.controllers.free_camera import FreeCamera
    
    ## These are the default controllers to be used ONLY if you don't pass your own
    #### controllers to this:
    from core1k.controllers.first_person_shooter_controller import FirstPersonShooterController
    from core1k.dev_tools.dev_pause_menu import DevPauseMenu
    from core1k.dev_tools.game_pause_menu_template import GamePauseMenuTemplate

class ControlsCenter(Entity):
    '''
    Params:
        incoming_name=__name__
        incoming_filename=__file__
        - incoming_name & incoming_filename:
            - Only need to pass this if you are testing a file that is not main.py
                - For example: controls_center.py would need these args
            - Do not need it when running main app (main.py)
            - Do not need it when testing dev_pause_menu (this file).
            
            
        '''
    def __init__(self, 
        dev_pause_menu=None, 
        game_pause_menu=None,
        player=None, 
        speed=25,
        incoming_name=__name__,
        incoming_filename=__file__,
        *args,
        **kwargs):
        
        super().__init__(*args, ignore_paused=True, **kwargs)
        
        ### If player is passed, we will mark it, and have him be the default controller
        ### Else, we import from the example controllers, and set
        ### the free_cam as the default controller. 
        player_was_passed = True if player is not None else False 
        self.player = (player if player is not None 
            else FirstPersonShooterController(level=Entity()))
        
        self.dev_pause_menu = (dev_pause_menu if dev_pause_menu is not None 
            else DevPauseMenu(incoming_name=incoming_name, incoming_filename=incoming_filename))
        
        self.game_pause_menu = (game_pause_menu if game_pause_menu is not None 
            else GamePauseMenuTemplate())
        
        self.saved_states = {}
        
        if application.development_mode:
            self.free_camera, self.orbital_camera = self.setup_editor_cameras(speed, self.position, self.rotation)
            

        
            
        if player_was_passed:
            self.disable_all_but_passed(self.player)
        else:
            self.disable_all_but_passed(self.free_camera)
            
        pt(self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, self.game_pause_menu.enabled, self.player.enabled)
        
    def disable_all_but_passed(self, passed_controller):
        for item in [self.player, self.dev_pause_menu, self.game_pause_menu, self.orbital_camera, self.free_camera]:
            if item != passed_controller:
                item.enabled = False
                
    def input(self, key):
        if key =='f1':
            if self.dev_pause_menu.enabled:
                self.saved_states = {
                    'game_pause_menu': self.game_pause_menu.enabled,
                    'player': self.player.enabled
                }
                self.dev_pause_menu.enabled = False
            else:
                for entity_name, initial_state in self.saved_states.items():
                    entity = getattr(self, entity_name)
                    if entity is not None:
                        entity.enabled = initial_state
                self.dev_pause_menu.enabled = True
                
            pt(key, self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, self.game_pause_menu.enabled, self.player.enabled)
            # application.paused = not application.paused
            # self.dev_pause_menu.enabled = not self.dev_pause_menu.enabled
            
        # if self.orbital_camera.enabled:
        #     return
        
        # if key == 'left mouse down':
        #     self.change_editor_cameras()
        
    def setup_editor_cameras(self, speed, position, rotation):
        
        self.free_target_base_pos = self.forward * 11
        self.free_target = Entity(
            name='free_target',
            model='cube',
            position=self.free_target_base_pos,
            rotation=(90,0,0),
            color=color.red,
            scale=.03,
            collider='box',
        )
        
        orbital_camera = OrbitalCamera(
            controls_center=self,
            free_target=self.free_target, 
            speed=speed, 
            enabled=False,
        )
        free_camera = FreeCamera(position=position, rotation=rotation,
            free_target=self.free_target,
            enabled=False,
        )
        
        
        # self.free_target.parent = self.free_camera
        self.free_target.parent = camera
        
        return free_camera, orbital_camera
        
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
    from src.core1k.dev_tools.dev_pause_menu import DevPauseMenu
    from src.core1k.dev_tools.game_pause_menu_template import GamePauseMenuTemplate
    
    app = Ursina(size=(1920,1080))
    

    ground = Entity(model='plane', position=(0,-5,0), scale=(222,1,222), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(parent=ground, model='cube', world_position=(0,-2.5,0), world_scale=(1,3,10), rotation_y=45, collider='box', texture='white_cube')
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1))
    box = Entity(name='box', model='cube', collider='box', position=(2, 0, 0))
    
    cc = ControlsCenter(
        dev_pause_menu = DevPauseMenu(incoming_name=__name__, incoming_filename=__file__),
        game_pause_menu = GamePauseMenuTemplate(),
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
    
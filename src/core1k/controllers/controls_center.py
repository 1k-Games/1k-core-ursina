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
        player_controllers=None, 
        speed=25,
        incoming_name=__name__,
        incoming_filename=__file__,
        *args,
        **kwargs):
        
        super().__init__(*args, ignore_paused=True, **kwargs)
        
        ### If player is passed, we will mark it, and have him be the default controller
        ### Else, we import from the example controllers, and set
        ### the free_cam as the default controller.
        

        if isinstance(player_controllers, list):
            self.player = player_controllers[0]
        elif player_controllers is not None:
            self.player = player_controllers
        else:
            self.player = FirstPersonShooterController(level=Entity())        
        self.player.enable()
        
        self.dev_pause_menu = (dev_pause_menu if dev_pause_menu is not None 
            else DevPauseMenu(incoming_name=incoming_name, incoming_filename=incoming_filename))
        
        self.game_pause_menu = (game_pause_menu if game_pause_menu is not None 
            else GamePauseMenuTemplate())
        
        
        if application.development_mode:
            self.free_camera, self.orbital_camera = self.setup_editor_cameras(speed, self.position, self.rotation)
            
        self.saved_states = {}
        self.main_items = [        
            self.player, 
            self.dev_pause_menu, 
            self.game_pause_menu, 
            self.free_camera,
            self.orbital_camera
        ]
        
        if player_controllers:
            pt('if')
            self.disable_all_but_passed(self.player)
        else:
            pt('else')
            # self.disable_all_but_passed(self.free_camera)
            self.disable_all_but_passed(self.orbital_camera)
            
        # pt('__init__', self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, self.game_pause_menu.enabled, self.player.enabled)
    
        self.counter = 0

    def disable_all_but_passed(self, passed_controllers):
        if not isinstance(passed_controllers, (list, tuple)):
            passed_controllers = (passed_controllers,)
        
        for item in self.main_items:
            item.disable()

        for item in passed_controllers:
            item.enable()

        pt('disable all but passed:',
        self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, 
        self.game_pause_menu.enabled, self.player.enabled)
        
    def save_current_states(self):
        self.saved_states = {
            'player': self.player.enabled, 
            'dev_pause_menu': self.dev_pause_menu.enabled, 
            'game_pause_menu': self.game_pause_menu.enabled, 
            'free_camera': self.free_camera.enabled, 
            'orbital_camera': self.orbital_camera.enabled
        }
        
    def restore_saved_states(self):
        for entity_name, initial_state in self.saved_states.items():
            entity = getattr(self, entity_name)
            if entity is not None:
                entity.enabled = initial_state
        
    def input(self, key):
        if key =='f1':
            if not self.dev_pause_menu.enabled:
                ## enable
                self.save_current_states()
                self.disable_all_but_passed(self.dev_pause_menu)
                self.dev_pause_menu.enabled = True
            else:
                ## disable
                self.restore_saved_states()
                self.dev_pause_menu.enabled = False
                
            pt(key, mouse.locked, camera.parent,
            self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, 
            self.game_pause_menu.enabled, self.player.enabled)
            # application.paused = not application.paused
            # self.dev_pause_menu.enabled = not self.dev_pause_menu.enabled
            
        # if self.orbital_camera.enabled:
        #     return
        
        # if key == 'left mouse down':
        #     self.change_editor_cameras()
    
    
    def update(self):
        ...
        # Other update code...
        # self.player.enabled=True
        # Increment the counter
        # self.counter += 1

        # # Check if the counter is odd or even
        # if self.counter % 2 == 0:
        #     # If the counter is even, disable the player
        #     self.player.enabled = False
        # else:
        #     # If the counter is odd, enable the player
        #     self.player.enabled = True
        # camera.parent = self.player.camera_boom 
        # if pt.r(seconds=1.9):
            # pt(self.free_camera.enabled, camera.parent)
        # pt.t(self.player.enabled)
    
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
            speed=speed
        )
        free_camera = FreeCamera(position=position, rotation=rotation,
            free_target=self.free_target,
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
    from src.core1k.controllers.third_person_controller import ThirdPersonController
    
    from src.core1k.dev_tools.dev_pause_menu import DevPauseMenu
    from src.core1k.dev_tools.game_pause_menu_template import GamePauseMenuTemplate
    
    app = Ursina(size=(1920,1080))
    

    ground = Entity(model='plane', position=(0,-5,0), scale=(222,1,222), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(parent=ground, model='cube', world_position=(0,-2.5,0), world_scale=(1,3,10), rotation_y=45, collider='box', texture='white_cube')
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 0, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1))
    box = Entity(name='box', model='cube', collider='box', position=(2, 0, 0))
    
    cc = ControlsCenter(
        position=(0,4,-22), rotation=(11,0,0),
        dev_pause_menu=DevPauseMenu(incoming_name=__name__, incoming_filename=__file__),
        game_pause_menu=GamePauseMenuTemplate(),
        # player_controllers=ThirdPersonController(use_actor=False, z=-12)
        # player = FirstPersonShooterController(position=(0,6,-11), level=Entity()),
    )
    
    app.run()
    
    '''
    - esc: game pause menu. 
    - f1: Dev Pause Menu
    - f2 up: Swap between player & editor cameras from their own last positions
    - f3 up: swap between player & editor cameras from the current camera position.
    - f4: Swap between various player controllers or dev_controllers
    
    f2/f3 down: display a tiny menu that shows alternative player
        controllers/dev controllers and the hotkey for it. 
        - Hotkey example: f2+2 (swap to the second controller on that list)
        - So you can swap between a 3rd person, first person, new fps, 6dof etc. 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
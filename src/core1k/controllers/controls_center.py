'''TODO

    - refactor the disable_all stuff. I don't think that is necessary to do.
        - maybe just disable all once in the very beginning.
        - Actually, there is a bug with the way I want to do it (some of the functions
        use my new way and some use disable all.) 
            - Bug: if not all are disabled then sometimes a menu button is currently 
            active while a new controller is being used. 
            - Fix: Either, everything uses the disable all, or I also get a list of the 
            menus, like I have a list of the dev_controllers and player controllers. And then
            disable those in the other functions. 
            
    - f4 should swaps cams to same position
    
    - f4/f3 code are basically identical (I think). combine if possible. 
    
    - orbital cam shouldn't set itself to 000 every time. 
        - 000 at the beginning
        - last pos/rot he was in if using f2. 
        - last pos/rot of last_controller if using f3/f4. But how?
            - He gets them as the target first. 
            - then He gets their pos and their rotation.
            
    - free+orbital cams:
        - Cams should switch between each other when clicked/unclicked. 
        
    - Text size bug:
        - When running each menu on their own, I get one text, but when running from 
        controls_center, I get a different sized text. 
    '''

from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)

from ursina import *

if __name__ != '__main__':
    from core1k.controllers.orbital_camera import OrbitalCamera
    from core1k.controllers.free_camera import FreeCamera
    
    ## These are the default controllers to be used ONLY if you don't pass your own
    
    from core1k.controllers.first_person_shooter_controller import FirstPersonShooterController
    from core1k.controllers.third_person_controller import ThirdPersonController
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
    Controls:
        - esc: game pause menu. 
        - f1: Dev Pause Menu
        - f2 up: Swap between player & editor cameras from their own last positions
        - f3 up: swap between player & editor cameras from the current camera position.
        - f4: Swap between all of the available player controllers if you are on them, 
            or dev controllers if you are on those)
        
        Not yet implemented:
            - f2/f3 down: display a tiny menu that shows alternative player
                controllers/dev controllers and the hotkey for it. 
                - Hotkey example: f2+2 (swap to the second controller on that list)
                - So you can swap between a 3rd person, first person, new fps, 6dof etc. 
            
            
            '''
class ControlsCenter(Entity):
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
        
        self.setup_key_actions()
        self.setup_controller_indices()
        self.setup_player_controllers(player_controllers)
        self.setup_pause_menus(dev_pause_menu, game_pause_menu, incoming_name, incoming_filename)
        self.setup_dev_controllers(speed)
        self.setup_main_items()
        self.setup_initial_controller(player_controllers)
        self.counter = 0
        
    def setup_key_actions(self):
        self.key_actions = {
            'escape': self.toggle_game_pause_menu,
            'f1': self.toggle_dev_pause_menu,
            'f2': self.switch_controllers,
            'f3': self.switch_controllers,
            'f4': self.switch_active_controller
        }
        
    def setup_controller_indices(self):
        self.cur_player_index = 0
        self.cur_dev_controller_index = 0
        
    def setup_player_controllers(self, player_controllers):
        if player_controllers is not None:
            self.player_controllers = player_controllers if isinstance(player_controllers, (list, tuple)) else (player_controllers,)
            self.cur_player_controller = self.player_controllers[self.cur_player_index]
        else:
            self.player_controllers = (
                FirstPersonShooterController(level=Entity()), 
                ThirdPersonController(use_actor=False) 
            )
            self.cur_player_controller = self.player_controllers[0]
            
    def setup_pause_menus(self, dev_pause_menu, game_pause_menu, incoming_name, incoming_filename):
        self.dev_pause_menu = dev_pause_menu if dev_pause_menu is not None else DevPauseMenu(incoming_name=incoming_name, incoming_filename=incoming_filename)
        self.game_pause_menu = game_pause_menu if game_pause_menu is not None else GamePauseMenuTemplate()
        
    def setup_dev_controllers(self, speed):
        if application.development_mode:
            self.free_camera, self.orbital_camera = self.dev_controllers = self.setup_editor_cameras(speed, self.position, self.rotation)
        self.cur_dev_controller = self.dev_controllers[0]
        
    def setup_main_items(self):
        self.saved_states = {}
        self.main_items = tuple([self.game_pause_menu, self.dev_pause_menu] + list(self.dev_controllers) + list(self.player_controllers))
        
    def setup_initial_controller(self, player_controllers):
        if player_controllers:
            pt('if')
            self.disable_all_but_passed(self.cur_player_controller)
        else:
            pt('else')
            self.disable_all_but_passed(self.orbital_camera)
            
    def toggle_game_pause_menu(self):
        if not self.game_pause_menu.enabled:
            ## enable
            self.save_current_states()
            self.disable_all_but_passed(self.game_pause_menu)
            self.game_pause_menu.enabled = True
        else:
            ## disable
            self.restore_saved_states()
            self.game_pause_menu.enabled = False
            
    def toggle_dev_pause_menu(self):
        if not self.dev_pause_menu.enabled:
            ## enable
            self.save_current_states()
            self.disable_all_but_passed(self.dev_pause_menu)
            self.dev_pause_menu.enabled = True
        else:
            ## disable
            self.restore_saved_states()
            self.dev_pause_menu.enabled = False
            
    # def switch_active_controller(self):
    #     if self.cur_player_controller.enabled:
    #         self.cur_player_index = (self.cur_player_index + 1) % len(self.player_controllers)
    #         self.cur_player_controller = self.player_controllers[self.cur_player_index]
    #         self.disable_all_but_passed(self.cur_player_controller)
    #     else:
    #         self.cur_dev_controller_index = (self.cur_dev_controller_index + 1) % len(self.dev_controllers)
    #         self.cur_dev_controller = self.dev_controllers[self.cur_dev_controller_index]
    #         self.disable_all_but_passed(self.cur_dev_controller)

    def switch_active_controller(self):
        if self.cur_player_controller.enabled:
            self.cur_player_index = (self.cur_player_index + 1) % len(self.player_controllers)
            new_controller = self.player_controllers[self.cur_player_index]
            self.switch_controllers(self.cur_player_controller, new_controller, switch_position=True)
            self.cur_player_controller = new_controller
        else:
            self.cur_dev_controller_index = (self.cur_dev_controller_index + 1) % len(self.dev_controllers)
            new_controller = self.dev_controllers[self.cur_dev_controller_index]
            self.switch_controllers(self.cur_dev_controller, new_controller, switch_position=True)
            self.cur_dev_controller = new_controller
        
    def switch_controller(self, controllers, controller_index, other_controller):
        controller_index = (controller_index + 1) % len(controllers)
        current_controller = controllers[controller_index]
        self.disable_all_but_passed(current_controller)

        # Save the position and rotation of the current controller
        new_pos = current_controller.world_position
        new_rot = current_controller.world_rotation

        # Switch to the next controller
        self.switch_controllers(current_controller, other_controller, switch_position=True)

    def switch_controllers(self, controller1, controller2, switch_position=False):
        controller1.enabled = False
        controller2.enabled = True

        if switch_position:
            new_pos = controller1.world_position
            new_rot = controller1.world_rotation

            controller2.position = new_pos
            controller2.rotation = new_rot
        
    def disable_all_but_passed(self, passed_controllers):
        if not isinstance(passed_controllers, (list, tuple)):
            passed_controllers = (passed_controllers,)
        
        for item in self.main_items:
            item.disable()
            
        for item in passed_controllers:
            item.enable()
            
        pt('disable all but passed:',
        self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, 
        self.game_pause_menu.enabled, self.cur_player_controller.enabled)
        
    def save_current_states(self):
        self.saved_states = {
            'cur_player_controller': self.cur_player_controller.enabled,
            'cur_dev_controller': self.cur_dev_controller.enabled,
            'dev_pause_menu': self.dev_pause_menu.enabled,
            'game_pause_menu': self.game_pause_menu.enabled,
        }
        
    def restore_saved_states(self):
        for entity_name, initial_state in self.saved_states.items():
            entity = getattr(self, entity_name)
            if entity is not None:
                entity.enabled = initial_state
        
    # def input(self, key):
    #     if key in self.key_actions:
    #         self.key_actions[key]()
            
    def input(self, key):
        if key in self.key_actions:
            if key in ['f2', 'f3']:
                active_controller = self.cur_player_controller if self.cur_player_controller.enabled else self.cur_dev_controller
                inactive_controller = self.cur_dev_controller if self.cur_player_controller.enabled else self.cur_player_controller
                switch_position = True if key == 'f3' else False
                self.key_actions[key](active_controller, inactive_controller, switch_position)
            else:
                self.key_actions[key]()
            
            # application.paused = not application.paused
            # self.dev_pause_menu.enabled = not self.dev_pause_menu.enabled
            
        # if self.orbital_camera.enabled:
        #     return
        
        # if key == 'left mouse down':
        #     self.change_editor_cameras()
    
    
    def update(self):
        ...
        # Other update code...
        # self.cur_player_controller.enabled=True
        # Increment the counter
        # self.counter += 1

        # # Check if the counter is odd or even
        # if self.counter % 2 == 0:
        #     # If the counter is even, disable the player
        #     self.cur_player_controller.enabled = False
        # else:
        #     # If the counter is odd, enable the player
        #     self.cur_player_controller.enabled = True
        # camera.parent = self.cur_player_controller.camera_boom 
        # if pt.r(seconds=1.9):
            # pt(self.free_camera.enabled, camera.parent)
        # pt.t(self.cur_player_controller.enabled)
    
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
            speed=speed
        )
        free_camera = FreeCamera(position=position, rotation=rotation,
            free_target=self.free_target,
        )
        
        
        # self.free_target.parent = self.free_camera
        self.free_target.parent = camera
        
        return free_camera, orbital_camera

    def change_editor_cameras(self):
        pt('---------- change cameras - -----------')
        pt.ex()
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
    

    ground = Entity(model='plane', position=(0,0,0), scale=(222,1,222), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(parent=ground, model='cube', world_position=(0,2.5,0), world_scale=(1,3,10), rotation_y=45, collider='box', texture='white_cube')
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 5, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1), position=(0,5,0))
    box = Entity(name='box', model='cube', collider='box', position=(2, 5, 0))
    
    cc = ControlsCenter(
        position=(0,4,-22), rotation=(11,0,0),
        dev_pause_menu=DevPauseMenu(incoming_name=__name__, incoming_filename=__file__),
        game_pause_menu=GamePauseMenuTemplate(),      
        player_controllers=(
            ThirdPersonController(
                use_actor=False, 
                z=-12),
            FirstPersonShooterController(
                position=(0,6,-11), 
                level=Entity()))
        )
    
    app.run()
    
    '''

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
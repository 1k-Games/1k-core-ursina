'''TODO

    - Possibly: refactor the disable_all stuff. I don't think that is necessary to do.
        - maybe just disable all once in the very beginning.
        - Actually, there is a bug that will happen if I switch to not using this: 
            - Bug: if not all are disabled then sometimes a menu button is currently 
            active while a new controller is being used. 
            - Fix: Either, everything uses the disable all, or I also get a list of the 
            menus, like I have a list of the dev_controllers and player controllers. And then
            disable those in the other functions. 
            
    positioner_3d - cube/uv's are wrong
        - In blender, I have the UV's or something wrong. 
        - by default, it shows me y as forward instead of z. 
        
        - While I am fixing the cube in blender, I need to remove these lines to test properly
            in dev_pause_menu:
                self.positioner_3d.rotation_y += 180
                self.positioner_3d.rotation_z += 33
                
    - Reticle/targets/positioner:
        - Free_cam: Need to get rid of free_cam target when switching off. 
        
    - Dev Menu 
        - positioners - information gathering
            - Can drag them over an object to change into the shape/size of that object. 
            - How to:
                - drag so mouse is over your target. 
                - Click a button or hotkey like "r"
        - Pressing Resume button should do the same thing as pressing the 'f1' key again (disable dev menu)
            - Perhaps just need to take any logit out of resume function, and redirect it to the 
            controls_controlle if it exists.
            
    - Print out The Name, attributes, (including model path, texture path etc) of 
        anything I click on. Possibly in another thread because entities seem to 
        cause a large amount of lag/stutter. 
        
    - Menus:
        - neither menu is pausing (i must have deleted that code)
            - figure out the best approach for them to do it themselves and
            for them to do it if they are being controlled by a 3rd party controller. 
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
    from core1k.dev_tools.menu_1k import MenuTemplate
    
class ControlsCenter(Entity):
    '''
    Params:
        dev_pause_menu=None (optional)
        game_pause_menu=None (optional)
        player_controllers=None (optional)
        incoming_name=__name__ (optional)
        incoming_filename=__file__ (optional)
        - incoming_name & incoming_filename:
            - Purpose
                - To track down which .py file actually needs to be restarted 
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
                controllers/dev controllers and the hotkey for each one. 
                - Hotkey example: f2+2 (swap to the second controller on that list)
                - So you can swap between a 3rd person, first person, new fps, 6dof etc. 
            
            
            '''
class ControlsCenter(Entity):
    def __init__(self, 
        dev_pause_menu=None, 
        game_pause_menu=None,
        player_controllers=None, 
        incoming_name=__name__,
        incoming_filename=__file__,
        *args,
        **kwargs
    ):
        
        super().__init__(*args, ignore_paused=True, **kwargs)
        
        pt.c('------- Controls Center --------')
        pt(self.world_position, self.position, self.world_rotation, self.rotation)
        
        self.setup_key_actions()
        self.setup_controller_indices()
        self.setup_dev_controllers()
        self.setup_player_controllers(player_controllers)
        self.all_controllers = self.dev_controllers + self.player_controllers
        self.set_controls_center_for_controllers()
        self.setup_pause_menus(dev_pause_menu, game_pause_menu, incoming_name, incoming_filename)
        self.setup_main_items()
        self.setup_initial_controller(player_controllers)
        self.setup_positions_rotations()
        
    def setup_positions_rotations(self):
        # pt.c('/////////// CC - setup positions rotations ///////////')
        if not self.world_position == (0,0,0) and not self.world_rotation == (0,0,0):
            camera.world_position=(0,0,0)
            camera.position=(0,0,0)
            for controller in self.all_controllers:
                # pt(1, controller.name, controller.world_position, controller.world_rotation)
                if controller.world_position == (0,0,0):
                    controller.world_position = self.position
                if controller.world_rotation == (0,0,0):
                    controller.world_rotation = self.rotation
                # pt(2, controller.name, controller.world_position, controller.world_rotation)
                    
    def set_controls_center_for_controllers(self):
        for controller in self.all_controllers:
            controller.controls_center = self
            # pt(controller, controller.controls_center)
            
    def setup_key_actions(self):
        self.key_actions = {
            'escape': self.toggle_game_pause_menu,
            'f1': self.toggle_dev_pause_menu,
            'f2': lambda: self.cycle_and_switch_to_next_controllers(
                self.cur_player_controller if self.cur_player_controller.enabled else self.cur_dev_controller,
                self.cur_dev_controller if self.cur_player_controller.enabled else self.cur_player_controller,
                switch_positions=False
            ),
            'f3': lambda: self.cycle_and_switch_to_next_controllers(
                self.cur_player_controller if self.cur_player_controller.enabled else self.cur_dev_controller,
                self.cur_dev_controller if self.cur_player_controller.enabled else self.cur_player_controller,
                switch_positions=True
            ),
            'f4': self.cycle_through_active_controllers
        }
        
    def setup_controller_indices(self):
        self.cur_player_index = 0
        self.cur_dev_controller_index = 0
        
    def setup_player_controllers(self, player_controllers):
        if player_controllers is not None:
            self.player_controllers = player_controllers if isinstance(player_controllers, (list, tuple)) else (player_controllers,)
            self.cur_player_controller = self.player_controllers[self.cur_player_index]
            
        else:
            ## NO Controllers were passed, so pass in some default ones. 
            self.player_controllers = (
                FirstPersonShooterController(level=Entity()), 
                ThirdPersonController(use_actor=False) 
            )
            self.cur_player_controller = self.player_controllers[0]
            
    def setup_pause_menus(self, dev_pause_menu, game_pause_menu, incoming_name, incoming_filename):
        self.dev_pause_menu = dev_pause_menu if dev_pause_menu is not None else DevPauseMenu(incoming_name=incoming_name, incoming_filename=incoming_filename)
        self.game_pause_menu = game_pause_menu if game_pause_menu is not None else MenuTemplate()
        
    def setup_dev_controllers(self):
        if application.development_mode:
            self.free_camera, self.orbital_camera = self.dev_controllers = self.setup_editor_cameras(self.position, self.rotation)
        self.cur_dev_controller = self.dev_controllers[0]
        # pt(self.cur_dev_controller)
        # pt(self.dev_controllers)
        
    def setup_main_items(self):
        self.saved_states = {}
        self.main_items = tuple([self.game_pause_menu, self.dev_pause_menu] + list(self.dev_controllers) + list(self.player_controllers))
        
    def setup_initial_controller(self, player_controllers):
        if player_controllers:
            pt('if player controllers')
            self.disable_all_controllers_except_given(self.cur_player_controller)
        else:
            pt('else player controllers')
            self.disable_all_controllers_except_given(self.cur_dev_controller)
            
    def toggle_game_pause_menu(self):
        if not self.game_pause_menu.enabled:
            ## enable
            self.save_current_states()
            self.disable_all_controllers_except_given(self.game_pause_menu)
            self.game_pause_menu.enabled = True
        else:
            ## disable
            self.restore_saved_states()
            self.game_pause_menu.enabled = False
            
    def toggle_dev_pause_menu(self):
        if not self.dev_pause_menu.enabled:
            ## enable
            self.save_current_states()
            self.disable_all_controllers_except_given(self.dev_pause_menu)
            self.dev_pause_menu.enabled = True
        else:
            ## disable
            self.restore_saved_states()
            self.dev_pause_menu.enabled = False
            
    def cycle_through_active_controllers(self):
        if self.cur_player_controller.enabled:
            self.cur_player_index = (self.cur_player_index + 1) % len(self.player_controllers)
            new_controller = self.player_controllers[self.cur_player_index]
            self.cycle_and_switch_to_next_controllers(self.cur_player_controller, new_controller, switch_positions=True)
            self.cur_player_controller = new_controller
        else:
            self.cur_dev_controller_index = (self.cur_dev_controller_index + 1) % len(self.dev_controllers)
            new_controller = self.dev_controllers[self.cur_dev_controller_index]
            self.cycle_and_switch_to_next_controllers(self.cur_dev_controller, new_controller, switch_positions=True)
            self.cur_dev_controller = new_controller
        
    def cycle_and_switch_to_next_controllers(self, controller1, controller2, switch_positions=False):
        if switch_positions:
            new_pos = controller1.world_position
            new_rot = controller1.world_rotation
            controller2.position = new_pos
            controller2.rotation = new_rot

        controller1.enabled = False
        controller2.enabled = True

        # if switch_positions:
        
    def disable_all_controllers_except_given(self, passed_controllers):
        if not isinstance(passed_controllers, (list, tuple)):
            passed_controllers = (passed_controllers,)
        
        for item in self.main_items:
            item.disable()
            
        for item in passed_controllers:
            item.enable()
            
        # pt('disable all but passed:',
        # self.orbital_camera.enabled, self.free_camera.enabled, self.dev_pause_menu.enabled, 
        # self.game_pause_menu.enabled, self.cur_player_controller.enabled)
        
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
            
    def input(self, key):
        if key in self.key_actions:
            self.key_actions[key]()
            
    def update(self):
        ...
        
    def setup_editor_cameras(self, position, rotation):
        
        self.free_target_base_pos = self.forward * 11
        self.free_target = Entity(
            name='free_target',
            model='cube',
            position=self.free_target_base_pos,
            rotation=(90,0,0),
            color=color.red,
            scale=.13,
            collider='box',
            enabled=False,
        )
        
        orbital_camera = OrbitalCamera(
            controls_center=self,
        )
        free_camera = FreeCamera(position=position, rotation=rotation,
            free_target=self.free_target,
        )
        
        # self.free_target.parent = self.free_camera
        self.free_target.parent = camera
        
        return free_camera, orbital_camera
    
    def change_editor_cameras(self, hit_info=None):
        pt('---------- change cameras - -----------')
        
        # if self.orbital_camera.enabled:
        #     self.free_camera.position = self.orbital_camera.position
        #     self.free_camera.rotation = self.orbital_camera.rotation
            
        # self.orbital_camera.target = None
        # self.orbital_camera.enabled = False
        
        # self.free_target.parent = camera
        # self.free_camera.enabled = True
        
if __name__ == "__main__":
    from src.core1k.controllers.orbital_camera import OrbitalCamera
    from src.core1k.controllers.free_camera import FreeCamera
    from src.core1k.controllers.first_person_shooter_controller import FirstPersonShooterController
    from src.core1k.controllers.third_person_controller import ThirdPersonController
    
    from src.core1k.dev_tools.dev_pause_menu import DevPauseMenu
    from src.core1k.dev_tools.menu_1k import MenuTemplate
    
    app = Ursina(size=(1920,1080))
    
    ground = Entity(model='plane', position=(0,0,0), scale=(222,1,222), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    wall = Entity(parent=ground, model='cube', world_position=(0,2.5,0), world_scale=(1,3,10), rotation_y=45, collider='box', texture='white_cube')
    ball = Entity(name='ball', model='sphere', collider='sphere', position=(-2, 5, 0))
    cyl = Entity(name='cyl', model='sphere', collider='box', scale=(1,3,1), position=(0,5,0))
    box = Entity(name='box', model='cube', collider='box', position=(2, 5, 0))
    
    cc = ControlsCenter(
        position=(3,6,-9), rotation=(5,5,0),
        dev_pause_menu=DevPauseMenu(incoming_name=__name__, incoming_filename=__file__),
        game_pause_menu=MenuTemplate(),      
        player_controllers=(
            FirstPersonShooterController(
                position=(0,6,-11), 
                level=Entity(),
                ),
            ThirdPersonController(
                use_actor=False, 
                # position=(0,2,-12),
                ),
        )
    )
    
    app.run()
    
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
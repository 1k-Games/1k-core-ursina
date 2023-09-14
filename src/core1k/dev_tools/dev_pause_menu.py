''' TODO

- Pass a parent, so we can see what positions/rotations in regards to the parent
- Pass a model to both the positioners so they look correct each time. 
- Create a separate class called "DevPauseMenu" and it's only functions are
    to load an instance of DevPauseMenu and then accept "esc" input
    which will enable/disable the entire DevPauseMenu without me needing to do it for
    every single entity. 
    
    - After this is complete, re-write the code so individual buttons/text/draggables
        aren't being enabled/disabled anymore. 

'''
import sys, subprocess
from pathlib import Path
from os.path import abspath

from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)


from ursina import *
    
class DevPauseMenu(Entity):
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
        player=None,
        ui_positioner_ent=None, 
        ui_p_parent=None, 
        scene_positioner_ent=None,
        scene_p_parent=None,
        incoming_name=__name__,
        incoming_filename=__file__,
        enabled=False,
        **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True, enabled=enabled, **kwargs)
        pt.c('---- Dev Pause Menu ----')
        self.quit_key = 'x'
        self.restart_key = 'r'
        self.dev_menu_key = 'f1'
        self.menu_shown = True  ## Enable the ability to press button to hide, the menu while remaining paused. 
        self.menu_visual_items = Entity()
        
        
        self.set_restart_filename(incoming_name, incoming_filename)
        
        self.p_menu()
        
    def set_restart_filename(self, incoming_name, incoming_filename):
        ### Restarting the File - Setting the originating_file so we know what to restart. 
        sys_argv = sys.argv[0]
        if incoming_name == '__main__':
            self.originating_file = incoming_filename
        elif sys_argv.endswith('.py'):
            self.originating_file = sys_argv
        else:
            self.originating_file = Path(f'{abspath(sys_argv)}/main.py')
            
        # pt(incoming_name, incoming_filename, sys_argv, self.originating_file)
        
    def update(self):
        if held_keys['right mouse']:
            if held_keys['left mouse']:
                self.scene_positioner.world_z += mouse.velocity[1] * 150
            else:
                self.scene_positioner.world_rotation_y -= mouse.velocity[0] * 150
                self.scene_positioner.world_rotation_x += mouse.velocity[1] * 200
        if held_keys['middle mouse']:
            self.scene_positioner.world_rotation_z += mouse.velocity[0] * 150
            
        if held_keys['w']:
            self.scene_positioner.rotation_x += time.dt * 100
        if held_keys['s']:
            self.scene_positioner.rotation_x -= time.dt * 100
        if held_keys['a']:
            self.scene_positioner.rotation_y += time.dt * 100
        if held_keys['d']:
            self.scene_positioner.rotation_y -= time.dt * 100
        if held_keys['e']:
            self.scene_positioner.rotation_z += time.dt * 100
        if held_keys['q']:
            self.scene_positioner.rotation_z -= time.dt * 100

        ## Scale
        if held_keys['up arrow']:
            self.scene_positioner.scale += Vec3(time.dt, time.dt, time.dt)
        if held_keys['down arrow']:
            self.scene_positioner.scale -= Vec3(time.dt, time.dt, time.dt)
        
        ## Texture Scale
        if held_keys['home']:
            self.scene_positioner.texture_scale += Vec2(time.dt, 0)
        if held_keys['end']:
            self.scene_positioner.texture_scale -= Vec2(time.dt, 0)
        if held_keys['page up']:
            self.scene_positioner.texture_scale += Vec2(0, time.dt)
        if held_keys['page down']:
            self.scene_positioner.texture_scale -= Vec2(0, time.dt)

    def input(self, key):
        if self.menu_shown: ## Allows us to pause the game, but still move about the world 
            if key == self.quit_key:
                self.exit()
            if key == self.restart_key:
                self.restart()
    
    def on_enable(self):
        mouse.locked = False
        
    def on_disable(self):
        ...
        
    def p_menu(self):
        self.paused_text = Text('Paused', x=0, y=.44,background=True, size=62, parent=self)
        self.resume_b = Button(y=.11,  scale=(.2, .1),      text=f'Resume ({self.dev_menu_key})', on_click = self.pause_resume,  ignore_paused=True, parent=self)
        self.restart_b = Button(y=-.11, scale=(.2, .1),    text=f'Restart ({self.restart_key})', on_click = self.restart,  ignore_paused=True, parent=self)
        self.exit_b   = Button(y=-.22, scale=(.2, .1),      text=f'Exit ({self.quit_key})', on_click = self.exit,  ignore_paused=True, parent=self)
        
        Text.size = .012
        self.reset_scene_p_b = Button(x=.44, y=.38, scale=(.1, .05), text=f'Reset Scene Positioner', on_click = self.reset_scene_positioner,  ignore_paused=True, parent=self)
        self.default_scene_positioner_pos = camera.ui.world_position + Vec3(4,3,10)
        self.default_scene_positioner_rot = (7,-13,22)
        
        Text.size = .020
        self.ui_positioner = Draggable(
            scale=(self.exit_b.scale),
            texture='..\\assets\\Square_Border',
            position=Vec2(-.225,.225),
            text="UI Positioner", color=color.hsv(360,1,1,.05), on_click=lambda: print(f"UI Positioner: {self.ui_positioner.position}"), z=-300,  ignore_paused=True, parent=self)
        
        Text.size = .010
        self.scene_positioner = Draggable(
            parent=scene,
            # model='cube',
            model='..\\assets\\scene_positioner_cube.obj',
            double_sided=True,
            text="Scene\nPositioner",
            scale=(1,1,1),
            texture='..\\assets\\colored_axis_cube',
            position=self.default_scene_positioner_pos,
            rotation=self.default_scene_positioner_rot,
            # color=color.hsv(360,1,1,.05),
            enabled=False,
            ignore_paused=True, 
            on_click=lambda: print(
                f"Scene Positioner:\n"
                f"    pos = {self.ui_positioner.position}, world_pos = {self.ui_positioner.world_position}\n"
                f"    rot = {self.ui_positioner.rotation}, world_rot = {self.scene_positioner.world_rotation}"
                )
            )
        # Text.size = .25
        # text_sp = Text(text="Scene\nPositioner", position=(-.33,.1,0), parent=self.scene_positioner, billboard=True)
    
    def reset_scene_positioner(self):
        self.scene_positioner.position = self.default_scene_positioner_pos
        self.scene_positioner.rotation = self.default_scene_positioner_rot
        
    def pause_resume(self):
        # application.paused = not application.paused
        # mouse.locked = not application.paused
        
        mouse.position = self.restart_b.position
        
        self.scene_positioner.enabled = not self.scene_positioner.enabled 
        
        self.enabled = not self.enabled
        
    def dev_cam(self):
        pt('dev cam')
        self.editor_camera.enabled = not self.editor_camera.enabled
        # mouse.locked = not application.paused
        # pt(mouse.locked)
        if self.enabled:
            self.disable()
            self.scene_positioner.disable()
            self.reset_scene_positioner()

        
        if self.player is not None:
            self.player.reticle.enabled = not self.editor_camera.enabled
            self.player.visible_self = not self.editor_camera.enabled
            # mouse.locked = not self.editor_camera.enabled
            
            sp = self.player.position
            self.editor_camera.position = Vec3(sp.x, sp.y+3, sp.z)
            self.editor_camera.world_rotation = self.player.world_rotation
        
    def restart(self):
        command = ['python', self.originating_file]
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
        
    def exit(self):
        application.quit()




if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina(size=(1920,1080))
    
    dev_pause_menu = DevPauseMenu(enabled=False)
    
    def input(key):
        if key == dev_pause_menu.dev_menu_key:
            dev_pause_menu.enabled = not dev_pause_menu.enabled
                
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    player = FirstPersonController(y=2, origin_y=-.5)

    app.run()
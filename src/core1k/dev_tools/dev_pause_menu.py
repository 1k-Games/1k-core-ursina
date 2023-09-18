''' TODO

- Pass a parent, so we can see what positions/rotations in regards to the parent


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
        positioner_ui_ent=None, 
        ui_p_parent=None, 
        positioner_3d_ent=None,
        scene_p_parent=None,
        incoming_name=__name__,
        incoming_filename=__file__,
        enabled=False,
        **kwargs):
        
        positioner_3d_saved_attributes = [
            'world_rotation', 
            'rotation', 
            'world_scale',
            'scale', 
            'texture_scale'
            ]
        
        self.setup_positioner_3d(positioner_3d_saved_attributes)
        super().__init__(parent=camera.ui, ignore_paused=True, enabled=enabled, **kwargs)
        
        pt.c('---- Dev Pause Menu ----')
        self.quit_key = 'x'
        self.restart_key = 'r'
        self.dev_menu_key = 'f1'
        self.menu_shown = True  ## Enable the ability to press button to hide the menu while remaining paused. 
        self.menu_visual_items = Entity()
                
        self.set_restart_filename(incoming_name, incoming_filename)
        
        self.p_menu()
        
    def setup_positioner_3d(self, positioner_3d_saved_attributes):
        self.has_reset_positioner_3d_been_ran = False
        self.positioner_3d = Draggable(
            parent=scene,
            scale=1,
            enabled=True,
            double_sided=True,
            ignore_paused=True,

            # model='cube',
            model='..\\assets\\positioner_3d_cube.obj',
            texture='..\\assets\\colored_axis_cube',
            text="Positioner\n3d",
            # color=color.hsv(360,1,1,.05),
            on_click=lambda: print(
                f"Positioner 3d:\n"
                f"    pos = {self.positioner_ui.position}, world_pos = {self.positioner_ui.world_position}\n"
                f"    rot = {self.positioner_ui.rotation}, world_rot = {self.positioner_3d.world_rotation}"
                )
        )
        self.default_positioner_3d_values = {name: getattr(self.positioner_3d, name) for name in positioner_3d_saved_attributes}
        
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
                self.positioner_3d.world_z += mouse.velocity[1] * 150
            else:
                self.positioner_3d.world_rotation_y -= mouse.velocity[0] * 150
                self.positioner_3d.world_rotation_x += mouse.velocity[1] * 200
        if held_keys['middle mouse']:
            self.positioner_3d.world_rotation_z += mouse.velocity[0] * 150
            
        if held_keys['w']:
            self.positioner_3d.rotation_x += time.dt * 100
        if held_keys['s']:
            self.positioner_3d.rotation_x -= time.dt * 100
        if held_keys['a']:
            self.positioner_3d.rotation_y += time.dt * 100
        if held_keys['d']:
            self.positioner_3d.rotation_y -= time.dt * 100
        if held_keys['e']:
            self.positioner_3d.rotation_z += time.dt * 100
        if held_keys['q']:
            self.positioner_3d.rotation_z -= time.dt * 100

        ## Scale
        if held_keys['up arrow']:
            self.positioner_3d.scale += Vec3(time.dt, time.dt, time.dt)
        if held_keys['down arrow']:
            self.positioner_3d.scale -= Vec3(time.dt, time.dt, time.dt)
        
        ## Texture Scale
        if held_keys['home']:
            self.positioner_3d.texture_scale += Vec2(time.dt, 0)
        if held_keys['end']:
            self.positioner_3d.texture_scale -= Vec2(time.dt, 0)
        if held_keys['page up']:
            self.positioner_3d.texture_scale += Vec2(0, time.dt)
        if held_keys['page down']:
            self.positioner_3d.texture_scale -= Vec2(0, time.dt)
        
    def input(self, key):
        if self.menu_shown: ## Allows us to pause the game, but still move about the world 
            if key == self.quit_key:
                self.exit()
            if key == self.restart_key:
                self.restart()
                
    def on_enable(self):
        self.positioner_3d.enabled = True
        self.reset_positioner_3d()
        mouse.locked = False
        try:
            mouse.position = restart_b.position
        except:
            mouse.position = (0,0,0)
            pt(mouse.position)
            ...
            
    def on_disable(self):
        # self.positioner_3d.parent = camera.ui
        self.positioner_3d.enabled = False
        ...
        
    def p_menu(self):
        self.paused_text = Text('Paused', x=0, y=.44,background=True, size=62, parent=self)
        self.resume_b = Button(y=.11,  scale=(.2, .1),      text=f'Resume ({self.dev_menu_key})', on_click = self.resume,  ignore_paused=True, parent=self)
        self.restart_b = Button(y=-.11, scale=(.2, .1),    text=f'Restart ({self.restart_key})', on_click = self.restart,  ignore_paused=True, parent=self)
        self.exit_b   = Button(y=-.22, scale=(.2, .1),      text=f'Exit ({self.quit_key})', on_click = self.exit,  ignore_paused=True, parent=self)
        
        Text.size = .012
        self.reset_positioner_3d_b = Button(x=.44, y=.38, scale=(.1, .05), text=f'Reset Positioner 3d', on_click = self.reset_positioner_3d,  ignore_paused=True, parent=self)
        
        Text.size = .020
        self.positioner_ui = Draggable(
            scale=(self.exit_b.scale),
            texture='..\\assets\\Square_Border',
            position=Vec2(-.225,.225),
            text="Positioner UI", color=color.hsv(360,1,1,.05), on_click=lambda: print(f"Positioner UI: {self.positioner_ui.position}"), z=-300,  ignore_paused=True, parent=self)
        
        Text.size = .010
        
        # Text.size = .25
        # text_sp = Text(text="Scene\nPositioner", position=(-.33,.1,0), parent=self.positioner_3d, billboard=True)
        
    def reset_positioner_3d(self):
        if self.has_reset_positioner_3d_been_ran:
            for key, value in self.default_positioner_3d_values.items():
                setattr(self.positioner_3d, key, value)
                
            self.positioner_3d.world_position = (
                camera.world_position
                + camera.forward * 16
                + camera.up * 3
                + camera.right * 8
            )
            self.positioner_3d.look_at(camera.ui.world_position)
            self.positioner_3d.rotation_y += 180
            self.positioner_3d.rotation_z += 33
            
        else:
            self.has_reset_positioner_3d_been_ran = True
            
            self.positioner_3d.position=camera.ui.world_position + Vec3(8,5,16)
            
    def resume(self):        
        self.enabled = False
        
    def dev_cam(self):
        pt('dev cam')
        self.editor_camera.enabled = not self.editor_camera.enabled
        # pt(mouse.locked)
        if self.enabled:
            self.disable()
            self.positioner_3d.disable()
            self.reset_positioner_3d()

        
        if self.player is not None:
            self.player.reticle.enabled = not self.editor_camera.enabled
            self.player.visible_self = not self.editor_camera.enabled
            
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
    
    dev_pause_menu = DevPauseMenu(enabled=True)
    
    ground = Entity(model='plane', scale=(100,1,100), color=color.rgba(.8, .8, 0, .22), texture='white_cube', texture_scale=(100,100), collider='box')
    player = FirstPersonController(
        y=2, 
        origin_y=-.5,
        enabled = not dev_pause_menu.enabled, # Set to opposite of dev pause menu when loadig the level
    )
    
    def input(key):
        if key == dev_pause_menu.dev_menu_key:
            dev_pause_menu.enabled = not dev_pause_menu.enabled
            player.enabled = not dev_pause_menu.enabled
            
    app.run()
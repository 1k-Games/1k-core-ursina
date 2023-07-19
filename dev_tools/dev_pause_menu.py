''' TODO

- Pass a parent, so we can see what positions/rotations in regards to the parent
- Pass a model to both the positioners so they look correct each time. 
- Create a separate class called "Dev_Pause_Menu" and it's only functions are
    to load an instance of PauseMenu and then accept "esc" input
    which will enable/disable the entire PauseMenu without me needing to do it for
    every single entity. 
    
    - After this is complete, re-write the code so individual buttons/text/draggables
        aren't being enabled/disabled anymore. 

'''

import subprocess

from ursina import *

from print_tricks import pt 

class PauseMenu(Entity):
    def __init__(self, 
                 player=None,
                 file_path=None,
                 ui_positioner_ent=None, 
                 ui_p_parent=None, 
                 scene_positioner_ent=None,
                 scene_p_parent=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.ignore_paused = True
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        self.pause_handler = Entity(ignore_paused=True, input=self.pause_input)
        self.player = player
        
        self.quit_shortcut = 'x'
        self.restart_shortcut = 'r'
        
        
        ## Running a file up a level
        # cwd = pt.l()
        # last_backslash = cwd.rfind("\\")
        # new_cwd = cwd[:last_backslash]q
        # file_name = 'main.py'
        # self.file_path = f'{new_cwd}\\{file_name}'qq
        
        ## Running this file
        self.file_path = pt.l(getFile=True)
        self.p_menu()
        
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
        if key == 'o':
            self.scene_positioner.rotation_x += 22

    def p_menu(self):
        self.paused_text = Text('Paused', x=0, y=.44,background=True, size=62, enabled=False)
        self.resume_b = Button(y=.11,  scale=(.2, .1),      text=f'Resume (esc)', on_click = self.pause_resume, enabled=False, ignore_paused=True)
        self.restart_b = Button(y=-.11,  scale=(.2, .1),    text=f'Restart ({self.restart_shortcut})', on_click = self.restart, enabled=False, ignore_paused=True)
        self.exit_b   = Button(y=-.22, scale=(.2, .1),      text=f'Exit ({self.quit_shortcut})', on_click = self.exit, enabled=False, ignore_paused=True)
        
        Text.size = .020
        self.ui_positioner = Draggable(
            scale=(self.exit_b.scale),
            texture='..\\assets\\Square_Border',
            position=Vec2(-.225,.225),
            text="UI Positioner", color=color.hsv(360,1,1,.05), on_click=lambda: print(f"UI Positioner: {self.ui_positioner.position}"), z=-300, enabled=False, ignore_paused=True)
        
        Text.size = .010
        self.scene_positioner = Draggable(
            parent=scene,
            # model='cube',
            model='..\\assets\\scene_positioner_cube.obj',
            double_sided=True,
            text="Scene\nPositioner",
            scale=(1,1,1),
            texture='..\\assets\\colored_axis_cube',
            position=camera.ui.world_position + Vec3(4,3,10),
            rotation=(7,-13,22),
            # color=color.hsv(360,1,1,.05),
            enabled=False, ignore_paused=True, 
            on_click=lambda: print(
                f"Scene Positioner:\n"
                f"    pos = {self.ui_positioner.position}, world_pos = {self.ui_positioner.world_position}\n"
                f"    rot = {self.ui_positioner.rotation}, world_rot = {self.scene_positioner.world_rotation}"
                )
            )
        # Text.size = .25
        # text_sp = Text(text="Scene\nPositioner", position=(-.33,.1,0), parent=self.scene_positioner, billboard=True)
    def pause_input(self, key):
        if key == 'escape':
            self.pause_resume()

        if application.paused:
            if key == 'x':
                self.exit()
            if key == 'r':
                self.restart()

        if application.development_mode:
            if key == 'tab': 
                self.dev_cam()
            
    def pause_resume(self):
        application.paused = not application.paused
        self.enabled = not self.enabled
        mouse.locked = not application.paused
        
        if application.development_mode:
            mouse.position = self.restart_b.position
        else: 
            mouse.position = self.resume_b.position
        
        self.paused_text.enabled = not self.paused_text.enabled
        self.resume_b.enabled = not self.resume_b.enabled
        self.restart_b.enabled = not self.restart_b.enabled
        self.exit_b.enabled = not self.exit_b.enabled
        self.ui_positioner.enabled = not self.ui_positioner.enabled
        self.scene_positioner.enabled = not self.scene_positioner.enabled 
        
    def dev_cam(self):
        self.editor_camera.enabled = not self.editor_camera.enabled
        
        if self.player is not None:
            self.player.reticle.enabled = not self.editor_camera.enabled
            self.player.visible_self = not self.editor_camera.enabled
            mouse.locked = not self.editor_camera.enabled
            
            sp = self.player.position
            self.editor_camera.position = Vec3(sp.x, sp.y+3, sp.z)
            self.editor_camera.rotation = self.player.rotation
        
    def restart(self):
        command = ['python', self.file_path]
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
        
    def exit(self):
        application.quit()
    
class Dev_Pause_Menu(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pause_menu = PauseMenu(
            enabled=False, 
            ignore_paused=True,
            )
    # def input(self, key):
    #     if key == 'escape':
    #         self.pause_menu.enabled = not self.pause_menu.enabled
            
if __name__ == '__main__':
    app = Ursina(size=(1920,1080))
    Dev_Pause_Menu()
    app.run()
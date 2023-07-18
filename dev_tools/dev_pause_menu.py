

import subprocess

from ursina import *

from print_tricks import pt

class PauseMenu:
    def __init__(self, player, **kwargs):
        # super().__init__(**kwargs)
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        self.pause_handler = Entity(ignore_paused=True, input=self.pause_input)
        self.player = player
        self.p_menu()

    def p_menu(self):
        self.paused_text = Text('Paused', y=.36, size=33, enabled=False)
        self.resume_b = Button(y=.11,  scale=(.2, .1), text='Resume (esc)', on_click = self.pause_resume, enabled=False, ignore_paused=True)
        self.restart_b = Button(y=-.11,  scale=(.2, .1), text='Restart (r)', on_click = self.restart, enabled=False, ignore_paused=True)
        self.exit_b   = Button(y=-.22, scale=(.2, .1), text='Exit (q)', on_click = self.exit, enabled=False, ignore_paused=True)

    def pause_input(self, key):
        if key == 'escape':
            self.pause_resume()

        if application.paused:
            if key == 'q':
                self.exit()
            if key == 'r':
                self.restart()

        if application.development_mode:
            if key == 'tab': 
                self.dev_cam()
            
    def pause_resume(self):
        application.paused = not application.paused
        mouse.locked = not application.paused
        
        if application.development_mode:
            mouse.position = self.restart_b.position
        else: 
            mouse.position = self.resume_b.position
        
        self.paused_text.enabled = not self.paused_text.enabled
        self.resume_b.enabled = not self.resume_b.enabled
        self.restart_b.enabled = not self.restart_b.enabled
        self.exit_b.enabled = not self.exit_b.enabled
        
    def dev_cam(self):
        self.editor_camera.enabled = not self.editor_camera.enabled
        self.player.reticle.enabled = not self.editor_camera.enabled
        self.player.visible_self = not self.editor_camera.enabled
        mouse.locked = not self.editor_camera.enabled
        
        sp = self.player.position
        self.editor_camera.position = Vec3(sp.x, sp.y+3, sp.z)
        self.editor_camera.rotation = self.player.rotation
        
    def restart(self):
        cwd = pt.l()
        last_backslash = cwd.rfind("\\")
        new_cwd = cwd[:last_backslash]
        command = ['python', f'{new_cwd}\\main.py']
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
        
    def exit(self):
        application.quit()
        
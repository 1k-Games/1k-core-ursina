import subprocess

from ursina import *

from print_tricks import pt 

class PauseMenu:
    def __init__(self, player=None, **kwargs):
        # super().__init__(**kwargs)
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        self.pause_handler = Entity(ignore_paused=True, input=self.pause_input)
        self.player = player
        
        ### Running a file up a level
        # cwd = pt.l()
        # last_backslash = cwd.rfind("\\")
        # new_cwd = cwd[:last_backslash]
        # file_name = 'main.py'
        # self.file_path = f'{new_cwd}\\{file_name}'
        
        ### Running this file
        self.file_path = pt.l(getFile=True)

        self.p_menu()

    def p_menu(self):
        self.paused_text = Text('Paused', y=.36, size=33, enabled=False)
        self.resume_b = Button(y=.11,  scale=(.2, .1), text='Resume (esc)', on_click = self.pause_resume, enabled=False, ignore_paused=True)
        self.restart_b = Button(y=-.11,  scale=(.2, .1), text='Restart (r)', on_click = self.restart, enabled=False, ignore_paused=True)
        self.exit_b   = Button(y=-.22, scale=(.2, .1), text='Exit (q)', on_click = self.exit, enabled=False, ignore_paused=True)
        self.ui_positioner = Draggable(
            scale=(self.exit_b.scale),
            position=Vec2(0,.225),
            text="UI Positioner", color=color.hsv(360,1,1,.05), on_click=lambda: print(f"UI_Positioner 1: {self.ui_positioner.position}"), z=-300, enabled=False, ignore_paused=True)


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
        self.ui_positioner.enabled = not self.ui_positioner.enabled
        
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
        
if __name__ == '__main__':
    app = Ursina()
    PauseMenu()
    app.run()
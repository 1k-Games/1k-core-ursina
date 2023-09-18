from print_tricks import pt
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton


class GamePauseMenuTemplate(Entity):
    def __init__(self,
                enabled=False,
                camera_fov=33,
                **kwargs):
        
        self.buttons = {}
        self.camera_fov = camera_fov
        self.intiation_over = False
        super().__init__(parent=camera.ui, ignore_paused=True, enabled=enabled, **kwargs)
        pt.c('---- Game Pause Menu ----')
        self.title = Text(text='Game Pause Menu Template', scale=2, y=0.4, origin=(0,0), parent=self)        
        self.menu_items = [
            'Resume',
            'Social',
            'Challenges/Achievements',
            'History',
            'Career Profile',
            'Options',
            'Readme',
            'FAQ',
            'Patch Notes',
            'Credits',
            '',
            'Exit'
        ]
        Text.size = .03
        for i, item in enumerate(self.menu_items):
            button = Button(text=item, y=0.3 - 0.05 * i, scale=(.5, .04), color=color.azure, parent=self)
            if item:  # Only add click function if item is not an empty string
                button.on_click = self.button_clicked(item)
            self.buttons[item] = button
        pt(Text.size)    
        
    def on_enable(self):
        try:
            camera.fov = self.camera_fov
            resume_button = self.buttons['Resume']
            mouse.position = resume_button.position
        except:
            ...
            
    def resume_clicked(self):
        ...
        # self.disable()
        
    def button_clicked(self, item):
        def inner():
            self.enabled = False
            self.submenus[item].enabled = True
        return inner
    
    def social_clicked(self):
        print("Social clicked")

    def challenges_achievements_clicked(self):
        print("Challenges/Achievements clicked")

    def history_clicked(self):
        print("History clicked")

    def career_profile_clicked(self):
        print("Career Profile clicked")

    def options_clicked(self):
        print("Options clicked")

    def readme_clicked(self):
        print("Readme clicked")

    def faq_clicked(self):
        print("FAQ clicked")

    def patch_notes_clicked(self):
        print("Patch Notes clicked")

    def credits_clicked(self):
        print("Credits clicked")

    def exit_clicked(self):
        print("Exit clicked")

    def back_clicked(self):
        self.submenu.enabled = False

    def video_tab_clicked(self):
        print("Video tab clicked")

    def audio_tab_clicked(self):
        print("Audio tab clicked")

    def controls_tab_clicked(self):
        print("Controls tab clicked")

if __name__ == '__main__':
    app = Ursina(size=(1920,1080))
    # pause_menu = GamePauseMenuTemplate(enabled=True)
    pause_menu = GamePauseMenuTemplate(
        enabled=True
        )
    def input(key):
        if key == 'escape':
            pause_menu.enabled = not pause_menu.enabled
    app.run()




'''



self.menu_items = ['Social', Challenges & Achievements, History, Career Profile, 'Options', Readme, FAQ, Patch Notes, Credits, '', 'Exit']






'''
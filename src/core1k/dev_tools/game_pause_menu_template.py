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
        from ursina.prefabs.ursfx import ursfx
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
        
        # self.hover_sound = Audio('path_to_your_sound_file', autoplay=False)
        # self.hover_sound = ursfx.Saw(rate=22050, freq=440.0, length=1)
        self.hover_sound = ursfx([(0.0, 1.0), (0.1, 0.5), (0.25, 0.5), (0.49, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=-18, pitch_change=-3, speed=2.8)
        
        for i, item in enumerate(self.menu_items):
            button = Button(text=item, y=0.3 - 0.05 * i, scale=(.5, .04), color=color.azure, parent=self)
            if item:  # Only add click function if item is not an empty string
                if item == 'Resume':
                    button.on_click = self.resume_clicked
                elif item == 'Exit':
                    button.on_click = self.exit_clicked
                else:
                    button.on_click = self.create_click_function(item)
                button.on_hover = self.play_hover_sound
                self.buttons[item] = button
        
    def on_enable(self):
        try:
            camera.fov = self.camera_fov
            resume_button = self.buttons['Resume']
            mouse.position = resume_button.position
            
        except:
            ...
            
    def play_hover_sound(self):
        pt('hovered')
        self.hover_sound = ursfx([(0.0, 1.0), (0.1, 0.5), (0.25, 0.5), (0.49, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=-18, pitch_change=-3, speed=2.8)
        self.hover_sound.play()
    def create_click_function(self, item):
        def func():
            print(f"{item} clicked")
        return func
    
    def resume_clicked(self):
        ...
        print("Resume clicked")
        # self.disable()
        
    def exit_clicked(self):
        ...
        # print("Exit clicked")

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

'''
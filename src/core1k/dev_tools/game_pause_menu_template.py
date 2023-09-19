from print_tricks import pt
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

class ButtonCore1k(Button):
    def __init__(self, 
        sound=None,
        # highlight_scale
        **kwargs
    ):
        from ursina.prefabs.ursfx import ursfx
        self.ursfx = ursfx
        super().__init__(**kwargs)
        self.sound = sound
        self.original_scale = self.scale
        self.original_y = self.y
        self.original_z = self.z

    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.hover_sound = self.ursfx([(0.0, 1.0), (0.1, 0.5), (0.25, 0.5), (0.49, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=-18, pitch_change=-3, speed=2.8)
        self.z -=1
        self.collider = 'box' ## Resets to the new highlighted size of the box. 
        # self.scale_y = self.original_scale[1]
        
        y_factor = (self.highlight_scale[1] - self.original_scale[1]) * .004
        pt(y_factor)

        for button in self.parent.buttons.values():
            if button is not self:
                if button.y > self.y:
                    button.y += y_factor
                elif button.y < self.y:
                    button.y -= y_factor
                    
    def on_mouse_exit(self):
        super().on_mouse_exit()
        self.scale = self.original_scale 
        self.z = self.original_z
        
        for button in self.parent.buttons.values():
            if button is not self:
                button.scale = button.original_scale
                button.y = button.original_y
                
    def input(self, key):
        super().input(key)
        if key == 'left mouse down' and self.hovered:
            self.play_click_sound()

    def play_click_sound(self):
        self.click_sound = self.ursfx([(0.0, 1.0), (0.12, 0.5), (0.25, 0.5), (0.44, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=12, speed=2.6)

class GamePauseMenuTemplate(Entity):
    def __init__(self,
        enabled=False,
        camera_fov=33,
        **kwargs):
        
        self.buttons = {}
        self.camera_fov = camera_fov
        from ursina.prefabs.ursfx import ursfx
        super().__init__(parent=camera.ui, ignore_paused=True, enabled=enabled, **kwargs)
        pt.c('---- Game Pause Menu ----')
        self.ursfx = ursfx
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
        # self.hover_sound = self.ursfx([(0.0, 1.0), (0.1, 0.5), (0.25, 0.5), (0.49, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=-18, pitch_change=-3, speed=2.8)
        
        for i, item in enumerate(self.menu_items):
            button = ButtonCore1k(text=item, y=0.3 - 0.05 * i, scale=(.5, .04), highlight_scale=(1.1, 2.5), color=color.azure, 
                # sound=self.hover_sound, 
                parent=self)
            if item:  # Only add click function if item is not an empty string
                if item == 'Resume':
                    button.on_click = self.resume_clicked
                elif item == 'Exit':
                    button.on_click = self.exit_clicked
                else:
                    button.on_click = self.create_click_function(item)
            self.buttons[item] = button
        
    def on_enable(self):
        try:
            camera.fov = self.camera_fov
            resume_button = self.buttons['Resume']
            mouse.position = resume_button.position
            
        except:
            ...
            
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
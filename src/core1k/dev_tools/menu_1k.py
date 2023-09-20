from print_tricks import pt
pt.easy_imports()
# pt.easy_testing(__name__)

import os
pt(os.getcwd())
# os.chdir('../../')
# pt(os.getcwd())
# os.chdir('assets/ui')
# pt(os.getcwd())

from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.shaders import lit_with_shadows_shader

class ButtonCore1k(Button):
    def __init__(self, 
        sound=None,
        button_type=None,
        hover_texture=None,
        # highlight_scale
        **kwargs
    ):
        from ursina.prefabs.ursfx import ursfx
        self.ursfx = ursfx
        super().__init__(**kwargs)
        self.sound = sound
        self.button_type = button_type
        self.hover_texture = hover_texture
        self.original_scale = self.scale
        self.original_y = self.y
        self.original_z = self.z
        self.adjusted_y = self.y
        self.original_texture = self.texture
        # self.shader = lit_with_shadows_shader
        
    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.hover_sound = self.ursfx([(0.0, 1.0), (0.1, 0.5), (0.25, 0.5), (0.49, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=-18, pitch_change=-3, speed=2.8)
        self.z -=1
        self.collider = 'box' ## This is required, at least for now... it resets the collider size to the new 
                                ## highlighted size of the button. 
        
        self.x_factor = (self.highlight_scale[0] - self.original_scale[0]) * .008
        self.y_factor = (self.highlight_scale[1] - self.original_scale[1]) * .008
        
        if self.button_type == 'icon' and self.hover_texture:
            self.texture = self.hover_texture
            
        if self.button_type == 'item':
            for button in self.parent.item_buttons.values():
                if button is not self:
                    if button.y > self.adjusted_y:
                        button.y += self.y_factor
                    else:
                        button.y -= self.y_factor
                        
        elif self.button_type == 'tab':
            for button in self.parent.tab_buttons.values():
                if button is not self:
                    if button.x > self.x:
                        button.x += self.x_factor
                    else:
                        button.x -= self.x_factor
                        
    def on_mouse_exit(self):
        super().on_mouse_exit()
        self.scale = self.original_scale 
        self.z = self.original_z
        
        if self.button_type == 'icon':
            self.texture = self.original_texture
            
        if self.button_type == 'item':
            for button in self.parent.item_buttons.values():
                if button is not self:
                    if button.y > self.adjusted_y:
                        button.y -= self.y_factor
                    else:
                        button.y += self.y_factor
                        
        elif self.button_type == 'tab':
            for button in self.parent.tab_buttons.values():
                if button is not self:
                    if button.x > self.x:
                        button.x -= self.x_factor
                    else:
                        button.x += self.x_factor
                
    def input(self, key):
        super().input(key)
        if key == 'left mouse down' and self.hovered:
            self.play_click_sound()
            
        if key == 't':
            self.shader = None 
            
        if key == 'g':
            self.shader = lit_with_shadows_shader
            
    def play_click_sound(self):
        self.click_sound = self.ursfx([(0.0, 1.0), (0.12, 0.5), (0.25, 0.5), (0.44, 0.5), (1.0, 0.0)], volume=0.75, wave='sine', pitch=12, speed=2.6)

class MenuTemplate(Entity):
    def __init__(self,
        title=None,
        title_graphic=None,
        title_position=(0,.4),
        item_names=None,
        items_start_point=(0,0,0),
        tab_names=None,
        tabs_start_point=(-.75,.337,0),
        icon_names= None, ## TODO DELETE, TEMPORARY, use icon names and textures
        icon_names_and_textures={},
        icons_start_point=(.84,.337,0),
        items_texture=None,
        background_texture=None,
        pause_on_enabled=False,
        enabled=False,
        camera_fov=33,
        **kwargs):
        from ursina.prefabs.ursfx import ursfx
        
        self.item_buttons = {}
        self.tab_buttons = {}
        self.icon_buttons = {}
        self.all_buttons = []

        self.camera_fov = camera_fov
        self.pause_on_enabled = pause_on_enabled
        
        super().__init__(parent=camera.ui, 
                        ignore_paused=True, 
                        enabled=enabled, **kwargs)
        
        pt.c('---- Game Pause Menu ----')
        self.ursfx = ursfx
        self.item_names = item_names
        self.items_start_point = items_start_point
        self.tab_names = tab_names
        self.tabs_start_point = tabs_start_point
        self.icon_names_and_textures = icon_names_and_textures
        self.icons_start_point = icons_start_point
        
        self.background = Entity(
            model='quad', 
            scale=(window.aspect_ratio, 1, 1),
            texture=background_texture,
            parent=self,
        )                         
                                # texture_scale=(1/window.aspect_ratio, 1),)
        self.title = Text(text='Game Pause Menu Template', scale=2, position=title_position, origin=(0,0), parent=self)
        
        if item_names: self.setup_items()     
        if tab_names: self.setup_tabs()
        if icon_names_and_textures: self.setup_icons()
        
    def setup_icons(self):
        total_width = 0
        for i, (icon, textures) in enumerate(reversed(self.icon_names_and_textures.items())):
            button = ButtonCore1k(
                button_type='icon',
                text=icon if textures[0] is None else None,
                x=self.icons_start_point[0] - total_width,
                y=self.icons_start_point[1],
                scale=(.075, .075),  # Set the scale of the button
                highlight_scale=(1.1, 1.2), 
                color=color.brown,
                texture=textures[0],  # Use the first texture
                hover_texture=textures[1] if len(textures) > 1 else None,  # Use the second texture if it exists
                parent=self,
                origin=(0.5, 0)
            )
            if icon:  ## Only add click if icon is not an empty string
                if icon == 'Resume':
                    button.on_click = self.resume_clicked
                elif icon == 'Exit':
                    button.on_click = self.exit_clicked
                else:
                    button.on_click = self.create_click_function(icon)
            self.icon_buttons[icon] = button
            total_width += button.scale_x + 0.001  # Add the width of the button and some padding
            
# texture=texture[0] if texture else icon,  # Use the texture if provided, otherwise use the name

    def setup_items(self):
        
        for i, item in enumerate(self.item_names):
            button = ButtonCore1k(
                button_type='item',
                text=item,
                x=self.items_start_point[0],
                y=self.items_start_point[1] - 0.05 * i, 
                scale=(.41, .04), 
                highlight_scale=(1.1, 1.8), 
                color=color.brown,
                # texture='oval_button',
                parent=self)
            if item:  ## Only add click if item is not an empty string
                if item == 'Resume':
                    button.on_click = self.resume_clicked
                elif item == 'Exit':
                    button.on_click = self.exit_clicked
                else:
                    button.on_click = self.create_click_function(item)
            self.item_buttons[item] = button
            
    def setup_tabs(self):
        total_width = 0
        for i, tab in enumerate(self.tab_names):
            scale_x = len(tab) * 0.02  # Adjust this factor as needed
            button = ButtonCore1k(
                button_type='tab',
                text=tab,
                x=self.tabs_start_point[0] + total_width,
                y=self.tabs_start_point[1],
                scale=(scale_x, .04),  # Use scale_x for the x scale
                highlight_scale=(1.1, 1.2), 
                color=color.brown,
                # texture='oval_button',
                parent=self,
                origin=(-0.5, 0)  # Set the origin to the left edge
            )
            if tab:  ## Only add click if tab is not an empty string
                if tab == 'Resume':
                    button.on_click = self.resume_clicked
                elif tab == 'Exit':
                    button.on_click = self.exit_clicked
                else:
                    button.on_click = self.create_click_function(tab)
            self.tab_buttons[tab] = button
            total_width += scale_x + 0.001  # Add the width of the button and some padding
        
    def on_enable(self):
        try:
            camera.fov = self.camera_fov
            resume_button = self.buttons['Resume']
            mouse.position = resume_button.position
            
        except:
            ...
        
        if self.pause_on_enabled: application.paused = True
        
        pt(self.pause_on_enabled, application.paused)
        
    def on_disable(self):
        if self.pause_on_enabled: application.paused = False
        
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
    from dev_pause_menu import DevPauseMenu
    
    class temp_game_manager(Entity):
        def __init__(self, **kwargs):
            super().__init__(ignore_paused=True, **kwargs)
        
        def input(self, key):
            if key == 'escape':
                pause_menu.enabled = not pause_menu.enabled
            if key == 'f1':
                dpm.enabled = not dpm.enabled
                
    pause_menu = MenuTemplate(
        background_texture='menu_background_delete.jpg',
        item_names=[
            'New Game',
            'Continue',
            # 'Resume',
            # 'Social',
            # 'Challenges/Achievements',
            # 'History',
            # 'Career Profile',
            # 'Options',
            # 'Readme',
            # 'FAQ',
            # 'Patch Notes',
            'Credits',
            '',
            'Exit'
        ],
        # items_start_point=(-.75,-.22,0),
        items_start_point=(-.48,-.22,0),
        tab_names=[
            'video',
            'controls',
            'sound',
        ],
        icon_names_and_textures={
            'Social':       ('social1.png', 'social2.png'), 
            'Achievements': ('achievements1.png', 'achievements2.png'), 
            'Settings':     ('settings1.png', 'settings2.png'),
            'Docs':         ('docs1.png', 'docs2.png')
        },
        pause_on_enabled=True,
        enabled=True
        )
    
    cube = Entity(model='cube', position=(2,1,4))
    def update():
        cube.rotation += Vec3(10,10,10) * time.dt
        
    temp_game_manager()
    
    dpm = DevPauseMenu()
    
    app.run()




'''

'''
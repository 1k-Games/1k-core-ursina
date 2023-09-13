from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton


class PauseMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False)

        self.title = Text(text='Game Pause Menu Template', scale=2, y=0.4, origin=(0,0))        
        self.menu_items = [
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
            'Exit']

        self.buttons = []

        for i, item in enumerate(self.menu_items):
            button = Button(text=item, y=0.3 - 0.05 * i, scale_y=0.04, color=color.azure)
            if item:  # Only add click function if item is not an empty string
                button.on_click = self.button_clicked(item)
            self.buttons.append(button)

        self.submenus = {item: Entity(parent=self, enabled=False) for item in self.menu_items if item}

        for item in self.submenus:
            back_button = Button(parent=self.submenus[item], text='Back', scale_y=0.1, color=color.azure, y=0.4)
            back_button.on_click = self.back_clicked

        self.options_tabs = ['Video', 'Audio', 'Controls']
        self.options_tab_buttons = []

        for i, tab in enumerate(self.options_tabs):
            tab_button = Button(parent=self.submenus['Options'], text=tab, y=0.3 - 0.1 * i, scale_y=0.1, color=color.azure)
            tab_button.on_click = getattr(self, f'{tab.lower()}_tab_clicked')
            self.options_tab_buttons.append(tab_button)

        self.labels = ['Resolution', 'Fullscreen', 'VSync']
        self.label_texts = []

        for i, label in enumerate(self.labels):
            label_text = Text(parent=self.submenus['Options'], text=label, x=-0.2, y=0.2 - 0.1 * i)
            self.label_texts.append(label_text)

        self.dropdown = DropdownMenu(parent=self.submenus['Options'], options=['800x600', '1024x768', '1920x1080'], default_value='1920x1080', y=0.2)
        # self.checkbox = CheckBox(parent=self.submenus['Options'], text='', y=0.1)
        self.slider = Slider(parent=self.submenus['Options'], min=0, max=100, default=50, y=0)

    def button_clicked(self, item):
        def inner():
            self.enabled = False
            self.submenus[item].enabled = True
        return inner
    
    def input(self, key):
        if key == 'escape':
            if self.submenu.enabled:
                self.submenu.enabled = False
            else:
                self.enabled = not self.enabled

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
        
app = Ursina()
pause_menu = PauseMenu()
app.run()




'''



self.menu_items = ['Social', Challenges & Achievements, History, Career Profile, 'Options', Readme, FAQ, Patch Notes, Credits, '', 'Exit']






'''
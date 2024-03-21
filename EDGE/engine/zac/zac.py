'''TODO & NOT TODO
    - Don't heavily optimize this in anyway until python 3.12 and thread unlock or I use things like
    trio/tractor etc. 
        - There's not need to optimiza by getting rid of entities (and converting to a singular entity
        or several nodepaths or a singular nodepath), if I don't even know what the optimization/threading/
        integration route will look like. )'''
import subprocess

from print_tricks import pt
# import lebowski
# lebowski.enable()

from ursina import *

store = [
    'Games',
    'Skins',
    'Mods',
    
]
tests = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',

]
engine_tests = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',

]
game_templates = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
    

]
games = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
    
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',

]
settings = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
    
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',

    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
    
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
]

class Zac:
    def __init__(self, game_templates, store, tests, engine_tests, games, settings):
        self.game_templates = game_templates
        self.store = store
        self.tests = tests
        self.engine_tests = engine_tests
        self.games = games
        self.settings = settings
        self.app_launcher_menus = {}  # Dictionary to hold AppLauncherMenu instances by category
        self.current_category = None  # Track the current category
        self.initialize_ui()

    def initialize_ui(self):
        self.top_menu = TopMenu(self.switch_app_category)
        # Initialize all categories at the start but do not display them
        for category in ["store", "tests", "engine_tests", "game_templates", "games", "settings"]:
            category_list = getattr(self, category)
            self.app_launcher_menus[category] = AppLauncherMenu(category_list, app_category=category)
            self.app_launcher_menus[category].disable()  # Start with all menus disabled
            pt(self.app_launcher_menus[category].name)

    def switch_app_category(self, category):
        # Disable the current launcher menu
        if self.current_category and self.current_category in self.app_launcher_menus:
            self.app_launcher_menus[self.current_category].disable()
        
        # Enable the selected category's launcher menu
        if category in self.app_launcher_menus:
            self.app_launcher_menus[category].enable()
            self.current_category = category



class TopMenu(Entity):
    def __init__(self, switch_function, **kwargs):
        super().__init__(**kwargs)
        self.parent = camera.ui
        self.menu_items = ["store", "tests", "engine_tests", "game_templates", "games", "settings"]
        self.switch_function = switch_function
        
        self.btn_y_pos = 0.46
        self.create_menu()

    def create_menu(self):
        max_length = max(len(item) for item in self.menu_items)  # Find the longest item
        base_scale_x = 0.1  # Base scale for X, adjust as needed
        base_scale_y = 0.05  # Base scale for Y, adjust as needed
        scale_factor = 0.15  # Adjust this factor to increase or decrease the scaling effect
        spacing = 0.05  # Spacing between buttons, adjust as needed

        # Calculate total width required for all buttons including spacing
        total_width = sum(base_scale_x + (len(item) / max_length) * scale_factor for item in self.menu_items)
        total_width += spacing * (len(self.menu_items) - 1)  # Add spacing between buttons

        # Calculate initial cumulative_x based on total width to center or align buttons as needed
        cumulative_x = -total_width / 2  # Adjust this to change alignment

        for i, item in enumerate(self.menu_items):
            text_length = len(item)
            # Calculate scale_x as base_scale_x plus an additional factor based on text length
            scale_x = base_scale_x + (text_length / max_length) * scale_factor

            btn = Button(text=item.capitalize(),
                        position=(cumulative_x + scale_x / 2, self.btn_y_pos),  # Adjust position to account for button width
                        scale=(scale_x, base_scale_y),
                        parent=self,
                        on_click=Func(self.switch_function, item))

            # Update cumulative_x for the next button, adding the current button's width plus fixed spacing
            cumulative_x += scale_x + spacing

            print(f"{btn.text}: position = {btn.position}, scale_x = {scale_x}")  # Debug print
            pt(btn.name, text_length, scale_x)


class AppLauncherMenu(Entity):
    def __init__(self, list_of_apps, app_category='game_templates', **kwargs):
        super().__init__(**kwargs)
        self.app_category = app_category
        self.list_of_apps = list_of_apps
        self.app_processes = {}  # Keep track of app processes
        self.parent = camera.ui
        self.app_buttons = []
        self.current_running_app = None
        
        self.update_interval = 0.25
        self.time_since_last_check = 0
        self.previous_hovered_entity = Entity()
        
        self.button_color = color.rgba(0, 0, 0, 1)
        self.button_run_color = color.rgba(0, 1, 0, 0.75)
        self.button_close_color = color.rgba(1, 0, 0, 0.75)
        self.button_close_location = -0.31

        self.create_app_buttons(list_of_apps)

    def run_app(self, app_name):
        app_script_path = f"edge/{self.app_category}/{app_name}/{app_name}.py"
        process = subprocess.Popen(["python", app_script_path], start_new_session=True)
        self.app_processes[app_name] = process

    def kill_app(self, app_name):
        # Terminate the app process
        if app_name in self.app_processes:
            self.app_processes[app_name].terminate()
            del self.app_processes[app_name]  # Remove the process from the dictionary

    def create_app_buttons(self, apps):
        screen_width = window.aspect_ratio
        screen_height = 1 
        
        grid_width = screen_width * (2/3)  # Grid takes up 2/3 of the screen width
        grid_height = screen_height * 0.8  # Adjust grid height to ensure buttons fit on screen
        
        # Calculate the number of columns and rows based on the number of apps
        # Ensure num_columns is at least 1 to avoid division by zero
        max_buttons_per_row = 4  # Adjust based on your preference
        num_columns = max(1, min(max_buttons_per_row, len(apps)))
        num_rows = len(apps) // num_columns + (1 if len(apps) % num_columns > 0 else 0)
        
        # Adjust button size to maintain aspect ratio and fit within the grid
        button_aspect_ratio = 1.6  # Adjust based on desired button width:height ratio
        button_width = min(grid_width / num_columns / 1.3, grid_height / num_rows / button_aspect_ratio)
        button_height = button_width / button_aspect_ratio
        
        # Calculate starting position
        start_x = (screen_width - grid_width) / 2  # Center the grid horizontally
        start_y = (grid_height / 2) - (button_height / 2)  # Start from the top of the grid
        
        for i, app_name in enumerate(apps):
            row = i // num_columns
            col = i % num_columns
            
            button_x = start_x + col * (button_width * 1.15) + button_width / 2
            button_y = start_y - row * (button_height * 1.15)
            
            button_text = f"{app_name}"
            button = Button(text=button_text, 
                            position=(button_x, button_y), 
                            scale=(button_width, button_height),
                            parent=self,
                            )
            
            def on_click(app_name=app_name, button=button):
                if mouse.point[1] < self.button_close_location:
                    self.kill_app(app_name)
                else:
                    self.run_app(app_name)
            
            button.on_click = Func(on_click)
            self.app_buttons.append(button)

    def update(self):
        self.time_since_last_check += time.dt
        if self.time_since_last_check > self.update_interval:
            self.time_since_last_check = 0
            self.previous_hovered_entity.color = self.button_color
            if mouse.hovered_entity in self.app_buttons:
                self.previous_hovered_entity = mouse.hovered_entity
                if mouse.point[1] < self.button_close_location:
                    mouse.hovered_entity.color = self.button_close_color
                else:
                    mouse.hovered_entity.color = self.button_run_color


if __name__ == "__main__":
    app = Ursina()

    zac = Zac(game_templates, store, tests, engine_tests, games, settings)

    EditorCamera()

    app.run()
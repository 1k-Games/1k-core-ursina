'''TODO & NOT TODO
    - Don't heavily optimize this in anyway until python 3.12 and thread unlock or I use things like
    trio/tractor etc. 
        - There's not need to optimiza by getting rid of entities (and converting to a singular entity
        or several nodepaths or a singular nodepath), if I don't even know what the optimization/threading/
        integration route will look like. )
        
    - While doing the python 3.12/multicore refactor, rebuild this using my 1k core Menu builder class, I was building for companion in the dark
    but to be a universal menu
    
    
        '''
import os, subprocess

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

import os

class DirectoryScanner:
    @staticmethod
    def scan_for_templates(directory, ignore_list=None):
        if ignore_list is None:
            ignore_list = []
        game_templates = [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item)) and item not in ignore_list]
        return game_templates
    
class ConfigReader:
    @staticmethod
    def read_edge_installed_apps(config_file_path):
        with open(config_file_path, 'r') as file:
            apps = [line.strip() for line in file.readlines()]
        return apps
    
class Zac:
    def __init__(self, game_templates_directory, store_apps_config_file, tests_directory, engine_tests_directory, games_config_file, settings):
        self.store = ConfigReader.read_edge_installed_apps(store_apps_config_file)
        self.games = ConfigReader.read_edge_installed_apps(games_config_file)
        self.tests = DirectoryScanner.scan_for_templates(tests_directory)
        self.engine_tests = DirectoryScanner.scan_for_templates(engine_tests_directory)
        self.game_templates = DirectoryScanner.scan_for_templates(game_templates_directory, ignore_list=['__pycache__', ''])
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
        
        grid_width = screen_width * (2/3)
        grid_height = screen_height * 0.85
        
        max_buttons_per_row = 4
        num_columns = max(1, min(max_buttons_per_row, len(apps)))
        num_rows = max(1, len(apps) // num_columns + (1 if len(apps) % num_columns > 0 else 0))
        
        button_aspect_ratio = 1.6
        spacing = 0.05
        total_spacing = spacing * (num_columns - 1)
        available_width_for_buttons = grid_width - total_spacing
        button_width = min(available_width_for_buttons / num_columns, grid_height / num_rows / button_aspect_ratio)
        button_height = button_width / button_aspect_ratio
        
        start_x = -0.5 + (screen_width - grid_width) / 2
        start_y = 0.5 - (button_height / 2) - ((1 - grid_height) / 2)
        
        for i, app_name in enumerate(apps):
            row = i // num_columns
            col = i % num_columns
            
            button_x = start_x + col * (button_width + spacing)
            button_y = start_y - row * (button_height * 1.15)
            
            button = Button(text=app_name, 
                            position=(button_x, button_y), 
                            scale=(button_width, button_height),
                            parent=self)
            
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
    # pt.easy_imports('main.py')
    
    app = Ursina()

    # zac = Zac(game_templates, store, tests, engine_tests, games, settings)

    zac = Zac(
            store_apps_config_file="EDGE/engine/zac/edge_store_apps.toml",
            games_config_file="EDGE/engine/zac/edge_installed_games.toml",
            tests_directory="EDGE/tests(move_crafspace_tests_here_and_organize)/",
            engine_tests_directory="EDGE/tests(move_crafspace_tests_here_and_organize)/est_engine_specific_tests/",
            game_templates_directory="EDGE/game_templates",
            settings=settings
    )

    EditorCamera()

    app.run()
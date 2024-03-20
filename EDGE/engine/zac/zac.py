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


class AppLauncher(Entity):
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
        self.previous_hovered_entity = None
        
        self.button_color = color.rgba(0, 0, 0, 1)
        self.button_run_color = color.rgba(0, 1, 0, 0.75)
        self.button_close_color = color.rgba(1, 0, 0, 0.75)
        self.button_close_location = -0.31

        self.create_app_buttons(list_of_apps)
        
    def run_app(self, app_name):
        # Path to the app script
        app_script_path = f"edge/game_templates/{app_name}/{app_name}.py"
        
        # Launch the app as a separate process
        process = subprocess.Popen(["python", app_script_path], start_new_session=True)
        
        # Store the process handle, using the app name as the key
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
        grid_height = screen_height  # Grid takes up full screen height
        
        # Calculate the number of columns and rows based on the number of apps
        # Adjust these values based on your needs for minimum button size or maximum buttons per row
        max_buttons_per_row = 4  # Example: Adjust based on your preference
        num_columns = min(max_buttons_per_row, len(apps))
        num_rows = len(apps) // num_columns + (1 if len(apps) % num_columns > 0 else 0)
        
        # Calculate button size
        button_width = grid_width / num_columns / 1.3
        button_height = grid_height / num_rows / 1.3
        
        # Calculate starting position
        start_x = screen_width / 3  # Since the grid is on the right 2/3 of the screen
        start_y = 0  
        
        for i, app_name in enumerate(apps):
            # Existing button setup code...
            # Integrate "x" into the button's text
            row = i // num_columns
            col = i % num_columns
            
            button_x = start_x + col * (button_width * 1.15) - screen_width / 2 + button_width / 2  # Adjust position based on grid size
            button_y = start_y - row * (button_height * 1.15) + button_height / 2  # Adjust position based on grid size
            
            # Adjust the number of '\n' and ' ' based on your button size and desired layout
            button_text = f"\n\n\n\n\n\n{app_name}\n\n\n\n\n\nx"
            button = Button(text=button_text, 
                            position=(button_x, button_y), 
                            scale=(button_width, button_height),
                            # highlight_color=color.rgba(0, 1, 0, .75), 
                            highlight_scale=1.1,
                            )
            self.previous_hovered_entity = button
            
            # Custom on_click function to handle both app launch and kill
            def on_click(app_name=app_name, button=button):
                if mouse.point[1] < self.button_close_location:
                    self.kill_app(app_name)
                    # pt('kill app')
                else:
                    self.run_app(app_name)
                    # pt(app_name)
            
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

    launcher_menu = AppLauncher(game_templates)

    EditorCamera()

    app.run()
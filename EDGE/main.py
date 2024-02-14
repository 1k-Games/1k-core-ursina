from print_tricks import pt
# import lebowski
# lebowski.enable()

from ursina import *
import importlib

# No need to import game modules at the top

# List of game names
games = [
    'companion',
    'haulers',
    'tiny_marbies',
    'tiny_energy_game',
    'simulation_shooter',
    'action_arcade',
    'smash',
    'tower',
]




import subprocess

class GameMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_processes = {}  # Keep track of game processes
        self.parent = camera.ui
        self.game_buttons = []
        self.current_running_game = None
        self.create_game_buttons()
        
    def run_game(self, game_name):
        # Path to the game script
        game_script_path = f"edge/game_templates/{game_name}/{game_name}.py"
        
        # Launch the game as a separate process
        process = subprocess.Popen(["python", game_script_path], start_new_session=True)
        
        # Store the process handle, using the game name as the key
        self.game_processes[game_name] = process

    def kill_game(self, game_name):
        # Terminate the game process
        if game_name in self.game_processes:
            self.game_processes[game_name].terminate()
            del self.game_processes[game_name]  # Remove the process from the dictionary

    def create_game_buttons(self):
        screen_width = window.aspect_ratio
        screen_height = 1 
        
        grid_width = screen_width * (2/3)  # Grid takes up 2/3 of the screen width
        grid_height = screen_height  # Grid takes up full screen height
        
        # Calculate the number of columns and rows based on the number of games
        # Adjust these values based on your needs for minimum button size or maximum buttons per row
        max_buttons_per_row = 4  # Example: Adjust based on your preference
        num_columns = min(max_buttons_per_row, len(games))
        num_rows = len(games) // num_columns + (1 if len(games) % num_columns > 0 else 0)
        
        # Calculate button size
        button_width = grid_width / num_columns / 1.3
        button_height = grid_height / num_rows / 1.3
        
        # Calculate starting position
        start_x = screen_width / 3  # Since the grid is on the right 2/3 of the screen
        start_y = 0  
        
        for i, game_name in enumerate(games):
            # Existing button setup code...
            # Integrate "x" into the button's text
            row = i // num_columns
            col = i % num_columns
            
            button_x = start_x + col * (button_width * 1.15) - screen_width / 2 + button_width / 2  # Adjust position based on grid size
            button_y = start_y - row * (button_height * 1.15) + button_height / 2  # Adjust position based on grid size
            
            # Adjust the number of '\n' and ' ' based on your button size and desired layout
            button_text = f"\n\n\n\n\n\n{game_name}\n\n\n\n\n\nx"
            button = Button(text=button_text, 
                            position=(button_x, button_y), 
                            scale=(button_width, button_height),
                            highlight_color=color.rgba(0, 1, 0, .75), 
                            highlight_scale=1.1,
                            )
            
            # Custom on_click function to handle both game launch and kill
            def on_click(game_name=game_name, button=button):
                if mouse.point[1] < -0.33:
                    self.kill_game(game_name)
                    # pt('kill game')
                else:
                    self.run_game(game_name)
                    # pt(game_name)
            
            button.on_click = Func(on_click)
            self.game_buttons.append(button)



if __name__ == "__main__":
    app = Ursina()

    game_menu = GameMenu() 

    EditorCamera()

    app.run()
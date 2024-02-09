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
        
        # Create a button for each game
        for i, game_name in enumerate(games):
            row = i // num_columns
            col = i % num_columns
            
            button_x = start_x + col * (button_width * 1.15) - screen_width / 2 + button_width / 2  # Adjust position based on grid size
            button_y = start_y - row * (button_height * 1.15) + button_height / 2  # Adjust position based on grid size
            
            button = Button(text=game_name, position=(button_x, button_y), scale=(button_width, button_height))
            button.on_click = Func(self.run_game, game_name)


        
if __name__ == "__main__":
    app = Ursina()

    game_menu = GameMenu()  # Instantiate the game menu

    

    # Attempt to load and run the last selected game, otherwise show the menu
    try:
        with open('selected_game.txt', 'r') as f:
            selected_game = f.read().strip()
        os.remove('selected_game.txt')  # Remove the file after reading to avoid automatic selection next time
        game_menu.run_game(selected_game)  # Automatically run the selected game
    except FileNotFoundError:
        game_menu.show()  # Show the game menu if no game is selected

    EditorCamera()

    app.run()
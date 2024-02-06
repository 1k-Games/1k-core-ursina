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

def run_game(game_name):
    try:
        print(f"Attempting to import: game_templates.{game_name}.{game_name}")

        game_module = importlib.import_module(f"game_templates.{game_name}.{game_name}")

        if hasattr(game_module, 'run'):
            game_module.run()
        else:
            print(f"The module {game_name} does not have a 'run' function.")
    except ModuleNotFoundError:
        print(f"No game module found with the name: {game_name}")

def create_game_buttons():
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
    button_width = grid_width / num_columns
    button_height = grid_height / num_rows
    
    # Calculate starting position
    start_x = screen_width / 3  # Since the grid is on the right 2/3 of the screen
    start_y = screen_height / 2  # Start from the middle of the screen
    
    # Create a button for each game
    for i, game_name in enumerate(games):
        row = i // num_columns
        col = i % num_columns
        
        button_x = start_x + col * button_width - screen_width / 2 + button_width / 2  # Adjust position based on grid size
        button_y = start_y - row * button_height + button_height / 2  # Adjust position based on grid size
        
        button = Button(text=game_name, position=(button_x, button_y), scale=(button_width, button_height))
        button.on_click = Func(run_game, game_name)

if __name__ == "__main__":
    # Initialize Ursina engine
    app = Ursina()
    create_game_buttons()
    app.run()
from print_tricks import pt
from ursina import *


# eg_EG_Globals.py
class EG_Globals:


    #################################
    # ent_colors
    #################################
    ent_colors = {
        "enemies_color": color.Color(1,.4,.4,1),
        "teammates_color": color.blue,
        "npcs_color": color.yellow,
        "local_objects_color": color.gray,
        "environment_color": color.Color(1,1,1,1),
        "sky_color": color.Color(1,1,1,1),
        "shield_color": color.Color(1,1,1,0.5),
        "shield_part_color": color.Color(1,1,1,1),
        "core_color": color.Color(1,1,1,1),
        "player_color": color.Color(0, 0.85, 0, 1),
    }


    #################################
    # Energy BASE_COLORS & Shield BASE_COLORS
    #################################
    BASE_ENERGY_ALPHA = .9
    BASE_SHIELD_ALPHA = 1
    INDIVIDUAL_BASE_SHIELD_ALPHAS = [
        .2,    # >= 0       1 key       White
        .6,    # >= 100     2 key       Purple
        .56,   # >= 200     3 key       Blue
        .48,   # >= 300     4 key       Cyan
        .3,    # >= 400     5 key       Green   
        .45,   # >= 500     6 key       Lime Green   
        .55,   # >= 600     7 key       Yellow
        .44,   # >= 700    8 key        Orange
        .43,   # >= 800     9 key       Red
        .54,   # >= 900     0 key       Dark Red
        .55    # >= 1000   - key        Black
    ]

    BASE_COLORS = (
        (1, 1, 1),        # >= 0       White
        (0.5, 0, 0.5),    # >= 100     Purple
        (0, 0, 1),        # >= 200     Blue
        (0, 1, 1),        # >= 300     Cyan
        (0, 1, 0),        # >= 400     Green
        (0.6, 1, 0),      # >= 500     Lighter Green
        (1, 1, 0),        # >= 600     Yellow
        (1, 0.6, 0),      # >= 700     Light Orange
        (1, 0.3, 0),      # >= 800     Orange
        # (1, 0, 0),      # >= 900     Red
        (0.545, 0, 0),    # >= 1000    Dark Red
        (0, 0, 0))        # >= 1000    Black

    # BASE_COLORS = (
    #     (1, 1, 1),        # >= 0       White
    #     (0.5, 0, 0.5),    # >= 100     Purple
    #     (0, 0, 1),        # >= 200     Blue
    #     (0, 1, 1),        # >= 300     Cyan
    #     (0, 1, 0),        # >= 400     Green
    #     (0.5, 1, 0),      # >= 500     Lime Green
    #     (1, 1, .2),        # >= 600     Yellow
    #     (.9, .6, .2),    # >= 700     Orange
    #     (1, 0, 0),        # >= 800     Red
    #     (0.545, 0, 0),    # >= 900     Dark Red
    #     (0, 0, 0))        # >= 1000    Black

    #################################
    # current game objects
    #################################

    current_sets = {
        'energy_beings': set(),
        'enemies': set(),
        'enemy_characters': set(),
        'enemy_cores': set(),
        'enemy_shields': set(),
        'enemy_shield_parts': set(),
        'enemy_shield_part2s': set(),
        'teammates': set(),
        'teammate_characters': set(),
        'teammate_cores': set(),
        'teammate_shields': set(),
        'teammate_shield_parts': set(),
        'teammate_shield_part2s': set(),
        'npcs': set(),
        'npc_characters': set(),
        'npc_cores': set(),
        'npc_shields': set(),
        'npc_shield_parts': set(),
        'npc_shield_part2s': set(),
        'player_characters': set(),
        'player_cores': set(),
        'player_shields': set(),
        'player_shield_parts': set(),
        'player_shield_part2s': set(),
        'local_objects': set(),
        'environment_objects': set(),
        'characters': set(),
        'cores': set(),
        'shields': set(),
        'shield_parts': set(),
        'shield_part2s': set(),
        'slots': set(),
    }

    entity_sets = {key: value for key, value in current_sets.items()}

    @classmethod
    def ENERGY_COLORS(cls):
        return tuple(color.Color(*cls.BASE_COLORS[i], cls.BASE_ENERGY_ALPHA) for i in range(len(cls.BASE_COLORS)))

    @classmethod
    def SHIELD_COLORS(cls):
        return tuple(color.Color(*cls.BASE_COLORS[i], cls.INDIVIDUAL_BASE_SHIELD_ALPHAS[i] * cls.BASE_SHIELD_ALPHA) for i in range(len(cls.BASE_COLORS)))
    #################################

    @classmethod
    def add_to_appropriate_set(cls, obj, obj_type):
        type_to_set_map = {
            'character': {
                'Enemy': cls.current_sets['enemy_characters'],
                'Teammate': cls.current_sets['teammate_characters'],
                'NPC': cls.current_sets['npc_characters'],
                'Player': cls.current_sets['player_characters']  # Add this line
            },
            'core': {
                'Enemy': cls.current_sets['enemy_cores'],
                'Teammate': cls.current_sets['teammate_cores'],
                'NPC': cls.current_sets['npc_cores'],
                'Player': cls.current_sets['player_cores']  # Add this line
            },
            'shield': {
                'Enemy': cls.current_sets['enemy_shields'],
                'Teammate': cls.current_sets['teammate_shields'],
                'NPC': cls.current_sets['npc_shields'],
                'Player': cls.current_sets['player_shields']  # Add this line
            },
            'shield_part': {
                'Enemy': cls.current_sets['enemy_shield_parts'],
                'Teammate': cls.current_sets['teammate_shield_parts'],
                'NPC': cls.current_sets['npc_shield_parts'],
                'Player': cls.current_sets['player_shield_parts']  # Add this line
            },
            'shield_part2': {
                'Enemy': cls.current_sets['enemy_shield_part2s'],
                'Teammate': cls.current_sets['teammate_shield_part2s'],
                'NPC': cls.current_sets['npc_shield_part2s'],
                'Player': cls.current_sets['player_shield_part2s']  # Add this line
            }
            # Add more object types here
        }
        
        parent_type = type(obj.energy_being).__name__
        type_to_set_map[obj_type][parent_type].add(obj)



from ursina import *
import sys

if __name__ == '__main__':
    app = Ursina()

    # Define the initial color alphas
    INDIVIDUAL_BASE_SHIELD_ALPHAS = list(EG_Globals.INDIVIDUAL_BASE_SHIELD_ALPHAS)

    # Define the increment and decrement step size
    step_size = 0.1

    # Create a sphere entity
    background = Entity(model='quad', scale=100, color=color.black, z=22)
    player = Entity(model='sphere', scale=(1,2.5,1), color=color.red, z = -6)
    sphere = Entity(parent=player, model='sphere', world_scale=3, color=EG_Globals.SHIELD_COLORS()[0])

    # Define a variable to hold the current alpha type
    current_alpha_type = 'shield'
    selected_index = 0  # Add this line before the input function

    def input(key):
        global current_alpha_type, selected_index, background  # Add selected_index here

        # Check for number key press
        for num_key in '1234567890-':
            if key == num_key:
                # Get the index corresponding to the number key
                selected_index = int(num_key) - 1

        # Check for tab key press to switch between energy and shield alpha
        if key == 'tab':
            current_alpha_type = 'shield' if current_alpha_type == 'energy' else 'energy'
            print(f"Switched to {current_alpha_type} alpha")

        if key == 'q':
            background.color = color.white 
        if key == 'e':
            background.color = color.black
        # Check for window close event
        if key == 'escape':
            sys.exit()

    def update():
        global current_alpha_type, selected_index  # Add selected_index here

        # Define alpha before the if and elif blocks
        alpha = EG_Globals.INDIVIDUAL_BASE_SHIELD_ALPHAS[selected_index]

        # Check if left mouse button is pressed
        if held_keys['left mouse']:
            # Decrease the alpha value
            EG_Globals.INDIVIDUAL_BASE_SHIELD_ALPHAS[selected_index] = max(0, alpha - step_size * time.dt)
            # Print the new value
            print(f"Alpha {selected_index+1}: {alpha:.2f}, Adjusted Alpha: {alpha * (EG_Globals.BASE_ENERGY_ALPHA if current_alpha_type == 'energy' else EG_Globals.BASE_SHIELD_ALPHA):.2f}")

        # Check if right mouse button is pressed
        elif held_keys['right mouse']:
            # Increase the alpha value
            EG_Globals.INDIVIDUAL_BASE_SHIELD_ALPHAS[selected_index] = min(1, alpha + step_size * time.dt)
            # Print the new value
            print(f"Alpha {selected_index+1}: {alpha:.2f}, Adjusted Alpha: {alpha * (EG_Globals.BASE_ENERGY_ALPHA if current_alpha_type == 'energy' else EG_Globals.BASE_SHIELD_ALPHA):.2f}")

        # Update the sphere color based on the current alpha type
        if current_alpha_type == 'energy':
            sphere.color = color.Color(*EG_Globals.BASE_COLORS[selected_index], EG_Globals.BASE_ENERGY_ALPHA)
        else:
            sphere.color = color.Color(*EG_Globals.BASE_COLORS[selected_index], alpha * EG_Globals.BASE_SHIELD_ALPHA)
    
    app.run()
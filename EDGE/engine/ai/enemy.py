from print_tricks import pt
from ursina import *
from ursina import curve

path = []

enemy = Entity(model="cube", color=color.red, scale=1, visible = False)

def go(enemy, pos, duration):
    enemy.animate('position', pos, duration=duration, curve=curve.linear)
    # pt(pos)
    
def move(world_positions):
    if len(world_positions) < 3:  # Ensure there are at least 3 points
        print("Need at least 3 points to move between averages.")
        return

    enemy.position = world_positions[0]  # Start at the first position
    enemy.visible = True
    counter = 0
    duration = 0.04

    # Start from the second position since we're averaging with the previous and next
    for i in range(1, len(world_positions) - 1):
        # Calculate the average of the previous, current, and next positions
        avg_position = (world_positions[i-1] + world_positions[i] + world_positions[i+1]) / 3
        counter += duration
        invoke(go, enemy, avg_position, duration=duration, delay=counter)



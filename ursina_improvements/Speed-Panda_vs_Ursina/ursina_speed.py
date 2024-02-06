from print_tricks import pt
from direct.showbase.ShowBaseGlobal import globalClock
import time
import sys
import os
from ursina import *
from screeninfo import get_monitors


''' URSINA SPEED TEST '''


TOT_TIME_TO_RUN = int(os.getenv("TOT_TIME_TO_RUN", 10))
TIME_BETWEEN_PRINTS = int(os.getenv("TIME_BETWEEN_PRINTS", 1))

app = Ursina(
    development_mode=False,
    size=Vec2(800,600),
    vsync=False,
)
# pt(scene.entities)
# window.cog_menu.enabled=False
monitor = get_monitors()[0]
window_width = window.size[0]
window_height = window.size[1]

x = (monitor.width / 2) - (window_width / 2) + window.size[0]/2
y = (monitor.height / 2) - (window_height / 2)
window.position = (x,y)

camera.position=(0,0,0)

cube = Entity(model='cube', color=color.gray, position=(0,0,5))

start_time = time.time()
frame_count = 0
total_frame_count = 0

def update(): 
    global start_time, total_start_time, frame_count, total_frame_count
    cube.rotation += Vec3(10,10,10) * globalClock.getDt()
    
    frame_count += 1
    total_frame_count += 1
    elapsed_time = time.time() - start_time
    total_elapsed_time = time.time() - total_start_time
    
    if elapsed_time > TIME_BETWEEN_PRINTS:
        fps = frame_count / elapsed_time
        print(f"Ursina Average FPS: {int(fps)} - {total_elapsed_time=:.0f}")
        frame_count = 0
        start_time = time.time()

    if total_elapsed_time >= TOT_TIME_TO_RUN:
        total_fps = total_frame_count / total_elapsed_time
        print(f"Ursina Total Average FPS: {int(total_fps)}")
        application.quit()

total_start_time = time.time()

app.run()

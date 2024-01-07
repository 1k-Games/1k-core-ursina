from print_tricks import pt
from direct.showbase.ShowBaseGlobal import globalClock
import time
import sys, os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3
from direct.task import Task



''' PANDA3D SPEED TEST '''

TOT_TIME_TO_RUN = int(os.getenv("TOT_TIME_TO_RUN", 10))
TIME_BETWEEN_PRINTS = int(os.getenv("TIME_BETWEEN_PRINTS", 1))

app = ShowBase()
cube = app.loader.loadModel("models/box")
cube.reparentTo(app.render)
cube.setScale(1,1,1)
cube.setPos(0, 5, 0)
cube.setColor(0.5, 0.5, 0.5, 1)

frame_counter = 0
total_frame_counter = 0
start_time = globalClock.getLongTime()

def rotate_cube(task):
    global frame_counter, total_frame_counter, start_time
    dt = globalClock.getDt()
    cube.setHpr(cube.getHpr() + Point3(10, 10, 10) * dt)

    frame_counter += 1
    total_frame_counter += 1
    elapsed_time = time.time() - start_time
    total_elapsed_time = time.time() - total_start_time


    if elapsed_time >= TIME_BETWEEN_PRINTS:
        fps = frame_counter / elapsed_time
        print(f"Panda3d Average FPS: {int(fps)} - {total_elapsed_time=:.0f}")
        frame_counter = 0
        start_time = time.time()

    if total_elapsed_time >= TOT_TIME_TO_RUN:
        total_fps = total_frame_counter / total_elapsed_time
        print(f"Panda3d Total Average FPS: {int(total_fps)}")
        sys.exit()

    return Task.cont

task = app.taskMgr.add(rotate_cube, 'rotate_cube')
total_start_time = time.time()

app.run()
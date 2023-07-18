from print_tricks import pt




from direct.showbase.ShowBaseGlobal import globalClock
from ursina import *
import time
   
app = Ursina(development_mode=False)
cube = Entity(model='cube', color=color.gray)

start_time = time.time()
frame_count = 0

def update(): 
    global start_time, frame_count
    cube.rotation += Vec3(10,10,10) * globalClock.getDt()
    
    frame_count += 1
    elapsed_time = time.time() - start_time
    
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        print("Average FPS: ", fps)
        pt("Average FPS: ", fps)
        frame_count = 0
        start_time = time.time()

app.run()





# from direct.showbase.ShowBase import ShowBase
# from direct.showbase.ShowBaseGlobal import globalClock
# from panda3d.core import Point3
# from direct.task import Task

# app = ShowBase()
# cube = app.loader.loadModel("models/box")
# cube.reparentTo(app.render)
# cube.setScale(1,1,1)
# cube.setPos(0, 5, 0)
# cube.setColor(0.5, 0.5, 0.5, 1)

# frame_counter = 0
# start_time = globalClock.getLongTime()

# def rotate_cube(task):
#     global frame_counter, start_time
#     dt = globalClock.getDt()
#     cube.setHpr(cube.getHpr() + Point3(10, 10, 10) * dt)

#     frame_counter += 1
#     if globalClock.getLongTime() - start_time >= 1:
#         print("Average FPS: ", frame_counter)
#         frame_counter = 0
#         start_time = globalClock.getLongTime()

#     return Task.cont

# task = app.taskMgr.add(rotate_cube, 'rotate_cube')
# app.run()
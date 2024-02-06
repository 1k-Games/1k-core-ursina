from ursina import *

app = Ursina(vsync = True)
# app.vsync = True
cube = Entity(model='cube')

app.run()
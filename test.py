from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)


from ursina import *

app = Ursina(size=(1920,1080), development_mode=True)

e = Entity(name='e', model='cube', texture='white_cube')
pt(e.name)

EditorCamera()
app.run()





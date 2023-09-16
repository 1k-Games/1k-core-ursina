from print_tricks import pt

from ursina import *

app=Ursina(size=(1920,1080))

for i in scene.entities: ## prints fine
    print(i)

pt(scene.entities)  ## crashes

for i in scene.entities:
    pt(i.name)
app.run()





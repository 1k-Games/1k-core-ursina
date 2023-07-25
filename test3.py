
# from print_tricks import pt

# from ursina import *

# class Second(Entity):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#         print('---init---')
        
#     def on_enable(self):
#         print('---on enable---')
#         print()
#     def on_disable(self):
#         print('---on disable---- ')

# class First(Entity):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#         self.second = Second(
#             add_to_scene_entities=False,
#         )

# app=Ursina(size=(1920,1080))

# testsecond = Second(
#     add_to_scene_entities=False,
# )
# # First()
# print(scene.entities)
# app.run()







# from ursina import *
# app=Ursina(size=(1920,1080))

# testent = Entity(add_to_scene_entities=False)
# print(scene.entities)
# app.run()




from ursina import *

class Second(Entity):
    def __init__(self, add_to_scene_entities=False, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

        for _ in range(10):
            r = random.uniform(-5,5)
            e=Entity(model='cube', position=(r,r,r), parent=self)
    def on_enable(self):
        print('---on enable---')
    def on_disable(self):
        print('---on disable---- ')

app = Ursina(size=(1920, 1080))

second=Second(
    # add_to_scene_entities=False, 
    # enabled=False
    )

# second.disable()


app.run()
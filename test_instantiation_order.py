from print_tricks import pt

from ursina import *

# class Second(Entity):
#     def __init__(self, **kwargs):
#         super().__init__(add_to_scene_entities=False, **kwargs)
        
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
#             enabled=False
#         )

class A(Entity):
    
    pt(1, ' - class') # _ 1 _ #
    
    def __init__(
        self,
        x=777,
        y=888, 
        z=999,
        *args, **kwargs,
    ):
        pt(3, ' - Before super, inside def __init__') # _ 3 _ # 
        
        pt(x) # prints 777
        pt(y) # prints 888
        pt(z) # prints 999
        
        self.x = 000000 ## NOT SET - will not work - Full Entity not completed until super() 
        self.y = 111111 ## NOT SET - will not work - Full Entity not completed until super()
        self.z = 222222 ## NOT SET - will not work - Full Entity not completed until super()
        
        pt(self) ## prints "destroyed entity"
        
        # pt(self.z)  ## WILL CRASH APP, because it's a "destroyed_entity", doesn't have 
                        ## a self.z until super(). and self.z will be the default 
                        ## Entity value of 0.0
        
        super().__init__(*args, x=x, **kwargs)
        
        pt(5, ' - Ater super, inside def __init__') # _ 5 _ # 
        
        pt(x) # prints 777
        pt(y) # prints 888
        pt(z) # prints 999
        
        pt(self.x) # prints 777.0 - WAS EXPLICITALY PASSED INTO SUPER
        pt(self.y) # prints 0.0
        pt(self.z) # prints 0.0
    
    def on_enable(self):
        pt(4, ' - on_enable') # _ 4 _ #
    def on_disable(self):
        pt(4, ' - on_disable') # _ 4 _ #   ## NOTE: Will be run twice if "a = A(enabled=False)".. No idea why
        
app=Ursina(size=(1920,1080),
            development_mode=True)

pt(2, ' - Before class instance')  # _ 2 _ #

a = A(enabled=True)

app.run()



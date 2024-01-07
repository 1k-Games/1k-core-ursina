from print_tricks import pt 



from ursina import *
app=Ursina()
class EG_Object(Entity):
    def __init__(self, *args, **kwargs):
        self.add_to_scene_entities = False
        super().__init__(*args, self.add_to_scene_entities, **kwargs)
    # def update(self):
    #     pt.c("EG_Object update")

class Combility(EG_Object):
    def __init__(self, *args, name='', ignore_list=None, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        # super().update()

        pt.c("Combility update")
    
    def input(self, key):
        self.add_to_scene_entities = not self.add_to_scene_entities
        pt(self.add_to_scene_entities)
        # pt.p()
        
Combility()
app.run()

####################################################################################
# ursina BUG Update not working
####################################################################################
from ursina import *
app=Ursina()
class Combility(Entity):
    def __init__(self, *args, name='', ignore_list=None, **kwargs):
        self.attacher_ent = Entity(name='attacher_ent', model='sphere', color=color.orange, enabled=False)

        self.projectile_target_types = None     ## TODO These might not be necessary to initialize here
        self.assistant_target_types = None    ## TODO These might not be necessary to initialize here
        
        self.acceptable_projectile_targets = Entity(name='acceptable_projectile_targets') ## shooting raycasts/interceptions
        self.acceptable_assistant_targets = Entity(name='acceptable_assistant_targets') ## Secondary raycasts for things like dash surface types

        super().__init__(*args, **kwargs)
        ''' NOTE: 
            - I am currently using the term "path" to mean the projectile/combility/mod path, 
            So this is the projectile shape and the projectile curve/movements etc. 
            '''
        

        self.combility_built = False ## check if 'built' has been run on this class. If not, then this is not valid. 
                            ## built will check for validation that everything has been set. It should run everytime 
                            ## someone adds a mod to the combility or changes the value of one of the mods. 
        
        
        if ignore_list is None:
            self.ignore_list = [self]
        else:
            self.ignore_list = ignore_list + [self]
            
        self.name = name
        self.hit_info = None    # TODO, all of these may be uneseccary
        self.eaat = None        # TODO, all of these may be uneseccary
        self.hate = None        # TODO, all of these may be uneseccary
        self.model = 'cube'
        self.color = color.blue
        self.world_scale = (.1, .1, 1)

        self.path_model = None
        self.combility_barrel_end = Entity(parent=self, name='barrel_end', world_scale=(1,1,1), position=(0, 0, self.scale_z * 0.5), 
            # model='sphere'
        )
        
        # barrel_end_forward_visual = Entity(parent=self.combility_barrel_end, position=self.combility_barrel_end.forward, model='cube', scale=.2)
        
        combility_forward_visual = Entity(parent=self, name='combility_forward visual', position=self.forward*2, model='sphere', scale=1.5)
        
        self.combility_barrel_end_visual = duplicate(self.combility_barrel_end, name='barrel_end_visual', world_scale=.05, model='sphere', color=color.white)

        
        ######
        # Path
        ######
        self.max_range = 100
        self.falloff_range = 25 ## full damage until falloff_range. Damage goes from full to 1 damage
                                ### based on falloff_rate & falloff_curve. 
        self.falloff_rate = 1
        self.falloff_curve = 'linear' ## placeholder. Get the ursina curves as an import? 
        self.speed = inf
        
        ######
        # Control After Firing
        #####
        self.attacher = False 
        self.attacher_health = 1
        self.auto_swivel = False 
        
    

    def update(self):
        pt.t()
    def on_enable(self):
        pt(1)
    def on_disable(self):
        pt(2)

Combility()
app.run()
####################################################################################
# ursina BUG Demo: @every printing no matter what. 
####################################################################################
from ursina import *
app = Ursina()
class TestClass(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update(self):
        print('---------')
    # @every(0.1)
    # def test_func(self):
    #     print('every 0.1')

t = TestClass()
# t.enabled = False
app.run()



from ursina import *
app = Ursina()
class TextClass(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # print(self.animations)
    def on_enable(self):
        self.animations = []
    def on_disable(self):
        self.animations = None
        self.animations = []
    
    @every(.05)
    def test_func(self):
        pt('every')
        pt.ex()

TextClass()
app.run()




####################################################################################
# ursina BUG Demo: Ursina getting window size 
####################################################################################
from ursina import *

app = Ursina()

def input(key):
    if key == 'f':
        window.fullscreen = not window.fullscreen
        print(f"Fullscreen mode is now {'on' if window.fullscreen else 'off'}")
        print(f"Fullscreen size: {window.fullscreen_size[0]}x{window.fullscreen_size[1]}")
        print(f" size: {window.size[0]}x{window.size[1]}")

app.run()
####################################################################################
# Test - Attempt to spawn a render to texture on a quad with a side view of the normal
# camera
####################################################################################

# from ursina import *
# from panda3d.core import GraphicsOutput, Texture
# from panda3d.core import WindowProperties, FrameBufferProperties

# app = Ursina()

# # Create main camera
# camera = EditorCamera()

# # Create side camera
# side_camera = Entity(parent=camera, y=2, z=-2)
# side_camera.look_at(camera)

# # Create offscreen buffer
# win_props = WindowProperties.size(window.size[0], window.size[1])
# fb_props = FrameBufferProperties()
# fb_props.setRgbColor(True)
# fb_props.setRgbaBits(8, 8, 8, 8)
# buffer = app.graphicsEngine.make_output(
#     app.pipe, "offscreen buffer", -100,
#     fb_props, win_props,
#     GraphicsOutput.BF_refuse_window,
#     app.win.getGsg(), app.win)

# # Render side camera view into buffer
# side_camera_texture = Texture()
# buffer.addRenderTexture(
#     side_camera_texture,
#     GraphicsOutput.RTM_copy_ram,
#     GraphicsOutput.RTP_color)

# # Create quad and apply texture
# quad = Entity(parent=camera, model='quad', texture=side_camera_texture)

# app.run()

##############################################################################

# from ursina import *

# app = Ursina(
#     development_mode=False,
#     size=(800,600))

# app.run()

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
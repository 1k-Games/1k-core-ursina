'''
    NOTE: 
    PORTALS & BETTER SKYBOX:
    
    PORTALS:
    - If you place yourself outside of one of these spheres, it not only looks really cool, like
    a portal to another dimension, but when you walk through it, it is a seamless transition to this
    other "distant" area. So we can take a 360' photo of the other level and apply it to sphere, 
    and then when we walk into the sphere, we'll see it around us, then the real level can load up
    - When you enter/touch the portal, it will auto-scale to the new clip plane size / 2 and old
    one will disappear and/or it can simply change the texture of the skybox_1k... simplest
    and easiest approach. Then it can load the real level. 
        - Or, it loads the skybox of that new area, and then blows up this portal sphere to 
        just the local area that is supposed to be a snapshot of the models / characters etc
        on the other side. 
        
    BETTER SKYBOX:
    - My skybox is likely much more performant and simple than ursina's. 
        - parented to camera instead of updated on every frame to it. 
        - Uses the compass effect for performant rotation-based on render/scene
        - uses -x scale to flip the texture inside the sp
        here (instead of using double_sided)
        - TODO: Allow compatibility with these shapes:
            - Sphere
            - Dome
            - Box
    
    '''

from print_tricks import pt
pt.easy_imports('main.py')

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
import random

class StationaryGame(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.directory = os.path.join(self.script_directory, 
            "assets", "pics_3d",
            # "FreePik_com"
            "FreePolyHaven",
            )
        self.image_list = self.load_images(self.directory)
        self.current_image_index = 0


        #######################################
        ## MY CUSTOM SKYBOX_1K
        self.skybox_1k = Entity(
            parent=camera, 
            model='sphere')
        clip_scale = camera.clip_plane_far / 2
        self.skybox_1k.scale = (-clip_scale, clip_scale, clip_scale)
        self.skybox_1k.setCompass()
        #######################################

        #######################################
        ## PORTALS
        self.portal = Entity(
            model='sphere',
            scale=(-8, 8, 8),
            position=(-15, 1.75, -12)
            )
        self.skybox_1k.scale = (-clip_scale, clip_scale, clip_scale)
        #######################################
        
        # self.ground = Entity(model='plane', y=-1, scale=(15, 1, 15), 
        #                     texture='brick',
        #                     color=color.rgba(0,1,0,0.24),
        #                     # collider='box'
        #                     )
        self.player = FirstPersonController()
        self.player.gravity = False

    def load_images(self, directory):
        """Load all images from the specified directory."""
        images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        return images

    def random_image(self):
        random_picture = random.choice(self.load_images(self.directory))

        return random_picture

    def input(self, key):
        # pt(key)
        if key == 'g':
            self.skybox_1k.texture = self.random_image()
            
        if key == 'left arrow' or key == '1':
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.skybox_1k.texture = os.path.join(self.image_list[self.current_image_index])        
            self.portal.texture = os.path.join(self.image_list[self.current_image_index-1])        
            pt(self.skybox_1k.texture)
            
        elif key == 'right arrow' or key == '2':
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.skybox_1k.texture = os.path.join(self.image_list[self.current_image_index])        
            self.portal.texture = os.path.join(self.image_list[self.current_image_index-1])        
            pt(self.skybox_1k.texture)





if __name__ == "__main__":
    app = Ursina(
        development_mode=False,
        # borderless=True,
        )
    # window.fullscreen = False
    # window.size = (1280, 720)
    app.setFrameRateMeter(True)
    
    
    game = StationaryGame()
    
    app.run()


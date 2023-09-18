from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)
from ursina import *
from direct.interval.ActorInterval import LerpAnimInterval
from direct.actor.Actor import Actor

class ThirdPersonController(Entity):
    def __init__(self, 
                actor_model=None, 
                use_actor=True, 
                height=1,
                position=(0,.5,0),
                speed=2, 
                *args, **kwargs):
        self.camera_boom = Entity(name='camera_boom')
        
        self.height = height
        self.speed = speed
        self.rotation_speed = 88
        self.default_y = position[1]
        
        super().__init__(*args, **kwargs)
        
        # Set position after calling super().__init__()
        self.position = position
        
        pt.ci('---------- third person controller --------')
        
        self.mouse_sensitivity = Vec2(40, 40)
        
        self.setup_actor_or_model(actor_model, use_actor)
        
        self.direction = (0,0,0) ## setting this with initial starting point so code in update can work right. 
        self.last_direction = (1,1,1)
        self.rotation = (0,0,0)
        self.last_rotation = (0,0,0)
        
        # pt(self.position, self.world_position, 
        #     self.camera_boom.position, self.camera_boom.world_position, 
        #     camera.position, camera.world_position)
        
    def on_enable(self):
        mouse.locked = True
        self.setup_camera()
        self.y += self.default_y
    
    def on_disable(self):
        ...
        
    def setup_camera(self):
        
        # pt(camera.parent, camera.world_position, camera.position)
        # camera.world_position = self.camera_boom.world_position
        
        camera.fov = 90
        self.camera_boom.parent = self
        self.camera_boom.position=(0,1.25,-3.25)
        
        camera.position = self.camera_boom.position
        camera.parent = self.camera_boom
        
        # pt(self.camera_boom.parent, camera.parent, 
        #     camera.world_position, self.camera_boom.world_position)
        
    def setup_actor_or_model(self, actor_model, use_actor):
        if use_actor:
            try:
                if actor_model == None:
                    pt.ci('no actor model')
                    this_dir = Path(pt.l())
                    parent = this_dir.parent
                    pt(this_dir, parent)
                    cube = parent / 'assets' / 'cube.glb'
                    # pt(cube)
                    pt(1)
                    self.actor = Actor(cube)
                    pt(2)
                    self.actor.setScale(.33,.33,.33)
                    self.actor.reparent_to(self)  ## NOTE: Should the actor be reparented to the 
                                            ## ThirdPersonController, or the Player class from 
                                            ## each game project?
                    self.color = color.red
                else:
                    self.actor = Actor(actor_model)
                    self.actor.reparent_to(self)
            except:
                self.set_model()
        else:
            self.set_model()
            
    def set_model(self):
        self.model = 'cube'
        self.color = color.rgba(.2,.2,1,1)
        
    def update(self):
        # pt('-------------- third person controller ---------')
        # if pt.r(seconds=5):
        #     pt(camera.parent, self.camera_boom.parent, camera.world_position, camera.position, self.world_position, self.position, self.camera_boom.world_position, self.camera_boom.position)
        #     pt.ex()
        # self.last_direction = self.direction
        
        direction = Vec3(
            self.forward * ((held_keys['w'] - held_keys['s']) or held_keys['gamepad left stick y'])
            + self.right * ((held_keys['e'] - held_keys['q']) or held_keys['gamepad right stick x'])
            ).normalized()
        
        self.direction = Vec3(direction).normalized()
        move_amount = self.direction * time.dt * self.speed
        self.position += move_amount

        rotation = ((held_keys['d'] - held_keys['a']))
        self.rotation_y += rotation * time.dt * self.rotation_speed
        
        if held_keys['right mouse']:
            self.camera_boom.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        if not held_keys['right mouse'] and self.camera_boom != self.forward:
            self.camera_boom.rotation = lerp(self.camera_boom.rotation, self.forward, 1.25 * time.dt)
            
    def blend_anim(self, actor, animation, duration = .75, loop = True):
        
        actor.enableBlend()
        if loop:
            actor.loop(animation)
        else:
            actor.play(animation)
        blend = LerpAnimInterval(actor, duration, actor.getCurrentAnim(), animation)
        blend.start()
        
    def play_animation(self, action):
        if action in self.anims:
            self.actor.stop()  # Stop the current animation
            self.actor.loop(action)
#         else:
#             self.actor.stop()
#             pt('stop')

if __name__ == '__main__':
    app = Ursina(size=(1920,1080))
    ground = Entity(model='plane', position=(0,0,0), scale=(222,1,222), color=color.gray.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    ThirdPersonController(use_actor=False)
    Entity(model='cube', x=3, z=2)
    Sky()
    
    app.run()
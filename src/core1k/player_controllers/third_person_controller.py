from ursina import *
from direct.interval.ActorInterval import LerpAnimInterval
from direct.actor.Actor import Actor
from print_tricks import pt

class ThirdPersonController(Entity):
    def __init__(self, actor_model, height=1, speed=2, **kwargs):
        super().__init__(**kwargs)
        
        self.height = height
        self.y = 0
        self.speed = speed
        self.rotation_speed = 88

        # self.model = "cube"
        # self.color = color.red

        self.mouse_sensitivity = Vec2(40, 40)

        camera.parent = self
        camera.fov = 90
        camera.y = 1.25
        camera.z = -3.25

        mouse.locked = True
        
        self.actor = Actor(actor_model)
        self.actor.reparent_to(self)  ## NOTE: Should the actor be reparented to the 
                                        ## ThirdPersonController, or the Player class from 
                                        ## each game project? 
        # pt(self.actor)
        
        self.direction = (1,1,1) ## setting this with initial starting point so code in update can work right. 
        self.last_direction = (0,0,0)
        
    def update(self):
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
            camera.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        if not held_keys['right mouse'] and self.direction != self.forward:
            camera.rotation = lerp(camera.rotation, self.forward, 1 * time.dt)


    def blend_anim(actor, animation, duration = .75, loop = True):
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
    app = Ursina()
    ThirdPersonController()
    Entity(model='cube', x=3, z=2)
    Sky()

    app.run()
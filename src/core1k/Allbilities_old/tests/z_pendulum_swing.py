from manim import *
import math
import numpy as np

# if you have manim community installed,  I launched this with this command.   Use other flags for higher quality
# manim -p -ql pendulum_example_to_post.py Video
Gravity = 9.81
class Video(MovingCameraScene):
    def construct(self):
        self.pendulums = self.create_pendulums()
        self.play(self.camera.frame.animate.set(width=2.8).move_to([0,1.75,0]),run_time=0.01)
        self.animate()

    def create_pendulums(self):
        cycles_per_minute=[x for x in range(51,66)]  
        # back out the length by inverting this equation  period = 2 * math.pi * math.sqrt(length/Gravity)
        periods = [60.0 / x for x in cycles_per_minute]        
        lengths = [(period / 2 / math.pi)**2  * Gravity for period in periods]  # get the length that the pendulum would need to be to have the desired period
        pendulums = [Pendulum(length) for length in lengths]
        return pendulums

    def animate(self):
        all_mobs,all_phase_dots,all_delta_phase_dots = [],[],[]

        colors = [RED,RED_E,RED_C,RED_A,ORANGE,YELLOW,YELLOW_E,YELLOW_C,YELLOW_A,GREEN_E,GREEN_C,GREEN_A,BLUE,BLUE_E,BLUE_C,BLUE_A,PURPLE,PURPLE_E,PURPLE_C,PURPLE_A]
        for i, pendulum in enumerate(self.pendulums):
            # actual pendulum dot
            dot = Circle(radius = .02,color=colors[i % len(colors)]).move_to(pendulum.position)
            dot.pendulum = pendulum           
            all_mobs.append(dot)

            # circle in the top left,  each gets its own radius corresponding to the length of the pendulum
            delta_phase_circle = Circle(radius=pendulum.length / 2.5,color="GREY",arc_center=[-1.0,2.3,0],stroke_width=0.005)   
            delta_phase_dot = Circle(radius=.01,color=colors[i % len(colors)],stroke_width=1.0).set_fill(colors[i % len(colors)],opacity=1.0).move_to(delta_phase_circle.point_from_proportion(0.0))  
            delta_phase_dot.pendulum = pendulum
            delta_phase_dot.circle = delta_phase_circle
            all_delta_phase_dots.append(delta_phase_dot)             

        rate = 2/3.0  # can be used to slow everything down if less than 1.0, or speed it up if greater than 1.0
        def update_position(mob,dt):
            mob.pendulum.update_position(dt*rate) # update the backend location
            mob.move_to(mob.pendulum.position)    # update the graphics location

        for mob in all_mobs:
            mob.add_updater(update_position)    

        def update_line(line,dt): # an updater for the line of the pendulum
            line.put_start_and_end_on([0,2,0], all_mobs[line.index].pendulum.position)

        for i,mob in enumerate(all_mobs):
            line = Line(start=[0,2,0],end=mob.pendulum.position,stroke_width=.2)
            line.index =i
            line.add_updater(update_line)
            self.add(mob)
            self.add(line)

        def update_phase_dot(dot,dt):
            dot.move_to(dot.circle.point_from_proportion(dot.pendulum.phase%1))

        # circles in the top left
        for i, delta_phase_dot in enumerate(all_delta_phase_dots):
            delta_phase_dot.add_updater(update_phase_dot)
            self.add(delta_phase_dot)

        self.wait(60./rate)

class Pendulum: 
    def __init__(self,length):
        self.max_amplitude = math.radians(90)  # 90 degrees
        self.length = length
        self.scaling = 2.0
        self.offset = 0.0

        self.position_offset = np.array([0.0,2.0,0.0])
        self.position = np.array([0.0,0.0,0.0]) 
        self.time = 0
        dt=0.0
        self.phase = 0

        self.update_position(dt)

    # from kahn academy video https://www.youtube.com/watch?v=WPa5IgLgDyQ
    def update_position(self,dt):
        self.time += dt
        period = 2 * math.pi * math.sqrt(self.length/Gravity)
        theta = self.max_amplitude * math.cos(2 * math.pi / period * self.time + self.offset)
        x,y = self.length*self.scaling * math.sin(theta),0 - (self.length*self.scaling * math.cos(theta))
        self.position = np.array([x,y,0.0]) + self.position_offset
        self.phase = self.time / period
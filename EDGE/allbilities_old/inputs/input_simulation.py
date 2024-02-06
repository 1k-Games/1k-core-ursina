''' We need:

    - Fake VR controller that acts like triggers, grips, buttons, etc. 
        - See EG sheets for more information
        



    - Combility Controller-trigger system:
        - The controller to actually control the combility itself. 
        - Maps one button & its pressure levels to the Combility stages. 
            - For example:
                - Press in: 
                    - Set a rope/attacher
                - don't change pressure:
                    - maintain length
                - press in more: 
                    - retract rope (you move towards attacher)
                - release more
                    - detract rope (lengthen / move away)
                - release all the way:
                    - on_disable the combility.
        - Actions at each stage:
            - Change any properties of your combility
            - Start other combilities
            - Stop any combilities (Pressure level 1 does one combility, and 2 starts another)
    

'''
from print_tricks import pt

from ursina import *

from allbilities.ccaus.ccaus import CAUS
from characters.target_types import Slot

# class FakeVRController_system2(Entity):
#     '''System 2'''
#     def __init__(self, combilities):
#         super().__init__()
#         self.cur_combilities = combilities if isinstance(combilities, list) else [combilities]

#         self.default_pressure_level = 0
#         self.cur_pressure_level = 0
#         self.max_pressure_level = 100
#         self.fake_pressure_increment = 20
        
#         self.time_since_pressure_change = 0
#         self.pressure_change_cooldown = 0.06  ## 60ms cooldown = 300ms to go from 0-100% pressure

#         #######################
#         ## Control Multiple user or enemy slots at once for testing purposes
#         ## NOT CURRENLTY USED. By default it goes through the list, which most likely
#         ## is a list of 1. 
#         ######################
#         self.cur_combility = self.cur_combilities[0] 
#         self.control_multiple_simultaneous_combilities = False
#         ######################
        
#     def action_mapping(self, pressure_level):
#         '''NOTE TEMP PLACEHOLDER:
#         - This system is per combility. What does this combility want to do when
#         different trigger systems are hit? '''
        
#         if pressure_level > 0:
#             # if not self.control_multiple_simultaneous_combilities:
#             #     self.cur_combilities[0].shoot()
            
#             # else: 
#                 for combility in self.cur_combilities:
#                     combility.shoot()
        
#     def input(self, key):
#         if key == 'left mouse down':
#             self.change_pressure(self.fake_pressure_increment)
#         elif key == 'right mouse down':
#             self.change_pressure(-self.fake_pressure_increment)
        
#     def update(self):
#         if held_keys['left mouse'] and time.time() - self.time_since_pressure_change > self.pressure_change_cooldown:
#             self.change_pressure(self.fake_pressure_increment)
#         elif held_keys['right mouse'] and time.time() - self.time_since_pressure_change > self.pressure_change_cooldown:
#             self.change_pressure(-self.fake_pressure_increment)

#     def change_pressure(self, change):
#         self.cur_pressure_level = min(max(self.cur_pressure_level + change, 0), self.max_pressure_level)
#         self.action_mapping(self.cur_pressure_level)
#         self.time_since_pressure_change = time.time()
#         # pt(self.cur_pressure_level)
            
#     def update_combilities_list(self, combilities):
#         self.cur_combilities = combilities
        
# class FakeVRController1(Entity):
#     '''system 2a'''
#     def __init__(self, combilities):
#         super().__init__()
#         self.cur_combilities = combilities if isinstance(combilities, list) else [combilities]
        
#         self.default_pressure_level = 0
#         self.cur_pressure_level = 0
#         self.max_pressure_level = 100
#         self.half_max_pressure = self.max_pressure_level / 2
#         self.fake_pressure_increment = 20
        
#         self.time_since_pressure_change = 0
#         self.pressure_change_cooldown = 0.12  ## 120ms cooldown = 600ms to go from 0-100% pressure

#         self.pressure_increment_mode = False
#         self.left_mouse_down_time = 0
        
#         ######################
#         ## Control Multiple user or enemy slots at once for testing purposes
#         ## NOT CURRENLTY USED. By default it goes through the list, which most 
#         ## likely is a list of 1. 
#         ######################
#         self.cur_combility = self.cur_combilities[0] 
#         self.control_multiple_simultaneous_combilities = False
#         ######################
        
#     def action_mapping(self, pressure_level):
#         '''NOTE TEMP PLACEHOLDER:
#         - This system is per combility. What does this combility want to do when
#         different trigger systems are hit? '''
        
#         if pressure_level > 0:
#             for combility in self.cur_combilities:
#                 combility.shoot()
        


#     def input(self, key):
#         if self.pressure_increment_mode:
#             if key == 'left mouse down':
#                 self.change_pressure(self.fake_pressure_increment)
#             elif key == 'right mouse down':
#                 self.change_pressure(-self.fake_pressure_increment)
#                 if self.cur_pressure_level == 0:
#                     self.pressure_increment_mode = False
#         else:
#             if key == 'left mouse down':
#                 self.time_since_pressure_change = time.time()
#                 self.cur_pressure_level = self.half_max_pressure
#                 self.change_pressure(0)
#             elif key == 'left mouse up':
#                 self.cur_pressure_level = 0
#                 self.change_pressure(0)
#                 self.time_since_pressure_change = 0
#             elif key == 'right mouse down':
#                 self.pressure_increment_mode = True
#             elif key == 'right mouse up':
#                 self.pressure_increment_mode = False
        
#     def update(self):
#         if self.pressure_increment_mode:
#             if held_keys['right mouse'] and held_keys['left mouse']:
#                 self.cur_pressure_level = 0
#                 self.pressure_increment_mode = False
#                 self.change_pressure(0)
                
#             elif held_keys['left mouse'] and time.time() - self.time_since_pressure_change > self.pressure_change_cooldown:
#                 self.change_pressure(self.fake_pressure_increment)
            
#             elif held_keys['right mouse'] and time.time() - self.time_since_pressure_change > self.pressure_change_cooldown:
#                 self.change_pressure(-self.fake_pressure_increment)
#         else:
#             if held_keys['left mouse'] and time.time() - self.time_since_pressure_change > self.pressure_change_cooldown:
#                 self.change_pressure(0)

#     def change_pressure(self, change):
#         self.cur_pressure_level = min(max(self.cur_pressure_level + change, 0), self.max_pressure_level)
#         self.action_mapping(self.cur_pressure_level)
#         self.time_since_pressure_change = time.time()
#         pt(self.cur_pressure_level)
            
#     def update_combilities_list(self, combilities):
#         self.cur_combilities = combilities


class VR_Trigger_Simulator(Entity):
    '''system 2a'''
    def __init__(self, caus_device, debug_pressure_levels=False, **kwargs):
        super().__init__(**kwargs)
        self.map_caus_to_trigger(caus_device)
        
        self.default_pressure_level = 0
        self.cur_pressure_level = 0
        self.max_pressure_level = 100
        self.half_max_pressure = self.max_pressure_level / 2
        self.fake_pressure_increment = 20
        
        self.time_since_pressure_change = 0
        self.pressure_change_cooldown = 0.12  # 120ms cooldown = 600ms to go from 0-100% pressure
        
        self.pressure_increment_mode = False
        self.left_mouse_down_time = 0
        
        self.debug_pressure_levels = debug_pressure_levels
        
    def change_pressure(self, change):
        self.cur_pressure_level = min(max(self.cur_pressure_level + change, 0), self.max_pressure_level)
        self.caus_device.action_mapping(self.cur_pressure_level)
        self.time_since_pressure_change = time.time()
        if self.debug_pressure_levels:
            pt(self.cur_pressure_level)
    
    def map_caus_to_trigger(self, caus_device):
        # print(f'---------------{caus_device.name=}')
        # pt(caus_device.name)
        # pt.ex()
        # self.caus_device = caus_device[0] ## BUG TODO, I'm currently just supporting one caus device
        self.caus_device = caus_device
        
    def input(self, key):
        if self.pressure_increment_mode:
            self.process_pressure_increment_mode(key)
        else:
            self.process_normal_mode(key)
        
        # if self.debug_pressure_levels:
        #     pt(self.cur_pressure_level)
    
    def update(self):
        if self.pressure_increment_mode:
            self.update_pressure_increment_mode()
        else:
            self.update_normal_mode()
        
    def process_pressure_increment_mode(self, key):
        if key == 'left mouse down':
            self.change_pressure(self.fake_pressure_increment)
        elif key == 'right mouse down':
            self.change_pressure(-self.fake_pressure_increment)
            if self.cur_pressure_level == 0:
                self.pressure_increment_mode = False

    def process_normal_mode(self, key):
        if key == 'left mouse down':
            self.time_since_pressure_change = time.time()
            self.cur_pressure_level = self.half_max_pressure
            self.change_pressure(0)
        elif key == 'left mouse up':
            self.reset_pressure()
        elif key == 'right mouse down':
            self.pressure_increment_mode = True
        elif key == 'right mouse up':
            self.pressure_increment_mode = False

    def reset_pressure(self):
        self.cur_pressure_level = 0
        self.change_pressure(0)
        self.time_since_pressure_change = 0

    def update_pressure_increment_mode(self):
        if held_keys['right mouse'] and held_keys['left mouse']:
            self.cur_pressure_level = 0
            self.pressure_increment_mode = False
            self.change_pressure(0)
        elif held_keys['left mouse'] and self.is_cooldown_over():
            self.change_pressure(self.fake_pressure_increment)
        elif held_keys['right mouse'] and self.is_cooldown_over():
            self.change_pressure(-self.fake_pressure_increment)

    def update_normal_mode(self):
        if held_keys['left mouse'] and self.is_cooldown_over():
            self.change_pressure(0)

    def is_cooldown_over(self):
        return time.time() - self.time_since_pressure_change > self.pressure_change_cooldown

class VRControllerSimulator(Entity):
    ''' (Currently PSEUDO CODE) 
    Goal: 
    - To simulate the HMD and both Controllers, completely. 
    - May or may not call isntances of other classes (like the trigger class)'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trigger_left = VR_Trigger_Simulator()
        self.grip_left = VR_Trigger_Simulator()
        self.trigger_right = VR_Trigger_Simulator()
        self.grip_right = VR_Trigger_Simulator()
        
        # Initialize buttons and joystick
        self.trigger = False
        self.grip = False
        self.joystick = {'x': 0, 'y': 0}
        self.joystick_button = False
        self.x_button = False
        self.y_button = False
        self.menu_button = False
        self.a_button = False
        self.b_button = False
        self.oculus_button = False

        # Initialize controller position and rotation
        self.position = {'x': 0, 'y': 0, 'z': 0}
        self.rotation = {'x': 0, 'y': 0, 'z': 0}

    # Button press/release methods
    def press_trigger(self):
        self.trigger = True

    def release_trigger(self):
        self.trigger = False

    # ... repeat for other buttons ...

    # Joystick move method
    def move_joystick(self, x, y):
        self.joystick['x'] = x
        self.joystick['y'] = y

    # Controller move and rotate methods
    def move_controller(self, x, y, z):
        self.position['x'] = x
        self.position['y'] = y
        self.position['z'] = z

    def rotate_controller(self, x, y, z):
        self.rotation['x'] = x
        self.rotation['y'] = y
        self.rotation['z'] = z

if __name__ == '__main__':
    from allbilities.ccaus.ccaus import CAUS
    class FakeCombility(Entity):
        def __init__(self, add_to_scene_entities=True, **kwargs):
            super().__init__(add_to_scene_entities, **kwargs)
            
        def shoot(self):
            pt(self.name, 'shoot')
            
    app=Ursina()
    fc = FakeCombility(name='fc - fake combility')
    test_caus_device_1 = CAUS(name='test_caus_device_1',
        combilities = fc)
    right_trigger = VR_Trigger_Simulator(test_caus_device_1, debug_pressure_levels=True)
    right_trigger.map_caus_to_trigger(test_caus_device_1) ## We can swap out caus's to triggers
                                                            ## here.
    app.run()
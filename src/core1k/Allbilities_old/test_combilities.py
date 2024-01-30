'''
Combilities organization: 

Main.py

game_manager.py

test_combilities.py (My placeholder that I currently have with hundreds of tests, all written out inefficiently)

Level.py

Input_simulation.py

Character classes

CCAUS.py

Combilities.py

pre-built_combilities.py (& sub files for the pre-builts)

mod_sender_category.py (one file to organize several modding files. These are the actions on the person sending the mod to the recipient)

Mod_receiver_category.py (the actions to be done on the character when receiving the mod action)

'''

from ursina import *

def test_combilities(app, level):
    
    from eg_globals import EG_Globals
    from allbilities.ccaus.ccaus import CAUS
    from inputs.input_simulation import VR_Trigger_Simulator
    from allbilities.combilities.combility import Combility
    
    player = level.player
    slot_owner = level.weapon_slot_1.owner

    enemies, teammates, npcs, local_objects, environment = EG_Globals.level_target_types
    
    
    class Test_Device_Builds_Manager(Entity):
        def __init__(self, test_device_builds):
            super().__init__()
            self._test_device_builds = test_device_builds
            self.cur_test_device_build_index = 0
            self.cur_test_device_build = self._test_device_builds[self.cur_test_device_build_index]
            self.current_combilities = self.cur_test_device_build.combilities  # List of combilities
            self.current_devices = self.cur_test_device_build.devices  # Update the list of combilities
            
            # print(self.current_combilities)
            # pt.ex()
            # self.current_trigger_simulator = MultiCombilityController(self.current_combilities)  # Pass the list to the controller
            # self.current_trigger_simulator = VR_Trigger_Simulator(self.current_combilities)  # Pass the list to the controller
            # self.current_trigger_simulator = VR_Trigger_Simulator(self.current_devices)  # Pass the list to the controller
            
            # Start all combilities disabled
            for device_build in self._test_device_builds:
                device_build.disable()
                for device in device_build.devices:
                    device.disable()
                for combility in device_build.combilities:
                    combility.disable()


            self.current_trigger_simulator = VR_Trigger_Simulator(device)
            
        def reset_transforms(self):
            level.reset_transforms()
            # for device in self.current_devices:
            #     device.attach_to_slot(level.weapon_slot_1)
            
        def input(self, key):
            if key == 'scroll up' or key == 'scroll down':
                # Disable the current devices
                for device in self.current_devices:
                    device.disable()

                for combility in self.current_combilities:
                    combility.disable()

                # Update the current combility index based on the scroll direction
                if key == 'scroll down':
                    self.cur_test_device_build_index = (self.cur_test_device_build_index + 1) % len(self._test_device_builds)
                else:
                    self.cur_test_device_build_index = (self.cur_test_device_build_index - 1) % len(self._test_device_builds)

                self.cur_test_device_build.disable()
                # Enable the new current combilities
                self.cur_test_device_build = self._test_device_builds[self.cur_test_device_build_index]
                self.cur_test_device_build.enable()

                self.current_combilities = self.cur_test_device_build.combilities  # Update the list of combilities
                self.current_devices = self.cur_test_device_build.devices  # Update the list of combilities


                # #######################
                # ## enable Devices
                for device in self.current_devices:
                    
                    # level.weapon_slot_1.attach_caus_device(device)
                    
                    self.current_trigger_simulator.map_caus_to_trigger(device)  # Pass the list to the controller

                    device.enable()
                    device.color = color.rgba(random.random(), random.random(), random.random(), 1)
                
                for combility in self.current_combilities:
                    combility.enable()
                    pt(combility.name)
                    # combility.add_to_scene_entities=False

            if key == 'r':
                self.reset_transforms()
                
    class test_device_builds:
        def __init__(self, debug=False):
            
            #############
            # instantiate all combilities, efficiently
            #############
            self.test_device_builds = [cls() for name, cls in inspect.getmembers(self, self.is_class_in_test_device_builds)]
            
            ############
            # instantiate all combilities for testing
            ############
            if debug:
                # pt.t(1)
                self.test_device_builds = []
                for name, cls in inspect.getmembers(self, self.is_class_in_test_device_builds):
                #     pt.t(cls)  # print the name
                    self.test_device_builds.append(cls())
                    pt(cls)
                #     pt.t(cls)
                
                # pt.t(1)
            ############
            
            self.manager = Test_Device_Builds_Manager(self.test_device_builds)
            
        def is_class_in_test_device_builds(self, member):
            return inspect.isclass(member) and member.__module__ == test_device_builds.__module__ and member != test_device_builds

        ###############################
        # TEST TYPES TESTS TYPES TESTS TO TRY test_types_test_combilities test combilities test tests testing
        ###############################

        class Test_camera_visual_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    slot_owner
                    
                })
                
                self.combility.compile_path(range=34)

        class Test_camera_prop_zoom_in(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_prop_zoom', fov=55, energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner,
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_prop_zoom_out(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_prop_zoom', fov=115, energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner,
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_prop_zooming_incremental_in(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_prop_zooming_incremental', fov_step=-3, step_timing=0.05, energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner,
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_prop_zooming_incremental_out(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_prop_zooming_incremental', fov_step=7, step_timing=0.025, energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner,
                })
                
                self.combility.compile_path(range=34)

        # class Test_camera_prop_pip(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_pip', 
        #             cam_parent=None, 
        #             position=Vec3(0,0,0),
        #             rotation=Vec3(0,0,0),
        #             energy_amount=111
        #             )                
        #         self.combility.add_target_types(general={
        #             # self.caus_device.slot_owner,
        #             self.combility,
        #         })
                
        #         self.combility.compile_path(range=34)

        # class Test_camera_prop_pip_backwards(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_pip', 
        #             cam_parent=None, 
        #             position=Vec3(0,0,0),
        #             rotation=Vec3(180,0,0), 
        #             energy_amount=111
        #             )                
        #         self.combility.add_target_types(general={
        #             # self.caus_device.slot_owner,
        #             self.combility,
        #         })
                
        #         self.combility.compile_path(range=34)

        # class Test_camera_prop_pip_zoom_in_pip_view(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_pip', 
        #             cam_parent=None, 
        #             position=Vec3(0,0,0),
        #             rotation=Vec3(0,0,0),
        #             energy_amount=111
        #             )
        #         self.combility.add_mod('camera_prop_zoom', fov=11, energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)

        # class Test_camera_prop_pip_zoom_in_main_view(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_pip', 
        #             cam_parent=None, 
        #             position=Vec3(0,0,0),
        #             rotation=Vec3(0,0,0),
        #             energy_amount=111
        #             )
        #         self.combility.add_mod('camera_prop_zoom', fov=11, energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)
        
        # class Test_camera_prop_rtt(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_rtt', 
        #             cam_parent=None, 
        #             position=Vec3(0,0,0),
        #             rotation=Vec3(0,0,0),
        #             energy_amount=111
        #             )
        #         # self.combility.add_mod('camera_prop_zoom', fov=11, energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)
        
        

        class Test_camera_prop_create_pip(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('create_pip',
                    pip_name='new pip',
                    camera_name=None,
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    corner_positions=(0.01, 0.38, 0.78, 0.98),
                    energy_amount=111
                    )                
                self.combility.add_target_types(general={
                    # self.caus_device.slot_owner,
                    self.combility,
                })
                
                self.combility.compile_path(range=34)

        class Test_camera_prop_new_cam_4_pip(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('new_camera',
                    cam_parent=None,
                    rtt_name=None,
                    pip_name='new pip',
                    camera_name='new pip',
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    energy_amount=111
                    )
                self.combility.add_target_types(general={
                    # self.caus_device.slot_owner,
                    self.combility,
                })
                
                self.combility.compile_path(range=34)

        class Test_camera_prop_pip_then_cam(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('create_pip',
                    pip_name='new pip',
                    camera_name=None,
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    corner_positions=(0.01, 0.38, 0.78, 0.98),
                    energy_amount=111
                    )
                self.combility.add_mod('new_camera',
                    cam_parent=None,
                    rtt_name=None,
                    pip_name='new pip',
                    camera_name='new pip',
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    energy_amount=111
                    )
                self.combility.add_target_types(general={
                    # self.caus_device.slot_owner,
                    self.combility,
                })
                
                self.combility.compile_path(range=34)

        class Test_camera_prop_cam_then_pip(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('new_camera',
                    cam_parent=None,
                    rtt_name=None,
                    pip_name='new pip',
                    camera_name='new pip',
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    energy_amount=111
                    )
                self.combility.add_mod('create_pip',
                    pip_name='new pip',
                    camera_name=None,
                    position=Vec3(0,0,0),
                    rotation=Vec3(0,0,0),
                    corner_positions=(0.01, 0.38, 0.78, 0.98),
                    energy_amount=111
                    )
                self.combility.add_target_types(general={
                    # self.caus_device.slot_owner,
                    self.combility,
                })
                
                self.combility.compile_path(range=34)
        
        
        class Test_camera_x_ray_grey(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_x_ray', mode='grey', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner,
                })
        
                self.combility.compile_path(range=34)
        class Test_camera_x_ray_colors(Entity):
            def __init__(self):

                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                # self.combility.attach_to_slot(level.weapon_slot_1)
                
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
                self.combility.add_mod('camera_x_ray', mode='colors', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.caus_device.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
                
        class Test_camera_night_vision_grey(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_night_vision', color=Color(0.25,0.25,0.25,1), energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_night_vision_green(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_night_vision', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_thermal_vision_grey(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_thermal_vision', color=Color(0.25,0.25,0.25,1), energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_thermal_vision_red(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_thermal_vision', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_bw_beings(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_bw_beings', color=Color(0.25,0.25,0.25,1), energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_bw_non_beings(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_bw_non_beings', color=Color(0.35,0.35,0.35,1), energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility.slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_visual_this_combility(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility,

                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_visual_others(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment,
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_tk_grab_others(Entity):
            '''TODO: 
                - It uses energy amount and distance to determine how delayed
                the tk is. But 3 kids (so far) want the opposite kind of? They seem to like the delayed one the
                best because they think it'd help make throwing easier. 
                - Figure out how it should work. Figure out the relationship
                with the amounts of energy/distance etc. 
                
                '''
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('tk_grab', energy_amount=1)
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    
                })
                
                self.combility.compile_path(range=22)
        class Test_dash_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('dash', 
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    visual_resolution=33,
                    path_resolution=6,
                    rotation=(0,0,45),
                    surface_types={
                        enemies,
                        teammates,
                        npcs,
                        local_objects,
                        environment}
                    )
                
                self.combility.add_target_types(general={slot_owner})
        class Test_dash_all(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('dash',
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=180,
                    rotation=(0,0,0),
                    surface_types={
                        enemies,
                        teammates,
                        npcs,
                        local_objects,
                        environment
                        }
                    )
                
                
                
                self.combility.add_target_types(general={
                    # self.combility,
                    slot_owner,
                    # enemies,
                    # teammates,
                    # npcs,
                    # local_objects,
                    # environment,
                })
                
                
                # self.combility.add_points_to_path(
                #     (0,.9,.05),
                #     (0,0,.3),
                #     (0,0,.6),
                # )
                # self.combility.compile_path(range=34)
        class Test_dash_others(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('dash', 
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    visual_resolution=33,
                    path_resolution=6,
                    rotation=(0,0,45),
                    surface_types={environment})
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_dash_others_direction(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                
                self.combility.add_mod('dash', 
                    range=20,
                    speed=100,
                    direction='right',
                    scale=(1,.6,1),
                    circle_degrees=360,
                    visual_resolution=33,
                    path_resolution=6,
                    surface_types={environment})
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_experimental_animation_points(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                self.combility.add_mod('experimental_animation_points',
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    rotation=(0,0,0))
                
                self.combility.add_target_types(general={slot_owner})
        class Test_experimental_juggle_others(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                
                self.combility.add_mod('experimental_animation_points',
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    rotation=(0,0,90))
                
                self.combility.add_target_types(general={enemies, teammates, npcs, local_objects})
                self.combility.compile_path(range=34)
        class test_copy_target(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment})
                
                self.combility.add_mod("copy_target")  

                
                self.combility.compile_path(range=33)
        class test_copy_target_body(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment},
                    specific='eb_body',
                    )
                
                self.combility.add_mod("copy_target")
                self.combility.compile_path(range=33)
        class test_camo_energy_being(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment})

                self.combility.add_mod("camo", 1.0)

                self.combility.compile_path(range=33)
        class test_camo_body(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(
                    general={
                        enemies, teammates, npcs,
                        local_objects, environment
                        }, 
                    specific='eb_body'
                    )

                # self.combility.add_weapon_type(
                #     WeaponTypeEnum.DeveloperLaser, 100)

                self.combility.add_mod("camo")
                
                self.combility.compile_path(range=33)
        class test_camo_shield(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(
                    general={enemies, teammates, npcs},
                    specific='eb_shield')
                
                self.combility.add_mod("camo")
                
                self.combility.compile_path(range=33)
        class test_visibility_energy_being(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(general={enemies, teammates, npcs})

                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.compile_path(range=33)
        class test_visibility_energy_being_damage(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                
                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.compile_path(range=33)
        class test_visibility_body(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_body')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_shield(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_shield')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_shield_damage(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_shield')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(general={slot_owner}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_this_combility(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(general={self.combility}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_local_objects(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_target_types(general={local_objects}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.add_mod('force', 'up', 3)

                self.combility.compile_path(range=33)
        class Test_Damage_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_mod('dmg_developer_laser', energy_amount=100)
                self.combility.add_target_types(general={slot_owner})

                self.combility.compile_path(range=33)     
        class Test_Damage(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]

                self.combility.add_mod('dmg_developer_laser', energy_amount=100)
                self.combility.add_target_types(general={enemies, teammates, npcs})

                self.combility.compile_path(range=33)      
        class Test_curve_scale_1(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies})
                self.combility.add_curve_to_path(circle_degrees=180)

                self.combility.compile_path(range=1)
        class Test_curve_range_10(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'up', 4)

                self.combility.add_curve_to_path(circle_degrees=180)

                self.combility.compile_path(range=10)
        class Test_curve_stretched_scale_1(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_curve_to_path(
                    scale=(1,1.2,11),
                    # scale=(1,11,3),
                    circle_degrees=180,
                )
                
                self.combility.compile_path(range=1)
        class Test_curve_stretched_range_10(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'up', 4)

                self.combility.add_curve_to_path(
                    scale=(1,1.2,11),
                    # scale=(1,11,3),
                    circle_degrees=180,
                )

                self.combility.compile_path(range=10)
        class Test_full_circle_10(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'right', 10)

                self.combility.add_curve_to_path(
                    # scale=(1,1.2,11),
                    # scale=(1,11,3),
                    circle_degrees=360,
                )

                self.combility.compile_path(range=10)
        class Test_full_circle_stretched_10(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_curve_to_path(
                    scale=(1,1.2,11),
                    # scale=(1,11,3),
                    circle_degrees=360,
                )

                self.combility.compile_path(range=10)
        class Test_blink_up(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,

                })
                
                self.combility.add_mod('force', 'up', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_forward_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    slot_owner,
                })
                
                self.combility.add_mod('force', 'forward', 11, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_push(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                
                self.combility.add_mod('force', 'push', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_left_8(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                
                self.combility.add_mod('force', 'left', 8, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_left_25(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                
                self.combility.add_mod('force', 'left', 25, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_right_15(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                
                self.combility.add_mod('force', 'right', 15, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_backward_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False)
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    slot_owner,
                })
                
                self.combility.add_mod('force', 'backward', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_up_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    slot_owner,
                })
                
                self.combility.add_mod('force', 'up', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_impulse_up_from_custom_verts(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                                
                # self.combility.add_mod('force', 'push', 10)
                self.combility.add_mod('force', 'up', 4)
                self.combility.add_points_to_path(
                    Vec3(0,.9,.05),
                    Vec3(0,0,.3),
                    Vec3(0,0,.6),
                )

                self.combility.compile_path(range=10, rotation=Vec3(180,-111,90))
        class Test_impulse_push_from_custom_verts(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                # self.combility.add_mod('dmg_developer_laser', 400)
                                
                # self.combility.add_mod('force', 'push', 10)
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_points_to_path(
                    Vec3(0,.9,.05),
                    Vec3(0,0,.3),
                    Vec3(0,0,.6),
                )

                self.combility.compile_path(range=10, rotation=Vec3(0,-78,90))
        class Test_impulse_up(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                # self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'up', 4)

                self.combility.compile_path(range=33)
        class Test_impulse_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    slot_owner,
                    # self.combility,
                    # enemies,
                    # teammates,
                    # npcs,
                })
                
                self.combility.add_mod('force', 'right', 3)

                self.combility.compile_path(range=10)
        class Test_impulse_on_this_combility(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    self.combility,
                    # enemies,
                    # teammates,
                    # npcs,
                })
                
                self.combility.add_mod('force', 'up', 3)

                self.combility.compile_path(range=10)
        class Test_impulse_custom_direction(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                # self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', Vec3(3,2,3), 10)

                self.combility.compile_path(range=33)
        class Test_teleport(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                # self.combility.add_mod('dmg_developer_laser', 400)
                                
                self.combility.add_mod('force', 'forward', 11, type='teleport')
                self.combility.compile_path(range=33)
        class Test_teleport_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    slot_owner,
                    # self.combility,
                    # enemies,
                    # teammates,
                    # npcs,
                })
                                
                self.combility.add_mod('force', Vec3(3,1,-3), 13, type='teleport')
                self.combility.compile_path(range=10)
        class Test_custom_complex_path_and_rotation(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                
                self.combility.add_mod('force', 'back', 10)                
                
                self.combility.add_points_to_path(
                    Vec3(.5, .5, 0),
                    Vec3(.8,-.5, 0)
                )

                self.combility.add_points_to_path(
                    Vec3(0,.9,.05),
                    Vec3(0,0,.3),
                    Vec3(0,0,.6),
                )

                self.combility.add_curve_to_path(
                    # scale=(1,1.2,11),
                    # scale=(1,3,3),
                    scale=(1,11,3),
                    circle_degrees=90,
                )


                self.combility.add_points_to_path(
                    Vec3(0,-.4,.7),
                    # Vec3(0,-4,8),
                    # Vec3(0,-4,9),
                )

                self.combility.compile_path(range=10, rotation=Vec3(45,0,0))
        class Test_attacher_straight_line(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'push', 10)
                
                self.combility.add_mod('attacher', 25)
                self.combility.compile_path(range=33)
        class Test_attacher_curved_line(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_curve_to_path(
                    # scale=(1,1.2,11),
                    scale=(1,3,3),
                    # scale=(1,11,3),
                    circle_degrees=220,
                )

                self.combility.add_mod('attacher', 25)
                self.combility.compile_path(range=22)
        class Test_attacher_straight_auto_swivel(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'push', 10)
                
                self.combility.add_auto_swivel()
                self.combility.add_mod('attacher', 25)

                self.combility.compile_path(range=22)
        class Test_attacher_curved_auto_swivel(Entity):
            def __init__(self):
                
                self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
                self.caus_device.attach_new_combility(self.combility)
                level.weapon_slot_1.attach_caus_device(self.caus_device)
                self.devices = [self.caus_device]
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_curve_to_path(
                    # scale=(1,1.2,11),
                    scale=(1,3,3),
                    # scale=(1,11,3),
                    circle_degrees=220,
                )

                self.combility.add_auto_swivel()
                self.combility.add_mod('attacher', 25)

                self.combility.compile_path(range=22)





        ######################### 
        ######################### 
        ######################### 
        # BROKEN COMBILITIES
        ######################### 
        ######################### 
        #########################
        
        # class Test_camera_prop_resolution_1920_300(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_prop_resolution', resolution=(1920,300), energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)
        # class Test_camera_prop_resolution_777_900(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_prop_resolution', resolution=(777,800), energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)
        # class Test_camera_prop_resolution_400_300(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         # self.combility.attach_to_slot(level.weapon_slot_1)
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        #         # self.right_trigger_assignment = VR_Trigger_Simulator(self.caus_device)
                
                
        #         self.combility.add_mod('camera_prop_resolution', resolution=(400, 300), energy_amount=111)

        #         self.combility.add_target_types(general={
        #             self.caus_device.slot_owner,
        #         })
                
        #         self.combility.compile_path(range=34)


        # class Test_camera_visual_projectile(Entity): ## NOT YET IMPLEMENTED 
        #     def __init__(self):
        
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
        
        
        #         self.combility.add_mod('camera_visual', energy_amount=111)
        
        #         projectile = 1
        #         self.combility.add_target_types(general={
        #             projectile,
        
        #         })
        
        #         self.combility.compile_path(range=34)

        # class Test_Damage_dispersion(Entity):
        #     def __init__(self):
        #         combility = self.create_combility(level.weapon_slot_1)
        #         combility.add_target_types({enemies, teammates, npcs})
        #         enemy_combility = self.create_combility(level.enemy_weapon_slot)
        #         enemy_combility.add_target_types({player})
                
        #         self.combilities = [combility, enemy_combility]

        #     def create_combility(self, slot):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', ignore_list=[])
        #         self.combility.attach_to_slot(slot)

        #         self.combility.add_mod('dmg_developer_laser', 100)

        #         self.combility.compile_path(range=11)
        #         return self.combility

        # class Test_c_dash_owner(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
                
                
        #         self.combility.add_mod('dash', 
        #             range=33,
        #             # speed=77,
        #             # direction=None, 
        #             rotation=(0,0,33), 
        #             # scale=(1,.6,1), 
        #             # circle_degrees=222, 
        #             # visual_resolution=33, 
        #             # path_resolution=6, 
        #             # surface_types={enemies, teammates, npcs, local_objects, environment},
        #             dash_style='c_dash', 
        #             c_dash_last_line=Vec3(1,-3,-1), 
        #             # path_type='assistant'
        #             )
                
        #         self.combility.add_target_types(general={slot_owner})

        # class Test_c_dash_others(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
                
                
        #         self.combility.add_mod('dash', 
        #             range=33,
        #             # speed=77,
        #             # direction=None, 
        #             rotation=(0,0,33)
        #         #     scale=(1,.6,1), 
        #         #     circle_degrees=222, 
        #         #     visual_resolution=33, 
        #         #     path_resolution=6, 
        #         #     surface_types={enemies, teammates, npcs, local_objects, environment},
        #         #     dash_style='c_dash', 
        #         #     c_dash_last_line=Vec3(1,-3,1), 
        #         #     path_type='assistant')
        #         )
                
        #         self.combility.add_target_types(general={
        #             enemies,
        #             teammates,
        #             npcs,
        #             local_objects,
        #             environment
                    
        #         })
                
        #         self.combility.compile_path(range=34)
                
        # class Test_camera_electro_magnetic(Entity):
        #     def __init__(self):
        
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
                
                
        #         self.combility.add_mod('camera_electro_magnetic', energy_amount=111)
                
        #         self.combility.add_target_types(general={
        #             self.combility
                    
        #         })
                
        #         self.combility.compile_path(range=34)
                
        # class test_mimic_energy_being(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types,
        #             name=f'Combility - {self.__class__.__name__}', ignore_list=[player],
        #                                     add_to_scene_entities=False
        #                                     )
        #         self.combilities = [self.combility,]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]
                
        #         self.combility.add_target_types(
        #             general={enemies, teammates, npcs, local_objects, environment},
        #             )
                
        #         self.combility.add_mod('mimic')
                
        #         self.combility.compile_path(range=33)
        # class test_mimic_shield(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #                                     add_to_scene_entities=False
        #                                     )
        #         self.combilities = [self.combility,]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]

        #         self.combility.add_target_types(
        #             general={enemies, teammates, npcs, local_objects, environment},
        #             specific='eb_shield',
        #             )
                
        #         self.combility.add_mod('mimic')
                
        #         self.combility.compile_path(range=33)
        # class test_mimic_body(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(EG_Globals.level_target_types, name=f'Combility - {self.__class__.__name__}', enabled=False, ignore_list=[player],
        #                                     add_to_scene_entities=False
        #                                     )
        #         self.combilities = [self.combility,]
        #         self.caus_device = CAUS(name=f'CAUS - {self.__class__.__name__}', enabled=False)
        #         self.caus_device.attach_new_combility(self.combility)
        #         level.weapon_slot_1.attach_caus_device(self.caus_device)
        #         self.devices = [self.caus_device]

        #         self.combility.add_target_types(
        #             general={enemies, teammates, npcs, local_objects, environment},
        #             specific='eb_body',
        #             )
                
        #         self.combility.add_mod("mimic", duration=1.0, debug=True)

                
        #         self.combility.compile_path(range=33)
        
        
        



    test_device_builds = test_device_builds()
    
    app.run()
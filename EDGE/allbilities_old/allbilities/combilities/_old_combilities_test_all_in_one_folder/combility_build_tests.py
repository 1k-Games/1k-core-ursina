'''NOTE Not currently working'''

from print_tricks import pt 
from ursina import *

from input_simulation import CombilityController
import globals
from combility import Combility

# import testing_range
# tester_bot = level.tester_bot
import testing_range_city as testing_range

if __name__ == '__main__':
    app = Ursina(
    # size=(1280, 720),
    # borderless=False,
    # fullscreen=True,
    # development_mode=False
    )
    window.position=(360,0)
    
    level = testing_range.BuildLevel()
    tester_bot = level.tester_bot
    combility_testing_equipment = level.combility_testing_equipment
    slot_owner = level.weapon_slot_1.owner

    enemies, teammates, npcs, local_objects, environment = globals.level_target_types


    class CombilityManager(Entity):
        def __init__(self, combilities):
            super().__init__()
            self.combility_builds = combilities
            self.current_combility_build_index = 0
            self.current_combility_build = self.combility_builds[self.current_combility_build_index]
            self.current_combilities = self.current_combility_build.combilities  # List of combilities
            
            self.cc = CombilityController(self.current_combilities)  # Pass the list to the controller
            
            # Start all combilities disabled
            for combility_build in self.combility_builds:
                combility_build.disable()
                for combility in combility_build.combilities:
                    combility.disable()
                    
        def reset_transforms(self):
            level.reset_transforms()
            for combility in self.current_combilities:
                combility.attach_to_slot(level.weapon_slot_1)
                
        def input(self, key):
            if key == 'scroll up' or key == 'scroll down':
                # Disable the current combilities
                self.current_combility_build.disable()
                for combility in self.current_combilities:
                    combility.disable()
                    
                # Update the current combility index based on the scroll direction
                if key == 'scroll down':
                    self.current_combility_build_index = (self.current_combility_build_index + 1) % len(self.combility_builds)
                else:
                    self.current_combility_build_index = (self.current_combility_build_index - 1) % len(self.combility_builds)
                    
                # Enable the new current combilities
                self.current_combility_build = self.combility_builds[self.current_combility_build_index]
                self.current_combility_build.enable()
                
                self.current_combilities = self.current_combility_build.combilities  # Update the list of combilities
                
                ## SWAP COMBILITIES
                for combility in self.current_combilities:
                    combility.enable()
                    combility.color = color.rgba(random.random(), random.random(), random.random(), 1)
                    # combility.add_to_scene_entities=False
                    pt(combility.name)
                    # pt.p()
                    
                self.cc.update_combilities_list(self.current_combilities)  # Update the combilities in the controller
            
            if key == 'r':
                self.reset_transforms()
    class TestCombilityBuilds:
        def __init__(self, debug=False):
            
            #############
            # instantiate all combilities, efficiently
            #############
            self.TestCombilityBuilds = [cls() for name, cls in inspect.getmembers(self, self.is_class_in_TestCombilityBuilds)]
            
            ############
            # instantiate all combilities for testing
            ############
            if debug:
                # pt.t(1)
                self.TestCombilityBuilds = []
                for name, cls in inspect.getmembers(self, self.is_class_in_TestCombilityBuilds):
                #     pt.t(cls)  # print the name
                    self.TestCombilityBuilds.append(cls())
                    pt(cls)
                #     pt.t(cls)
                
                # pt.t(1)
            ############
            
            self.manager = CombilityManager(self.TestCombilityBuilds)
            
        def is_class_in_TestCombilityBuilds(self, member):
            return inspect.isclass(member) and member.__module__ == TestCombilityBuilds.__module__ and member != TestCombilityBuilds

        ###############################
        # TEST TYPES TESTS TYPES TESTS TO TRY test_types_test_combilities test combilities
        ###############################


        class Test_camera_x_ray_1(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('camera_x_ray_1', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility
                    
                })
                
                self.combility.compile_path(range=34)

        class Test_camera_electro_magnetic(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('camera_electro_magnetic', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_visual_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    slot_owner
                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_visual_this_combility(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    self.combility,

                    
                })
                
                self.combility.compile_path(range=34)
        class Test_camera_visual_others(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('camera_visual', energy_amount=111)
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment,
                    
                })
                
                self.combility.compile_path(range=34)
        # class Test_camera_visual_projectile(Entity):
        #     def __init__(self):
                
        #         self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
        #             add_to_scene_entities=False
        #         )
        #         self.combilities = [self.combility]
        #         self.combility.attach_to_slot(level.weapon_slot_1)
                
                
        #         self.combility.add_mod('camera_visual', energy_amount=111)
                
        #         projectile = 1
        #         self.combility.add_target_types(general={
        #             projectile,
                    
        #         })
                
        #         self.combility.compile_path(range=34)
        class Test_tk_grab_others(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('tk_grab', energy_amount=200)
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    
                })
                
                self.combility.compile_path(range=34)
        
        class Test_c_dash_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('dash', 
                    range=33,
                    # speed=77,
                    # direction=None, 
                    rotation=(0,0,33), 
                    # scale=(1,.6,1), 
                    # circle_degrees=222, 
                    # visual_resolution=33, 
                    # path_resolution=6, 
                    # surface_types={enemies, teammates, npcs, local_objects, environment},
                    # dash_style='c_dash', 
                    # c_dash_last_line=Vec3(1,3,1), 
                    # path_type='assistant'
                    )
                
                self.combility.add_target_types(general={slot_owner})

        class Test_c_dash_others(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
                self.combility.add_mod('dash', 
                    range=33,
                    # speed=77,
                    # direction=None, 
                    rotation=(0,0,33)
                #     scale=(1,.6,1), 
                #     circle_degrees=222, 
                #     visual_resolution=33, 
                #     path_resolution=6, 
                #     surface_types={enemies, teammates, npcs, local_objects, environment},
                #     dash_style='c_dash', 
                #     c_dash_last_line=Vec3(1,-3,1), 
                #     path_type='assistant')
                )
                
                self.combility.add_target_types(general={
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                    environment
                    
                })
                
                self.combility.compile_path(range=34)
                

        class Test_dash_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                self.combility.add_mod('experimental_animation_points',
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    rotation=(0,0,0))
                
                self.combility.add_target_types(general={slot_owner})
                
        class Test_experimental_juggle_others(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                    add_to_scene_entities=False
                )
                self.combilities = [self.combility]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                self.combility.add_mod('experimental_animation_points',
                    range=20,
                    scale=(1,.6,1),
                    circle_degrees=360,
                    rotation=(0,0,90))
                
                self.combility.add_target_types(general={enemies, teammates, npcs, local_objects})
                self.combility.compile_path(range=34)
                
        class test_mimic_energy_being(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types,
                    name=self.__class__.__name__, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                
                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment},
                    )
                
                self.combility.add_mod('mimic')
                
                self.combility.compile_path(range=33)
        class test_mimic_shield(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment},
                    specific='eb_shield',
                    )
                
                self.combility.add_mod('mimic')
                
                self.combility.compile_path(range=33)
        class test_mimic_body(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment},
                    specific='eb_body',
                    )
                
                self.combility.add_mod("mimic", duration=1.0, debug=True)

                
                self.combility.compile_path(range=33)
        class test_copy_target(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment})
                
                self.combility.add_mod("copy_target")  

                
                self.combility.compile_path(range=33)
        class test_copy_target_body(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment},
                    specific='eb_body',
                    )
                
                self.combility.add_mod("copy_target")

                
                self.combility.compile_path(range=33)
                
        class test_camo_energy_being(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs, local_objects, environment})

                self.combility.add_mod("camo", 1.0)

                self.combility.compile_path(range=33)
        class test_camo_body(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(
                    general={enemies, teammates, npcs},
                    specific='eb_shield')
                
                self.combility.add_mod("camo")
                
                self.combility.compile_path(range=33)
        class test_visibility_energy_being(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(general={enemies, teammates, npcs})

                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.compile_path(range=33)
        class test_visibility_energy_being_damage(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                
                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.compile_path(range=33)
        class test_visibility_body(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_body')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_shield(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_shield')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_shield_damage(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_mod('dmg_developer_laser', 100)
                self.combility.add_target_types(general={enemies, teammates, npcs}, specific='eb_shield')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(general={slot_owner}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_this_combility(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(general={self.combility}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)

                self.combility.compile_path(range=33)
        class test_visibility_local_objects(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_target_types(general={local_objects}, specific='')
                
                self.combility.add_mod('visibility', 0.0, 1.0)
                
                self.combility.add_mod('force', 'up', 3)

                self.combility.compile_path(range=33)
        class Test_Damage_dispersion(Entity):
            def __init__(self):
                combility = self.create_combility(level.weapon_slot_1)
                combility.add_target_types({enemies, teammates, npcs})
                enemy_combility = self.create_combility(level.enemy_weapon_slot)
                enemy_combility.add_target_types({tester_bot})
                
                self.combilities = [combility, enemy_combility]

            def create_combility(self, slot):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, ignore_list=[])
                self.combility.attach_to_slot(slot)

                self.combility.add_mod('dmg_developer_laser', 100)

                self.combility.compile_path(range=11)
                return self.combility
        class Test_Damage(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)

                self.combility.add_mod('dmg_developer_laser', energy_amount=100)
                self.combility.add_target_types(general={enemies, teammates, npcs})

                self.combility.compile_path(range=33)      
        class Test_curve_scale_1(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies})
                self.combility.add_curve_to_path(circle_degrees=180)

                self.combility.compile_path(range=1)
        class Test_curve_range_10(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_mod('dmg_developer_laser', 400)
                self.combility.add_target_types(general={enemies, teammates, npcs})
                self.combility.add_mod('force', 'up', 4)

                self.combility.add_curve_to_path(circle_degrees=180)

                self.combility.compile_path(range=10)
        class Test_curve_stretched_scale_1(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
        class Test_blink_push(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
        class Test_blink_right_15(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False)
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_target_types(general={
                    slot_owner,
                })
                
                self.combility.add_mod('force', 'backward', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_blink_up_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_target_types(general={
                    slot_owner,
                })
                
                self.combility.add_mod('force', 'up', 5, type='blink')

                self.combility.compile_path(range=33)
        class Test_impulse_up_from_custom_verts(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                    (0,.9,.05),
                    (0,0,.3),
                    (0,0,.6),
                )

                self.combility.compile_path(range=10, rotation=Vec3(180,-111,90))
        class Test_impulse_push_from_custom_verts(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                self.combility.add_mod('force', 'push', 10)

                self.combility.add_points_to_path(
                    (0,.9,.05),
                    (0,0,.3),
                    (0,0,.6),
                )

                self.combility.compile_path(range=10, rotation=Vec3(0,-78,90))
        class Test_impulse_up(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', 'up', 4)

                self.combility.compile_path(range=33)
        class Test_impulse_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                
                self.combility.add_mod('force', Vec3(3,2,3), 10)

                self.combility.compile_path(range=33)
        class Test_teleport(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
                self.combility.add_target_types(general={
                    # slot_owner,
                    # self.combility,
                    enemies,
                    teammates,
                    npcs,
                    local_objects,
                })
                self.combility.add_mod('dmg_developer_laser', 400)
                                
                self.combility.add_mod('force', 'forward', 11, type='teleport')
                self.combility.compile_path(range=33)
        class Test_teleport_slot_owner(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                    (.5, .5, 0),
                    (.8,-.5, 0)
                )

                self.combility.add_points_to_path(
                    (0,.9,.05),
                    (0,0,.3),
                    (0,0,.6),
                )

                self.combility.add_curve_to_path(
                    # scale=(1,1.2,11),
                    # scale=(1,3,3),
                    scale=(1,11,3),
                    circle_degrees=90,
                )


                self.combility.add_points_to_path(
                    (0,-.4,.7),
                    # (0,-4,8),
                    # (0,-4,9),
                )

                self.combility.compile_path(range=10, rotation=Vec3(45,0,0))
        class Test_attacher_straight_line(Entity):
            def __init__(self):
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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
                
                self.combility = Combility(globals.level_target_types, name=self.__class__.__name__, enabled=False, ignore_list=[combility_testing_equipment],
                                            add_to_scene_entities=False
                                            )
                self.combilities = [self.combility,]
                self.combility.attach_to_slot(level.weapon_slot_1)
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



    TestCombilityBuilds()
    
    app.run()
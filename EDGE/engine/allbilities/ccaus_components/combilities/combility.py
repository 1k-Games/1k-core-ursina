'''
    Keys:
        (Note: severely limit the keys. These are mainly for cutting out long typing, but if I don't
        immediately remember what each key is when reading it, then it won't really help)
        
        - eaat: 'The entity who is going to eat our actions' - 'entity_to_apply_actions_to'
        - hate: 'Your targeting me to use against others' - 'hit_assistant_target_ent'
'''

from print_tricks import pt
from bidict import bidict

import weakref
from enum import Enum
import inspect, textwrap
import math
from math import sin
from collections import deque

from ursina import *
from ursina import curve
from panda3d.core import CompassEffect  ## use this for rotations only. Can point
                                        ## at another ent for free, don't use for
                                        ## rotations/scales due to rendering/cull.
from panda3d.core import Camera

from allbilities.mod_senders import mod_senders_main
import inspect


                
from temp_core1k.light_entities import *
from temp_core1k.linecast import linecast
from assets.dynamic.create_mesh_path import Mesh_Creator
from characters.target_types import EnergyBeing, EG_Object, Shield, AnimatingShieldPart, Character, Core
from eg_globals import EG_Globals

mesh_creator = Mesh_Creator()

# import hotloader


# class Jitter_Teleport_Curve:
#     def __init__(self, 
#         jitter_duration=1.0, 
#         jump_duration=0.01, 
#         end_duration=0.04,
#         backward_jitter=-0.05,
#         forward_jitter=0.01,
#     ):
        
#         self.combility_backward_jitter = backward_jitter
#         self.forward_jitter = forward_jitter
        
        
#         # Normalize the durations
#         self.total = jitter_duration + jump_duration + end_duration
#         self.jitter_duration = jitter_duration / self.total
#         self.jump_duration = jump_duration / self.total
#         self.end_duration = end_duration / self.total
#         self.jitter_ended = False

#     def __call__(self, t):
#         t /= self.total  # normalize t to the duration
#         if t < self.jitter_duration:
#             ## Jitter back and forward, mostly back. 
#             return self.combility_backward_jitter * t + self.forward_jitter * sin(10 * pi * t)
#         else:
#             if not self.jitter_ended:
#                 self.jitter_ended = True
#                 return 0.93
#             else:
#                 # Use a square root function for the end phase
#                 end_t = (t - (self.jitter_duration + self.jump_duration)) / self.end_duration
#                 return 0.93 + 0.07 * (1 - sqrt(1 - min(end_t, 1)))


class WeaponTypeEnum(Enum):
    Ice = "Ice"
    Fire = "Fire"
    Gas = "Gas"
    Lightning = "Lightning"
    Solids = "Solids"
    SuspendedSolids = "SuspendedSolids"
    FusedSolids = "FusedSolids"
    ElectroLaserTunnel = "ElectroLaserTunnel"
    Microwave = "Microwave"
    Plasma = "Plasma"
    Laser = "Laser"
    EnergyDisruptor = "EnergyDisruptor"
    DeveloperLaser = "DeveloperLaser"

################################
#       -form Types             #
################################
class FormEnum(Enum):
    TKHand = "TKHand"
    Rod = "Rod"
    Rope = "Rope"
    Grapple = "Grapple"
    Beam = "Beam"
    Beam_EnergyBeam = "EnergyBeam"
    Beam_Rod = "Rod"
    Beam_Rope = "Rope"
    Beam_Grapple = "Grapple"
    Ball = "Ball"
    SelfCore = "SelfCore"
    SelfShield = "SelfShield"
    ShieldProjection = "ShieldProjection"
    Noform = "Noform"
    Specialforms = "Specialforms"

class EnergyShapeTypeEnum(Enum):
    Cylinder = "Cylinder"
    Cube = "Cube"
    Cone = "Cone"
    ReversedCone = "Reversed Cone"
    Sphere = "Sphere"
    Custom = "Custom"

class Form:
    ################################
    #       -form Functions         #
    ################################0-
    @staticmethod
    def add_form(form):
        if isinstance(form, str):
            form = form.strip().upper().replace(' ', '_')
            for form_class in vars(Form).values():
                if isinstance(form_class, type):
                    form_type = getattr(form_class, form, None)
                    if form_type is not None:
                        return form_type
            else:
                raise ValueError(f"Invalid form type: {form}")
        elif isinstance(form, form):
            return form
        else:
            raise TypeError("form must be a string or an instance of form")


class Combility(EG_Object):

    '''
    ##############################################################################
    # BUILD A MOD, TUTORIAL:
    ##############################################################################
    - user creates a "add_mod" call, which dynamically looks for and loads:
        - prepare_action (optional)
            - changing variable values if needed, calculating things, creating helper entities. 
        - use_action
            - What to do when we shoot and hit a target
        - update_action (optional)
            - What to do on update frames
            
    - Example:
        class Combility:
            default_action_params = {
            "example": {
                "args": ("arg_1", "arg_2"), 
                "kwargs": {"kwarg_1": 2.0, "kwarg_2": "extra_value"}
            }}
                
            Call: 
                self.combility.add_mod("example", energy_amount)
                
            def prepare_example(self, energy_amount):
                energy_amount += 100
                self.example_health = 443 * energy_amount
                self.example_ent = Entity(enabled=False)

                return energy_amount ## optional return
                
            def use_example(self, energy_amount):
                self.example_ent.enabled = True 

                self.add_update_function_if_exists("example", (energy_amount,))

            def update_example(self, energy_amount):
                print(energy_amount)            
        ##############################################################################
        '''
    
    
    stored_copied_entity = None             ## Stored for all Combilities to use
    stored_copied_entity_attributes = None  ## Stored for all Combilities to use
    fixed_combility_updates_list = []
    
    
    ## Displays and cameras have a nickname that is either user-created, or auto-generated, 
    pip_regions = {}
    rtt_regions = {}
    cameras = {}
    
    def __init__(self, level_target_types, *args, name='', ignore_list=None, **kwargs):
        
        self.level_target_types = level_target_types
        
        self.attacher_ent = None
        self.eternal = False
        
        self.original_animations = None
        
        
        self.mod_actions = []
        self.mod_actions_readable = []
        self.mod_updates = []
        self.mod_updates_readable = []
        self.mod_enables = []
        self.mod_enables_readable = []
        self.mod_disables = []
        self.mod_disables_readable = []
        
        ###########################
        # Temp vars for testing, maybe be used permanently eventually. 
        ###########################
        self.is_grabbing = False ## TODO: Either delete this or move this to add_tk or something. 
        self.compass_effect = None
        
        
        
        ##################
        # Target Types
        ##################
        self.projectile_target_types = None     ## TODO These might not be necessary to initialize here
        self.assistant_target_types = None    ## TODO These might not be necessary to initialize here
        
        self.acceptable_bot_projectile_targets = Entity(name='acceptable_bot_projectile_targets') ## shooting raycasts/interceptions
        self.acceptable_bot_assistant_targets = Entity(name='acceptable_bot_assistant_targets') ## Secondary raycasts for things like dash surface types
        ## plural name(s), because each entity controls all of the children parented to hit
        ###NOTE: ^^^^^^^^^^^^^^^^^^^^^ This is an optimizatin that WILL more than likely CAUSE A BUG in the future. 
        ### - We set the parent all of the entities that can be hit by this combility to self.acceptable_bot_projectile_targets. 
        ### - We pass self.acceptable_bot_projectile_targets into the traverse target. 
        
        ### POSSIBLE BUG 1:
        ### - if all enemy entities have a parent of "enemies", then they can't be parented to other
        ###   objects etc. like a spaceship etc. 
        ### SOLUTION BUG 1:
        ###- We could use panda3d CompassEffect on them though, which doesn't have the benefits
        ###  or drawbacks of using a parent, beause it just updates their position/rotation. 
        
        ### POSSIBLE BUG 2:
        ### - If target types get parented to a combility Self.acceptable_bot_projectile_targets ,then 
        ###  the target types are stuck under that original combility. 
        ### SOLUTION BUG 2:
        ### - Whenever the Combility is about to do its own personal frame update
        ###   (on input/update), it gets the self.acceptable_bot_projectile_targets from when this combility was
        ###   first created, and it parents them under self.acceptable_bot_projectile_targets once again (20-30us)
        ####################################
        
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
        self.combility_barrel_end = Entity(name='barrel_end', parent=self, world_scale=(1,1,1), position=(0, 0, self.scale_z * 0.5))
        self.combility_barrel_end_visual = duplicate(self.combility_barrel_end, name='barrel_end_visual', world_scale=.05, model='sphere', color=color.white)
                
        combility_forward_visual = Entity(name='combility_forward_visual', parent=self, position=self.forward*5, model='sphere', scale=(.5,.5,2))
        
        self.weapon_functions = {weapon_type: getattr(self, self.to_snake_case(weapon_type.value), None) for weapon_type in WeaponTypeEnum}  
        ## ^^^^^^  This builds the weapon functions from those listed in WeaponTypeEnum
        
        
        ######
        # Path
        ######
        # self.max_range = 100
        self.path_range = 1
        self.falloff_range = 25 ## full damage until falloff_range. Damage goes from full to 1 damage
                                ### based on falloff_rate & falloff_curve. 
        self.falloff_rate = 1
        self.falloff_curve = 'linear' ## placeholder. Get the ursina curves as an import? 
        self.speed = inf
        
        ######
        # Wave Reception
        ######
        self.default_camera_fov = 90
        ######
        # Control After Firing
        #####
        self.attacher_health = 16
        self.auto_swivel = False
        
        ######
        # Display Regions & Extra Cameras
        # display_regions
        ######
        # self.main_display_region = None ## Temp set to none in case none of our mods need access to these. 
        # self.ursina_window = None   ## Temp set to none in case none of our mods need access to these. 

        ######
        # Animation vars
        #####
        
        # self.animations.append(Sequence(
        #     Func(self.testblah), Wait(1), loop=True, started=True))
                
        # self.animations.append(Sequence(
        #     Func(self.testblah), Wait(1), loop=True, started=True))
        
        # self.animation_sequence = Sequence(
        #     Func(self.testblah), Wait(1), loop=True, started=True
        # )
        # self.animations.append(self.animation_sequence)
    ################################
    #       -Defaults              #
    ################################
    
    def input(self, key):
        if key == 'o':
            scene.entities.append(self)
            pt(scene.entities)
        if key == 'p':
            scene.entities.remove(self)
            pt(scene.entities)
        
    def update(self):
        self.perform_updates()
            
    def on_enable(self):
        if self.attacher_ent:
            self.attacher_ent.enabled = True
        
        self.perform_enables()
        
        scene.entities.append(self)
        
        self.fixed_combility_update_1 = Sequence(
            Func(self.fixed_update_1), Wait(1), loop=True, started=True
        )
        self.fixed_combility_updates_list.append(self.fixed_combility_update_1)
        self.animations.append(self.fixed_combility_update_1)
        
    def on_disable(self):
        # pt.c('-------------------on disable------------------')
        
        try:
            # pt('on_disable: ', self.name)

            if self.attacher_ent:
                self.attacher_ent.enabled = False
            
            self.perform_disables(debug=False)
            
            # if self.name == 'Test_camera_x_ray_grey' or 'Test_camera_x_ray_colors':
            #     pt('if: ', self.name)
            #     pt(111)
            #     self.disable_camera_x_ray()
            #     pt(222)
            if self.fixed_combility_updates_list: ## TODO, this could be for other ursina animations
                                ## I should probably create my own list of my own
                                ## animations that I create then disable them 
                                ## each in here in
                for fixed_update in self.fixed_combility_updates_list:
                    fixed_update.kill()
                    
            if self in scene.entities:
                scene.entities.remove(self)

        except Exception as e:
            import traceback
            traceback.print_exc()
            
    def fixed_update_1(self):
        ...
        
    ################################
    #       -Combility Functions   #
    ################################
    def to_snake_case(self, name):
        return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
    
    def parent_targets_to_acceptable_bot_targets(self, path_type='projectile', debug=False):
        ''' 
        - This is happening in 20-35us depending on the amount of target_types, 
        - This is far faster than even a single extra linecast of 200-300us. 
        - This requires only one linecast to the self.acceptable_bot_projectile_targets '''
        
        if debug:
            pt.c('Deugging parent_targets_to_acceptable_bot_targets')
            pt(path_type)
            target_types = getattr(self, f"{path_type}_target_types", [])
            acceptable_bot_target_types = getattr(self, f"acceptable_bot_{path_type}_targets", None)
            pt(self.name, path_type, target_types, acceptable_bot_target_types, acceptable_bot_target_types.children)
            
        for target in getattr(self, f"{path_type}_target_types", []):
            target.parent = getattr(self, f"acceptable_bot_{path_type}_targets", None)
        
    def get_real_eaat(self):
        # pt(self.eaat, self.eaat.parent, self.eaat.parent.parent, self.eaat.parent.parent.parent)
        
        eaat = self.eaat ## local var For faster access
        
        ## Organized by likelyhood of being shot.
        if isinstance(eaat, Shield):
            
            # pt(eaat.parent.parent.parent)
            return eaat.parent.parent.parent
        elif eaat.parent.name == 'environment':
            
            return eaat
        elif isinstance(eaat, (EnergyBeing, EG_Object)):
            
            return eaat
        elif isinstance(e, Character):
            
            return eaat.parent
        elif isinstance(e, Core):
            
            return eaat.parent.parent
        else:
            
            return eaat
    ###########
    # shooting/raycasts
    ###########
    def shoot(self, path_type='projectile'):
        
        if self in self.projectile_target_types:
            self.eaat = self
            self.perform_actions()
        elif self.slot_owner in self.projectile_target_types:
            self.eaat = self.slot_owner.shield ## NOTE: Shield sends all functions to the EnergyBeing anyways, 
                                                ## But now the owner will be treated exactly in the same logic 
                                                ## as any other entity type of the target_types. 
            self.perform_actions()
        else:
            self._choose_ray_type()

    def _choose_ray_type(self, path_type='projectile'):
        self.current_path_type = path_type
        self.parent_targets_to_acceptable_bot_targets(self.current_path_type)
        self.traverse_target = getattr(self, f"acceptable_bot_{self.current_path_type}_targets", None)

        path_ent = getattr(self, f"{self.current_path_type}_path_ent")
        path_vertices = getattr(self, f"{self.current_path_type}_path_vertices", [Vec3(0,0,0)])

        if len(path_vertices) == 2:
            self._straight_raycast(path_ent, path_vertices)
        else:
            self._segmented_linecast(path_ent, path_vertices)

    def _straight_raycast(self, path_ent, path_vertices):

        start_vertex = self.combility_barrel_end.world_position
        end_vertex = scene.getRelativePoint(path_ent, path_vertices[1])
        self._process_hit_info(start_vertex, end_vertex)

    def _segmented_linecast(self, path_ent, path_vertices):
        vertices = [self.world_position] + [scene.getRelativePoint(path_ent, vertex) for vertex in path_vertices]
        
        for i in range(len(vertices) - 1):
            hit_occurred = self._process_hit_info(vertices[i], vertices[i + 1], index=i)
            if hit_occurred:
                break
            
    def _process_hit_info(self, start_vertex, end_vertex, index=1):
        # pt(start_vertex, end_vertex, index)
        
        hit_info = linecast(
            start_vertex, end_vertex,
            debug=True,
            debug_time=1,
            traverse_target=self.traverse_target,
            ignore=self.ignore_list)
        
        self.start_pos = start_vertex
        self.end_pos = end_vertex
        self.hit_direction = (self.start_pos - self.end_pos).normalized()
        
        return self.actions_if_hit(hit_info, index)
    
    def actions_if_hit(self, hit_info, index):
        if hit_info.hit:
            # pt.c('hit')
            
            self.hit_info = hit_info
            self.index_of_last_point_before_hit = index
            if self.current_path_type == 'projectile':
                self.eaat = hit_info.entity
            elif self.current_path_type == 'assistant':
                self.hate = hit_info.entity
            self.perform_actions()
            
            return True  # Return True if a hit occurred
        
        return False  # Return False if no hit occurred
        
    def perform_debugger(self, actions, debug_message, mod_readable_list):
        print(f"--- {debug_message} ---")
        for i, action in enumerate(actions):
            print(f"{i} - {textwrap.dedent(inspect.getsource(action))}")
            print(f"func: {action.func}")
            print(f"prepared_values: {action.prepared_values}")
            action()
        print(f"--- {debug_message} Readable ---")
        pt(mod_readable_list)
        # for readable in enumerate(mod_readable_list):
        #     pt(readable)
        
    def perform_actions(self, debug_print=False):
        if not debug_print:
            for action_func in self.mod_actions:
                action_func()
        else:
            self.perform_debugger(self.mod_actions, "perform_actions", self.mod_actions_readable)


    def perform_updates(self, debug_print=False):
        if not debug_print:
            for update_func in self.mod_updates:
                update_func()
        else:
            self.perform_debugger(self.mod_updates, "perform_updates", self.mod_updates_readable)

    def perform_enables(self, debug_print=False):
        if not debug_print:
            for enable_func in self.mod_enables:
                enable_func()
        else:
            self.perform_debugger(self.mod_enables, "perform_enables", self.mod_enables_readable)

    def perform_disables(self, debug=False):
        if not debug:
            for disable_func in self.mod_disables:
                disable_func()
        else:
            self.perform_debugger(self.mod_disables, "perform_disables", self.mod_disables_readable)
        
    ############################
    
    
    
    def show_visuals(self):
        self.path_shape.enabled = True
        self.path_shape.color = self.path_color
        self.path_shape.scale_z = self.max_range / self.combility_barrel_end.world_scale_z
        self.path_shape.z = (self.path_shape.world_scale_z * 0.5) / self.combility_barrel_end.world_scale_z
        r, g, self.combility, a = self.path_color
        self.path_shape.animate_color(color.rgba(r,g,self.combility,0.), duration=.5)
        # pt(self.path_shape.world_scale, self.path_shape.scale, self.path_shape.world_z, self.path_shape.z)
    
    ################################
    #       -Combility setup        #
    ################################
    def attach_to_slot(self, slot):
        '''add_to_slot attach to slot add to slot
        '''
        ######
        # Slot
        ######
        current_scale = self.world_scale
        
        # pt(self.parent)
        self.parent = slot
        # pt(self.parent)
        # self.rotation=(-180,-180,-180),
        # pt(self.parent.rotation, self.parent.world_rotation,self.rotation, self.world_rotation)
        
        self.world_scale = current_scale
        
        self.position = (0, self.scale_y * 0.55, 0)
        
        ##########
        # slot owner (who does this slot belong to?)
        ##########
        self.slot_owner = slot.owner
        self.slot_owners_arm = slot.owners_arm
        self.slot = slot
    
    def add_target_types(self, general=None, specific=None, path_type='projectile'):
        ''' Types of targets:  (aka set_target_types)
        - Any number of enemies/teammates/shields/npcs etc. 
        - Or:
            - self (this combility)
            - owner of the slot this combility is connected to.
            
            '''
        enemies, teammates, npcs, local_objects, environment = self.level_target_types 
        if general is None:
            general = {enemies, npcs, local_objects, environment}

        if self in general and len(general) > 1:
            raise ValueError("'this combility (self)' cannot coexist with other target types")
        if self.slot_owner in general and len(general) > 1:
            raise ValueError("'slot_owner' cannot coexist with other target types")
        
        setattr(self, f'{path_type}_target_types', general)
        # self.projectile_target_types = general
        
        ######################
        # specific targets
        ######################
        if specific is None:
            self.specific_target = "energy_being"
            setattr(self, f'{path_type}_target_types', general)
        elif specific in ["eb_body", "eb_shield"]:
            self.specific_target = specific
        
        ########
        # if any combination of the following is true: 
        # - ["eb_body", "eb_shield"]
        # - ["eb_shield", "eb_body"]
        # - ["eb_body", "eb_shield", "energy_being"]
        # - ["energy_being", "eb_body", "eb_shield"]
        # - etc.
        
        elif set(specific).issubset({"eb_body", "eb_shield", "energy_being"}):
            self.specific_target = "energy_being"
        else:
            raise ValueError(f'Specific type must be "energy_being", "eb_body", or "eb_shield". Not "{specific}"')
        ########################
        
        if self not in general and self.slot_owner not in general:
            self.parent_targets_to_acceptable_bot_targets(path_type=path_type)
        
        # pt(self.name, self.projectile_target_types, self.specific_target)
    
    def add_max_range(self, max_range):
        self.max_range = max_range
    
    def add_damage(self, dmg_amt):
        self.dmg_amt = dmg_amt
    
    def add_speed(self, speed):
        self.speed = speed

    def _extend_path_vertices(self, incoming_visual_vertices, incoming_path_vertices, path_type):
        """
        This method extends the path vertices for a given path type.

        Parameters:
        vertices (list): A list of vertices to extend the path.
        path_type (str): The type of the path.
        
        
        """
        
        visual_vertices_attr = f"{path_type}_visual_vertices"
        path_vertices_attr = f"{path_type}_path_vertices"


        ## Get vertices lists of {path_type} name.
        ## If they don't exist, create them. 
        ## For example: self.{path_type}_visual_vertices = []
        visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
        path_vertices = getattr(self, path_vertices_attr, [Vec3(0,0,0)])
        # pt('_extend path 1', visual_vertices)
        
        
        ## extend
        visual_vertices.extend(incoming_visual_vertices)
        path_vertices.extend(incoming_path_vertices)
        # pt('_extend path 2', visual_vertices)
        
        # Set the visual and path vertices attributes of the object to the updated lists
        setattr(self, visual_vertices_attr, visual_vertices)
        setattr(self, path_vertices_attr, path_vertices)
        
        return visual_vertices, path_vertices
    
    def add_points_to_path(self, *vertices, path_type='projectile'):
        # pt('add_points', vertices)
        
        self._extend_path_vertices(vertices, vertices, path_type=path_type)
    
    def add_curve_to_path(self, *args, path_type='projectile', **kwargs):
        # pt('add curve', curve)
        
        visual_curve_vertices, path_curve_vertices,  = self._create_curve(*args, **kwargs)
        
        self._extend_path_vertices(visual_curve_vertices, path_curve_vertices, path_type=path_type)
    
    def _create_curve(self, 
            scale=(1,1,1), 
            circle_degrees=360, 
            visual_resolution=22, 
            path_resolution=6,
            existing_visual_vertices=None, 
            existing_path_vertices=None,
    ):
        # pt(self.name, visual_resolution, path_resolution, existing_visual_vertices, existing_path_vertices)
        
        
        ## Normalize scale
        max_scale_value = max(scale)
        normalized_scale = Vec3(*tuple(s / max_scale_value for s in scale))

        ## Setup a circle with specified resolution
        circle_resolution = 56
        circle_points = [Vec3(0, math.sin(2 * math.pi * i / circle_resolution), -math.cos(2 * math.pi * i / circle_resolution)) for i in range(circle_resolution)]
        points_to_include = int(circle_resolution * (circle_degrees / 360)) + 1

        ## Create vertices for the mesh based on the included points
        visual_vertices = [v - Vec3(0, 0, -1) for v in circle_points[:points_to_include]]
        pt(visual_vertices)
        pt(visual_resolution)
        # pt.ex()
        ## Close the circle when circle_degrees is 360
        if circle_degrees == 360:
            visual_vertices.append(visual_vertices[0])

        ## Reduce the resolution of visual_vertices
        step_size = len(visual_vertices) / visual_resolution
        reduced_visual_vertices = [visual_vertices[int(i * step_size)] for i in range(visual_resolution - 1)]
        reduced_visual_vertices.append(visual_vertices[-1])
        visual_vertices = reduced_visual_vertices
        
        ## Create reduced vertices for raycasting based on reduced_visual_vertices
        path_vertices = visual_vertices[::len(visual_vertices) // path_resolution]

        ## If an existing user-created path exists, offset each new vertex
        ### by where the last vertex of the existing path is. So it starts correctly
        if existing_visual_vertices is not None and len(existing_visual_vertices) > 1:
            last_vertex = existing_visual_vertices[-1]
            visual_vertices = [v + last_vertex for v in visual_vertices]
                    
        if existing_path_vertices is not None and len(existing_path_vertices) > 1:
            last_vertex = existing_path_vertices[-1]
            path_vertices = [v + last_vertex for v in path_vertices]
            
        ## Scaled
        visual_vertices = [v * normalized_scale for v in visual_vertices]
        path_vertices = [v * normalized_scale for v in path_vertices]
    
        return visual_vertices, path_vertices ## Only for functions that need a curve but that don't get added to the path vertices
    
    def add_path_rotation(self, rotation=(0,0,0)):
        self.path_rotation = rotation
    
    # def orient_to_attacher(self):
    #     '''

    #     - only responsible for orienting towards an attacher
    #     - rope/solids might care if attacher actually connects or not, 
    #         but this function does not. 
    #     - DO NOT shorten paths for attacher distance. We may have
    #         penetration, etc. This only is for orientation. 
    #     - The self.path_ent is not the models interacting/stopping 
    #         via hit detection. 
        
    #     '''
        
    #     if self.auto_swivel:
    #         self.look_at_in_local_space(self, self.attacher_ent)
    #     else:
    #         ## TODO BUGFIX: I should be able to pass only the self.combility_barrel_end instead of both
    #         ##  the self.path_ent and self.raycast_path_ent, to achieve the same/cleaner version
    #         ##  of the same thing. But when I use the bullet_end, the path shrinks in size. 
    #         # self.look_at_in_local_space(self.combility_barrel_end, self.attacher_ent)
            
    #         self.look_at_in_local_space(self.projectile_visual_ent, self.attacher_ent)
    #         self.look_at_in_local_space(self.projectile_path_ent, self.attacher_ent)        
    #         direction_self = self.world_position - self.parent.world_position
    #         direction_attacher = self.attacher_ent.world_position - self.parent.world_position

    #         # Calculate the angle between the direction vectors
    #         angle = self.angle_between(direction_self, direction_attacher)

    #         # If the angle is greater than 90 degrees, disable the attacher_ent
    #         if angle > 90:
    #             self.attacher_ent.enabled = False
    #             return

    def angle_to_start_stop_attacher(self, stop_angle=89):
        # Get the direction vectors
        direction_self = -self.forward ## TODO - Investigate why we have to use a negative forward?
                                            ## Maybe arm or one of its parents is turned around? 
        direction_attacher = self.attacher_ent.world_position - self.world_position

        # Calculate the angle between the direction vectors
        angle = self.angle_between(direction_self, direction_attacher)
        # pt(angle);pt.ex()
        # If the angle is greater than 90 degrees, disable the attacher_ent
        if angle > stop_angle:
            # rotation = self.calculate_rotation_from_direction(self.forward)
            self.projectile_visual_ent.world_rotation = self.combility_barrel_end.world_rotation
            self.projectile_path_ent.world_rotation = self.combility_barrel_end.world_rotation
            
            self.attacher_ent.enabled = False
            
            return
            

        # Only enable the attacher_ent if it's currently disabled
        if not self.attacher_ent.enabled:
            self.attacher_ent.enabled = True
            
    def orient_to_attacher(self):
        '''
        - rope/solids might care if attacher actually connects or not, 
            but this function does not. It only looks to orient. 
        - DO NOT shorten paths for attacher distance. We may have
            penetration, etc. This only is for orientation. 

        '''
        
        if self.auto_swivel:
            self.look_at_in_local_space(self, self.attacher_ent)
        else:
            self.look_at_in_local_space(self.projectile_visual_ent, self.attacher_ent)
            self.look_at_in_local_space(self.projectile_path_ent, self.attacher_ent)
            
            self.angle_to_start_stop_attacher(89)
            ## TODO BUGFIX: I should be able to pass only the self.combility_barrel_end instead of both
            ##  the self.path_ent and self.raycast_path_ent, to achieve the same/cleaner version
            ##  of the same thing. But when I use the bullet_end, the path shrinks in size. 
            # self.look_at_in_local_space(self.combility_barrel_end, self.attacher_ent)
            
            
            
    def calculate_rotation_from_direction(self, direction):
        # Convert the direction vector to a rotation
        rotation_y = -math.degrees(math.atan2(direction.x, direction.z))
        
        # Clamp direction.y to the range -1 to 1 to avoid math domain errors
        clamped_y = max(min(direction.y, 1), -1)
        rotation_x = -math.degrees(math.asin(clamped_y))

        # Ensure rotation_y is in the range [0, 360)
        if rotation_y < 0:
            rotation_y += 360

        return (rotation_x, rotation_y, 0)

    # def compile_path(self, range=1, rotation=(0,0,0), path_type='projectile'):
    #     self.path_range = range
    #     visual_vertices_attr = f"{path_type}_visual_vertices"
    #     path_vertices_attr = f"{path_type}_path_vertices"
        
    #     visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
    #     path_vertices = getattr(self, path_vertices_attr, [Vec3(0,0,0)])
        
    #     if len(visual_vertices) == 1:
    #         visual_vertices.append(Vec3(visual_vertices[0]) + Vec3(0, 0, 1))
    #         path_vertices.append(Vec3(path_vertices[0]) + Vec3(0, 0, 1))
    #     # pt('compile', visual_vertices)
        
            
    #     setattr(self, visual_vertices_attr, visual_vertices)
    #     setattr(self, path_vertices_attr, path_vertices)
        
    #     z_dist = self.last_vert_path_z_distance(visual_vertices)
    #     scale = range / z_dist
        
    #     visual_ent = Entity(name='visual_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=visual_vertices, mode='line', 
    #             thickness=33, 
    #             render_points_in_3d=False,
    #             ),
    #         color=color.rgba(1,1,0,.6))
        
    #     path_ent = Entity(name='path_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=path_vertices, mode='line', 
    #             thickness=4,
    #             render_points_in_3d=False,
    #             ),
    #         color=color.rgba(1, .647, 0, .85))
        
    #     for entity in [visual_ent, path_ent]:
    #         entity.rotation = rotation
    #         entity.scale = scale
            
    #     setattr(self, f"{path_type}_visual_ent", visual_ent)
    #     setattr(self, f"{path_type}_path_ent", path_ent)
        
        
    def compile_path(self, range=1, rotation=(0,0,0), path_type='projectile'):
        self.path_range = range
        visual_vertices_attr = f"{path_type}_visual_vertices"
        path_vertices_attr = f"{path_type}_path_vertices"
        
        visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
        path_vertices = getattr(self, path_vertices_attr, [Vec3(0,0,0)])
        
        if len(visual_vertices) == 1:
            visual_vertices.append(Vec3(visual_vertices[0]) + Vec3(0, 0, 1))
            path_vertices.append(Vec3(path_vertices[0]) + Vec3(0, 0, 1))
        # pt('compile', visual_vertices)
        
            
        setattr(self, visual_vertices_attr, visual_vertices)
        setattr(self, path_vertices_attr, path_vertices)
        
        z_dist = self.last_vert_path_z_distance(visual_vertices)
        z_scale = range / z_dist
        
        # visual_vertices = [v * z_scale for v in visual_vertices]
        # path_vertices = [v * z_scale for v in path_vertices]
        # pt(visual_vertices)
        
        
        
        
        num_sides = 4
        rotation_mesh = 45
        diameter=.5 / z_scale  ## Must divide the radius I want by the z_scale or else
                                ## it'll get crazily stretched out. 
        
        new_vertices, triangles, new_uvs, new_normals = mesh_creator.create_mesh_data(
            visual_vertices, 
            num_sides=num_sides, 
            rotation=rotation_mesh,
            # diameter=0.025,
            diameter=diameter,
            interpolate=False,
            )
        visual_mesh = Mesh(vertices=new_vertices, triangles=triangles, uvs=new_uvs, normals=new_normals, mode='triangle')
        visual_ent = Entity(name='visual_ent',
            parent=self.combility_barrel_end, 
            model=visual_mesh, 
            color=Color(1,1,0,0.6))
        
        new_vertices, triangles, new_uvs, new_normals = mesh_creator.create_mesh_data(
            path_vertices,
            num_sides=num_sides,
            rotation=rotation_mesh,
            # diameter=0.025,
            diameter=diameter,
            interpolate=False,
            )
        path_mesh = Mesh(vertices=new_vertices, triangles=triangles, uvs=new_uvs, normals=new_normals, mode='triangle')
        path_ent = Entity(name='visual_ent',
            parent=self.combility_barrel_end, 
            model=path_mesh, 
            color=Color(1,0.647,0,0.6))
        
        
        
        
        # visual_ent = Entity(name='visual_ent',
        #     parent=self.combility_barrel_end,
        #     model=Mesh(vertices=visual_vertices, mode='line', 
        #         thickness=33, 
        #         render_points_in_3d=False,
        #         ),
        #     color=color.rgba(1,1,0,.6))
        
        # path_ent = Entity(name='path_ent',
        #     parent=self.combility_barrel_end,
        #     model=Mesh(vertices=path_vertices, mode='line',
        #         thickness=4,
        #         render_points_in_3d=False
        #     ),
        #     color=color.rgba(1, .647, 0, .85))
        
        for entity in [visual_ent, path_ent]:
            entity.rotation = rotation
            entity.scale = z_scale
        # pt(path_ent.model.vertices)
        # pt.ex()
            
        setattr(self, f"{path_type}_visual_ent", visual_ent)
        setattr(self, f"{path_type}_path_ent", path_ent)
        
    
    
    
    
    # def create_box(self, center, size=1):
    #     d = size / 2
    #     return [
    #         center + Vec3(-d, -d, -d),
    #         center + Vec3(d, -d, -d),
    #         center + Vec3(d, d, -d),
    #         center + Vec3(-d, d, -d),
    #         center + Vec3(-d, -d, d),
    #         center + Vec3(d, -d, d),
    #         center + Vec3(d, d, d),
    #         center + Vec3(-d, d, d)
    #     ]

    # def compile_path(self, range=1, rotation=(0,0,0), path_type='projectile'):
    #     self.path_range = range
    #     visual_vertices_attr = f"{path_type}_visual_vertices"
    #     path_vertices_attr = f"{path_type}_path_vertices"
        
    #     visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
    #     path_vertices = getattr(self, path_vertices_attr, [Vec3(0,0,0)])
        
    #     if len(visual_vertices) == 1:
    #         visual_vertices.append(Vec3(visual_vertices[0]) + Vec3(0, 0, 1))
    #         path_vertices.append(Vec3(path_vertices[0]) + Vec3(0, 0, 1))
        
    #     setattr(self, visual_vertices_attr, visual_vertices)
    #     setattr(self, path_vertices_attr, path_vertices)
        
    #     z_dist = self.last_vert_path_z_distance(visual_vertices)
    #     scale = range / z_dist

    #     box_size = .01  # Change this to the size you want

    #     # Create a box around each point in visual_vertices
    #     visual_vertices_boxes = [self.create_box(vertex, box_size) for vertex in visual_vertices]

    #     # Create a box around each point in path_vertices
    #     path_vertices_boxes = [self.create_box(vertex, box_size) for vertex in path_vertices]

    #     # Flatten the list of boxes into a single list of vertices
    #     visual_vertices = [vertex for box in visual_vertices_boxes for vertex in box]
    #     path_vertices = [vertex for box in path_vertices_boxes for vertex in box]

    #     visual_ent = Entity(name='visual_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=visual_vertices, mode='point', 
    #             thickness=33, 
    #             render_points_in_3d=False,
    #             ),
    #         color=color.rgba(1,1,0,.6))
        
    #     path_ent = Entity(name='path_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=path_vertices, mode='line', 
    #             thickness=4,
    #             render_points_in_3d=False,
    #             ),
    #         color=color.rgba(1, .647, 0, .85))
        
    #     for entity in [visual_ent, path_ent]:
    #         entity.rotation = rotation
    #         entity.scale = scale
            
    #     setattr(self, f"{path_type}_visual_ent", visual_ent)
    #     setattr(self, f"{path_type}_path_ent", path_ent)




    # def create_box(self, center, size=1, front_face=False, back_face=False):
    #     d = size / 2
    #     vertices = [
    #         center + Vec3(-d, -d, -d),
    #         center + Vec3(d, -d, -d),
    #         center + Vec3(d, d, -d),
    #         center + Vec3(-d, d, -d),
    #         center + Vec3(-d, -d, d),
    #         center + Vec3(d, -d, d),
    #         center + Vec3(d, d, d),
    #         center + Vec3(-d, d, d)
    #     ]
    #     faces = [
    #         [0, 1, 2, 3],  # bottom face
    #         [4, 5, 6, 7],  # top face
    #         [0, 1, 5, 4],  # front face
    #         [2, 3, 7, 6],  # back face
    #         [0, 3, 7, 4],  # left face
    #         [1, 2, 6, 5]   # right face
    #     ]
    #     if not front_face:
    #         faces.remove([0, 1, 5, 4])
    #     if not back_face:
    #         faces.remove([2, 3, 7, 6])
    #     # Convert faces to triangles
    #     triangles = []
    #     for face in faces:
    #         triangles.append([face[0], face[1], face[3]])
    #         triangles.append([face[1], face[2], face[3]])
    #     return vertices, triangles

    # def compile_path(self, range=1, rotation=(0,0,0), path_type='projectile'):
    #     self.path_range = range
    #     visual_vertices_attr = f"{path_type}_visual_vertices"
    #     path_vertices_attr = f"{path_type}_path_vertices"
        
    #     visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
    #     path_vertices = getattr(self, path_vertices_attr, [Vec3(0,0,0)])
        
    #     if len(visual_vertices) == 1:
    #         visual_vertices.append(Vec3(visual_vertices[0]) + Vec3(0, 0, 1))
    #         path_vertices.append(Vec3(path_vertices[0]) + Vec3(0, 0, 1))
        
    #     setattr(self, visual_vertices_attr, visual_vertices)
    #     setattr(self, path_vertices_attr, path_vertices)
        
    #     z_dist = self.last_vert_path_z_distance(visual_vertices)
    #     scale = range / z_dist

    #     box_size = .01  # Change this to the size you want

    #     # Scale the vertices in the Z direction
    #     scaled_visual_vertices = [Vec3(vertex.x, vertex.y, vertex.z * scale) for vertex in visual_vertices]
    #     scaled_path_vertices = [Vec3(vertex.x, vertex.y, vertex.z * scale) for vertex in path_vertices]

    #     # Create a box around each point in scaled_visual_vertices
    #     visual_vertices_boxes = [self.create_box(vertex, box_size, front_face=i==0, back_face=i==len(scaled_visual_vertices)-1) for i, vertex in enumerate(scaled_visual_vertices)]

    #     # Create a box around each point in scaled_path_vertices
    #     path_vertices_boxes = [self.create_box(vertex, box_size, front_face=i==0, back_face=i==len(scaled_path_vertices)-1) for i, vertex in enumerate(scaled_path_vertices)]
        
        
    #     # Flatten the list of boxes into a single list of vertices and triangles
    #     visual_vertices = [vertex for box in visual_vertices_boxes for vertex in box[0]]
    #     visual_triangles = [triangle for box in visual_vertices_boxes for triangle in box[1]]
    #     path_vertices = [vertex for box in path_vertices_boxes for vertex in box[0]]
    #     path_triangles = [triangle for box in path_vertices_boxes for triangle in box[1]]

    #     visual_ent = Entity(name='visual_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=visual_vertices, triangles=visual_triangles, mode='line'),
    #         color=color.rgba(1,1,0,.6))
        
    #     path_ent = Entity(name='path_ent',
    #         parent=self.combility_barrel_end,
    #         model=Mesh(vertices=path_vertices, triangles=path_triangles, mode='line'),
    #         color=color.rgba(1, .647, 0, .85))
        
    #     for entity in [visual_ent, path_ent]:
    #         entity.rotation = rotation
    #         entity.scale = scale
            
    #     setattr(self, f"{path_type}_visual_ent", visual_ent)
    #     setattr(self, f"{path_type}_path_ent", path_ent)
        
        
    #     if len(visual_vertices) > 0:
    #         pt(visual_vertices)
    #         pt(visual_triangles)
    #         pt(visual_ent.model.vertices)
    #         pt(visual_ent.model.triangles)
        
        
        
        
    def last_vert_path_z_distance(self, vertices):
        first_vertex = vertices[0]
        farthest_vertex = max(vertices, key=lambda vertex: vertex[2])
        return abs(farthest_vertex[2] - first_vertex[2])
    
    def get_length_of_path(self, vertices, scale=1):
        '''
        - Used for calculating the overall distance that this path covers, and thus
        its energy usage
        - the same Max range on a curve/segmented line will be more energy than a straight line. 
        
        - need to add the calculation with the max range, unless that is already
        accounted for here. Actually it is not counted. 
            - It might be if I used self.path_ent.model.vertices, if not will have to calculate
            via the scale etc. 
            
        '''
        
        
        total_length = 0
        num_vertices = len(vertices)
        for i in range(num_vertices - 1):
            total_length += distance(vertices[i], vertices[i+1])
            # pt(vertices[i], vertices[i+1], total_length)
            
        return total_length * scale, num_vertices

    def look_at_in_local_space(self, entity, target):
        target_position = target.world_position if isinstance(target, Entity) else Vec3(*target)
        entity.lookAt(scene, target_position)
        
    def prepare_laser_sparks(self):
        texture = 'sparks/sparks3_rotated-0.png'
        
        
        self.vertices_for_mesh_points += [v + Vec3(-.5, .5, .5) for v in self.vertices_for_mesh_points]
        self.vertices_for_mesh_points += [v + Vec3(-.5,-.5, -.5) for v in self.vertices_for_mesh_points]
        
        self.laser_sparks = Entity(name='laser_sparks',
            parent=self.combility_barrel_end,
            model=Mesh(
                # vertices=[],
                vertices=self.vertices_for_mesh_points,
                mode='point', 
                thickness=.5
            ), 
            texture=texture, 
            # render_points_in_3d=True
        )
        
        
        # self.laser_sparks.model.vertices = self.vertices_for_mesh_points
        # self.laser_sparks.model.generate()
        
        self.laser_sparks.rotation = self.curve_path_ent.rotation
        self.laser_sparks.scale = self.curve_path_ent.scale 

        
    def add_path_shape(self, shape_enum):
        if shape_enum in EnergyShapeTypeEnum:
            self.path_shape.model = self.to_snake_case(shape_enum.value)
        else:
            raise ValueError("Invalid shape type")
    
    def add_form(self, form):
        self.combility_model = Form.add_form(form)
        if isinstance(form, str):
            form = form.strip().upper().replace(' ', '_')
            for form_class in vars(Form).values():
                if isinstance(form_class, type):
                    form_type = getattr(form_class, form, None)
                    if form_type is not None:
                        self.form = form_type
                        break
            else:
                raise ValueError(f"Invalid form type: {form}")
        elif isinstance(form, Form):
            self.form = form
        else:
            raise TypeError("form must be a string or an instance of Form")
    
    # def add_form(self, form):
    #     form = form.strip().upper().replace(' ', '_')
    #     for form_class in vars(Form).values():
    #         if isinstance(form_class, type):
    #             form_type = getattr(form_class, form, None)
    #             if form_type is not None:
    #                 self.form = form_type
    #                 break
    #     else:
    #         raise ValueError(f"Invalid form type: {form}")
    
    ################################
    #        -Mod Actions          #
    ################################
# 


    def prepare_experimental_animation_points(self, 
        range=20, 
        speed=105, 
        scale=(1,.4,1), 
        circle_degrees=180, 
        rotation=(0,0,0),
        path_type='animation',
        ):
        '''
        - This is a blank slate for acquiring points, and then sending them 
        to be animated by the target type of the slot_owner (for now). 
        - Originally designed for the dash with the slot_owner. In this
        simplified state, it will be much easier to build other classes from
        this one. 
        '''
        
        self.add_curve_to_path(
            scale=scale, 
            circle_degrees=circle_degrees, 
            path_type=path_type
            )
        
        self.compile_path(
            range, 
            rotation,
            path_type=path_type,
            )
        
        dist_of_visual_vertices, num_vertices_path = self.get_length_of_path(
            self.animation_path_ent.model.vertices, scale=range)

        duration = dist_of_visual_vertices / speed 

        curve_points = [Vec3(self.world_position)] + [
            Vec3(scene.getRelativePoint(self.animation_visual_ent, vertex)) 
            for vertex in self.animation_visual_vertices]

        direction_vec = Vec3(0,0,1)

        return duration, curve_points, direction_vec

    def use_experimental_animation_points(self, duration, curve_points, direction_vec):
        self.eaat._experimental_recieve_animation_points(direction_vec, duration, curve_points)

    def prepare_example(self, arg_1, arg_2, kwarg_1=1.0, kwarg_2='some text'):
        kwarg_that_was_prepped = kwarg_1 * 0.5
        self.example_exists = True
        
        return kwarg_that_was_prepped ## (optional return)
    
    def use_example(self, arg_1, arg_2, kwarg_1=1.0, kwarg_2='some text'):
        kwarg_2 = kwarg_1 
        self.add_update_function_if_exists("example", arg_1, arg_2, kwarg_1=1.0, kwarg_2='some text')

    def update_example(self, energy_amount):
        print('update example')


    def add_function_if_exists(self, action_name, prepared_values, func_prefix, mod_list, mod_readable_list):
        func_name = f"{func_prefix}_{action_name}"
        if hasattr(self, func_name):
            pt()
            func = getattr(self, func_name)

            # Get the parameters of the function
            params = inspect.signature(func).parameters

            # If prepared_values is not a tuple and it's a single value, make it a tuple
            if not isinstance(prepared_values, tuple):
                prepared_values = (prepared_values,)

            # Filter the prepared_values to only include the ones that the function needs
            prepared_values = tuple(value for name, value in zip(params, prepared_values) if name in params)

            def action_func():
                return func(*prepared_values)

            # Store func and prepared_values as attributes of action_func
            action_func.func = func
            action_func.prepared_values = prepared_values

            mod_list.append(action_func)
            func_add = func_name + str(prepared_values)
            mod_readable_list.append(func_add)
            return True
        else:
            pt()
            for name, obj in inspect.getmembers(mod_senders_main):
                if inspect.isclass(obj):
                    if hasattr(obj, func_name):
                        func = getattr(obj, func_name)
                        # Get the parameters of the function
                        params = inspect.signature(func).parameters

                        # If prepared_values is not a tuple and it's a single value, make it a tuple
                        if not isinstance(prepared_values, tuple):
                            prepared_values = (prepared_values,)

                        # Filter the prepared_values to only include the ones that the function needs
                        prepared_values = tuple(value for name, value in zip(params, prepared_values) if name in params)

                        def action_func():
                            return func(*prepared_values)

                        # Store func and prepared_values as attributes of action_func
                        action_func.func = func
                        action_func.prepared_values = prepared_values

                        mod_list.append(action_func)
                        func_add = func_name + str(prepared_values)
                        mod_readable_list.append(func_add)
                        return True
        return False

    # def add_function_if_exists(self, action_name, prepared_values, func_prefix, mod_list, mod_readable_list):
    #     func_name = f"{func_prefix}_{action_name}"
        
    #     # First, check the current class
    #     if hasattr(self, func_name) and inspect.ismethod(getattr(self, func_name)):
    #         func = getattr(self, func_name)
    #         # rest of your code
    #     else:
    #         # If not found in the current class, check the classes in mod_senders_main
    #         for name, obj in inspect.getmembers(mod_senders_main):
    #             if inspect.isclass(obj) and hasattr(obj, func_name) and inspect.ismethod(getattr(obj, func_name)):
    #                 func = getattr(obj, func_name)
    #                 # rest of your code

    #                 # Get the parameters of the function
    #                 params = inspect.signature(func).parameters

    #                 # If prepared_values is not a tuple and it's a single value, make it a tuple
    #                 if not isinstance(prepared_values, tuple):
    #                     prepared_values = (prepared_values,)

    #                 # Filter the prepared_values to only include the ones that the function needs
    #                 prepared_values = tuple(value for name, value in zip(params, prepared_values) if name in params)

    #                 def action_func():
    #                     return func(*prepared_values)

    #                 # Store func and prepared_values as attributes of action_func
    #                 action_func.func = func
    #                 action_func.prepared_values = prepared_values

    #                 mod_list.append(action_func)
    #                 func_add = func_name + str(prepared_values)
    #                 mod_readable_list.append(func_add)
    #                 return True
    #             return False
    
                    
    # def add_function_if_exists(self, action_name, prepared_values, func_prefix, mod_list, mod_readable_list):
    #     func_name = f"{func_prefix}_{action_name}"
    #     for name, obj in inspect.getmembers(mod_senders_main):
    #         if inspect.isclass(obj):
    #             if hasattr(obj, func_name):
    #                 func = getattr(obj, func_name)
    #                 # Get the parameters of the function
    #                 params = inspect.signature(func).parameters

    #                 # If prepared_values is not a tuple and it's a single value, make it a tuple
    #                 if not isinstance(prepared_values, tuple):
    #                     prepared_values = (prepared_values,)

    #                 # Filter the prepared_values to only include the ones that the function needs
    #                 prepared_values = tuple(value for name, value in zip(params, prepared_values) if name in params)

    #                 def action_func():
    #                     return func(*prepared_values)

    #                 # Store func and prepared_values as attributes of action_func
    #                 action_func.func = func
    #                 action_func.prepared_values = prepared_values

    #                 mod_list.append(action_func)
    #                 func_add = func_name + str(prepared_values)
    #                 mod_readable_list.append(func_add)
    #                 return True
    #             return False

    # def add_function_if_exists(self, action_name, prepared_values, func_prefix, mod_list, mod_readable_list):
    #     func_name = f"{func_prefix}_{action_name}"
    #     if hasattr(self, func_name):
    #         func = getattr(self, func_name)

    #         # Get the parameters of the function
    #         params = inspect.signature(func).parameters

    #         # If prepared_values is not a tuple and it's a single value, make it a tuple
    #         if not isinstance(prepared_values, tuple):
    #             prepared_values = (prepared_values,)

    #         # Filter the prepared_values to only include the ones that the function needs
    #         prepared_values = tuple(value for name, value in zip(params, prepared_values) if name in params)

    #         def action_func():
    #             return func(*prepared_values)

    #         # Store func and prepared_values as attributes of action_func
    #         action_func.func = func
    #         action_func.prepared_values = prepared_values

    #         mod_list.append(action_func)
    #         func_add = func_name + str(prepared_values)
    #         mod_readable_list.append(func_add)
    #         return True
    #     return False

    def add_use_function_if_exists(self, action_name, prepared_values):
        return self.add_function_if_exists(action_name, prepared_values, "use", self.mod_actions, self.mod_actions_readable)
    
    def add_update_function_if_exists(self, action_name, prepared_values):
        return self.add_function_if_exists(action_name, prepared_values, "update", self.mod_updates, self.mod_updates_readable)
    
    def add_enable_function_if_exists(self, action_name, prepared_values):
        return self.add_function_if_exists(action_name, prepared_values, "enable", self.mod_enables, self.mod_enables_readable)
    
    def add_disable_function_if_exists(self, action_name, prepared_values):
        # pt(self.name, action_name)
        return self.add_function_if_exists(action_name, prepared_values, "disable", self.mod_disables, self.mod_disables_readable)


    def prepare_func_values(self, action_name, *args, **kwargs):
        prepare_func_name = f"prepare_{action_name}"
        prepare_func = None

        # First, check the current class
        if hasattr(self, prepare_func_name):
            prepare_func = getattr(self, prepare_func_name)
        else:
            # If not found in the current class, check the classes in mod_senders_main
            for name, obj in inspect.getmembers(mod_senders_main):
                if inspect.isclass(obj) and hasattr(obj, prepare_func_name):
                    prepare_func = getattr(obj, prepare_func_name)
                    break

        if prepare_func is not None:
            # Check if prepare_func is a bound method
            if getattr(prepare_func, '__self__', None) is not None:
                result = prepare_func(*args, **kwargs)
            else:
                result = prepare_func(self, *args, **kwargs)
            if result is not None:
                if isinstance(result, tuple):
                    return result
                else:
                    return (result,)
        return args + tuple(kwargs.values())

    # def prepare_func_values(self, action_name, *args, **kwargs):
    #     prepare_func_name = f"prepare_{action_name}"
    #     if hasattr(self, prepare_func_name):
    #         prepare_func = getattr(self, prepare_func_name)
    #         result = prepare_func(*args, **kwargs)
    #         if result is not None:
    #             if isinstance(result, tuple):
    #                 return result
    #             else:
    #                 return (result,)
    #     return args + tuple(kwargs.values())
    
    def add_mod(self, action_name, *args, debug=False, **kwargs):
        prepared_values = self.prepare_func_values(action_name, *args, **kwargs)
        
        if not self.add_use_function_if_exists(action_name, prepared_values):
            if not self.add_update_function_if_exists(action_name, prepared_values):
                raise ValueError(f'There is no use_function or update_function for {action_name}')
        
        self.add_enable_function_if_exists(action_name, prepared_values)
        self.add_disable_function_if_exists(action_name, prepared_values)
        
        if debug:
            print(f"{action_name}_values: {prepared_values}")
        
    def _is_descendant(self, entity, parent):
        if entity.parent is None:
            return False
        elif entity.parent == parent:
            return True
        else:
            return self._is_descendant(entity.parent, parent)
        
    def _get_parents(self, entity):
        parents = []
        current_parent = entity.parent
        while current_parent is not None:
            parents.append(current_parent)
            current_parent = current_parent.parent
        return parents

    # def _set_camera_parent_properties(self, world_rotation=None):
    #     cam_ent = self.slot_owner.cam_mount_main_ent
    #     cam_ent.parent = scene
    #     cam_ent.world_position = self.hit_info.world_point
    #     cam_ent.look_at(self)
        
    
    def _set_camera_parent_properties(self, world_rotation=None):
        self.cam_ent = self.slot_owner.cam_mount_main_ent
        self.cam_ent_orig_pos = self.cam_ent.position 
        self.cam_ent_original_rot = self.cam_ent.rotation
        # cam_ent.parent = scene
        # cam_ent.world_position = self.hit_info.world_point
        # cam_ent.look_at(self)
            
        #########
        ## Slot Owner
        #########
        if self.slot_owner in self.projectile_target_types:
            self.cam_ent.parent = self.slot_owner
            self.cam_ent.position = self.slot_owner.cam_mount_main_default_pos
            
        #########
        ## Everything Else
        #########
        else:
    
            ## POSSIBLE BUG: By checking if self.hit_info and never resetting it to None (as of right now, hit_info never resets to None, then we might have a hit_info
            ## even though we are about to apply this weapon to a self.this_combility or something.
            ## Maybe... We can actually set the hit_info information to the slot_owner or this_combility? I could manually do it, but it wouldn't have a normal, right? 
            ## I'm not really sure at this point. But some ideas to keep in mind. )
            if self.hit_info:
                ## NOTE: We look at the self (this combility), so we always look the direction that the camera was shot in,
                ## Whether the camera was attached/separated from the slot_owner at the time. 
                self.cam_ent.parent = scene
                self.cam_ent.world_position = self.hit_info.world_point
                self.cam_ent.look_at(self)
            
            #########
            ## Self (This Combility):
            else:
                self.cam_ent.parent = self.eaat
                self.cam_ent.world_position = self.eaat.world_position
                self.cam_ent.rotation = self.eaat.rotation
                eaat_scale = self.eaat.scale
                counter_scale = [1/s for s in eaat_scale]
                
                self.cam_ent.scale = counter_scale
                self.cam_ent.world_scale = 1
                
        if world_rotation is not None:
            self.cam_ent.world_rotation = world_rotation
    
    def _unset_camera_parent_properties(self):
        self.cam_ent = self.slot_owner.cam_mount_main_ent

        self.cam_ent.parent = self.slot_owner
        
        self.cam_ent.position = self.slot_owner.cam_mount_main_default_pos

        self.cam_ent.rotation = (0,0,0)
        
        # pt(self.cam_ent.scale, self.cam_ent.world_scale)
        
        self.cam_ent.world_scale = 1
        
        window.render_mode = 'default'
        
    def _set_camera_render_properties(self, render_mode='default'):
        window.render_mode = render_mode        
        
    def _set_camera_properties(self, render_mode, world_rotation=None):
        self._set_camera_parent_properties(world_rotation)
        self._set_camera_render_properties(render_mode)
    
    def _unset_camera_properties(self):
        self._unset_camera_parent_properties()
        
        window.render_mode = 'default'
        camera.fov = self.default_camera_fov
        
    def _set_entity_colors(self, entity_color_category):
        ent_color_attr = f"entity_{entity_color_category}_colors"
        entity_colors = getattr(self, ent_color_attr)
        for entity, color in entity_colors.items():
            entity.color = color
        
    def _generate_entity_colors(self, entity_color_category='original', default_color=None, **kwargs):
        entity_colors_attr = f"entity_{entity_color_category}_colors"
        setattr(self, entity_colors_attr, {})

        # First, set the colors of the entities specified in kwargs
        for entity_set_name, color in kwargs.items():
            entity_set = EG_Globals.entity_sets.get(entity_set_name)
            if entity_set is not None:
                for entity in entity_set:
                    if hasattr(entity, 'color'):
                        getattr(self, entity_colors_attr)[entity] = color

        # Then, set the colors of the remaining entities to the default color
        for entity_set_name, entity_set in EG_Globals.entity_sets.items():
            for entity in entity_set:
                if entity not in getattr(self, entity_colors_attr) and hasattr(entity, 'color'):
                    if entity_color_category == 'original':
                        getattr(self, entity_colors_attr)[entity] = entity.color
                    elif default_color is not None:
                        getattr(self, entity_colors_attr)[entity] = default_color
                    else:
                        getattr(self, entity_colors_attr)[entity] = entity.color
    
    def prepare_camera_night_vision(self, 
        color=Color(0, .25, 0, 1), ## Low Light Green
        energy_amount=121,
        **kwargs
    ):
        
        self._prepare_camera_colors(
            entity_color_category='camera',
            default_color=color,
            shields=Color(0,0,0,0),
            shield_parts=Color(0,0,0,0),
            shield_part2s=Color(0,0,0,0),
            sky=Color(0, 0, 0, 0)
        )
    
    def use_camera_night_vision(self):
        self._set_camera_properties('default')
        self._set_entity_colors(entity_color_category='camera')

    def disable_camera_night_vision(self):
        self._unset_camera_properties()    
        self._set_entity_colors(entity_color_category='original')
    
    def prepare_camera_bw_beings(self,
        color=Color(0.25, 0.25, 0.25, 1), ## Low light Red
        energy_amount=121,
        **kwargs
    ):

        self._prepare_camera_colors(
            entity_color_category='camera',
            characters=color,
        )
    
    def use_camera_bw_beings(self):
        self._set_camera_properties('default')
        self._set_entity_colors(entity_color_category='camera')

    def disable_camera_bw_beings(self):
        self._unset_camera_properties()    
        self._set_entity_colors(entity_color_category='original')
        
    def prepare_camera_bw_non_beings(self, 
        color=Color(0.25, 0.25, 0.25, 1), ## Low light Red
        energy_amount=121,
        **kwargs
    ):

        self._prepare_camera_colors(
            entity_color_category='camera',
            default_color=color,
            enemy_characters=(1,0,0,1),
            teammate_characters=(0,0,1,1),
            npc_characters=(1,1,0,1),
        )
    
    def use_camera_bw_non_beings(self):
        self._set_camera_properties('default')
        self._set_entity_colors(entity_color_category='camera')

    def disable_camera_bw_non_beings(self):
        self._unset_camera_properties()    
        self._set_entity_colors(entity_color_category='original')
        
    def prepare_camera_thermal_vision(self, 
        color=Color(0.25, 0, 0, 1), ## Low light Red
        energy_amount=121,
        **kwargs
    ):
        # c = color*2.5
        # s = color*.8
        # pt(c,s)
        r,g,b,a = color
        shields_color = (r*4.5, g*4.5, b*4.5, a*1.75)
        self._prepare_camera_colors(
            entity_color_category='camera',
            default_color=color,
            characters=color*1.25,
            cores=color*5.5,
            shields=shields_color,
            shield_parts=Color(0,0,0,0),
            shield_part2s=Color(0,0,0,0),
            sky=Color(0, 0, 0, 0)
        )
    
    def use_camera_thermal_vision(self):
        self._set_camera_properties('default')
        self._set_entity_colors(entity_color_category='camera')

    def disable_camera_thermal_vision(self):
        self._unset_camera_properties()    
        self._set_entity_colors(entity_color_category='original')
        
    def prepare_camera_x_ray(self, 
        mode='grey',
        energy_amount=121,
        **kwargs
    ):
        core_color = Color(0.5, 0.5, 0.5, 0.95)
        slots_color = Color(0.5,0.5,0.5,0.95)
        sky_color = Color(0, 0, 0, 0)

        if mode == 'colors':
            enemy_characters = Color(1, 0, 0, 0.1)
            teammate_characters = Color(0, 0, 1, 0.1)
            npc_characters = Color(1, 1, 0, 0.1)
            
            self._prepare_camera_colors(
                entity_color_category='camera',
                default_color=Color(0.5, 0.5, 0.5, 0.1),
                enemy_characters=enemy_characters,
                teammate_characters=teammate_characters,
                npc_characters=npc_characters,
                cores=core_color,
                slots=slots_color,
                sky=sky_color
            )
        else:
            self._prepare_camera_colors(
                entity_color_category='camera',
                default_color=Color(0.5, 0.5, 0.5, 0.1),
                cores=core_color,
                slots=slots_color,
                sky=sky_color
            )

    def _prepare_camera_colors(self, entity_color_category, **kwargs):
        self._generate_entity_colors(entity_color_category='original')
        self._generate_entity_colors(entity_color_category, **kwargs)
    
    def use_camera_x_ray(self):
        self._set_camera_properties('default')
        self._set_entity_colors(entity_color_category='camera')
        
    def disable_camera_x_ray(self):
        self._unset_camera_properties()    
        self._set_entity_colors(entity_color_category='original')
        
    def use_camera_visual(self):
        self._set_camera_properties('default')
        
    def disable_camera_visual(self):
        # pt.c(' disable cam visual')
        self._unset_camera_properties()
        
    def use_camera_electro_magnetic(self):
        self._set_camera_properties('normals')
    
    def disable_camera_electro_magnetic(self):
        # pt.c(' disable cam electro magnetic')
        self._unset_camera_properties()
        
    def use_camera_prop_zoom(self, fov=90):
        camera.fov = max(3, min(179, fov))
        
    def disable_camera_prop_zoom(self):
        self._unset_camera_properties()

    def prepare_camera_prop_zooming_incremental(self, fov_step=5, step_timing=0.05, energy_amount=100):
        self.start_step_time = time.time() ## NOTE: I'm not sure if time.time() is appropriate here, or if I should
                                            ## be using some ursina equivalent
        
    def use_camera_prop_zooming_incremental(self, fov_step=5, step_timing=0.05):
        if time.time() - self.start_step_time <= step_timing:
            return

        camera.fov = max(2, min(179, camera.fov + fov_step))
        
    def disable_camera_prop_zooming_incremental(self):
        self._unset_camera_properties()
        
    def use_camera_prop_resolution(self, resolution=(128, 128)):
        '''    TODO - Not currently working
            Change Game Resolution, independent of the window size
        '''
        if hasattr(self, 'rtt_display'):
            ...
        
        self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 
            resolution[0], resolution[1]
            )

        ## Camera
        self.rtt_camera = app.makeCamera(self.rtt_buffer)
        self.rtt_camera.node().getLens().setFov(90)
        self.rtt_camera.reparentTo(self.slot_owner)
        # camera.clip_far = 11

        ## Display
        self.rtt_display = Entity(model='quad', scale=2, position=(0, 0, 0.5))
        self.rtt_display.parent = camera.ui
        self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())
        
    def disable_camera_prop_resolution(self):
        self._unset_camera_properties




    # def _setup_display_regions(self):
        
    def use_camera_pip(self, cam_parent=None, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
        
        if hasattr(self, 'pip_display_region'):
            self.ursina_window.removeDisplayRegion(self.pip_display_region)
            self.camera_2.removeNode()
            
        ## Ursina's main display region
        self.main_display_region = app.camNode.getDisplayRegion(0)
        # self.main_display_region.setDimensions(0, 1, 0, 1)
        # self.main_display_region.setSort(0)
        self.ursina_window = self.main_display_region.getWindow()
        
        ## secondary display region & camera
        self.camera_node_2 = Camera('CameraNode2')
        self.camera_2 = scene.attachNewNode(self.camera_node_2)
        self.camera_2.node().getLens(0).setFar(11333)
        # self.camera_2.node().getLens(0).setFar(13444)
        
        # self.camera_2.setPos(camera.getPos() + Vec3(0, 0, 0))
        if cam_parent is not None:
            self.camera_2.reparent_to(cam_parent)
        else:
            self.camera_2.reparent_to(camera)
            
        self.camera_2.setPos(position)
        self.camera_2.setHpr(rotation)
        
        self.pip_display_region = self.ursina_window.makeDisplayRegion(0.4, 0.6, 0.78, 0.98)
        self.pip_display_region.setCamera(self.camera_2)
        self.pip_display_region.setSort(22)
        
        
        
        # main_camera_fov = app.camLens.getFov()
        # camera_2_fov = camera_node_2.getLens().getFov()
        # pt(main_camera_fov, camera_2_fov)
        # # camera_node_2.getLens().setFov(main_camera_fov)

        # aspect_ratio = window.size[0] / window.size[1]  # Get the aspect ratio of the window
        # pt(aspect_ratio)
        # fov = app.camLens.getFov()  # Get the current field of view
        # new_fov = (fov[0], fov[0] / aspect_ratio)  # Calculate the new field of view
        # pt(fov, new_fov)
        # app.camLens.setFov(new_fov)  # Set the new field of view

    def disable_camera_pip(self):
        # self.pip_display_region.setActive(False)
        # self.ursina_window.removeDisplayRegion(self.pip_display_region)
        # self.camera_2.removeNode()
        # pt('disable camera pip')
        if hasattr(self, 'pip_display_region'):
            self.ursina_window.removeDisplayRegion(self.pip_display_region)
            self.camera_2.removeNode()

    def use_camera_rtt(self, cam_parent=camera, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
        ''' Render to Texture, main scene objects'''
        if hasattr(self, 'rtt_display'):
            ...
        

        self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 512, 512)

        ## Camera
        self.rtt_camera = app.makeCamera(self.rtt_buffer)
        self.rtt_camera.node().getLens().setFov(90)
        self.rtt_camera.reparentTo(scene)
            
        self.rtt_camera.setPos(position)
        self.rtt_camera.setHpr(rotation)


        ## Display
        self.rtt_display = Entity(model='quad', scale=2, position=(2, 0, 3))
        self.rtt_display.parent = camera
        self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())

        # if cam_parent is not None:
        #     self.rtt_display.reparent_to(camera)

    def disable_camera_rtt(self):
        if hasattr(self, 'rtt_display'):
            self.rtt_display.enabled = False
            # self.rtt_display = None

        if hasattr(self, 'rtt_camera'):
            self.rtt_buffer.removeNode()
            # self.rtt_buffer = None

        if hasattr(self, 'rtt_render'):
            self.rtt_render.removeNode()
            # self.rtt_render = None

        if hasattr(self, 'rtt_buffer'):
            app.graphicsEngine.removeWindow(self.rtt_buffer)
            # self.rtt_buffer = None

    def use_camera_rtt_specific_objects(self, cam_parent=camera, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
        ''' Render to Texture, render specific objects only (like your avatar or map stuff etc.)
        TODO - make a test for this, choose combility slot owner as target or something
        
        '''
        
        if hasattr(self, 'rtt_display'):
            ...
        

        self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 512, 512)
        self.rtt_render = NodePath("rtt render")

        ## Camera
        self.rtt_camera = app.makeCamera(self.rtt_buffer)
        self.rtt_camera.node().getLens().setFov(90)
        self.rtt_camera.reparentTo(self.rtt_render)
            
        self.rtt_camera.setPos(position)
        self.rtt_camera.setHpr(rotation)


        ## Display
        self.rtt_display = Entity(model='quad', scale=2, position=(2, 0, 3))
        self.rtt_display.parent = camera
        self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())

        # if cam_parent is not None:
        #     self.rtt_display.reparent_to(camera)

    def disable_camera_rtt_specific_objects(self):
        if hasattr(self, 'rtt_display'):
            self.rtt_display.enabled = False
            # self.rtt_display = None

        if hasattr(self, 'rtt_camera'):
            self.rtt_buffer.removeNode()
            # self.rtt_buffer = None

        if hasattr(self, 'rtt_render'):
            self.rtt_render.removeNode()
            # self.rtt_render = None

        if hasattr(self, 'rtt_buffer'):
            app.graphicsEngine.removeWindow(self.rtt_buffer)
            # self.rtt_buffer = None






    def use_create_pip(self, 
        pip_name=None, 
        camera_name=None,
        position=Vec3(0,0,0), 
        rotation=Vec3(0,0,0), 
        corner_positions=(0.4, 0.6, 0.78, 0.98), 
        energy_amount=111
    ):
        main_display_region = app.camNode.getDisplayRegion(0)
        main_camera = main_display_region.getCamera()
        self.ursina_window = main_display_region.getWindow()

        num_regions = self.ursina_window.getNumDisplayRegions()
        generated_name = f'pip_display_region_{num_regions}'

        pip_display_region = self.ursina_window.makeDisplayRegion(
            corner_positions[0], corner_positions[1], corner_positions[2], corner_positions[3]
        )
        pip_display_region.setSort(22)

        # If no camera_name is given or if the camera_name is not found, 
        # use the last created camera or the default Ursina camera
        if camera_name is None or not hasattr(self, camera_name):
            if self.cameras:
                camera_to_use = self.cameras[-1]
            else:
                camera_to_use = main_camera
        else:
            potential_camera = getattr(self, camera_name)
            if isinstance(potential_camera, Camera):
                camera_to_use = potential_camera
            else:
                raise ValueError(f"{camera_name} is not a valid Camera object")

        pip_display_region.setCamera(camera_to_use)


        # Store the pip_name with the associated display region in the dictionary
        pip_name = generated_name if pip_name is None else pip_name
        Combility.pip_regions[pip_name] = pip_display_region
        
        # setattr(self, pip_name, pip_display_region)

    def disable_create_pip(self, pip_name):
        pip_region = Combility.pip_regions.get(pip_name)

        if pip_region is not None:
            self.ursina_window.removeDisplayRegion(pip_region)
            del Combility.pip_regions[pip_name]

    def use_new_camera(self,
        cam_parent=None,
        rtt_name=None,
        pip_name=None,
        camera_name=None,
        position=Vec3(0,0,0), rotation=Vec3(0,0,0), 
        resolution=(512, 512),
        energy_amount=100):

        # Try to find the rtt display region first
        display_region = None
        if rtt_name is not None:
            display_region = Combility.rtt_regions.get(rtt_name)

        # If no rtt display region found, try to find the pip display region
        if display_region is None and pip_name is not None:
            display_region = Combility.pip_regions.get(pip_name)

        # If no display region found, default to the last rtt or pip
        if display_region is None:
            if Combility.rtt_regions:
                display_region = list(Combility.rtt_regions.values())[-1]
                rtt_name = list(Combility.rtt_regions.keys())[-1]
            elif Combility.pip_regions:
                display_region = list(Combility.pip_regions.values())[-1]
                pip_name = list(Combility.pip_regions.keys())[-1]
            else:
                raise ValueError('No display region found')

        ## secondary display region & camera
        self.camera_node_2 = Camera('CameraNode2')
        self.camera_2 = scene.attachNewNode(self.camera_node_2)
        self.camera_2.node().getLens(0).setFar(11333)

        if cam_parent is not None:
            self.camera_2.reparent_to(cam_parent)
        else:
            self.camera_2.reparent_to(camera)

        self.camera_2.setPos(position)
        self.camera_2.setHpr(rotation)

        # If using rtt, setup a texture buffer and make a camera with it
        if rtt_name is not None:
            texture_buffer = app.win.makeTextureBuffer(rtt_name, *resolution)
            mirror_camera = app.makeCamera(texture_buffer)
            display_region.setCamera(mirror_camera)
        else:
            display_region.setCamera(self.camera_2)

        # Generate a system name for the camera
        num_cameras = len(Combility.cameras)
        generated_name = f'camera_{num_cameras}'

        # Store the camera_name in the dictionary
        camera_name = generated_name if camera_name is None else camera_name
        Combility.pip_regions[camera_name] = self.camera_2




    def disable_new_camera(self, camera_name):
        this_camera = Combility.cameras.get(camera_name)

        if this_camera is not None:
            # self.ursina_window.removeDisplayRegion(pip_region)
            del Combility.cameras[camera_name]
            self.this_camera.removeNode()
            
    def prepare_camera_vr_simulation(self):
        ...
        
    def prepare_dash(self, 
        range=22,
        speed=205,
        direction=None,
        rotation=None,
        scale=(1,.4,1),
        circle_degrees=222,
        visual_resolution=22,
        path_resolution=6,
        surface_types=None,
        dash_style='arc_dash',
        c_dash_last_line=None,
        path_type='assistant'):
        # pt( 
        # range,
        # speed,
        # direction,
        # rotation,
        # scale,
        # circle_degrees,
        # visual_resolution,
        # path_resolution,
        # surface_types,
        # dash_style,
        # c_dash_last_line,
        # path_type)
        '''
        - Speed is in units/second (meters/sec)
        - rotation and direction are actually identical properties, so we can only recieve one. But we 
        convert the direction to a rotation if its an argument
        
        '''
        if dash_style not in ['arc_dash', 'g_dash', 'c_dash']:
            raise ValueError(f'The {dash_style=} must be an arc_dash, g_dash, or c_dash')
        
        if rotation and direction:
            raise ValueError(f"Cannot pass both a rotation and a direction. Choose one - In Class {self.name}")
        # If direction is passed, convert it to a rotation
        if direction:
            direction_vec = self.calculate_user_passed_direction_vec(direction)
            rotation = self.calculate_rotation_from_direction(direction_vec)
        # pt(direction)
        
        self.add_curve_to_path(
            scale=scale,
            circle_degrees=circle_degrees,
            visual_resolution=visual_resolution,
            path_resolution=path_resolution,
            path_type=path_type
            )

        if dash_style != 'c_dash' and c_dash_last_line is not None:
            raise ValueError('c_dash_last_line is only for "dash_style=c_dash"!')
        if dash_style == 'c_dash':
            if not c_dash_last_line:
                # Get the last two points of the path
                last_two_points = self.assistant_visual_vertices[-2:]
                # Calculate the vector from the second last point to the last point
                vector = last_two_points[1] - last_two_points[0]
                # Add the vector to the last point to get the new point
                new_point = last_two_points[0] + vector * 10
                # Add the new point to the path
                self.add_points_to_path(new_point, path_type=path_type)
            else:
                self.add_points_to_path(c_dash_last_line, path_type=path_type)
        
        self.compile_path(
            range=range, 
            rotation=rotation,
            path_type=path_type,
            # direction_vec=direction_vec,
            )
        
        self.add_target_types(general=surface_types, path_type=path_type)
        
        visual_vertices = self.assistant_visual_ent.model.vertices 
        dist_of_visual_vertices, num_points_visual_vertices = self.get_length_of_path(
            visual_vertices, scale=range)
        
        path_vertices = self.assistant_path_ent.model.vertices
        dist_of_path_vertices, num_points_path_vertices = self.get_length_of_path(
            path_vertices, scale=range)
        
        duration = dist_of_visual_vertices / speed 
        
        ratio_visual_verts_to_path_verts = num_points_visual_vertices / num_points_path_vertices
        
        avg_dist_between_visual_points = dist_of_visual_vertices / (num_points_visual_vertices - 1)
        
        self.is_performing_action_dash = False
        

        return surface_types, path_type, duration, num_points_visual_vertices, ratio_visual_verts_to_path_verts, path_vertices, avg_dist_between_visual_points
        
    def use_dash(self,
        surface_types,
        path_type,
        duration,
        num_points_visual_vertices,
        ratio_visual_verts_to_path_verts,
        path_vertices,
        avg_dist_between_visual_points):

        if self.is_performing_action_dash:
            return
        
        
        self.assistant_path_ent.world_position = self.eaat.world_position
        curve_points = [Vec3(self.world_position)] + [Vec3(scene.getRelativePoint(self.assistant_path_ent, vertex)) for vertex in self.assistant_visual_ent.model.vertices]
        
        # pt(surface_types, path_type)
        self.add_target_types(general=surface_types, path_type=path_type)
        self.is_performing_action_dash = True
        self._choose_ray_type(path_type=path_type)
        self.assistant_path_ent.world_position = self.combility_barrel_end.world_position
        
        if not self.hate:
            pt.c("Dash failed. Target surface type is not in the acceptable_bot targets list.")
            self.is_performing_action_dash = False
            return
        
        equivalent_visual_index = int(self.index_of_last_point_before_hit * ratio_visual_verts_to_path_verts)
        hit_point_distance = (self.hit_info.world_point - path_vertices[self.index_of_last_point_before_hit]).length()
        vertices_to_remove = int(hit_point_distance / avg_dist_between_visual_points)
        equivalent_visual_index -= vertices_to_remove
        
        new_curve_points = curve_points[:equivalent_visual_index+1]
        new_point = self.hit_info.world_point + self.hit_info.normal * (self.eaat.world_scale*0.5)
        new_curve_points.append(new_point)
        
        adjusted_duration = duration * (len(new_curve_points) / num_points_visual_vertices)
        
        if len(new_curve_points) > 1:
            self.eaat.recieve_dash(adjusted_duration, new_curve_points)
            
        self.is_performing_action_dash = False
        
    def use_visibility(self, alpha=0.0, duration=1.0):
        self.eaat.recieve_visibility(self.specific_target, alpha=alpha, duration=duration)
            
    def get_new_hit_ent_attributes(self, ignore_list):
        if Combility.stored_copied_entity_attributes is not None:
            return Combility.stored_copied_entity_attributes['texture'], Combility.stored_copied_entity_attributes['texture_scale'], Combility.stored_copied_entity_attributes['color'], Combility.stored_copied_entity

        # First raycast in the forward direction
        hit_info = raycast(self.eaat.world_position, self.eaat.forward, 
                        distance=12, ignore=ignore_list,
                        debug=True,
                        )
        if not hit_info.hit:
            # Second raycast in the downward direction
            hit_info = raycast(self.eaat.world_position, -self.eaat.up, distance=12, ignore=ignore_list)
        if hit_info.hit:
            return hit_info.entity.texture, hit_info.entity.texture_scale, hit_info.entity.color, hit_info.entity
        else:
            # Default values if no entity is hit
            return None, None, None, None

    def use_mimic(self, duration=1.0):
        if self.get_real_eaat().parent.name == 'environment':
            return

        ignore_list = self.get_relevant_descendants(self.eaat)
        texture, texture_scale, color, entity = self.get_new_hit_ent_attributes(ignore_list)
        self.eaat.recieve_mimic(self.specific_target, entity=entity, duration=duration)

    def use_camo(self, duration=1.0):
        if self.get_real_eaat().parent.name == 'environment':
            return

        ignore_list = self.get_relevant_descendants(self.eaat)
        texture, texture_scale, color, entity = self.get_new_hit_ent_attributes(ignore_list)
        self.eaat.recieve_camo(specific_target=self.specific_target, texture=texture, texture_scale=texture_scale, color=color, duration=duration)
        self.add_update_function_if_exists("camo", (texture, texture_scale, color, duration))
    
    def use_copy_target(self):
        real_eaat = self.get_real_eaat()
        Combility.stored_copied_entity = real_eaat ## STORES THIS AS A WEAK REFERENCE
                                                                ## so it can be garbage collected when destroyed
        Combility.stored_copied_entity_attributes = {
            'model': real_eaat.model,
            'world_scale': real_eaat.world_scale,
            'world_rotation': real_eaat.world_rotation,
            'texture': real_eaat.texture,
            'texture_scale': real_eaat.texture_scale,
            'color': real_eaat.color,
            'alpha': real_eaat.color.a,
            'always_on_top': real_eaat.always_on_top,
        }
        # pt('stored ent, stored attributes', Combility.stored_copied_entity_attributes, 
            # real_eaat.name, real_eaat)
            
    def prepare_attacher(self, energy_amount):
        self.attacher_ent = Entity(name='attacher_ent', model='sphere', color=color.orange, enabled=False)
        self.attacher_health = energy_amount
        
    def use_attacher(self, energy_amount):
        self.attached_entity = self.get_real_eaat()
        
        self.attacher_ent.enabled = True 
        self.attacher_ent.world_position = self.hit_info.world_point
        self.attached_entity_offset = self.attached_entity.world_position - self.attacher_ent.world_position
        self.add_update_function_if_exists("attacher", (energy_amount,))
    
    def update_attacher(self, energy_amount):
        if self.attacher_ent.enabled:
            self.orient_to_attacher()
            self.attached_entity.world_position = self.attacher_ent.world_position + self.attached_entity_offset
            
    def add_auto_swivel(self):
        self.auto_swivel = True
        
    def prepare_tk_grab(self, energy_amount=100):
        
        deque_size = max(1, int(1 / (energy_amount / 100)))
        self.tk_grabbed_ent_positions_deque = deque(maxlen=deque_size)
        pt(deque_size)

        
        
        # self.tk_grab_hand = Light_Position_Model_Entity(
        #     parent=self, 
        #     color=tk_grab_hand_color,
        # )
        color_index = min(energy_amount // 100, 10)
        tk_grab_hand_color = EG_Globals.SHIELD_COLORS()[int(color_index)]
        
        self.tk_grab_hand = Entity(name='tk_grab_hand',
            parent=self,
            add_to_scene_entities=False, 
            model='cube',
            world_scale=.6,
            color=tk_grab_hand_color,
            enabled=False,
            )
        
    def use_tk_grab(self, energy_amount):
        self.tk_grabbed_ent = self.get_real_eaat()
        self.tk_grab_hand.enabled = True
        
        self.tk_grab_hand.world_position = self.hit_info.world_point
        self.tk_grabbed_ent_offset = self.tk_grabbed_ent.world_position - self.tk_grab_hand.world_position

        # Calculate the initial distance between self and tk_grab_hand world positions
        initial_distance = distance(self.world_position, self.tk_grab_hand.world_position)
        
        # Calculate the number of elements to add to the deque based on the initial distance
        
        num_elements_to_add = int((initial_distance / self.path_range) * self.tk_grabbed_ent_positions_deque.maxlen)
        pt(energy_amount, initial_distance, self.path_range, initial_distance/self.path_range, num_elements_to_add,
            self.tk_grabbed_ent_positions_deque.maxlen)
        
        
        new_position = self.tk_grab_hand.world_position + self.tk_grabbed_ent_offset
        self.tk_grabbed_ent_positions_deque.extend([new_position] * num_elements_to_add)

        self.add_update_function_if_exists('tk_grab', energy_amount)
        
    def update_tk_grab(self, energy_amount):
        # pt.t(2)
        # Save the new position in the deque
        new_position = self.tk_grab_hand.world_position + self.tk_grabbed_ent_offset

        self.tk_grabbed_ent_positions_deque.append(new_position)
        self.tk_grabbed_ent.world_position = self.tk_grabbed_ent_positions_deque.popleft()


    def calculate_user_passed_direction_vec(self, direction):
        direction_mapping = {
            "forward": Vec3(0, 0, 1),
            "push": Vec3(0, 0, 1),
            "back": Vec3(0, 0, -1),
            "backward": Vec3(0, 0, -1),
            "pull": Vec3(0, 0, -1),
            "left": Vec3(1, 0, 0),
            "right": Vec3(-1, 0, 0),
            "up": Vec3(0, 1, 0),
            "down": Vec3(0, -1, 0),
        }
        if isinstance(direction, str):
            direction = direction.lower()
            if direction not in direction_mapping:
                raise ValueError(f"Invalid direction: {direction}")
            direction_vec = direction_mapping[direction]
        elif isinstance(direction, Vec3):
            direction_vec = direction
        else:
            raise TypeError("direction must be a string or a Vec3 instance")

        # Normalize, which means the Vector now has a total length of 1!!!
        direction_vec = direction_vec.normalized()
        return direction_vec

    def calculate_energy_dist_for_teleport_hit(self, initial_direction_vec, intial_energy_distance, ignore_list, half_size_eaat):
        original_world_position_eaat = self.eaat.world_position
        total_energy_distance = intial_energy_distance  # Initialize total_energy_distance with the initial energy amount
        energy_distance = intial_energy_distance
        attempt = 0
        while True:
            attempt +=1
            if attempt == 4:
                self.eaat.world_position = original_world_position_eaat
                pt('max teleportation bonus through geometry reached, cancelling telport')
                return total_energy_distance
            destination = self.eaat.world_position + initial_direction_vec * energy_distance
            self.eaat.world_position = destination
                
            hit_info = self.eaat.intersects(ignore=ignore_list)
            if hit_info.hit:
                energy_distance += 1
                total_energy_distance += energy_distance  # Increase the total_energy_distance by 1
            else:
                forward_hit_info = raycast(self.eaat.world_position, 
                    initial_direction_vec, distance=200, ignore=ignore_list)
                backward_hit_info = raycast(self.eaat.world_position, 
                    -initial_direction_vec, distance=energy_distance, ignore=ignore_list, debug=True)
                if backward_hit_info.hit and forward_hit_info.hit and backward_hit_info.entity == forward_hit_info.entity:
                    energy_distance = forward_hit_info.distance
                else:
                    self.eaat.world_position = original_world_position_eaat
                    break
                
        return total_energy_distance
    
    def calculate_energy_dist_from_hit(self, direction_vec, energy_amount, ignore_list, half_size_eaat):
        hit_info = raycast(self.eaat.world_position, direction_vec,
                        ignore=ignore_list,
                        distance=energy_amount + half_size_eaat, debug=True)
        if hit_info.hit:
            return distance(self.eaat.world_position, hit_info.world_point) - half_size_eaat
        return energy_amount

    def calculate_real_time_direction_vec_from_hit(self, direction_vec):
        if self.hit_info and self.hit_info.hit:
            forward = Vec3(-self.hit_direction)
            right = Vec3(forward.cross(Vec3(0, 1, 0)).normalized())
            up = Vec3(right.cross(forward).normalized())
            return direction_vec.x * right + direction_vec.y * up + direction_vec.z * forward
        else:
            return direction_vec.x * self.combility_barrel_end.right + direction_vec.y * self.combility_barrel_end.up + direction_vec.z * self.combility_barrel_end.forward

    # def prepare_force(self, direction, energy_distance, type=None):
    #     type = 'impulse' if type is None else type

    #     if type not in ['impulse', 'teleport', 'blink']:
    #         raise ValueError(f'"{type}" is not a valid type for "add_force"')

    #     initial_direction_vec = self.calculate_user_passed_direction_vec(direction)

    #     if type == 'teleport':
    #         custom_curve = Jitter_Teleport_Curve(jitter_duration=0.5, jump_duration=0.01, end_duration=1.5)
    #         duration = 1.5
    #     else:
    #         if type == 'blink':
    #             custom_curve = curve.linear
    #             duration = 0.0
    #         elif type == 'impulse' or type == 'impulse_force':
    #             custom_curve = curve.out_expo
    #             duration = 0.3

    #     # Return the values that will be used as arguments for the use_force function
    #     return initial_direction_vec, energy_distance, custom_curve, duration, type
    
    # def use_force(self, initial_direction_vec, energy_distance, custom_curve, duration, type):
    #     if self.get_real_eaat().parent.name == 'environment':
    #         return
    #     final_direction_vec = self.calculate_real_time_direction_vec_from_hit(initial_direction_vec)
    #     ignore_list = self.get_relevant_descendants(self.eaat)
    #     half_size_eaat = self.eaat.world_scale.x * 0.5

    #     if type == 'teleport':
    #         energy_distance = self.calculate_energy_dist_for_teleport_hit(final_direction_vec, energy_distance, ignore_list, half_size_eaat)
    #     else:
    #         energy_distance = self.calculate_energy_dist_from_hit(final_direction_vec, energy_distance, ignore_list, half_size_eaat)
    #     self.eaat.recieve_impulse(final_direction_vec, energy_distance, duration, custom_curve)
        
    #     ## TODO, REDO this section, too many repetitive if statements
    #     if type == 'teleport':
    #         Audio('teleport-90137.mp3', autoplay=True)

    #     elif type == 'blink':
    #         Audio('futuristic-smg-sound-effect-100378.mp3', autoplay=True)
            
    #     else:
    #         Audio('push_wind_whipy-woosh-transition-38006', autoplay=True)
        



    # def _get_descendants(self, entity):
    #     descendants = []
    #     for child in entity.children:
    #         descendants.append(child)
    #         descendants.extend(self._get_descendants(child))
    #     return descendants
    def _get_descendants(self, entity, max_depth=15):
        if max_depth <= 0:
            pt(self.eaat)
            pt.ex()
            return []
        descendants = []
        for child in entity.children:
            descendants.append(child)
            descendants.extend(self._get_descendants(child, max_depth - 1))
        return descendants

    def get_relevant_descendants(self, entity):
        relevant_names = ['scene', 'enemies', 'local_objects', 'npcs', 'teammates']
        while entity.parent and entity.parent.name not in relevant_names:
            entity = entity.parent
        return [entity] + self._get_descendants(entity)
        
    def angle_between(self, u, v):
        dot_product = u.dot(v)
        magnitude_u = math.sqrt(u.dot(u))
        magnitude_v = math.sqrt(v.dot(v))

        cos_angle = dot_product / (magnitude_u * magnitude_v)
        cos_angle = max(min(cos_angle, 1), -1)
        angle = math.degrees(math.acos(cos_angle))
        
        return 180 - angle
    
    def calculate_adjusted_damage(self, damage):
        
        ## Vector from Center of Bubble shield to the hit point
        hit_vector = self.hit_info.world_point - self.hit_info.entity.world_position
        # pt(self.hit_info.world_normal, hit_vector)
        
        ## Angle between the projectile and the center of shield
        angle = self.angle_between(-self.hit_direction, hit_vector)
        
        ## Create a sweet spot for max damage. 
        if angle <= 12:
            return damage 
        
        #################################################
        # Damage calc - 
        #################################################
        #    return damage * (1 - (angle / 100) * 0.3)
        #       (angle /100) is just getting angle in decimal form. 
        #   return damage * (1 - (angle / 83) * 0.3)
        #       (angle/83) is getting something more accurate because thats about the max
        #       angle we can hit against the sphere ~ 83 degrees
        #   0.3: 
        #       (0.3) means that we can take away a maximum of 0.3 damage away, so 70% damage 
        #       minimum is counted at the extremes)
        #
        return damage * (1 - (angle / 83) * 0.3)
        #################################################
    
    def cause_damage(self, damage):
        if self.get_real_eaat().parent.name == 'environment':
            return
        if self.hit_info is not None:
            
            adjusted_damage = self.calculate_adjusted_damage(damage)
            
            self.eaat.recieve_damage(adjusted_damage, self.hit_info.world_point, self.hit_info.world_normal)
            pt(self.eaat.name, damage, adjusted_damage)
        else:
            
            self.eaat.recieve_damage(damage, self.eaat.world_position, self.eaat.forward)


    ###############################
    ## DON'T DELETE these!!!!
    ## THIS IS THE ORIGINAL ONE. THE ONE BENEATH WAS JUST FOR TESTING the visuals
    ###############################
    # def prepare_dmg_developer_laser(self, energy_amount=100):
    #     damage = energy_amount * 1
    #     return damage
    
    # def use_dmg_developer_laser(self, damage):
    #     '''Testing laser for developers only. 
        
    #     - 1:1 ratio of damage to energy '''
    #     self.cause_damage(damage)
        
    #     self.projectile_visual_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
    #     self.projectile_visual_ent.color = color.red
        
    #     self.projectile_path_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
    #     self.projectile_path_ent.color = color.yellow
    #     laser_sound = Audio('laser_pulse_lazerius-139178', autoplay=True)

    ######################################
    ## TEMP - CREATED FOR TESTING VISUALS/AUDIO
    ######################################
    def prepare_dmg_developer_laser(self, energy_amount=100):
        damage = energy_amount * 1
        self.dmg_dev_laser_offset = 0
        return damage
    
    def use_dmg_developer_laser(self, damage):
        '''Testing laser for developers only. 

        - 1:1 ratio of damage to energy '''
        self.cause_damage(damage)

        original_texture = self.projectile_visual_ent.texture
        original_color = self.projectile_visual_ent.color
        original_texture_offset = self.projectile_visual_ent.texture_offset

        self.projectile_visual_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
        self.projectile_visual_ent.color = color.red

        self.projectile_path_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
        self.projectile_path_ent.color = color.yellow
        laser_sound = Audio('laser_pulse_lazerius-139178', autoplay=True)

        # Animate the texture offset for half a second
        for i in range(35):  # 10 steps in the animation
            invoke(self.animate_texture_offset, delay=i*0.05)  # 0.05 seconds delay between each step

        # Return to the original colors, textures, and texture offset after half a second
        invoke(self.reset_visuals, original_texture, original_color, original_texture_offset, delay=0.5)

    def animate_texture_offset(self):
        self.dmg_dev_laser_offset += time.dt * -11
        self.projectile_visual_ent.texture_offset = (self.dmg_dev_laser_offset*0.2, self.dmg_dev_laser_offset)
        self.projectile_path_ent.texture_offset = (self.dmg_dev_laser_offset*0.1, self.dmg_dev_laser_offset)

    def reset_visuals(self, original_texture, original_color, original_texture_offset):
        self.projectile_visual_ent.texture = original_texture
        self.projectile_visual_ent.color = original_color
        self.projectile_visual_ent.texture_offset = original_texture_offset
        self.projectile_path_ent.texture = original_texture
        self.projectile_path_ent.color = original_color
    
    # def update_dmg_developer_laser(self):
        
    def ice(self, energy_amount):
        pass

    def fire(self, energy_amount):
        pass

    def gas(self, energy_amount):
        pass

    def lightning(self, energy_amount):
        pass

    def solids(self, energy_amount):
        pass

    def suspended_solids(self, energy_amount):
        pass

    def fused_solids(self, energy_amount):
        pass

    def electro_laser_tunnel(self, energy_amount):
        pass

    def microwave(self, energy_amount):
        pass

    def plasma(self, energy_amount):
        pass

    def laser(self, energy_amount):
        self.cause_damage(energy_amount * 5)
        pass

    def energy_disruptor(self, energy_amount):
        pass






'''BUG - BUG bug:
- add texture to dev laser
- Test_damage_dispersion = see if works
- add simple graphic for the CAUS. Like a outer weapon skin with "dials", trigger etc. 

- Visual_vertices/path vertices are making waaaay too many vertices. They seem to be adding
about 8 vertices per location. So, for example, I have an arc that is taking up 22 separate points
on the map, there might be 8 different ones that are just slightly different at each of the 
22 points. This will cause mistakes with my dashing/getting length of the points between lines
for calculating speed, energy, or creating 3d models etc. 


- I still have no way of catching bugs/crashes that happen within the 
    perform_actions, perform_disables etc.
    - I need a way to actually simulate what happens, or cause some 
    sort of crash/disruption.
        - Part of me likes that they are silent, because it may prevent
        crazy things from happening. But I need to be able to debug
        that stuff for development.
        - Perhaps using tracing will work?
        - Maybe decorators?
        - Maybe adding a simple return to every one of my functions, 
        and then a check on the temp function that is added to the list 
            - The check is "did it return anything at all? 
                - if not, raise error.
    - Maybe just make the actual function call where I want it. 
        - If its supposed to be in disables..
            - I take the malfunctioning function, and call it in actual disables!
                
- c_dash_others doesn't dash (most of the time...)


- 
'''

'''TODO - TODO todo:
- Def input():
    - Lots of probably unecessary disabling iterations. I need to just disable the
    last index maybe? I'm not sure. It\s safe to keep it like it is, but I think
    its totally unecessary. But ALSO, THIS IS JUST A TEST SYSTEM, NOT HOW THE 
    REAL SYSTEM WILL WORK. So meh. 


- Caus system implemented so...
    - Remove references to "mod mixes" These are just back to combilities now. 




What I can work on now:
    - New Function type: "on_activation"
        - I noticed that for some abilities, I don't need to hit any targets
        - I just want something to happen even if I don't hit a target
            - Like my camera mods. 
            
    - More Smaller-mods, more pre-builts:
        - What if everything with complicated steps was actually just a single, simple combility?
        - A dash has its own range, arc, custom point, etc. These are all things
        that we have mods for. So why not just make it out of the mods that
        we already have? So instead of the dash needing special dash logic with 2 different targeting systems in place,
        we simply isolate these into 2 separate combilities that the CAUS then has some control over. 

    - Hybrid controller:
        - Personal Shield:
            - perhaps two different entities for this. 
                - One that is almost completely transparent but
                that is always in front of him but can recieve textures/animations when it gets shot, 
                - Second that is the color that it should be / shield color updates. but is just barely
                around the edges of his vision.
                    - Alt idea:
                        - Change the existing Animated Shields to double-sided = True whenever it is shot 
                        and we are applying hit effects to it on the outside (scale, faster animations etc). 
                        So we also add double_sided with invoke to turn it off, so that the player can see it as well. 

- TODO Later:
- Change all strings when creating the self.add_mod('mod_name')
    - Change to Enums. 
        - Enums are created from the google spreadsheet    

- Mimic / Clone Projector problem:
    - ursina duplicate not working on EnergyBeing 
        - due to the required "energy_being" args in Character, Core, Shield. 
        - Possibly due to other things. 
    
    Solution All:
        - This solution will likely be used no matter what the alt 
        solutions are. 
        - We put a try statement where we try to duplicate the normal way
        - if fails, we do whatever our alternate approach is. 
            - Might make sense in future to check type before attempting to 
            mimic. 
            
    Solution Alt 1:
        - We use instancing to instance both the parent and children nodes
            - Pros:
                - Will be optimizing resources
                - They are non-collision which is what we want. 
                - Opens the door for dozens of clones at the same time (fun
                anime clone-type of mods)
                - Opens the door for me using isntancing in other parts of EG. 
            - Cons:
                - Will be difficult to pull off.
                
    Solution Alt 2:
        - Recreate the original Entity:
            - We just copy out the attributesof the entity in the recieve_mimic
            function, and then just re-instantiate a new class with those attributes!
            
    Solution Alt 3:
        - Create modification to Ursina's duplicate file/class. We start with that
        module, make our own version of it, and figure it out til it works well. 
            - Could even probably have this modified module handle whether the 
            duplicate needs to be done in the simple/normal way or in the advanced/
            complex way. 
            
- Camo / Mimic
    - prebuilt combilities:
        - trigger down:
            select target to copy
        - trigger up:
            apply "target to copy" properties to eaat
            
- Clone projector:
    - Update_clone_projector:
        - make sure to check for enabled status of the Combility in update, or every few frames. 
            
- Possible great Optimization change:
    - I'm currently setting self.acceptable_bot_targets right before I raycast. But... is this actually necessary?
    If I was using the same entity (to save on entity's) that existed outside of all of my classes, then 
    I could see needing to do this. But this entity literally was created from this class so...
    I think we can get rid of it, and just let this happen when we add_acceptable_bot_targets. 
    - Note, I originally did this with the thought that they'd be passing this guy around, but because
    each combility will do its code in order, then they'd have to re-do what the acceptable_bot targets
    were. Again, this would make sense if I passed in some entity for this behavior. But if I am
    not, I could get rid of this repeated 40us call... 

- Animate along path:
    - This will be the basis for Shooting as well as dashing and other activities. 
        - It is vital that we make this as fast & efficient as possible. 
    - All beings/entities & projectiles are actually moved by a mesh vert system. 
        - This serves as the outer-most lod. But is also the only thing that actually moves. 
        - Entities are assigned a vert #. When that vert moves, then they are updated. 
    - bullets are only models/entities while they are close distance to the observer. 
        - assigned to a vert mesh object rather quickly. 
        
        
- Dash things to overcome:
    - Animating along my set of vertices:
        - Potential Solution 1: "Sequence, positions"
            - Make the path extremely refined (very detailed, many points)
            - add a bunch of movement functions to an ursina sequence. 
            
        - Potential Solution 2: Sequence, animations:
            - Keep path normal resolution
            - add several animations that animate between each point  to the sequence. 
        
        - potential solution 3: custom animator 
            - Use either ursina or panda3d. 
            
        - Potential solution 1a & 2a & 3a:
            - Use my logic in the segmented linecast for setting this up. 
                - then simply have to either move or animate through those points. 
                
        - Potential Solution 4: Inserting own logic into application.sequence
            - Ursina's Sequence() gets organized, then sends it off to application.sequence or something
            - Find out what its doing in there. Either directly insert my logic into that, or go a step
            further and do the panda3d route. 
            
        - Potential Solution 5: custom core1k update:
            - We have an ongoing def update in core1k. 
            - It peforms each function, one after the other, in its list of update_actions (see combility
            perform_actions for the logic)
            - These update_actions list can be updated at any time. So the animation sequence gets added
            then removed when its finished. 
            - I think that means we'd have to pass the instance of the core1k class with us wherever
            we went. I don't think we could just keep incorporating the same module.. but I could try. 
                - If we have to pass the instance, then look into combining this with the game manager
                concept. Perhaps we don't need the core1k version anymore, and just use the same
                type of function in gamemanager, or perhaps we can pass the core1k version along with
                the gamemanager instance.
                


- Range needs separate logic for if you have an external or internal eeat. 
    - If user sets range but the eeat is themselves, then what does the range do?
    - If they have a secondary / assistive raycast (for something like dashing, target etc), then
    does this share the same range? Or does it need its own range type set? 


- Mods requiring the use of the 'assistant' entity & path type for self.acceptable_bot_targets etc. 
    - Booster target for Impulse's
    - Camo target
    - Mimic Target
    - Dash
    




- Dispersion:
    - Instead of trying to do complex math "in the world" or setup colliders, we can just use
        vectors, and angles to determine if both players are hitting each other, and if so, are their
        angles/vectors are close? If so, then we have a cheap way of determining that the bullets
        should be colliding with each other. 
    - If player A shot first, then dispersion would happen right in front of player B's shield. 
    - If both player's shot within a frame of eachother, then the dispersion would happen in the
        center between the players. 
    
    - To implement dispersion:
        - The player who is shooting and hits a hit_info.entity:
            - checks if they are also getting shot. 
                - If being shot by the same hit_info entity,
                    - checks their projectile angle & vector vs the enemy projectile angle & vector. 
                    - if within tolerances... 
        - Implement controls for beam/pulse etc. 
        - Implement visuals for the projectiles
        - add an additional projectile model at the dispersion point for each projectile involved
            - This will be the rough dispersion model. Just a mostly-flat sphere in a disc-like shape
            - Shader is responsible for making this look good. 
            - damage is calculated for interception with this model of any entities 
                (probably any entities in the area via grid-like system or something)
            - damage checks for entities, 
                - damage goes down opposite of the scale of this new projectile dispersion model
                    (so the larger the width/scale of the model, the damage/energy it does)
                - then distance to center of dispersion is calculated. 
                - Sum:
                    -Distance and size of dispersion model are accounted for. 
            - Applies any movement actions from the vector of center point to the hit entity. 
                - So if there was a "push", they'd get pushed based on their vector to the center
                point and the amount of energy transferred. 
                
NOTE / NOTES / IDEAS:

- AOE / Shield relationship?
    - Could your energy shield simply be a certain Combility?
        - Mods: AOE, Shield, Attached to slot "Core"
        - For now, your core is limited to:
            - AOE Combilities
            - Physical Movement & Armor Combilities
                - Head
                - Torso
                - Arms
                - Legs


- Explaining the Shield:
    - Your Core constantly generates energy and stores it up to its maximum capacity. 
    - Extra Energy not being used by your Character must be dissipated. 
    - The shield is one of the best ways of utilizing energy not being used by anything else
    

- Cheap enemy aim indicator:
    - I pasted the functions angle_between( and calculate_adjusted_damage( to cursor gpt4 and
        asked it a question on how to detect 2 vectors. 
            "I am getting the angle between the hit point and the center of the bubble shield. 
            But if I wanted to generate another raycast from the center of the sphere to outside 
            of the sphere and get the angle of it, I would want to know if the angle matched or 
            was within a close enough angle to matcihing the original one, but also that the vector 
            itself was close to the original vector. Because otherwise, the angles could be identical, 
            even though the incoming hit_vector is on the Right of the bubble shield and the outgoing 
            one was on the upper-left or seomthing."
    - Then I asked it if I could use this for cheap collision:
            "In a game engine, instead of calculating collision with raycasts or collision models,.. 
            if I knew where player 1 was in the world and where he was aiming ,and I knew where player 
            2 was and where he was aiming, couldn't I get both of their vectors and see if each of the 
            players vectors were close at that distance? "
    - cost of vector math collision:
        - I can run this cheap vector math check to see if either of the two arms are pointing at 
        any of the bubble shields in the area. 
        - If I had to iterate over several different guys in the area, this would get costly quickly. 
    - Adapting with entities in grids (cheaper cost): 
        - if keep track of entities per grid, then vectors could indicate which grids it was "looking"
        at within a certain range, then go from closest grid to furthest, seeing if there is an entity
        in that grid that we are pointing at. 
    - Altternative: linecast:
        - I'm not sure, but it might be better to simply have permanent linecasts coming out of each 
        arm whenever they are not shooting a combility from that arm. The linecast would be at the range
        of the combility on that arm with the largest max_range. 
        
- Think about the relationships with targets, types, 
    what can recieve effects, etc:
    
    - Expand Target Categories:
        - combility can't currently affect both the user and the other 
            types of targets. 
        - I'd like to be able to hit multiple entities at a time
            - Shotgun
            - AOE Explosions
            - Multiple entities being pulled/pushed
            - Lightning hitting multiple target simultaneously. 

        - Target categories:
            - Categories:
                - projectile_target_types: 
                    Who to apply the effects to. 
                - assistant_target_types
                    What helps to boost this ability
                - aoe_target_types:
                    Who gets hit by an AOE
            - Relationship between them:
                Example 1:
                    - a projectile_target_type could be of type "teammate"
                    - while at the same time, the splash target types could be "enemy"
                    - So.. you shoot teammate and an explosion damaging enemies happens
                Example 2:
                    - Assistant_target_type is "environment" for the dash, which means
                    that is the surface the dash can connect to. 
                    - Projectile_target_types is "teammate" which means that the teammate
                    will be dashed to the surface position.
        
                
Rebuild Combility:
    - Combility Builder class should be used. 
        - it auto-organizes the users choices, so that the correct order ensues and then destroys their
        current combility and makes a brand new instance of one. This happens every time they change
        a part? 
    - What class Combility needs to do:
        - It still needs to adjust individual settings on the fly.. how to? 
        
Visual Paths - Maybe...
    - add ability to turn on/off the showing of the visual paths.  
        - They can be the defaults for showing you the path like a preview (dash path)
        - Can actually be the base of the 3d graphics for your gun...
            - So Instead of creating a 3d mesh for the arc path to follow, perhaps we simply make the lines
            much larger and in_line with the shape/scale parameters in the shape category.
            
To build a combility: 
    - setup all the functions that will happen when:
        - Button is pressed (perform_actions)
        - enable runs
        - disable runs
        - updates runs
            - For Optimization Later on, separate the updates that happen with and without hitting a target
                - Updates for if path hit target and separate updates to run if not. 
                



'''

'''TODO Needed Refactors:


- Color generation with Wave Reception Cameras:
    - Option 1: specific iteration:
        - Shouldn't iterate through the entire scene.entities list and look for items. 
        - Should simply pull in my sets () from EG_Globals of all of the entities that have been 
        added to each type of set. 
        - Can then get the "originals" of these colors. 
    - Option 2: originals, at time set:
        - If instead, we got their original colors at the time we activated the camera, 
        then a player could hold down two different cameras, A, then B. He could continually
        let go of B to check on A, and then re-engage on B again to check on B. 
            Problem:
                - If he let go of A first, then colors would go original, but then when let go of 
                B, colors would revert to A... 
            Maybe Solution:
                - It would revert to A's colors if A's colors still existed in memory. If not, it
                would revert to the default colors. 
    
    
'''

'''NOTE Optimizations

Class vs Entity:
    - Does Enemy, Teammate, NPC etc. classes, and enemies/teammates etc. classes all need
    to be entities? If this were just classes that passed through their data, I could 
    eliminate a lot of overhead on every character in the game.
    
All textures power of 2 squares:
    - Digit_rain (or whatever equivalent I AI that into), is standard 16x9
    - lots of other texture probably are too. 
    - Will be more optimized and compatible with more pc's/OS's/mobile/browser etc.add()
    if I make them all a power of 2, and all square. 
    - power of 2 does not mean that one side is 2x larger than other. It means
    that it's literally "2^power" of numbers. 
    - Also, square was originally only thing that would work, and still possibly more optimized/compatible today.
        Proper Values:
            1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192
        Proper combinations:
            1x1, 2x2, 4x4, 8x8, 16x16, 32x32, 64x64, 128x128... etc. 
    
    
'''
'''
    NOTE on this msg. It might make the most sense to put this "keys" notes and the 
    self.eeat stuff into a file for mods of helper functions category
    
    Keys:
        (Note: severely limit the keys. These are mainly for cutting out long typing, but if I don't
        immediately remember what each key is when reading it, then it won't really help)
        
        - eaat: 'The entity who is going to eat our actions' - 'entity_to_apply_actions_to'
        - hate: 'Your targeting me to use against others' - 'hit_assistant_target_ent'
            TODO May be unecessary as I shift to the 2-combilities system for things like dashes. 
        - pip: Picture-In-Picture (display regions)
        - rtt: Render-To-Texture (Either used like a display region, or used in the 3d world)
        - path: I am currently using the term "path" to mean the projectile/combility/mod path, 
            So this is the projectile shape, curve, trajectory, movements, speed etc. 
            
    TODO:
    - Add shortcuts for adding mods via both:
        - combility.add_mod 
        - combility.add_mods
        - combility.remove_mod
        (they'll go through the proper channels to add mods, add to appropriate lists, etc.)
        
    - Eliminate the path_ent, make it the visuals/models for the combility itself. 
    - ccaus will function for the device. 
    - Perhaps the visual_ent can be either a panda3d actor, or a nodepath with
    shaders/graphics etc. Or maybe it can remain an entity til I figure it out. 
    

        
    BUG 1-2:
        FOR sELF.ACCEPTABLE_BOT_PROJECTILE_TARGETS:
        ## plural name(s), because each entity controls all of the children parented to hit
        ###NOTE: ^^^^^^^^^^^^^^^^^^^^^ This is an optimizatin that WILL more than likely CAUSE A BUG in the future. 
        ### - We set the parent of all of the entities that can be hit by this combility to self.acceptable_bot_projectile_targets. 
        ### - We pass self.acceptable_bot_projectile_targets into the traverse target. 
        
        ### POSSIBLE BUG 1:
        ### - if all enemy entities have a parent of "enemies", then they can't be parented to other
        ###   objects etc. like a spaceship etc. 
        ### SOLUTION BUG 1:
        ###- We could use panda3d CompassEffect on them though, which doesn't have the benefits
        ###  or drawbacks of using a parent, because it just updates their position/rotation. 
        ###   - But compass effect with positions have a strange culling error unless you give large/infinite
        ###     bounding volume to the main parent. Also, the compasseffect might still be some type of nodepath...
        ### SOLUTION BUG 1b:
        ### - We already swap the enemies to the acceptable target type for that combility for that frame. And we
        ###   And we already have to do this for every combility. So why not keep track of this, and swap
        ###   Back to their original parents after all combilities have finished? 
        
        
        ### POSSIBLE BUG 2:
        ### - If target types get parented to a combility Self.acceptable_bot_projectile_targets ,then 
        ###  the target types are stuck under that original combility. 
        ### SOLUTION BUG 2:
        ### - Whenever the Combility is about to do its own personal frame update
        ###   (on input/update), it gets the self.acceptable_bot_projectile_targets from when this combility was
        ###   first created, and it parents them under self.acceptable_bot_projectile_targets once again (20-30us)
        ####################################
        

'''
import lebowski
lebowski.enable() ## TODO - Lebowski.enable() should be totally unecessary to have to do
# lebowski.disable() # If desired



from print_tricks import pt

import inspect
import types
import math

from ursina import *

import combility_code
import mods


# from light_entities import *      ## TODO TURN BACK ON
# from linecast import linecast     ## TODO TURN BACK ON

## TODO - Basically remove both of these. Globals and target types should be dynamically
##       created and brought in per game, not just for energy game.
from target_types import EnergyBeing, EG_Object, Shield, AnimatingShieldPart, Character, Core
from eg_globals import EG_Globals


class Merged_Combilities(Entity):
    '''
    - Goal of this class is to merge the graphics, collision and logic between 
    multiple combilities so that we have less Entities, draw calls etc. 
    - Will have to merge the models, textures, shaders, and combility_code
    
    '''

class Combility(Entity):
    ########################################################################
    ### Class Variables
    ########################################################################
    
    stored_copied_entity = None             ## Stored for all Combilities to use
    stored_copied_entity_attributes = None  ## Stored for all Combilities to use
    fixed_updates_list = []
    
    ## Displays and cameras have a nickname that is either user-created, or auto-generated, 
    pip_regions = {}
    rtt_regions = {}
    cameras = {}
    
    ########################################################################
    ### initialization 
    ########################################################################
    
    def __init__(self, *args, name='', combility_code=None, **kwargs):
        super().__init__()
        # super().__init__(*args, **kwargs)
        
        self.name = name
        
        self.setup_defaults()
        
        self.setup_mod_lists()
        
        if combility_code is not None:
            self._add_combility_code_to_lists(combility_code)
        
        
    def setup_defaults(self):
        # self.mesh_creator = Mesh_Creator() ## TODO TURN BACK ON
        
        self.default_camera_fov = 90
        
        self.spawned_sub_entities = [] ## TODO Any entities dynamically created by a combility
        ## must be added to this list. Then they can be turned on/off by iterating through it during
        ## enable/disable. 
        self.fixed_updates_list = []
        
        self.hit_info = None    # TODO, all of these may be uneseccary
        self.eaat = None        # TODO, all of these may be uneseccary
        self.hate = None        # TODO, all of these may be uneseccary
        ## TODO - possibly remove self.hate, as we are doing double combilities now for
        ## any complex hit detection and reaction systems. 
        
        
    ########################################################################
    ### DEBUG 
    ########################################################################
    
    def generate_func_call_str(self, func, args, kwargs):
        args_str = ', '.join(repr(arg) for arg in args)
        kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
        all_args_str = ', '.join(filter(None, [args_str, kwargs_str]))
        original_location = f"{func.__module__}.{func.__qualname__}"
        current_location = f"{func.__self__.__class__.__module__}.{func.__self__.__class__.__name__}"
        return (f"\n{current_location} call:\n"
                f" {func.__name__}({all_args_str})\n"
                f"  ({original_location})\n"
                )
        
    def test_mods(self, combility):
        # Now, call perform_debug_mod_list for each list in Combility
        self.perform_debug_mod_list(combility.mods_prepare_list, "mods_prepare_list")
        self.perform_debug_mod_list(combility.mods_use_list, "mods_use_list")
        self.perform_debug_mod_list(combility.mods_update_list, "mods_update_list")
        self.perform_debug_mod_list(combility.mods_enable_list, "mods_enable_list")
        self.perform_debug_mod_list(combility.mods_disable_list, "mods_disable_list")
        self.perform_debug_mod_list(combility.mods_helper_functions_list, "mods_helper_functions_list")

        # Now, call perform_debug_mod_list for each list in Combility
        self.perform_debug_mod_list(combility.mods_prepare_list, "mods_prepare_list")
        self.perform_debug_mod_list(combility.mods_use_list, "mods_use_list")
        self.perform_debug_mod_list(combility.mods_update_list, "mods_update_list")
        self.perform_debug_mod_list(combility.mods_enable_list, "mods_enable_list")
        self.perform_debug_mod_list(combility.mods_disable_list, "mods_disable_list")
        self.perform_debug_mod_list(combility.mods_helper_functions_list, "mods_helper_functions_list")
        
    def perform_debug_mod_list(self, mod_list, list_name):
        print(f"\nTesting {list_name}...")
        for func, args, kwargs in mod_list:
            func_call_str = self.generate_func_call_str(func, args, kwargs)
            print(f"{func_call_str}")
            func(*args, **kwargs)

    def print_mod_lists(self):
        print("mods_prepare_list:", combility.mods_prepare_list)
        print("mods_use_list:", combility.mods_use_list)
        print("mods_update_list:", combility.mods_update_list)
        print("mods_enable_list:", combility.mods_enable_list)
        print("mods_disable_list:", combility.mods_disable_list)
        print("mods_helper_functions_list:", combility.mods_helper_functions_list)


    ########################################################################
    ### Cleanup
    ########################################################################
    
    def track_spawned_sub_entity(self, entity):
        self.spawned_sub_entities.append(entity)
    
    def reenable_spawned_sub_entities(self):
        for entity in self.spawned_sub_entities:
            entity.enable()
            # scene.entities.append(entity) ## TODO: Performance optimization to ensure that their 
            ## code stopped running. But might not be necessary on current ursina versions. 
    
    def disable_spawned_sub_entities(self):
        for entity in self.spawned_sub_entities:
            entity.disable()
            # scene.entities.remove(entity) ## TODO: Performance optimization to ensure that their 
            ## code stopped running. But might not be necessary on current ursina versions. 
    
    def create_fixed_update(self, func, wait=1, loop=True, started=True):
        fixed_update_name = f"fixed_update_{func.__name__}"
        
        if not hasattr(self, fixed_update_name):
            setattr(self, fixed_update_name, Sequence(
                Func(func), Wait(wait), loop=loop, started=started
            ))
            
            self.animations.append(getattr(self, fixed_update_name))
            
            self.fixed_updates_list.append(getattr(self, fixed_update_name))
    
    def reenable_all_fixed_updates(self):
        for fixed_update in self.fixed_updates_list:
            fixed_update.start()

    def reenable_fixed_update(self, func_name):
        fixed_update_name = f"fixed_update_{func_name}"
        fixed_update = getattr(self, fixed_update_name, None)
        if fixed_update:
            fixed_update.start()
    
    def disable_all_fixed_updates(self):
        for fixed_update in self.fixed_updates_list:
            fixed_update.kill()
    
    def disable_fixed_update(self, func_name):
        fixed_update_name = f"fixed_update_{func_name}"
        fixed_update = getattr(self, fixed_update_name, None)
        if fixed_update:
            fixed_update.kill()
    
    def remove_all_fixed_updates(self):
        for fixed_update in self.fixed_updates_list:
            fixed_update.kill()
            self.fixed_updates_list.remove(fixed_update)
            self.animations.remove(fixed_update)
            delattr(self, fixed_update)
    
    def remove_fixed_update(self, func_name):
        fixed_update_name = f"fixed_update_{func_name}"
        fixed_update = getattr(self, fixed_update_name, None)
        if fixed_update:
            fixed_update.kill()
            self.fixed_updates_list.remove(fixed_update)
            self.animations.remove(fixed_update)
            delattr(self, fixed_update_name)
    
    ########################################################################
    ### Perform Mod Functions 
    ########################################################################
    
    ##  Mod functions:
    def setup_mod_lists(self):
        self.mods_prepare_list = []
        self.mods_use_list = []
        self.mods_update_list = []
        self.mods_enable_list = []
        self.mods_disable_list = []
        self.mods_helper_functions_list = []
    
    def add_combility_code(self, combility_code, debug=False):
        '''
        - Add all of the mods codes to the various lists
        - Run all the perform_ functions from the perform lists
        
        '''
        self._add_combility_code_to_lists(combility_code, debug)
        
        self.perform_mods_list(self.mods_prepare_list)
    
    def _add_combility_code_to_lists(self, combility_code, debug):
        if debug: pt(combility_code)
        
        for mix_category, mod_mixes in combility_code.items():  # Iterate over key-value pairs
            if debug: pt(mix_category)  # This will print the category name
            
            for mod_mix in mod_mixes:  # Iterate over each mod_mix in the list of mod_mixes
                if debug: pt(mod_mix)  # This will print the current mod_mix list
                
                for mod in mod_mix:  # Iterate over the list of mod dictionaries within the current mod_mix
                    if debug: pt(mod)  # This will print the mod dictionary
                    self._process_mod(mod)  # Process each mod dictionary
    
    def _process_mod(self, mod):
        mod_class = mod['method']  # This gets the class
        args = mod.get('args', ())
        kwargs = mod.get('kwargs', {})
        
        # Define the order of method types and their corresponding lists
        method_order = ['prepare_', 'use_', 'update_', 'enable_', 'disable_']
        method_lists = {
            'prepare_': self.mods_prepare_list,
            'use_': self.mods_use_list,
            'update_': self.mods_update_list,
            'enable_': self.mods_enable_list,
            'disable_': self.mods_disable_list,
        }

        # Track if args and kwargs have been added
        args_kwargs_added = False

        # Iterate through each method type in order
        for prefix in method_order:
            for method_name in dir(mod_class):
                if method_name.startswith(prefix):
                    method = getattr(mod_class, method_name)
                    if inspect.isfunction(method):
                        bound_method = types.MethodType(method, self)
                        if not args_kwargs_added:
                            # Add with args and kwargs for the first matching method
                            method_lists[prefix].append((bound_method, args, kwargs))
                            args_kwargs_added = True
                        else:
                            # Subsequent methods get empty args and kwargs
                            method_lists[prefix].append((bound_method, (), {}))

        # If no method matched the prefixes, add to helper functions with original args and kwargs
        if not args_kwargs_added:
            for method_name in dir(mod_class):
                if not any(method_name.startswith(prefix) for prefix in method_order) and not method_name.startswith('__'):
                    method = getattr(mod_class, method_name)
                    if inspect.isfunction(method):
                        bound_method = types.MethodType(method, self)
                        self.mods_helper_functions_list.append((bound_method, args, kwargs))
                        break  # Add only the first non-prefix method as a helper function
    
    def perform_mods_list(self, mod_list, list_name='', debug=False):
        if debug:
            self.perform_debug_mod_list(mod_list, list_name)
        else:
            for func, args, kwargs in mod_list:
                func(*args, **kwargs)


    ########################################################################
    ### Entity Methods 
    ########################################################################
    
    def enable(self, debug=False):
        self.reenable_spawned_sub_entities()
        
        self.perform_mods_list(self.mods_enable_list, 'mods_enable_list', debug)
        
        # Check if fixed_updates have been created already
        if not hasattr(self, 'fixed_updates_created'):
            self.create_fixed_update(self.fixed_update_1, wait=1, loop=True, started=True)
            self.fixed_updates_created = True  # Set the flag to True after creating fixed updates
        
        self.reenable_all_fixed_updates()

    def disable(self, debug=False):
        self.perform_mods_list(self.mods_disable_list, 'mods_disable_list', debug)
        
        self.disable_spawned_sub_entities()
        
        self.disable_all_fixed_updates()

    def update(self, debug=False):
        self.perform_mods_list(self.mods_update_list, 'mods_update_list', debug)
        
        
        
if __name__ == "__main__":
    trajectory_mix = mods.create_trajectory_mix(
        mods.add(mods.mods_trajectories.Path_Shape, 20),
        mods.add(mods.mods_trajectories.Path_Curve, curve=5))
    
    effect_mix = mods.create_effects_mix(
        mods.add(mods.Mod_One_A, a='new kwarg for a'),
        mods.add(mods.Mod_One_B, 777),
        mods.add(mods.Mod_Two_A), 
        mods.add(mods.Mod_Two_B, 723, f='new kwarg for f'))
    
    effect_mix_2 = mods.create_effects_mix(
        mods.add(mods.Mod_One_A, a='mod one a in effect mix 2'))
    
    combility_code = combility_code.create(trajectory_mix, [effect_mix, effect_mix_2])
    pt(combility_code)
    
    combility = Combility()
    combility.add_combility_code(combility_code)
    
    

    combility.print_mod_lists()
    combility.test_mods(combility)
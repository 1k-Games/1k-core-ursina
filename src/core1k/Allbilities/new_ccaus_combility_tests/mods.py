import importlib
import inspect
import textwrap


import mods_effects
from mods_effects import *

from mods_trajectories import *
import mods_trajectories

effects_methods = {getattr(mods_effects, name) for name in dir(mods_effects) if callable(getattr(mods_effects, name))}
trajectory_methods = {getattr(mods_trajectories, name) for name in dir(mods_trajectories) if callable(getattr(mods_trajectories, name))}

def add(method, *args, **kwargs):
    return {'method': method, 'args': args, 'kwargs': kwargs}

def add_to_mix(mix, mod, *args, **kwargs):
    # If mod is a callable, create the mod dictionary here
    if callable(mod):
        mod = {'method': mod, 'args': args, 'kwargs': kwargs}
    
    method = mod['method']
    args = mod.get('args', ())
    kwargs = mod.get('kwargs', {})

    if not mix:
        mix.append(mod)
    else:
        is_trajectory_mix = mix[0]['method'] in trajectory_methods
        if is_trajectory_mix and method not in trajectory_methods:
            pt(f">> Warning: Only trajectory methods can be added to a trajectory mix. Not a {method}")
            return
        if not is_trajectory_mix and method in trajectory_methods:
            pt(f">> Warning: Trajectory methods ({method}) cannot be added to an effects mix.")
            return
        mix.append(mod)
    return mix

# Modify the create_effects_mix function to use the new add_to_mix function
def create_effects_mix(*effects):
    effects_mix = []
    for mod in effects:
        # Check if the mod is a trajectory method, which is not allowed in effects_mix
        if mod['method'] in trajectory_methods:
            pt(f">> Warning: Trajectory methods ({mod}) cannot be added to an effects mix.")
            continue
        add_to_mix(effects_mix, mod)
    return effects_mix

# Modify the create_trajectory_mix function to use the new add_to_mix function
def create_trajectory_mix(*mod_methods):
    trajectory_mix = []
    for mod in mod_methods:
        # Check if the mod is not a trajectory method, which is not allowed in trajectory_mix
        if mod['method'] not in trajectory_methods:
            pt(f">> Warning: Only trajectory methods can be added to a trajectory mix. Not a {mod}")
            continue
        add_to_mix(trajectory_mix, mod)

    # Ensure default methods are included if they were not passed
    default_method_names = ["Path_Range", "Path_Shape", "Path_Curve", "Target_Types"]
    default_methods = {getattr(mods_trajectories, name) for name in default_method_names}
    for default_method in default_methods:
        if all(default_method is not item['method'] for item in trajectory_mix):
            add_to_mix(trajectory_mix, add(default_method))

    return trajectory_mix

def remove_mod_from_mix(mix, *mods_to_remove):
    """
    Removes all mods with the given references from the mix.
    
    :param mix: The list of mods to remove from.
    :param mods_to_remove: The mod method references to remove.
    """
    # Use list comprehension to keep mods not in mods_to_remove
    mix[:] = [mod for mod in mix if mod['method'] not in mods_to_remove]
    
def print_mod_sources(*args):
    '''Takes any of these:
        - A single mod
        - Multiple mods like this: mod1, mod2, mod3 etc
        - a mod mix with one or more mods in it
        
        '''
    for arg in args:
        # If the argument is a dictionary and has a 'method' key, it's a single mod
        if isinstance(arg, dict) and 'method' in arg:
            _print_method_source(arg['method'])
        # If the argument is a list or tuple, iterate through it assuming it's a mod mix
        elif isinstance(arg, (list, tuple)):
            for item in arg:
                if isinstance(item, dict) and 'method' in item:
                    _print_method_source(item['method'])
        # If the argument is a callable, it's a direct method
        elif callable(arg):
            _print_method_source(arg)
        else:
            print(f"Unsupported type: {type(arg)}. Expected a mod dict, list of mods, or a callable.")

def _print_method_source(method):
    if callable(method):
        try:
            source_code = inspect.getsource(method)
            dedented_code = textwrap.dedent(source_code)
            print(f">> Source code for {method.__name__}:\n{dedented_code}\n")
        except TypeError:
            print(f"The source code for {method.__name__} could not be found.")
    else:
        print(f"Provided method is not callable: {method}")

def print_modified_mod_calls(mod_mix):
    for mod in mod_mix:
        modified_call = _generate_modified_call(mod)
        print(modified_call)

def _generate_modified_call(mod):
    if isinstance(mod, dict) and 'method' in mod:
        method = mod['method']
        args = mod.get('args', ())
        kwargs = mod.get('kwargs', {})
        
        if callable(method):
            args_str = ', '.join(repr(arg) for arg in args)
            kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args_str = ', '.join(filter(None, [args_str, kwargs_str]))
            return f"{method.__name__}({all_args_str})"
        else:
            return f"Provided method is not callable: {method}"
    else:
        return f"Provided mod is not in the expected format: {mod}"
    
if __name__ == "__main__":
    import mods
    
        
    def tests_create_effects():

        
        # Create initial effect mixes
        effect_mix_1 = mods.create_effects_mix(
            mods.add(Mod_One_A),
            mods.add(Mod_One_A, a='new kwarg for a'),
            mods.add(Mod_Two_B, 723, f='new kwarg for f')
        )
        pt(effect_mix_1)
        
        # test against adding wrong trajectory mod to effects:
        effect_mix_2 = mods.create_effects_mix(
            mods.add(mods_trajectories.Path_Range)
        )
        pt(effect_mix_2)
        
        # Add a mod to the existing list
        mods.add_to_mix(effect_mix_1, add(Mod_Two_B, 44.32, f=' added new mod, this is a new kwarg for f'))
        pt(effect_mix_1)
        
        ## Test against adding wrong trajectory mod to effects
        mods.add_to_mix(effect_mix_1, mods_trajectories.Path_Range)
        pt(effect_mix_1)
        
        ## Remove a mod from the list
        mods.remove_mod_from_mix(effect_mix_1, Mod_One_A) ## TODO Test this and add this back in
        pt(effect_mix_1)
        
    def tests_create_trajectory():
        # No methods passed
        trajectory_mix_1 = mods.create_trajectory_mix()
        pt(trajectory_mix_1)
        
        
        # 2 methods passed
        trajectory_mix_2 = mods.create_trajectory_mix(
            mods.add(mods_trajectories.Path_Shape, 10, 20),
            mods.add(mods_trajectories.Path_Curve, curvature=5)
        )
        pt(trajectory_mix_2)

        
        # 4 methods passed
        trajectory_mix_3 = create_trajectory_mix(
            mods.add(mods_trajectories.Path_Range),
            mods.add(mods_trajectories.Path_Shape, 10, 20),
            mods.add(mods_trajectories.Path_Curve, curvature=5), 
            mods.add(mods_trajectories.Target_Types, 'enemy')
        )
        pt(trajectory_mix_3)

        # adding wrong effects mod to trajectory
        trajectory_mix_4 = mods.create_trajectory_mix(
            mods.add(mods_trajectories.Path_Curve),
            mods.add(Mod_One_B)
        )
        pt(trajectory_mix_4)
        
        mods.add_to_mix(trajectory_mix_4, mods_trajectories.Path_Range)
        pt(trajectory_mix_4)
        
    def tests_print_sources():
        mods.print_mod_sources(Mod_One_A)
        pt.c('----------')
        mods.print_mod_sources(Mod_One_A, Mod_Two_A)
        pt.c('----------')
        
        effect_mix = mods.create_effects_mix(
            mods.add(Mod_One_A), 
            mods.add(Mod_One_B), 
            mods.add(Mod_Two_A))
        mods.print_mod_sources(effect_mix)
        
        pt.c('--------------')
        
    def tests_print_modified_mod_calls():
        effect_mix = mods.create_effects_mix(
            mods.add(Mod_One_A),
            mods.add(Mod_One_A, a='new kwarg for a'),
            mods.add(Mod_Two_B, 723, f='new kwarg for f'))
        print_modified_mod_calls(effect_mix)
        
    tests_create_effects()
    tests_create_trajectory()
    
    tests_print_sources()
    tests_print_modified_mod_calls()

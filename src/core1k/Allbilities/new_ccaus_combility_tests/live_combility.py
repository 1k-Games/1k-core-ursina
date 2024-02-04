from print_tricks import pt

import inspect
import types

import combility_code
import mods


class Combility:
    def __init__(self):
        self.mods_prepare_list = []
        self.mods_use_list = []
        self.mods_update_list = []
        self.mods_enable_list = []
        self.mods_disable_list = []
        self.mods_helper_functions_list = []

    # def add_combility_code(self, *mod_mixes):
    #     for mod_mix in mod_mixes:
    #         for mod in mod_mix:
    #             self._process_mod(mod)

    def add_combility_code(self, combility_code):
        pt(combility_code)
        for mix_category, mod_mixes in combility_code.items():  # Iterate over key-value pairs
            pt(mix_category)  # This will print the category name
            for mod_mix in mod_mixes:  # Iterate over each mod_mix in the list of mod_mixes
                pt(mod_mix)  # This will print the current mod_mix list
                for mod in mod_mix:  # Iterate over the list of mod dictionaries within the current mod_mix
                    pt(mod)  # This will print the mod dictionary
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
    
    
    def print_mod_lists():
        print("mods_prepare_list:", combility.mods_prepare_list)
        print("mods_use_list:", combility.mods_use_list)
        print("mods_update_list:", combility.mods_update_list)
        print("mods_enable_list:", combility.mods_enable_list)
        print("mods_disable_list:", combility.mods_disable_list)
        print("mods_helper_functions_list:", combility.mods_helper_functions_list)
        
    def test_mods(combility):
        print("\nTesting mods_prepare_list...")
        for func, args, kwargs in combility.mods_prepare_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)

        print("\nTesting mods_use_list...")
        for func, args, kwargs in combility.mods_use_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)

        print("\nTesting mods_update_list...")
        for func, args, kwargs in combility.mods_update_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)

        print("\nTesting mods_enable_list...")
        for func, args, kwargs in combility.mods_enable_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)

        print("\nTesting mods_disable_list...")
        for func, args, kwargs in combility.mods_disable_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)

        print("\nTesting mods_helper_functions_list...")
        for func, args, kwargs in combility.mods_helper_functions_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func(*args, **kwargs)
            
    print_mod_lists()
    test_mods(combility)
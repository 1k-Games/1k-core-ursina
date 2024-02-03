from print_tricks import pt

import inspect


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
        prepare_list = []
        use_list = []
        update_list = []
        enable_list = []
        disable_list = []
        helper_functions_list = []

        # Assuming 'mod' is a dictionary with the structure:
        # {"method": <class '...'>, "args": (...), "kwargs": {...}}
        mod_class = mod['method']  # This gets the class

        # Now, iterate through each method of the class
        for method_name in dir(mod_class):
            if method_name.startswith('__'):
                continue  # Skip magic methods
            method = getattr(mod_class, method_name)
            if inspect.isfunction(method):  # Check if the attribute is a method
                # Categorize the method based on its name
                if method_name.startswith('prepare_'):
                    prepare_list.append(method)
                elif method_name.startswith('use_'):
                    use_list.append(method)
                elif method_name.startswith('update_'):
                    update_list.append(method)
                elif method_name.startswith('enable_'):
                    enable_list.append(method)
                elif method_name.startswith('disable_'):
                    disable_list.append(method)
                else:
                    helper_functions_list.append(method)

        # Assuming you want to add these methods to the class lists
        self.mods_prepare_list.extend(prepare_list)
        self.mods_use_list.extend(use_list)
        self.mods_update_list.extend(update_list)
        self.mods_enable_list.extend(enable_list)
        self.mods_disable_list.extend(disable_list)
        self.mods_helper_functions_list.extend(helper_functions_list)


# Example usage
# if __name__ == "__main__":
#     prepare, update, enable, disable = _process_mod(mod_category_two)
#     print("Prepare methods:", prepare)
#     print("Update methods:", update)
#     print("Enable methods:", enable)
#     print("Disable methods:", disable)

# Usage
if __name__ == "__main__":
    trajectory_mix = mods.create_trajectory_mix(
        mods.add(mods.mods_trajectories.Path_Shape, 10, 20),
        mods.add(mods.mods_trajectories.Path_Curve, curvature=5))
    
    effect_mix = mods.create_effects_mix(
        mods.add(mods.Mod_One_A, a='new kwarg for a'),
        mods.add(mods.Mod_One_B),
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
        print("Testing mods_prepare_list...")
        for func in combility.mods_prepare_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mods_use_list...")
        for func in combility.mods_use_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mods_update_list...")
        for func in combility.mods_update_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mods_enable_list...")
        for func in combility.mods_enable_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mods_disable_list...")
        for func in combility.mods_disable_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mods_helper_functions_list...")
        for func in combility.mods_helper_functions_list:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()
            
    print_mod_lists()
    test_mods(combility)
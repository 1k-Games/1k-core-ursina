
from print_tricks import pt



import combility_code
import mods


class Combility:
    def __init__(self):
        self.mod_prepares = []
        self.mod_actions = []
        self.mod_updates = []
        self.mod_enables = []
        self.mod_disables = []
        self.mod_helpers = []

    def add_combility_code(self, *mod_mixes):
        for mod_mix in mod_mixes:
            for mod in mod_mix:
                self._process_mod(mod)

    def add_combility_code(self, combility_code):
        pt(combility_code)
        for mix_category in combility_code:
            pt(mix_category)
            for mod_mix in mix_category:
                pt(mod_mix)
                for mod in mod_mix:
                    pt(mod)
                    pt.ex()
                    self._process_mod(mod)
                
    def _process_mod(self, mod):
        mod_namespace = mod.__class__.__name__
        for func_name in dir(mod):
            if callable(getattr(mod, func_name)):
                if func_name.startswith('prepare'):
                    self.mod_prepares.append(getattr(mod, func_name))
                elif func_name.startswith('action'):
                    self.mod_actions.append(getattr(mod, func_name))
                elif func_name.startswith('update'):
                    self.mod_updates.append(getattr(mod, func_name))
                elif func_name.startswith('enable'):
                    self.mod_enables.append(getattr(mod, func_name))
                elif func_name.startswith('disable'):
                    self.mod_disables.append(getattr(mod, func_name))
                else:
                    self.mod_helpers.append(getattr(mod, func_name))

# Usage
if __name__ == "__main__":
    trajectory_mix = mods.create_trajectory_mix(
        mods.add(mods.mods_trajectories.Path_Shape, 10, 20),
        mods.add(mods.mods_trajectories.Path_Curve, curvature=5))
    
    effect_mix = mods.create_effects_mix(
        mods.add(mods.Mod_One_A, a='new kwarg for a'),
        mods.add(mods.Mod_Two_B, 723, f='new kwarg for f'))
    
    combility_code = combility_code.create(trajectory_mix, effect_mix)
    # pt(combility_code)
    
    combility = Combility()
    combility.add_combility_code(combility_code)
    
    
    def print_mod_lists():
        print("mod_prepares:", combility.mod_prepares)
        print("mod_actions:", combility.mod_actions)
        print("mod_updates:", combility.mod_updates)
        print("mod_enables:", combility.mod_enables)
        print("mod_disables:", combility.mod_disables)
        print("mod_helpers:", combility.mod_helpers)
        
    def test_mods(combility):
        print("Testing mod_prepares...")
        for func in combility.mod_prepares:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mod_actions...")
        for func in combility.mod_actions:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mod_updates...")
        for func in combility.mod_updates:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mod_enables...")
        for func in combility.mod_enables:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mod_disables...")
        for func in combility.mod_disables:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()

        print("Testing mod_helpers...")
        for func in combility.mod_helpers:
            print(f"Calling {func.__name__} from {func.__self__.__class__.__name__}")
            func()
            
    print_mod_lists()
    test_mods(combility)
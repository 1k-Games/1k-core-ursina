from print_tricks import pt

import mods


def create(trajectory_mixes=None, effects_mixes=None):
    """
    Adjusted to ensure the structure is always a dict of lists of lists,
    correctly handling different scenarios for input arguments.
    """
    # Function to ensure the argument is a list of lists
    def ensure_list_of_lists(arg):
        if arg is None:
            return []  # Correctly initialize as an empty list for no input
        elif isinstance(arg, list):
            if not arg or not isinstance(arg[0], list):
                return [arg]  # Wrap in another list if it's a single list or empty
            return arg  # Return as is if it's already a list of lists
        else:
            return [[arg]]  # Wrap non-list arguments in a list of lists

    # Apply the ensure_list_of_lists function to both sets of mixes
    trajectory_mixes = ensure_list_of_lists(trajectory_mixes)
    effects_mixes = ensure_list_of_lists(effects_mixes)

    # Check if the mixes are empty and add default mixes if necessary
    if not trajectory_mixes:
        trajectory_mixes = [mods.create_trajectory_mix()]  # Initialize with a default mix in a list of lists
    if not effects_mixes:
        effects_mixes = [mods.create_effects_mix(mods.add(mods.Mod_One_A))]  # Initialize with a default mix in a list of lists

    combility_code = {
        "trajectory_mixes": trajectory_mixes,
        "effects_mixes": effects_mixes
    }

    return combility_code


if __name__ == '__main__':
    new_blank_combility_code = create()
    pt(new_blank_combility_code)    
    pt(new_blank_combility_code['trajectory_mixes'])    
    pt(new_blank_combility_code['effects_mixes'])    
    
    
    
    trajectory_mix = mods.create_trajectory_mix(
        mods.add(mods.mods_trajectories.Path_Shape, 10, 20),
        mods.add(mods.mods_trajectories.Path_Curve, curvature=5))
    
    effect_mix = mods.create_effects_mix(
        mods.add(mods.Mod_One_A, a='new kwarg for a'),
        mods.add(mods.Mod_Two_B, 723, f='new kwarg for f'))


    
    new_combility_code = create(trajectory_mix, effect_mix)
    pt(new_combility_code)
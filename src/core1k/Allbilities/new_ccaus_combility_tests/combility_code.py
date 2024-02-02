from print_tricks import pt

import mods


def create(trajectory_mixes=None, effects_mixes=None):
    """
    Creates a combility which is a dictionary containing keys "trajectory_mixes" and "effects_mixes".
    Each key maps to a list of respective mixes. Ensures that the provided trajectory_mixes and effects_mixes are not empty.
    
    :param trajectory_mixes: A list of trajectory mix lists.
    :param effects_mixes: A list of effects mix lists.
    :return: A dictionary with keys "trajectory_mixes" and "effects_mixes" mapping to their respective lists.
    """
    if not trajectory_mixes or not any(trajectory_mixes):
        pt(f">>Warning: At least one trajectory mix is required. Adding a default Trajectory mix of mods")
        trajectory_mixes = [mods.create_trajectory_mix()]
        
    if not effects_mixes or not any(effects_mixes):
        pt(">>Warning: At least one effects mix is required. Adding an effects mod mix")
        effects_mixes = [mods.create_effects_mix(mods.add_mod(mods.Mod_One_A))]
        
    combility = {
        "trajectory_mixes": [mix for mix in trajectory_mixes if mix],  # Ensure the trajectory mixes are not empty
        "effects_mixes": [mix for mix in effects_mixes if mix]  # Ensure the effects mixes are not empty
    }
    
    return combility


if __name__ == '__main__':
    new_blank_combility = create()
    pt(new_blank_combility)    
    
    
    
    trajectory_mix = mods.create_trajectory_mix(
        mods.add_mod(mods.mods_trajectories.Path_Shape, 10, 20),
        mods.add_mod(mods.mods_trajectories.Path_Curve, curvature=5))
    
    effect_mix = mods.create_effects_mix(
        mods.add_mod(mods.Mod_One_A, a='new kwarg for a'),
        mods.add_mod(mods.Mod_Two_B, 723, f='new kwarg for f'))
            
    new_combility = create(trajectory_mix, effect_mix)
    pt(new_combility)
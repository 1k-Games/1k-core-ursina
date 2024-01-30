from print_tricks import pt
from ursina import *

class Mod:
    def __init__(self, name, energy_drain):
        self.name = name
        self.energy_drain = energy_drain

class MiscMods(Mod):
    def damage(self, damage=1):
        return damage

class EnergyForceMovementsMod(Mod):
    def __init__(self, name, energy_drain, force):
        super().__init__(name, energy_drain)
        self.force = force

    def push(self, energy_drain):
        self.energy_drain = energy_drain
        return self

    def pull(self, energy_drain):
        self.energy_drain = energy_drain
        return self

        
class Formations:
    class FormationMod(Mod):
        ...
    class Rod(FormationMod):
        def __init__(self, name, shape):
            super().__init__(name)
            self.shape = shape
            
    class Ball(FormationMod):
        def __init__(self, name, shape):
            super().__init__(name)
            self.shape = shape
            
    class Beam(FormationMod):
        def __init__(self, name, energy_drain, shape):
            super().__init__(name, energy_drain)
            self.shape = shape
            
        def cylinder(self):
            pass
        
        def cube(self):
            pass
        
        def cone(self):
            pass
        
        def reversed_cone(self):
            pass

class TargetsMod(Mod):
    def __init__(self, name, energy_drain, targets):
        super().__init__(name, energy_drain)
        self.targets = targets

    def all_targets(self):
        ...
    
    def enemy(self):
        ...
    
    def teammate(self):
        ...

class Combility:
    def __init__(self, mods):
        self.mods = mods
        
class CombilityBuilder:
    def __init__(self):
        self.mods = []
        self.mod_types = set()
        self.single_use_mod_types = {Formations.FormationMod, } ## TODO: Add more when i become aware of ones that can't be doubled 
        
    def add_mod(self, mod):
        mod_type = type(mod)
        if mod_type in self.single_use_mod_types and mod_type in self.mod_types:
            raise ValueError(f"A mod of type {mod_type.__name__} has already been added.")
        self.mods.append(mod)
        self.mod_types.add(mod_type)
        return self
    
    ## NOTE: Only to be used by Devs for testing, or for constructing Combilities through scripts. 
        ## User-created combilities will use add_mods instead to let them know if the mod they are 
        ## trying to insert can't be (like repeating the damage types). 
    def _add_mods(self, *mods):
        for mod in mods:
            mod_type = type(mod)
            if mod_type in self.single_use_mod_types and mod_type in self.mod_types:
                raise ValueError(f"A mod of type {mod_type.__name__} has already been added.")
            self.mods.append(mod)
            self.mod_types.add(mod_type)
        return self
    
    def build(self):
        return Combility(self.mods)
    
if __name__ == '__main__':
    app = Ursina(size=(1920,1080))

    class BuildCombility:
        '''This class is simply for organizing this testing area'''

        misc_mod = MiscMods("misc_mod", 10)
        misc_mod.damage(5)

        energy_force_movement_mod = EnergyForceMovementsMod("energy_force_movement_mod", 20, 5)
        energy_force_movement_mod.push(10)

        beam_formation_mod = Formations.Beam("beam_formation_mod", 10, "cube")

        targets_mod = TargetsMod("targets_mod", 40, ["target1", "target2"])
        targets_mod.all_targets()

        builder = CombilityBuilder()

        builder._add_mods(misc_mod, energy_force_movement_mod, beam_formation_mod, targets_mod)

        combility = builder.build()
        pt(combility)

    import testing_range
    app.run()
    
'''   



















'''
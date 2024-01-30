from print_tricks import pt
from ursina import *

from eg_globals import EG_Globals


class CAUS(Entity):
    '''CAUS - Controlled Combility Actions Universal System'''
    def __init__(self, slot=None, **kwargs):
        super().__init__(**kwargs)        
        self.control_multiple_simultaneous_combilities = False
        self.cur_combilities = []
        self.slot=None
        
    def action_mapping(self, pressure_level):
        '''Trigger system per combility'''
        if pressure_level > 0:
            for combility in self.cur_combilities:
                combility.shoot()
                
    def update_combilities_list(self, combilities):
        self.cur_combilities = combilities if isinstance(combilities, list) else [combilities]
        
    def attach_new_combility(self, combility):
        self.cur_combilities.append(combility)
        
        original_scale = combility.world_scale
        
        combility.parent = self
        
        combility.world_scale = original_scale

        ########
        combility.caus_device = self
        
        if self.slot:
            combility.slot_owner = self.slot_owner
            combility.slot_owners_arm = self.slot_owners_arm
            combility.slot = self.slot
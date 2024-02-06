from print_tricks import pt

from ursina import *

from target_types import EG_Object

class CCAUS(EG_Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ccaus_barrel_end = Entity(name='barrel_end', parent=self, world_scale=(1,1,1), position=(0, 0, self.scale_z * 0.5))
        self.ccaus_barrel_end_visual = duplicate(self.ccaus_barrel_end, name='barrel_end_visual', world_scale=.05, model='sphere', color=color.white)

        self.model = 'cube'
        self.color = color.blue
        self.world_scale = (.1, .1, 1)
        
        
        ## Debug
        self.combility_forward_visual = Entity(name='combility_forward_visual', parent=self, position=self.forward*5, model='sphere', scale=(.5,.5,2))


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

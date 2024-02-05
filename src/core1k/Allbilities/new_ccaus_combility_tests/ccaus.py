from print_tricks import pt

from ursina import *

from target_types import EG_Object

class CCAUS(EG_Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ccaus_barrel_end = Entity(name='barrel_end', parent=self, world_scale=(1,1,1), position=(0, 0, self.scale_z * 0.5))
        self.ccaus_barrel_end_visual = duplicate(self.ccaus_barrel_end, name='barrel_end_visual', world_scale=.05, model='sphere', color=color.white)
                
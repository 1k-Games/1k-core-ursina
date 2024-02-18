from print_tricks import pt
pt.easy_imports('main.py')

from engine.aura.aura import Aura

'''
    These can be either:
    - Aura's directly, that then use CCAUSE devices (that are a sub-type of Aura), or
    - CCAUS Devices (subtype of Aura)
    '''
pt.c('placeable_turrets.py')


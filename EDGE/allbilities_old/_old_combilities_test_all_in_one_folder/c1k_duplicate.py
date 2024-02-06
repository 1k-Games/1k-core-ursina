from print_tricks import pt

from ursina import Entity, Audio
from copy import copy

# from target_types import EnergyBeing, Shield

def duplicate(entity, copy_children=True, parent=None, *args, **kwargs): # use a for loop instead of duplicate() if you can.
    if entity.__class__ == Entity:
        pt.c('if')
        e = entity.__class__(entity.add_to_scene_entities, *args, **kwargs)
    # elif entity.__class__ == Shield:
        # pt.c('elif')
        # e = entity.__class__(entity.color, *args, **kwargs)
    else:
        pt.c('else')
        e = entity.__class__(*args, **kwargs)
    
    e.parent = entity.parent if parent == None else parent
    pt(e.parent)
    
    if hasattr(entity, 'model') and entity.model:
        e.model = copy(entity.model)


    for name in entity.attributes:
        if name == 'model':
            continue
        elif name == 'collider' and entity.collider and entity.collider.name:
            # TODO: currently only copies colliders set with strings, not custom colliders.
            e.collider = entity.collider.name

        elif name == 'scripts':
            for script in entity.scripts:
                e.add_script(copy(script))

        else:
            if hasattr(entity, name):
                setattr(e, name, getattr(entity, name))

    for c in entity.children:
        clone = duplicate(c, copy_children=True, parent=e)
        clone.world_parent = e

    if isinstance(e, Audio):
        e.volume = entity.volume
        e.pitch = entity.pitch
        e.balance = entity.balance
        e.loop = entity.loop
        e.loops = entity.loops
        e.autoplay = entity.autoplay

        e.clip = entity.clip


    if hasattr(entity, 'text'):
        e.text = entity.text


    for key, value in kwargs.items():
        setattr(e, key ,value)

    return e


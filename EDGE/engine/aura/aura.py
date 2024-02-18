from ursina import *
from print_tricks import pt

class Aura:
    def __init__(self, 
                    entity: Entity = None,
                    position: Vec3 = None,
                    kvt_pos: [] = None,
                    **kwargs):
        
        self.entity = entity
        self.position = position
        self.kvt_pos = kvt_pos
        self.kwargs = kwargs
        self.lod_entities = []  # List to manage LOD entities

    def lod_manager(self):
        ...

    def calculate_distance(self, position1, position2):
        """
        Calculate the distance between two positions.
        """
        return (position1 - position2).length()

    def reenable_entity(self, entity):
        """
        Wake an entity (e.g., make it active/render it).
        """
        # Implementation depends on how entities are defined to be "awake"
        pass

    def disable_entity(self, entity):
        """
        Sleep an entity (e.g., make it inactive/hide it).
        """
        # Implementation depends on how entities are defined to be "asleep"
        pass

    def create_entity(self, **kwargs):
        """
        Create a new entity.
        """
        # Implementation depends on how entities are created in your system
        pass

    def destroy_entity(self, entity):
        """
        Destroy an entity.
        """
        # Implementation depends on how entities are destroyed in your system
        pass

    def reassign_entity(self, entity, new_position):
        """
        Re-assign an entity to a new position.
        """
        # Implementation depends on how entities are reassigned in your system
        pass
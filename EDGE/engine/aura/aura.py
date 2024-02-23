from print_tricks import pt

from ursina import *
from panda3d.core import NodePath

class AuraManager:
    '''
    - MOVE THIS TO ITS OWN FILE (move out of aura.py)
    
    
    Multiple Aura managed locations:
        - I may want an Aura_Zone for each zone (sectioned off in distance to player,
        and coordinates around the player). 
        - So each AuraZone would need their own spatial hash grid dict, and own dict of 
        aura id's etc. Then AuraManager would hellp move aura's around between all of
        the various zones. 
        
    '''
    aura_count = 0
    
    def __init__(self) -> None:
        self.auras = {}
        
        ######################################################
        ## Collisions - Version: Simple Spatial Hash Grid 
        ######################################################
        self.active_spatial_hash_grid = {} ## positions of all of the dynamic aura's.
        self.stationary_spatial_has_grid = {} ## pos of all temporarily stationary aura's. 
    
    def get_aura(self, aura_id):
        return self.auras.get(aura_id)
    
    def add_aura(self, aura_id, aura):
        self.auras.set(aura_id, aura)
        
    def set_aura_position(self, aura_id, position):
        self.aura_positions[aura_id] = position
    

aura_manager = AuraManager()

class Aura:
    '''
    The being/object/model/part/player/enemy Lives for the entirety of the game. 
    I can support at least 1 million of these, if they don't have active entities, 
    and have simplified nodepaths. Can possibly hold even more if the nodepaths are 
    removed as well (for very distant objects). 
    
    POSSIBLE TODO:
    __slots__: 
        - I may want to use them. Faster attribute access, less memory. 
        - However, no __dict__ or __weakref__ which... not sure what this would do
        
    Aura Names:
    - Necessary for development and debugging
    - Maybe should be removed for deployment to remove the memory of millions of strings
    that might not be used. 
    
        '''
    def __init__(self,
        name: str = '',
        aura_id: int = None,
        entity: Entity = None,
        nodepath: NodePath = None,
        position: Vec3 = None,
        kvt_pos: [] = None,
        **kwargs):
        
        self.name = name
        self.aura_id = aura_id
        self.entity = entity
        self.nodepath = nodepath
        
        self.position = position
        self.kvt_pos = kvt_pos
        self.kwargs = kwargs
        self.lod_entities = []  # List to manage LOD entities
        
        
        self.aura_id = aura_manager.aura_count + 1
        pt(f'{self.name} - {self.aura_id}')
        if self.name is '':
            pt(f'-------------WARNING: Aura ID# {self.aura_id} has no name. It is best to have one for debugging purposes')


    ######################################################
    ## VISUALS - COLLISION - MANAGEMENT
    ######################################################
    def set_visual(self):
        '''
            Where we assign this as a:
            - Non-visible (rare)
            
            - a color within another mesh vertice point.
                - So the "parent" point has a billboard, where one of the pixels is this aura. 
            
            - a picture within another mesh vertice point picture/billboard:
                - The "parent" billboard has a smaller image of this aura, next to other aura's. 
                
            - a billboard
            
            - a nodepath
                - various LOD models
            
            - An entity
                - various LOD models
            
            '''
        
    def lod_manager(self):
        ...

    ######################################################
    ## NODEPATH Life Cycle
    ######################################################
    def create_nodepath_from_data(self, data=None, **kwargs):
        """
        Create a new NodePath.
        """
        self.nodepath = NodePath('new_node')
        self.nodepath.setPos(self.position.x, self.position.y, self.position.z)
        # Assuming kvt_pos is a custom attribute, you might need to store it differently for NodePaths.
        # NodePath does not have a direct equivalent of 'kwargs' like Ursina's Entity.

    def add_nodepath(self, nodepath):
        self.nodepath = nodepath
        self.nodepath.setPos(self.position.x, self.position.y, self.position.z)
        # Handle kvt_pos and other kwargs if necessary

    def reenable_nodepath(self, nodepath):
        """
        Wake a NodePath (Make it active/render/enable because was previously disabled).
        """
        if self.nodepath:
            self.nodepath.setPos(self.position.x, self.position.y, self.position.z)
            self.nodepath.show()  # Assuming the nodepath was hidden to disable it

    def disable_nodepath(self, nodepath):
        """
        Sleep a NodePath (e.g., make it inactive it/hide it/disable it).
        """
        if self.nodepath:
            self.nodepath.hide()

    def destroy_nodepath(self, nodepath):
        """
        Destroy a NodePath.
        """
        if self.nodepath:
            self.nodepath.removeNode()

    ######################################################
    ## Entity Life Cycle
    ######################################################
    def create_entity_from_data(self, data=None, **kwargs):
        """
        Create a new entity.
        """
        
        self.entity = Entity()
        self.entity.position = self.position
        self.entity.kvt_pos = self.kvt_pos
        self.entity.kwargs = self.kwargs

    def add_entity(self, entity):
        self.entity = entity
        self.entity.position = self.position
        self.entity.kvt_pos = self.kvt_pos
        
    def reenable_entity(self, entity):
        """
        Wake an entity (Make it active/render/enable because was previously disabled).
        """
        if self.entity:
            self.entity.position = self.position
            self.entity.kvt_pos = self.kvt_pos
            self.entity.enable()

    def disable_entity(self, entity):
        """
        Sleep an entity (e.g., make it inactive it/hide it/disable it).
        """
        if self.entity:
            self.entity.disable()

    def destroy_entity(self, entity):
        """
        Destroy an entity.
        """
        if self.entity:
            destroy(self.entity)


'''
Composure Strat:
    - Start with a builder strategy or composition or my own thing to set up all of the structure,
    - Then the built combility is actually a function composition that has it's variables set, 
    and then runs the added *functions code one after the other. 
    
    
For builder/composition/composure:
    - I need no if statements to see if a type of mod exists. There is an automatic, default, build that covers
    all aspects of a combility. So set the defaults, and unless another mod changes those defaults, we proceed on. 
    
    Defaults:
    - pulsed
    - beam
    - laser
    - no element
    - damage
    - 50 range
    - 100 speed
    - straight line (no curve)
    
Build for the function composition: 
    - The initializations of every mod that will run in the init. 
    - The enable that will run. 
    - The disable that will run. 
    - The updates that will run. 
        - For Optimization Later on, separate the updates that happen with and without hitting a target
            - Updates for if projectile hit target and separate updates to run if not. 
            
'''
from print_tricks import pt 
from ursina import *
from functools import partial


def create_composed_function(*functions):
    def composed_function():
        for f in functions:
            f()
    return composed_function
        
class Combility(Entity):
    def __init__(self, 
        mod_instance=None,
        compiled_init=None, 
        compiled_update=None,
        compiled_action=None, 
        compiled_on_enable=None,
        compiled_on_disable=None,
        name='',
        **kwargs):
        super().__init__(**kwargs)
        self.compiled_init       = compiled_init
        self.compiled_update     = compiled_update
        self.compiled_action     = compiled_action
        self.compiled_on_enable  = compiled_on_enable
        self.compiled_on_disable = compiled_on_disable
        
        # Add methods from the Mod instance to this Combility instance
        if mod_instance is not None:
            for method_name in ['push', 'damage']:
                method = getattr(mod_instance, method_name)
                if callable(method):
                    setattr(self, method_name, method)
        
        # Add attributes from the Mod instance to this Combility instance
        if mod_instance is not None:
            self.__dict__.update(mod_instance.__dict__)
            
        
        self.acceptable_targets = Entity() ## plural name, singular entity. But it represents all of its children
        ###NOTE: ^^^^^^^^^^^^^^^^^^^^^ This is an optimizatin that WILL more than likely CAUSE A BUG in the future. 
        ### - We set the parent all of the entities that can be hit by this combility to self.acceptable_targets. 
        ### - We pass self.acceptable_targets into the traverse target. 
        ### - Likely BUG: This isn't a real-time updated parent of those entities. They would have to be added 
        ###   again which might take some more time than multiple raycasts or multiple checks of some sort. 
        ### - How to solve the possible BUG: Always update any new entities to the appropriate parent of 
        ###   "enemies, teammates, objects, shields, etc" when they are created. 
        ### -  TODO - What I wrote above is at least somewhat inaccurate now that I am not parenting entities to 
        ###     self.acceptable_targets but instead parenting the entities parent. Which is much more simple and 
        ###     will likely be more manageable. 
        
        self.create_acceptable_targets()
        
    def create_acceptable_targets(self):
        for target in self.target_types:
            target.parent = self.acceptable_targets
            pt(target, target.parent)
            
    def cast_ray(self):
        print('--- cast ray ---')
        hit_info = raycast(self.barrel.world_position, self.barrel.forward, 
            distance=self.ray_dist, 
            traverse_target=self.acceptable_targets,
            ignore=[self.barrel],
            debug=True)
        
        if hit_info.hit:
            
            pt(hit_info.entity.name)
            self.hit_info = hit_info
            self.hit_ent = hit_info.entity
            # if isinstance()
            self.perform_action()
            
    def update(self):
        if self.compiled_update:
            self.compiled_update()
        
    def input(self, key):
        ...
        # self.compiled_action()
    
    def perform_action(self):
        self.compiled_action()
    # def on_enable(self):
    #     self.compiled_enable()
        
    # def on_disable(self):
    #     self.compiled_disable()

class Mod(Entity):
    def __init__(self, barrel=None, target_types=None, ray_dist=50):
        super().__init__()
        self.name = ''
        self.hit_ent = None
        self.hit_info = None
        self.barrel = barrel
        self.barrel_w_pos = barrel.world_position
        self.target_types = target_types
        self.ray_dist = ray_dist

    def push(self):
        self.hit_ent.animate_position(self.hit_ent.world_position + self.barrel.forward *66, duration=.15)
    
    def damage(self, damage):
        self.hit_ent.take_damage(damage, self.hit_info.world_point, self.hit_info.world_normal)
    
    def set_target_types(self, target_types):
        self.target_types = target_types
    
    def max_distance(self, max_distance):
        self.ray_dist = max_distance
        
class CombilityController(Entity):
    possible_target_types = {'enemies', 'teammates', 'objects'}
    def __init__(self, barrel, ray_dist=100, target_types={}):
        super().__init__()
        self.barrel = barrel
        self.barrel_w_pos = barrel.world_position
        self.ray_dist = ray_dist
        self.hit_ent = None
        self.hit_info = None
        self.target_types = target_types
        
        self.acceptable_targets = Entity() ## plural name, singular entity. But it represents all of its children
        ###NOTE: ^^^^^^^^^^^^^^^^^^^^^ This is an optimizatin that WILL more than likely CAUSE A BUG in the future. 
        ### - We set the parent all of the entities that can be hit by this combility to self.acceptable_targets. 
        ### - We pass self.acceptable_targets into the traverse target. 
        ### - Likely BUG: This isn't a real-time updated parent of those entities. They would have to be added 
        ###   again which might take some more time than multiple raycasts or multiple checks of some sort. 
        ### - How to solve the possible BUG: Always update any new entities to the appropriate parent of 
        ###   "enemies, teammates, objects, shields, etc" when they are created. 
        ### -  TODO - What I wrote above is at least somewhat inaccurate now that I am not parenting entities to 
        ###     self.acceptable_targets but instead parenting the entities parent. Which is much more simple and 
        ###     will likely be more manageable. 
        
        self.create_acceptable_targets()
        
    def create_acceptable_targets(self):
        for target in self.target_types:
            target.parent = self.acceptable_targets
            pt(target, target.parent)
            
    def cast_ray(self):
        print('--- cast ray ---')
        hit_info = raycast(self.barrel.world_position, self.barrel.forward, 
            distance=self.ray_dist, 
            traverse_target=self.acceptable_targets,
            ignore=[self.barrel],
            debug=True)
        
        if hit_info.hit:
            
            pt(hit_info.entity.name)
            self.hit_info = hit_info
            self.hit_ent = hit_info.entity
            # if isinstance()
            self.perform_action()

    def perform_action(self):
        Mod(barrel=self.barrel, hit_ent=self.hit_ent, hit_info=self.hit_info).push()

    def input(self, key):
        if key == 'left mouse down':
            self.cast_ray()
        
    def update(self):
        ...
        # if held_keys['right mouse']:
        #     self.cast_ray()

class CombilityController2(Entity):
    possible_target_types = {'enemies', 'teammates', 'objects'}
    def __init__(self, combility, barrel, ray_dist=100):
        super().__init__()
        self.combility = combility
        self.barrel = barrel
        
        self.hit_ent = None
        self.hit_info = None
        
    # def perform_action(self):
    #     Mod(barrel=self.barrel, hit_ent=self.hit_ent, hit_info=self.hit_info).push()
    
    def input(self, key):
        if key == 'left mouse down':
            self.combility.cast_ray()
        
    def update(self):
        ...
        # if held_keys['right mouse']:
        #     self.cast_ray()





app=Ursina(size=(1920,1080))
import testing_range

barrel = testing_range.BuildLevel.barrel
barrel_start_pos = barrel.world_position
enemies = testing_range.BuildLevel.enemies

mod_instance = Mod(barrel=barrel, target_types={enemies}, ray_dist=33)
bullet_shredder = Combility(name='bullet_shredder',
    mod_instance        = mod_instance,
    compiled_action       = create_composed_function(
        partial(mod_instance.push), 
        partial(mod_instance.damage, 1111), 
        # speed_action
        ),
    
#     compiled_update      = create_composed_function([push_update, dmg_update, range_update, speed_update]),
#     compiled_on_enable   = create_composed_function([push_on_enable, dmg_on_enable, range_on_enable, speed_on_enable]),
#     compiled_on_disable  = create_composed_function([push_on_disable, dmg_on_disable, range_on_disable, speed_on_disable]),
)

# co = CombilityController(barrel=barrel, target_types={testing_range.BuildLevel.enemies})
co2 = CombilityController2(combility=bullet_shredder, barrel=barrel)

def input(key):
    if key == '1':
        barrel.world_position = barrel_start_pos
        
app.run()

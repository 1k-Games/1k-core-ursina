

from print_tricks import pt

from direct.actor.Actor import Actor
from panda3d.core import BillboardEffect

from ursina import * 
from ursina.shaders.normals_shader import normals_shader
from ursina.shaders.matcap_shader import matcap_shader
from ursina.shaders.unlit_shader import unlit_shader

from eg_globals import EG_Globals
from temp_core1k.c1k_duplicate import duplicate as c1k_duplicate


class Shared_Mixins:

    def _experimental_recieve_animation_points(self, direction_vec, duration, curve_points):
        self.curve_points = curve_points
        self.duration = duration  # store the total duration
        self.current_point_index = 0

        # Start the animation task
        self.animate_along_curve()

    def _experimental_animate_along_curve(self):
        seq = Sequence()

        # Calculate the time for each segment based on the total duration and the number of segments
        segment_time = self.duration / (len(self.curve_points) - 1)

        for i in range(len(self.curve_points) - 1):
            start = Vec3(self.curve_points[i])
            end = Vec3(self.curve_points[i + 1])

            seq.append(Func(self.update_position, start, end))
            seq.append(Wait(segment_time))

        seq.start()
        
    def _experimental_update_position(self, start, end):
        self.world_position = lerp(start, end, 1)
    
    def recieve_impulse(self, direction_vec, energy_amount, duration, curve):
        # pt(direction_vec)
        self.animate('world_position',
            self.world_position + direction_vec * energy_amount, 
            duration=duration,
            curve=curve)
    
    def recieve_dash(self, duration, curve_points):
        self.curve_points = curve_points
        self.duration = duration  # store the total duration

        self.animate_along_curve()

    def animate_along_curve(self):
        seq = Sequence()

        # Calculate the time for each segment based on the total duration and the number of segments
        segment_time = self.duration / (len(self.curve_points) - 1)

        for i in range(len(self.curve_points) - 1):
            start = Vec3(self.curve_points[i])
            end = Vec3(self.curve_points[i + 1])

            seq.append(Func(self.update_position, start, end))
            seq.append(Wait(segment_time))

        seq.start()
        
    def update_position(self, start, end):
        self.world_position = lerp(start, end, 1)
        
    def assign_targets(self, specific_target):
        targets = []
        if isinstance(self, EG_Object):
            targets.append(self)
        else:
            if specific_target == 'energy_being':
                targets.extend([self.character, self.shield])
            elif specific_target == 'eb_shield':
                targets.append(self.shield)
            elif specific_target == 'eb_body':
                targets.append(self.character)
        return targets
    
    def recieve_camo(self, specific_target, texture=None, texture_scale=None, color=None, duration=1.0):
        targets = self.assign_targets(specific_target)
        self.originals_camo = {}
        for target in targets:
            target.texture = texture
            target.color = color
            target.texture_scale = texture_scale
            
        invoke(self.reset_camo, targets, delay=duration)
        
    def reset_camo(self, targets):
        for target in targets:
            target.texture = target.original_texture 
            target.texture_scale = target.original_texture_scale 
            target.color = target.original_color
            if isinstance(target, Shield):
                self.shield.update_shield_color()
        

    def recieve_mimic(self, specific_target, entity=None, duration=1.0):
        targets = self.assign_targets(specific_target)
        self.temp_entity = None
        
        largest_target = max(targets, key=lambda t: max(t.world_scale.x, t.world_scale.y, t.world_scale.z))
        
        for target in targets:
            
            ## Make the real entities invisible, so we can see the fake-created one
            target.color = color.Color(target.color.r, target.color.g, target.color.b, 0)
            ## Create a temporary entity that mimics the entity if the target is the largest
            if target is largest_target:
                temp_entity = c1k_duplicate(entity, copy_children=True)
                temp_entity.collision = False
                temp_entity.collider = None
                temp_entity.world_scale = Vec3(
                    min(entity.world_scale.x, target.world_scale.x),
                    min(entity.world_scale.y, target.world_scale.y),
                    min(entity.world_scale.z, target.world_scale.z)
                )
                temp_entity.world_position = target.world_position
                pt(temp_entity.world_scale, entity.world_scale.x, target.world_scale.x,
                    entity.world_scale.y, target.world_scale.y,
                    entity.world_scale.z, target.world_scale.z)
                self.temp_entity = temp_entity
                
            invoke(self.reset_mimic, targets, delay=duration)
        
    def reset_mimic(self, targets):
        if self.temp_entity:
            destroy(self.temp_entity)
            self.temp_entity = None
        for target in targets:            
            target.color = target.original_color
        
    def recieve_visibility(self, specific_target, alpha=None, duration=1.0):
        targets = self.assign_targets(specific_target)
        
        for target in targets:
            
            ## Make invisible
            target.color = color.Color(target.color.r, target.color.g, target.color.b, alpha)
            
        invoke(self.reset_visibility, targets, delay=duration)
        
    def reset_visibility(self, targets):
        for target in targets:
            target.color = target.original_color
            if isinstance(target, (Shield, EnergyBeing)):
                self.shield.update_shield_color()
                
    def change_attributes(self, specific_target, entity=None, mode=None, alpha=None, duration=1.0):
        targets = {}

        if isinstance(self, EG_Object):
            targets[specific_target] = (self,)
        else:
            targets = {
                'eb_body': (self.character,),
                'eb_shield': (self.shield,),
                'energy_being': (self.character, self.shield),
            }
        self.originals = {} 
        self.temp_entity = None

        largest_target = max(targets.get(specific_target, ()), key=lambda t: max(t.world_scale.x, t.world_scale.y, t.world_scale.z))
        for target in targets.get(specific_target, ()):
            self.originals[target] = {
                'model': target.model,
                'scale': target.scale,
                'rotation': target.world_rotation,
                'texture': target.texture,
                'texture_scale': target.texture_scale,
                'color': target.color,
                'alpha': target.color.a,
                'always_on_top': target.always_on_top,
            }

            if mode == 'mimic':
                # Make the target invisible
                target.color = color.Color(target.color.r, target.color.g, target.color.b, 0)

                # Create a temporary entity that mimics the entity if the target is the largest
                if target is largest_target:
                    temp_entity = duplicate(entity)
                    temp_entity.world_scale = Vec3(
                        min(entity.world_scale.x, target.world_scale.x),
                        min(entity.world_scale.y, target.world_scale.y),
                        min(entity.world_scale.z, target.world_scale.z)
                    )
                    temp_entity.world_position = target.world_position
                    self.temp_entity = temp_entity

            elif mode == 'camo':
                target.texture = entity.texture
                target.color = entity.color 
                target.texture_scale = entity.texture_scale

            elif mode == 'visibility':
                target.color = color.Color(target.color.r, target.color.g, target.color.b, alpha)

        invoke(self.reset_attributes, specific_target, mode=mode, delay=duration)
        
    def reset_attributes(self, specific_target, mode=None):
        targets = {}

        if isinstance(self, EG_Object):
            targets[specific_target] = (self,)
        else:
            targets = {
                'eb_body': (self.character,),
                'eb_shield': (self.shield,),
                'energy_being': (self.character, self.shield),
            }

        for target in targets.get(specific_target, ()):
            original = self.originals.get(target)

            if original:
                if mode == 'mimic':
                    # Delete the temporary entity
                    if self.temp_entity:
                        destroy(self.temp_entity)
                        self.temp_entity = None

                    # Restore the original alpha value
                    target.color = color.Color(target.color.r, target.color.g, target.color.b, original['alpha'])

                elif mode == 'camo':
                    target.model = original['model']
                    target.scale = original['scale']
                    target.world_rotation = original['rotation']
                    target.texture = original['texture']
                    target.texture_scale = original['texture_scale']
                    target.color = original['color']

                elif mode == 'visibility':
                    target.color = color.Color(target.color.r, target.color.g, target.color.b, original['alpha'])
                    if ('eb_shield' in specific_target or 'energy_being' in specific_target) and not isinstance(self, EG_Object):
                        self.shield.update_shield_color()

class AnimatingShieldPart(Entity):
    def __init__(self, shield_part_double_sided=True, **kwargs):
        super().__init__(**kwargs)
        self.energy_being = self.parent.parent.parent
        shared_model = 'sphere_center_tunnel_wide_slower2'
        # shared_model = 'sphere_center_tunnel_reset'
        # shared_model = 'sphere_center_tunnel_unwrap'
        # shared_model = 'sphere_center_tunnel_custom2'
        
        
        # shared_model = 'Sphere_ico_uv_cube'                   ## Prison Cell
        # shared_model = 'Sphere_ico_uv_cylinder_horizontal'    ## Spherical Pulses
        # shared_model = 'Sphere_ico_uv_cylinder_vertical'      ## Spherical Vortex
        # shared_model = 'Sphere_ico_uv_light_map_pack'         ## Animated Wrapping Paper
        # shared_model = 'Sphere_ico_uv_reset'                  ## Wallpaper pattern
        # shared_model = 'Sphere_ico_uv_smart_uv'               ## Speed Hamster Ball
        # shared_model = 'Sphere_ico_uv_sphere'                 ## Spherical Pulses 2
        # shared_model = 'Sphere_ico_uv_unwrap'                 ## Warping Reality (similar to wrapping paper, but much better)
        # shared_model = 'robot_simple'                 
        # shared_model = 'robot_military'                
        # shared_model = 'robot_humanoid'                
                
        self.model = shared_model
        # shield_part_double_sided = False
        EG_Globals.current_sets['shield_parts'].add(self)
        EG_Globals.add_to_appropriate_set(self, 'shield_part')
        
        
        size_factor = 1.05
        self.base_part_scale = self.energy_being.shield.world_scale * size_factor  
        
        self.world_scale = self.base_part_scale
        # pt(self.world_scale)
        
        self.texture='digit_rain_white_clear_strip'
        # self.texture='digit_david7'
        # self.texture='digit_david'
        self.color = self.energy_being.character.color
        
        # Tiriaq has always loved you. He still loves you. He wasn't himself when he was
        # mistreating you. 
        
        rotation=(0,0,0)
        # rotation=(0,0,180)
        # rotation=(0,0,33)
        part2_w_scale = self.base_part_scale * (1,1,1)
        # pt(part2_w_scale)
        self.part2 = Entity(name=f'{self.name} - animating_shield_part - part 2',
            parent=self,
            # model='sphere',
            # model = 'sphere_center_tunnel_wide',
            # model = 'sphere_center_tunnel_wide_slower',
            model = shared_model,
            color=self.color,
            texture=self.texture,
            world_scale=part2_w_scale,
            rotation=rotation,
            double_sided=shield_part_double_sided,
            shader=None,
            )
        
        EG_Globals.current_sets['shield_part2s'].add(self.part2)
        EG_Globals.add_to_appropriate_set(self, 'shield_part2')
        
        self.offset = 0
        self.offset2 = 0
        
        ########################################################
        # KEEP THESE EXPERIMENTS
        ########################################################
        # self.setBillboardPointEye(-10, fixed_depth=True)
        self.scales = [
            (1,1,1),
            (.85,1,85),
            (85,1,85),
            (85,1,.85),
            (1,85,1),
            (1,42,.42),
            (1,88,88),
            (3,42,.42),
            (4.2,26,26,2,5,.3,21,21),
            (4.2,26,26,2,5,.3,21,21,21,4.7),
            (7.3,17,17,6,8,8,12,15,15,18,15,15),
            Vec3(15.876, 98.28, 98.28),
            (2.5,2.5,2.5,8,8.9),
            (3,12,13),
            (1,.41,.42),
            (1.3,.60,.62),
            (1.7,1.2,1.4)
        ]
        self.current_scale_index = 0
        ############################

    def input(self, key, debug=False):
        # pt(self.name)
        if key == 'right arrow':
            self.current_scale_index = (self.current_scale_index + 1) % len(self.scales)
        elif key == 'left arrow':
            self.current_scale_index = (self.current_scale_index - 1) % len(self.scales)
        elif key == 'up arrow':
            self.setBillboardPointEye(-10, fixed_depth=True)
        elif key == 'down arrow':
            self.setBillboardPointEye(False)
            
        self.part2.world_scale = self.base_part_scale * self.scales[self.current_scale_index]
        
        if debug:
            pt(self.part2.world_scale, self.current_scale_index, self.scales[self.current_scale_index])
    
    def update(self):
        self.offset += time.dt * -0.3

        self.part2.texture_offset = (self.offset*0.1, self.offset)
        self.texture_offset = (self.offset*-0.1, self.offset*0.9)  
    
class Shield(Entity):
    # shader = None ## TODO POTENTIAL BUG
    # shader = normals_shader
    
    shield_update_timer = 0.05
    def __init__(self,
            max_health=1000, 
            recharge_per_cycle=7.5,
            shield_cycle_time=0.05,
            **kwargs):
        
        self.shield_cycle_time = shield_cycle_time
        super().__init__(
            shader=None,
            # shader=normals_shader, 
            **kwargs)
        
        self.energy_being = self.parent.parent.parent

        EG_Globals.current_sets['shields'].add(self)     
        EG_Globals.add_to_appropriate_set(self, 'shield')
        

        self.max_health = max_health
        self.shield_health = self.max_health
        # self.shield_health = self.energy_being.energy_level
        # pt(self.shield_health)
        
        self.recharge_per_cycle = recharge_per_cycle
        self.model = 'sphere'
        self.collider = 'sphere'
        # self.world_scale = self.energy_being.character.bounds.size * 3
        self.world_scale = self.core.world_scale * 12
        
        
        self.original_model = self.model
        self.original_world_scale = self.world_scale
        self.original_world_rotation = self.world_rotation
        self.original_texture = self.texture
        self.original_texture_scale = self.texture_scale
        self.original_color = EG_Globals.SHIELD_COLORS()[-1]
        self.original_alpha = self.alpha
        self.original_shader = self.shader
        self.original_always_on_top = self.always_on_top
        
        
        self.does_shield_belong_to_player = False if not self.parent.parent.parent.name == 'player' else True
        # pt(self.does_shield_belong_to_player, self.parent.parent.parent.name)
        # pt.ex()

        

        self.update_shield_color()
        

    def on_enable(self):
        ## Enable update()
        scene.entities.append(self)
        
        ## Enable function with a fixed update (similar to @every)
        self.animation_sequence = Sequence(
            Func(self.recharge_shield), Wait(self.shield_cycle_time), loop=True, started=True)
        self.animations.append(self.animation_sequence)

    def on_disable(self):
        scene.entities.remove(self)
        self.animation_sequence.kill()
    

    def recieve_damage(self, dmg_amount, hit_point, hit_normal):
        self.hit_point = hit_point
        self.hit_normal = hit_normal

        self.shield_health -= dmg_amount
        if self.shield_health <= 0:
            self.shield_health = 0
        self.update_shield_color()
        
        if self.does_shield_belong_to_player:
            self.parent.parent.parent.update_inner_colored_shield()            
    
    def drain_shield(self, drain_amount):
        '''When user uses energy, it drains the shield'''
        
        if self.shield_health >= 100:
            ## Shield is non-functional for last 99 energy user has, but it can still
            ## take damage (why the take damage doesn't have this check)
            self.shield_health -= drain_amount
    
    def update_shield_color(self):
        ''' 0(1) lookup time
            100 = the health per level
            10  = the number of levels
            '''
        # pt.c('update shield color')
        # normalized_health = self.shield_health / self.max_health

        index = min(self.shield_health // 100, 10)
        self.color = EG_Globals.SHIELD_COLORS()[int(index)]
        
    
    def recharge_shield(self):
        # pt.t('shield - ', self.energy_being.name)

        if self.shield_health < self.max_health:
            # pt(self.shield_health)
            self.shield_health += self.recharge_per_cycle
            if self.shield_health > self.max_health:
                self.shield_health = self.max_health
            self.update_shield_color()
            
    def __getattr__(self, name):
        """
        - When Shield is Struck:
            - Python first looks for the method name in Shield(). If not found, then it uses __getattr__ to look. 
            - So we are overriding the normal __getattr__ method in the class to redirect it to look
                in the energy_being class instead. 
        """
        if name == 'energy_being':
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'energy_being'")
        
        if hasattr(self.energy_being, name):
            return getattr(self.energy_being, name)
        else:
            raise AttributeError(f"Neither '{self.__class__.__name__}' nor '{self.energy_being.__class__.__name__}' object has attribute '{name}'")

class Core(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy_being = self.parent.parent
        
        EG_Globals.current_sets['cores'].add(self)
        EG_Globals.add_to_appropriate_set(self, 'core')
        
        self.model='sphere'
        self.collider='sphere'
        self.collision=False
        
        self.world_scale = (.3,.3,.3)
        
        ######################################
        ## (always_on_top=True)
        ## NOTE BUG: DO NOT SET THIS AGAIN. 
        ## unintended consequences with its parent and children not 
        ## rendering properly under certain conditions. Also, I really
        ## wouldn't ever want this. Because then, even if there was a building
        ## another character, or object in the way, you'd always see this. 
        ## It would be acceptable to pass "always_on_top" to some entity that
        ## was solo, or was parented to an entity that didn't change its size/shape/model
        ## self.always_on_top = False
        ######################################
        
    def recieve_impulse(self, *args, **kwargs):
        self.energy_being.recieve_impulse(*args, **kwargs)
        
    def remove_core(self):
        self.parent = scene
        
class Character(Entity):
    def __init__(self, character_model=None, character_scale=2.5, **kwargs):
        super().__init__(
            # shader=matcap_shader, 
            **kwargs)
        self.energy_being = self.parent
        self.color = self.energy_being.color
        
        EG_Globals.current_sets['characters'].add(self)
        EG_Globals.add_to_appropriate_set(self, 'character')
        

        
        if character_model:
            try: 
                self.actor = Actor(character_model)
                self.model.setScale(2.5,2.5,2.5)
                self.actor.reparentTo(self)
            except:
                self.model = character_model
                self.world_scale = character_scale
                # self.shader = matcap_shader
                # self.texture = 'shore'
                self.shader = matcap_shader
                self.texture = 'robot_humanoid'
        else:
            self.model = 'sphere'        
            self.world_scale = (1,2.5,1)
            self.shader = matcap_shader
            self.texture = 'shore'
        
        # pt(self.energy_being.name, character_scale, self.scale, self.world_scale)
        
        
        self.original_model = self.model
        self.original_world_scale = self.world_scale
        self.original_world_rotation = self.world_rotation
        self.original_texture = self.texture
        self.original_texture_scale = self.texture_scale
        self.original_color = self.color
        self.original_alpha = self.alpha
        self.original_shader = self.shader
        self.original_always_on_top = self.always_on_top
        
    def recieve_impulse(self, *args, **kwargs):
        self.energy_being.recieve_impulse(*args, **kwargs)
        
class EnergyBeing(Shared_Mixins, Entity):

    def __init__(self,
        character_model=None,
        character_scale=2.5,
        core_offset = Vec3(0, 0, 0),
        shield_part_double_sided=True,
        **kwargs):
        
        
        
        super().__init__(**kwargs)
        EG_Globals.current_sets['energy_beings'].add(self)
        # EG_Globals.add_to_appropriate_set(self, 'energy')
        
        # print('inside eb: ', self.name, self.parent, self.parent.name)
        self.energy_level = 1000

        self.character = Character(name=f'{self.name} - character',
            parent=self,
            character_model=character_model,
            character_scale=character_scale,
            # actor_model=fr'eg\allbilities\combilities\farmer.glb'
            )
        
        self.core = Core(name=f'{self.name} - core',
            parent=self.character,
            color=self.color,
            position=core_offset)
        
        relative_position = self.world_position - self.core.world_position
        self.shield = Shield(name=f'{self.name} - shield',
            parent=self.core,
            position=relative_position,
            rotation=(0,0,0),
            billboard=True)
        
        self.shield.texture='border_white_150_px_center'
        self.shield.texture='border_white_200_px_center'
        self.shield.texture_scale=(2, 1)

        
        self.animating_shield_part = AnimatingShieldPart(name=f'{self.name} - animating_shield_part',
            parent=self.core,
            shader=None,
            rotation=(-90,0,0),
            shield_part_double_sided=shield_part_double_sided,
            )
        
        
        self.player_health = 1
        self.base_player_health = self.player_health
        self.hit_point = None
        self.hit_normal = None


    def recieve_damage(self, dmg_amount, hit_point, hit_normal):
        self.hit_point = hit_point
        self.hit_normal = hit_normal
        self.take_player_health(dmg_amount)
        
    def take_player_health(self, dmg_amount):
        self.player_health -= dmg_amount
        if self.player_health <= 0:
            self.eb_die()
            
    def eb_die(self):
        self.animate_rotation(Vec3(90, self.world_rotation.y, self.world_rotation.z), duration=.3)

class EG_Object(Entity, Shared_Mixins):

    def __init__(self, *args, health=100, **kwargs):
        super().__init__(*args, **kwargs)
        EG_Globals.current_sets['local_objects'].add(self)
        
        self.original_model = self.model
        self.original_world_scale = self.world_scale
        self.original_world_rotation = self.world_rotation
        self.original_texture = self.texture
        self.original_texture_scale = self.texture_scale
        self.original_color = self.color
        self.original_alpha = self.alpha
        self.original_shader = self.shader
        self.original_always_on_top = self.always_on_top
        
        self.max_health = health 
        self.health = self.max_health
        
    def recieve_damage(self, dmg_amount, hit_point, hit_normal):
        self.hit_point = hit_point
        self.hit_normal = hit_normal
        self.remove_health(dmg_amount)
        
    def remove_health(self, dmg_amount):
        self.health -= dmg_amount
        if self.health <= 0:
            self.eb_die()
    
    def eb_die(self):
        self.rotation_x = 90
    
class Environment_Object(EG_Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        EG_Globals.current_sets['local_objects'].remove(self)
        EG_Globals.current_sets['environment_objects'].add(self)
    '''
    - Make all environment stuff out of this class. (walls, buildings, etc)
    - At least stuff without an energy shield.... 
    
    - Perhaps all items of EG_Object and Environment_Object do have a "visual" shield, but it does
    nothing? Actually, it'd still be good for it to do something for better collisions. 
    
    - But anyways, why can't my environments be manipulated like everything else can? With enough energy. 
        - Be blinked, teleported, pushed, TK'd, etc. 
        
    - I can still optimize environment stuff like I did in my Cheap_physics thing and combine stuff
    but then still keep track of their individual locations and re-implement colliders when you
    or your projectiles are close. 
    
    '''

class Enemy(EnergyBeing):
    def __init__(self, **kwargs):
        super().__init__(
            color=EG_Globals.ent_colors["enemies_color"],
            **kwargs)
        EG_Globals.current_sets['enemies'].add(self)

class Teammate(EnergyBeing):
    def __init__(self, **kwargs):
        super().__init__(
            color=EG_Globals.ent_colors['teammates_color'],
            # core_color=color.blue,
            **kwargs)
        EG_Globals.current_sets['teammates'].add(self)
        
class NPC(EnergyBeing):
    def __init__(self, **kwargs):
        super().__init__(
            color=EG_Globals.ent_colors['npcs_color'],
            # core_color=color.yellow,
            **kwargs)
        EG_Globals.current_sets['npcs'].add(self)

class Slot(Entity):
    ''' 
    - Slot must be able to pass on the owner of this slot to 
        the Combilities, so that each combility knows how to apply forces
        to the owner, and not just the combility itself. 
    - For example: 
        Hopping up in the air with your energy_being body via your combility
        set to "push" and EnergyBeing type is "self.owner" 
    - Changing owners:
        - Must change owners when an NPC that has a slot on it is placed
        onto another owner. 
            - Like when an arm gets placed onto a new energy_being. 
    - Owners can be:
        - energy_beings, drones, buildings, vehicles, walls, trash cans, etc
    
    '''
    def __init__(self, initial_owner, model=None, **kwargs):
        super().__init__(**kwargs)
        EG_Globals.current_sets['slots'].add(self)
        
        self.owner = initial_owner
        self.owners_arm = self.parent
        self.color = self.owner.color
        self.alpha = 0.6
        if model is None:
            self.model = Cone(resolution=12, height=2)
        else: 
            self.model = model
            
        
        ## NOTE: owners_arm and owner could be the same thing if this slot was attached to
        ##  a simple object without a grandparent. But otherwise, this distinction in here
        ## is likely necesary. Same with the distintion with the parent.
        
        
    def change_owner(self):
        ...
        
    def attach_caus_device(self, caus_device):
        self.caus_device = caus_device
        
        original_scale = self.caus_device.world_scale
        caus_device.parent = self
        caus_device.world_scale = original_scale
        
        self.caus_device.position = (0, self.scale_y * 0.55, 0)
        
        self.caus_device.slot_owner = self.owner 
        self.caus_device.slot_owners_arm = self.owners_arm
        self.caus_device.slot = self

        if self.caus_device.cur_combilities:
            for combility in self.caus_device.cur_combilities:
                combility.slot_owner = self.owner
            
'''
- TODO 
- Center circle of animating_shield stretched:
    - I'm currently using a texture_scale attribute to change it
    - But for calculating the actual size of the weak spot accurately,
    it'd be good to.... ?
    
    Potential visual &/or optimizaton for shields:
        - Real shield has gradient while also has an animating texture at samee time. 
            - Be aware that the shield stuff will be transparent though. 



- Getting shot: 
    - we could  temporarily change an inner shield part to face the direction hit and then set a scale & position that makes it look like the shield particles are moving behind the player temporarily. 


- Ice: 
    - One of the shaders of ursina has an effect remeniscient of ice forming from a sphere.

- Core graphics:
    - Core with Rod:
        - If we added a model that was a sphere with a very thin rod through it, 
        we could visually simulate with practically no cost, that the energy 
        shield particles that push out and suck in, are being generated from the
        inner core right there. It'll make the whole setup more expainable. 
        - If we did this: 
            - we could orient the core in the direction that the shield_part's should
            be facing (so instead of changing their direction, we change the cores?)
    - Other lit-up areas indiciating team color/npc etc. 
        - Light light orbs on shoulders, arms, or maybe just light shooting out from 
        limbs? 

- TK Anchor points (yeb):
    - If you are anchored to ground (standing or maybe grabbing?), then you have more
    weight, therefore you can lift things around you. 
    - If you are not anchored and the other person is heavier or achored, then you
    move yourself around them. 


- TODO Longterm todolongterm to do long term



'''
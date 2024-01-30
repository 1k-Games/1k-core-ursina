''' TODO:
    - Table should turn into a sphere/character model just like the other characters. 
        - I'd like the testing in the future to be your own character model that you see holding
        each combility and shooting it. So it's a cool 3rd/4th person perspective on yourself
        shooting the combility.
        
        pip install --no-deps --upgrade --no-cache-dir --force-reinstall git+https://github.com/1k-Games/1k-core-ursina.git@main

    '''

from print_tricks import pt

from ursina import *
from ursina.shaders.matcap_shader import matcap_shader

from core1k import *
from characters.target_types import *
from temp_core1k.eg_fps_rts_hybrid_controller import Player
from eg_globals import EG_Globals
class BuildLevel:
    def __init__(self):
        # self.cam = BuildLevel.Cam()
        
        self.initial_transforms = {}
        
        self.enemies = Entity(name='enemies', color=EG_Globals.ent_colors["enemies_color"])
        self.teammates = Entity(name='teammates', color=EG_Globals.ent_colors["teammates_color"])
        self.npcs = Entity(name='npcs', color=EG_Globals.ent_colors["npcs_color"])
        self.local_objects = Entity(name='local_objects', color=EG_Globals.ent_colors["local_objects_color"])
        self.environment = Entity(name='environment', color=EG_Globals.ent_colors["environment_color"])
        
        self.ground = Environment_Object(name='ground',
            parent=self.environment, model='plane', collider='box', scale=(100,1,100),
            color=color.blue.tint(-.2), texture='white_cube', texture_scale=(100,100))
        
        
        self.wall = Environment_Object(name='wall',
            parent=self.environment,
            model='cube', collider='box', scale=(35, 6, 1), position=(0, 3, 10),
            texture='brick',
            texture_scale=(11, 5),
            )
        
        self.solid_building = Environment_Object(name='solid building',
            parent=self.environment, model='cube', collider='box',
            scale=(15,7.5,15), position=(-33, 3.25,0), color=color.rgba(.65, .16, .16, .8),
            # texture='white_cube',
            texture='digit_rain.png',
            )
        
        table_model = 'ursina_table.bam'
        skyscraper = Environment_Object(parent=self.environment, position=(7, 0, 30))
        level_1 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,          0, 0), color=color.brown)
        level_2 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_1.y+10,0), color=color.brown)
        level_3 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_2.y+10,0), color=color.brown)
        level_4 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_3.y+10,0), color=color.brown)
        level_5 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_4.y+10,0), color=color.brown)
        level_6 = Environment_Object(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_5.y+10,0), color=color.brown)
        skyscraper.combine()
        
        sky = Sky()
        
        EG_Globals.current_sets['environment_objects'].add(sky)
        self.combility_testing_equipment=Entity(name='Combility Testing Equipment')

        self.player = Player(name='player',
            # model='cube',
            # texture='robot_simple.png',
            # texture='shore.png',
            # color=color.gray,
            # shader=matcap_shader,
            character_model='robot_simple.obj',
            core_offset=Vec3(0, 0.15, 0),
            cam_height=.47,
            # starting_cam_pos='left',
            )
        self.player.world_y = self.player.character.scale_y / 2
        
        
        controls_center = ControlsCenter(player_controllers=self.player)
        
        
        self.combility_info = Text(name='Combility Info',
            parent=self.player,
            double_sided=True,
            text='Combility: ',
            scale=24,
            position=(0, 11, 0),
            rotation=(0,90,0))
        
        self.weapon_slot_1 = Slot(name='weapon_slot_1',
            initial_owner=self.player,
            parent=self.player,
            # initial_owner=self.cam.dev_controllers,
            # parent=self.cam.dev_controllers,
            
            # # position=(.265, .73, 1.0),
            # # rotation=(180,180,0),
            # world_scale=1,
            
            position=(.265, .65, 1.0),
            model='cone_reversed',
            world_scale=(0.065, 0.1, 0.065)
            )
        
        self.weapon_slot_2 = Slot(name='weapon_slot_2',
            initial_owner = self.player,
            parent=self.player,
            position=(.265, .35, 1.0),
            rotation=(0,0,0),
            world_scale=.1)
        
        self.weapon_slot_3 = Slot(name='weapon_slot_3',
            initial_owner = self.player,
            parent=self.player,
            
            # position=(-.32, .73, 1.0),
            # rotation=(180,180,0),
            # world_scale=.1
            
            position=(-.32, .65, 1.0),
            model='cone_reversed',
            world_scale=(0.065, 0.1, 0.065)
            
            )
        

        self.weapon_slot_4 = Slot(name='weapon_slot_4',
            initial_owner = self.player,
            parent=self.player,
            position=(-.32, .35, 1.0),
            rotation=(0,0,0),
            world_scale=.1)
        

        self.enemy_target = Enemy(name='enemy_target',
            parent=self.enemies,
            position=(self.weapon_slot_1.world_position.x - 6, self.player.world_position.y, self.weapon_slot_1.world_position.z),
            rotation_y=90,
            character_model='robot_humanoid',
            texture='robot_humanoid',
            core_offset = Vec3(.05, 0.15, 0)
        )
        
        self.teammate_target = Teammate(name='teammate_target',
            parent=self.teammates,
            position=(self.weapon_slot_1.world_position.x - 10, self.player.world_position.y, self.weapon_slot_1.world_position.z),
            rotation_y=90,
            character_model='robot_military',
            core_offset = Vec3(.05, 0.15, 0),
        )
        
        self.npc_target = NPC(name='npc_target',
            parent=self.npcs,
            position=(self.weapon_slot_1.world_position.x - 14, self.player.world_position.y, self.weapon_slot_1.world_position.z),
            rotation_y=90,
            character_scale=1,
            character_model='orb_ant',
        )
        
        self.rando_object = EG_Object(name='rando_object',
            parent=self.local_objects,
            position=(self.weapon_slot_1.world_position.x - 18, self.player.world_position.y, self.weapon_slot_1.world_position.z),
            rotation_y=0,
            model='cube',
            collider='box',
            scale=(1.5,2,1.5),
            color=color.gray,
        )
        
        
        # new_object_position = self.enemy_target.world_position + self.enemy_target.forward * 1
        # new_object = Entity(parent=self.enemy_target, model='cube', position=new_object_position)
        
        # self.enemy_dummy_arm = Entity(
        #     parent=self.enemy_target, name='enemy dummy arm', model='cube',
        #     color=color.Color(.3,.3,.3,1),
        #     world_scale=(.8,.2,.2), 
        #     position=(.7,0,-.5))
        
        self.enemy_weapon_slot = Slot(name='enemy_weapon_slot',
            parent=self.enemy_target,
            model='cone_reversed',
            initial_owner = self.enemy_target,
            color=color.rgba(0.5, 0, 0.5, 0.6),
            position=(.3, .65, 1),
            world_scale=.1)
        
        self.saved_transform_entities = [
            'enemies',
            'teammates',
            'npcs',
            'local_objects',
            'player',
        ]
        self.store_initial_transforms()
        
        EG_Globals.level_target_types = [
            self.enemies,
            self.teammates,
            self.npcs,
            self.local_objects,
            self.environment]
                


    def store_initial_transforms(self):
        for entity in self.saved_transform_entities:
            if entity in ['player', 'dummy_arm']:
                self.initial_transforms[entity] = [(getattr(self, entity).world_position, getattr(self, entity).world_rotation, getattr(self, entity).world_scale)]
            else:
                self.initial_transforms[entity] = [(child.world_position, child.world_rotation, child.world_scale) for child in getattr(self, entity).children]

    def reset_transforms(self):
        pt('reset transforms')
        for entity in self.saved_transform_entities:
            if entity in ['player', 'dummy_arm']:
                getattr(self, entity).world_position, getattr(self, entity).world_rotation, getattr(self, entity).world_scale = self.initial_transforms[entity][0]
            else:
                for i, child in enumerate(getattr(self, entity).children):
                    child.world_position, child.world_rotation, child.world_scale = self.initial_transforms[entity][i]
    
    class Cam:
        def __init__(self):
            self.dev_controllers = ControlsCenter(
                player_controllers=(FirstPersonShooterController(level=Entity)),
                # world_position=(0.5, 1.5, -1.37),
                world_position=(0.5, 13.5, -11.37),
                world_rotation=(5, -54, 0),
                starting_cam='free_cam',
            )
    
# EditorCamera()

class InputStuff(Entity):
    def __init__(self, **kwargs):
        super().__init__(ignore_paused=True, **kwargs)
        
    def input(self, key):
        if key == 'p':
            pt(camera.world_position, camera.world_rotation)

        
# InputStuff()


if __name__ == '__main__':
    app = Ursina(position=(.8, -.8))
    window.position=(360, 0)
    BuildLevel()
    InputStuff()
    app.run()
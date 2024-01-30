''' TODO:
    - Table should turn into a sphere/character model just like the other characters. 
        - I'd like the testing in the future to be your own character model that you see holding
        each combility and shooting it. So it's a cool 3rd/4th person perspective on yourself
        shooting the combility. 
    '''

from print_tricks import pt

from ursina import *
from ursina.shaders.matcap_shader import matcap_shader

from core1k import *
from target_types import *
import globals

class BuildLevel:
    def __init__(self):
        self.initial_transforms = {}

        self.enemies = Entity(name='enemies')
        self.teammates = Entity(name='teammates')
        self.npcs = Entity(name='npcs')
        self.local_objects = Entity(name='local_objects')
        self.environment = Entity(name='environment')
        
        self.ground = Entity(parent=self.environment, model='plane', collider='box', name='ground',  scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100))
        self.wall = Entity(parent=self.environment, model='cube', collider='box', name='wall', scale=(35, 6, 1), position=(0,3,10), texture='brick', texture_scale=(11,5))
        self.solid_building = Entity(parent=self.environment, model='cube', collider='box', name='solid building', scale=(15,7.5,15), position=(-33, 3.25,0), color=color.rgba(.65,.16,.16,.8), texture='white_cube')
        
        table_model = 'table'
        table_model = 'ursina_table.bam'
        skyscraper = Entity(parent=self.environment, position=(7,0,30))
        level_1 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,          0, 0), color=color.brown)
        level_2 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_1.y+10,0), color=color.brown)
        level_3 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_2.y+10,0), color=color.brown)
        level_4 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_3.y+10,0), color=color.brown)
        level_5 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_4.y+10,0), color=color.brown)
        level_6 = Entity(parent=skyscraper, model=table_model, colider='mesh', scale=(20, 10, 20), position=(0,level_5.y+10,0), color=color.brown)
        
        Sky()
        
        self.combility_testing_equipment=Entity(name='Combility Testing Equipment')
        ## TABLE
        # table_builder = Entity(name='table_model')
        # leg1 = Entity(parent=table_builder, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(-0.45, -0.5, 0.45))
        # leg2 = Entity(parent=table_builder, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(0.45, -0.5, 0.45))
        # leg3 = Entity(parent=table_builder, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(-0.45, -0.5, -0.45))
        # leg4 = Entity(parent=table_builder, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(0.45, -0.5, -0.45))
        # top = Entity(parent=table_builder, model='cube', color=color.white, scale=(1, 0.1, 1), position=(0, 0, 0))
        
        # table_builder.combine()
        # table = Object(name='table', character_model=table_builder.model)
        # table = Object(name='table', character_model='ursina_table', double_sided=True)
        self.table = EnergyBeing(
            name='table',
            shader=matcap_shader,
            # character_model='ursina_table',
            character_model='simple_robot.obj',
            texture='simple_robot.png',
            )
        
        # table.model.save('ursina_table')
        # table.collider='box'
        # table = Object(name='table', model='ursina_table')
        
        self.table.position = (.5, 1, 0)
        # table.rotation = (0, 3, 0)
        self.table.parent = self.combility_testing_equipment
        
        self.combility_info = Text(parent=self.table, name='c Info',
            text='Combility:',
            scale=24,
            position=(0, 0, 0))
        
        ### WEAPON
        self.stand = Entity(
            parent=self.table, name='stand', 
            model='cube', 
            color=color.rgba(0,1,0,.8), 
            world_scale=(0.1, .25, 0.1),
            position=(0, 0.125, 0),
            )
        
        self.dummy_arm = Entity(
            parent=self.stand, name='dummy_arm', model='cube', 
            color=color.rgba(0,0,1,.8), 
            world_scale=(0.2, .2, 1), 
            position=(0, 1, 0),
            rotation_y=-90
            )
        
        self.weapon_slot = Slot(
            initial_owner = self.table,
            parent=self.dummy_arm, name='self.weapon_slot', model='sphere', 
            color=color.rgba(0.5, 0, 0.5, 0.6), 
            position=(0, .5, .35),
            world_scale=.1)
        
        # pt(self.dummy_arm.world_position, self.dummy_arm.position, self.dummy_arm.world_scale, self.dummy_arm.world_scale,
        #     self.weapon_slot.world_position, self.weapon_slot.position, self.weapon_slot.world_scale, self.weapon_slot.world_scale)
        
        
        self.enemy_target = Enemy(parent=self.enemies, color=color.red, rotation_y=0, 
            name='enemy_target', character_model='sphere', scale=(1,2.5,1), 
            position=(self.weapon_slot.world_position.x - 8, self.weapon_slot.world_position.y, self.weapon_slot.world_position.z))
        
        self.teammate_target = Teammate(parent=self.teammates, color=color.blue, rotation_y=0, 
            name='teammate_target', character_model='sphere', scale=(1,2.5,1), 
            position=(self.weapon_slot.world_position.x - 10, self.weapon_slot.world_position.y, self.weapon_slot.world_position.z))
        
        self.npc_target = NPC(parent=self.npcs, color=color.yellow, rotation_y=0, 
            name='npc_target', character_model='sphere', scale=(1, 2.5, 1), 
            position=(self.weapon_slot.world_position.x - 12, self.weapon_slot.world_position.y, self.weapon_slot.world_position.z))
        
        self.rando_object = EG_Object(parent=self.local_objects, color=color.gray, rotation_y=0, 
            name='rando_object', model='cube', collider='box', scale=(1.5,2,1.5), 
            position=(self.weapon_slot.world_position.x - 16, self.weapon_slot.world_position.y, self.weapon_slot.world_position.z))
        
        # new_object_position = self.enemy_target.world_position + self.enemy_target.forward * 1
        # new_object = Entity(parent=self.enemy_target, model='cube', position=new_object_position)
        
        self.enemy_dummy_arm = Entity(
            parent=self.enemy_target, name='enemy dummy arm', model='cube',
            color=color.Color(.3,.3,.3,1),
            world_scale=(.8,.2,.2), 
            position=(.7,0,-.5))
        
        self.enemy_weapon_slot = Slot(
            initial_owner = self.enemy_target,
            parent=self.enemy_dummy_arm, name='enemy_weapon_slot', model='sphere', 
            color=color.rgba(0.5, 0, 0.5, 0.6), 
            position=(.4, .5, 0),
            rotation_y=90,
            world_scale=.1)
        
        BuildLevel.Cam()

        self.saved_transform_entities = [
            'enemies', 
            'teammates', 
            'npcs', 
            'local_objects', 
            'table',
            'dummy_arm',
        ]
        self.store_initial_transforms()
        
        globals.level_target_types = [
            self.enemies,
            self.teammates,
            self.npcs,
            self.local_objects,
            self.environment]

    def store_initial_transforms(self):
        for entity in self.saved_transform_entities:
            if entity in ['table', 'dummy_arm']:
                self.initial_transforms[entity] = [(getattr(self, entity).world_position, getattr(self, entity).world_rotation, getattr(self, entity).world_scale)]
            else:
                self.initial_transforms[entity] = [(child.world_position, child.world_rotation, child.world_scale) for child in getattr(self, entity).children]

    def reset_transforms(self):
        pt('reset transforms')
        for entity in self.saved_transform_entities:
            if entity in ['table', 'dummy_arm']:
                getattr(self, entity).world_position, getattr(self, entity).world_rotation, getattr(self, entity).world_scale = self.initial_transforms[entity][0]
            else:
                for i, child in enumerate(getattr(self, entity).children):
                    child.world_position, child.world_rotation, child.world_scale = self.initial_transforms[entity][i]
    class Cam:
        def __init__(self):
            cam = ControlsCenter(
                player_controllers=(FirstPersonShooterController(level=Entity)),
                # world_position=(0.5, 1.5, -1.37),
                world_position=(0.5, 1.5, -11.37),
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
        if key == 'o':
            window.render_mode = 'normals'
        if key == 'i':
            window.render_mode = 'default'
        # if key == 'f2':
        #     cam.world_position = Vec3(3.5, 3.5, -13) 
        #     cam.world_rotation = Vec3(9.5, -24, 0)
        # if key == 'f4':
        #     cam.world_position = (13.5, 2, 0)
        #     cam.world_rotation = (4.7, -90, 0)
        
# InputStuff()


if __name__ == '__main__':
    app = Ursina(position=(.8,-.8))
    window.position=(360,0)
    BuildLevel()
    InputStuff()
    app.run()
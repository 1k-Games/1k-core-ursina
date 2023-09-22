from print_tricks import pt
from ursina import *
from controls_center import ControlsCenter

app=Ursina(size=(1920,1080))

class BuildLevel:
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    wall = Entity(model='cube', scale=(35, 6, 1), position=(0,0,10), texture='brick', texture_scale=(100,100))
    Sky()
    
    ### TABLE
    table = Entity()
    leg1 = Entity(parent=table, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(-0.45, -0.5, 0.45))
    leg2 = Entity(parent=table, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(0.45, -0.5, 0.45))
    leg3 = Entity(parent=table, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(-0.45, -0.5, -0.45))
    leg4 = Entity(parent=table, model='cube', color=color.white, scale=(0.1, 1.0, 0.1), position=(0.45, -0.5, -0.45))
    
    top = Entity(parent=table, model='cube', color=color.white, scale=(1, 0.1, 1), position=(0, 0, 0))
    
    table.combine()
    table.collider='box'
    table.y =1
    
    combility_info = Text(text='Combility information:', position=(0, 0, 0), parent=table)
    
    ### WEAPON
    weapon_stand = Entity(parent=table, model='cube', color=color.dark_gray, world_scale=(0.1, .25, 0.1), position=(0, 0.125, 0))
    
    weapon = Entity(model='cube', color=color.blue, world_scale=(1, 0.1, 0.1), world_position=(0, 1.3, 0))
    weapon_end = Entity(parent=weapon, model='sphere', color=color.red, scale=(.15,.5,.5), position=(-0.5, 0, 0))
    
    ### setup first target:
    dummy_target = Entity(model='sphere', collider='box', scale=(1,2.5,1), position=(weapon.world_position.x - 8, weapon.world_position.y, weapon.world_position.z))

class InputStuff(Entity):
    def __init__(self, **kwargs):
        super().__init__(ignore_paused=True, **kwargs)
        
    def input(self, key):
        if key == 'p':
            pt(cc.orbital_camera.enabled, cc.free_camera.enabled, cc.dev_pause_menu.enabled, 
                cc.game_pause_menu.enabled, cc.cur_player_controller.enabled)
            pt(cc.cur_dev_controller, cc.cur_dev_controller.world_position, cc.cur_dev_controller.position, 
                camera.world_position, camera.position)
InputStuff()

cc = ControlsCenter(
    position=(0.5, 1.5, -1.37), 
    rotation=(5, -54, 0), 
    starting_cam='free_cam'
)
pt(cc.orbital_camera.enabled, cc.free_camera.enabled, cc.dev_pause_menu.enabled, 
    cc.game_pause_menu.enabled, cc.cur_player_controller.enabled)
pt(cc.cur_dev_controller, cc.cur_dev_controller.world_position, cc.cur_dev_controller.position, 
    camera.world_position, camera.position)
app.run()

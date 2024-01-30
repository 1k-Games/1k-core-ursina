from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import win32gui, win32con, win32api
from print_tricks import pt
# NOTE: do pip install pywin32 in order to access the win32gui/win32con/win32api

app = Ursina()
window.vsync = False
window.size = (1920,1080)
ground = Entity(model='plane', scale=(100,1,100), color=color.hsv(240,.6,.1,.75), texture='white_cube', texture_scale=(100,100), collider='box')
e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)
e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)

drone_model_1 = Entity(model="orb_ant_uvMapped_combined.obj", 
                            texture = "sci_fi_tile_pipes_edit_B.png", 
                            world_position = (3, 2, 8), 
                            rotation = (0, 180, 0),
                            collider = 'sphere',
                            )
drone_model_1.collider.visible = True
        
player = FirstPersonController(y=2, origin_y=-.5)

# Create layered window
hwnd = application.base.win.getWindowHandle().getIntHandle()
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

transparency = 255 # 255 = full opaque (unsigned byte integer)
final_transparency = 188
def update():
    global transparency
    if transparency > final_transparency:
        transparency -= 1 # decrease transparency by 1 each frame
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), transparency, win32con.LWA_ALPHA)

app.run()




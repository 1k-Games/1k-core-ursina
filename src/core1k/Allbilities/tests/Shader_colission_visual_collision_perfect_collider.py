'''
https://discourse.panda3d.org/t/picking-visible-models/29022
https://gist.github.com/fireclawthefox/825bfe5f3b699fa27c578a81e1a33d93

Make several versions of this file, and place in ursina improvements or a new folder for 
    fast collision detection
    - Check clickup app for notes on "Colliding With Shaders - Optimizations"
    
    
'''
from print_tricks import pt
import random
import itertools
from PIL import Image
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader, RenderState, ShaderAttrib, LVecBase4f, PNMImage, loadPrcFileData, CardMaker, TextureAttrib, NodePath


loadPrcFileData(
    "",
    """
    textures-power-2 none
    textures-auto-power-2 #f
    show-buffers #t
    show-frame-rate-meter #t
    frame-rate-meter-milliseconds #t
    """)

base = ShowBase()

shaderVert = """
#version 150
// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
// Vertex inputs
in vec4 p3d_Vertex;
void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
"""

shaderFrag = """
#version 150
// Our models color
uniform vec4 objectColor;
// Output to the screen
out vec4 p3d_FragColor;
void main() {
    // convert colors from 0-255 range to 0-1 range
    float r = objectColor.x / 255;
    float g = objectColor.y / 255;
    float b = objectColor.z / 255;
    // Now set the color of the model
    // we currently ignore alpha. If this is important, just add it.
    p3d_FragColor = vec4(r,g,b,1);
}
"""

debug = False ## show the picture:
disable_textures = True ## Textures unecessary. tiny speedup. save gpu memory etc. on more texture-heavy scenes
num_models = 100
res_width = base.win.getSize()[0]
res_height = base.win.getSize()[1]
# res_width = 100
# res_height = 75
box_render = NodePath("BoxRender")
original_to_copy = {}  # Mapping from original models to copies


# this map will contain colors and their respective models
pick_map = {}

used_color_list = []
def get_random_color():
    global used_color_list
    # get the maximum color value (usually will be 255)
    maxVal = PNMImage().get_maxval()
    # search for an unused color value
    while True:
        r = random.randrange(0, maxVal)
        g = random.randrange(0, maxVal)
        b = random.randrange(0, maxVal)
        color = LVecBase4f(r, g, b, maxVal)
        if color not in used_color_list:
            # found a good color, store and return it
            used_color_list.append(color)
            return color

def arrange():
    # add some pickable models
    model_names = itertools.cycle(['panda', 'models/teapot'])
    for i in range(num_models - 2):  # Subtract 2 for the boxes
        # The color for the model. Must be integer values between 0 and 255 to
        # be able to accurately pick the color again later on
        pick_col = get_random_color()
        model_name = next(model_names)
        model = loader.load_model(model_name)
        model.name = f"{model_name.split('/')[-1].capitalize()}{i}"
        model.reparent_to(base.render)
        model.set_x(random.randrange(-15, 15))
        model.set_y(random.randint(50, 150))
        model.set_z(random.randrange(-20, 5))
        # model.set_shader_input("objectColor", pick_col)
        model.set_hpr(0, 90, 0)  # Rotate the model 90 degrees
        # pick_map[pick_col] = model

    # Add two boxes
    for i in range(2):
        pick_col = get_random_color()
        model = loader.load_model('models/box')
        model.name = f"Box{i}"
        model.reparent_to(base.render)
        model.set_x(random.randrange(-15, 15))
        model.set_y(random.randint(50, 150))
        model.set_z(random.randrange(-20, 5))
        model.set_shader_input("objectColor", pick_col)
        model.set_hpr(0, 90, 0)  # Rotate the model 90 degrees
        model.set_scale(11)  # Scale the box
        model_copy = model.copy_to(box_render)
        original_to_copy[model] = model_copy
        pick_map[pick_col] = model_copy
        
    pt(list(pick_map.items())[0])
# remove everything in the scene and create new random models
def rearrange():
    for color, model in pick_map.items():
        model.remove_node()
    pick_map.clear()  # Clear the pick_map
    original_to_copy.clear()
    arrange()

# load our shader
shader = Shader.make(Shader.SL_GLSL, shaderVert, shaderFrag)

picker_buffer = None


def pick():
    pt.t()
    x = 0
    y = 0
    if base.mouseWatcherNode.hasMouse():
        # get the current mousepointer location
        x = int(base.win.get_pointer(0).get_x())
        y = int(base.win.get_pointer(0).get_y())
    else:
        # we don't have a mousepointer location, hence we can't pick anything
        return

    
    # create the buffer we render in
    picker_buffer = base.win.makeTextureBuffer("picking Buffer", res_width, res_height, to_ram=True)

    picker_buffer.setSort(-100)

    # set up a camera which we use to fill the buffer
    picker_cam = base.makeCamera(picker_buffer)
    # "render" should be the root node that contains the pickable objects. It
    # may not always be "render"
    picker_cam.reparentTo(box_render)
    # copy our main cameras position and rotation
    picker_cam.set_pos(camera.get_pos())
    picker_cam.set_hpr(camera.get_hpr())

    # load the shader on the camera
    if not disable_textures:
        picker_cam.node().setInitialState(RenderState.make(ShaderAttrib.make(shader, 100000)))
    else:
        # disable textures for the picking camera
        rs = RenderState.make(ShaderAttrib.make(shader, 100000))
        rs = rs.setAttrib(TextureAttrib.makeOff())
        picker_cam.node().setInitialState(rs)
        
    # render two frames to get the buffer actually filled and usable
    # pt.t()
    # base.graphicsEngine.renderFrame()
    pt.t()
    base.graphicsEngine.renderFrame()
    pt.t()

    # convert the rendered texture into a PNM Image
    picker_img = PNMImage(res_width, res_height)
    picker_texture = picker_buffer.getTexture()
    picker_texture.store(picker_img)



    if debug:
        # Convert PNMImage to PIL Image
        width = picker_img.get_x_size()
        height = picker_img.get_y_size()
        # Get the image data from the texture
        image_data = picker_texture.get_ram_image_as("RGBA")

        # Convert the image data to a PIL Image
        pil_image = Image.frombytes('RGBA', (width, height), image_data, 'raw', 'RGBA')

        # Display the image
        pil_image.show()

    # get the color at the mouse position
    col = LVecBase4f(
        picker_img.getRedVal(x,y),
        picker_img.getGreenVal(x,y),
        picker_img.getBlueVal(x,y),
        picker_img.getAlphaVal(x,y))

    # deselect all models
    for mapCol, model_copy in pick_map.items():
        # Find the original model corresponding to the model copy
        for original, copy in original_to_copy.items():
            if copy == model_copy:
                original.clear_color_scale()
                break
    
    # select the model with the picked color
    if col in pick_map:
        picked_model_copy = pick_map[col]
        # Find the original model corresponding to the picked copy
        for original, copy in original_to_copy.items():
            if copy == picked_model_copy:
                original.setColorScale(1, 1, 0, 1)
                break

    # clear up our buffer window
    base.graphicsEngine.removeWindow(picker_buffer)

base.accept("mouse1-up", pick)
base.accept("r", rearrange)

#initial random arrangement of pandas
arrange()

base.run()
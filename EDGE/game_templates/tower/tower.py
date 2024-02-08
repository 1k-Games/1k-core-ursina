from print_tricks import pt

pt.c('------- tower ---------')


from print_tricks import pt

from PIL import Image

import io
from ursina import *
from ursina.shaders import basic_lighting_shader as bls
# from enemy import *


Entity.default_shader = bls
pt(Entity.default_shader)

class Level_Editor(Entity):
    def __init__(self, *args, 
                grid_cells=20, 
                ground_scale=(20, 1, 20), 
                texture_resolution=200,
                **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_cells = grid_cells
        self.cell_size = texture_resolution // grid_cells
        
        base_grid_size_in_pixels = self.grid_cells * self.cell_size
        ratio_grid_to_grid_size_in_pixels = int(texture_resolution / base_grid_size_in_pixels)
        self.grid_size_in_pixels = base_grid_size_in_pixels * ratio_grid_to_grid_size_in_pixels
        pt(ratio_grid_to_grid_size_in_pixels)
        pt(self.grid_size_in_pixels)


        self.in_memory_texture = None
        self.ground = Entity(model='cube', scale=ground_scale, collider='box')
        
        self.create_grid_texture()
        self.apply_texture_to_ground()

        self.editor_cam = EditorCamera()
        self.editor_cam.position = Vec3(1, 22, -19)
        self.editor_cam.rotation = Vec3(50, -1.3, 0)
        self.sky = Sky(texture = "sky_sunset")

    def input(self, key):

        if mouse.hovered_entity == self.ground:
            if key == 'left mouse down':
                self.click_mouse(add_path=True)
            elif key == 'right mouse down':
                self.click_mouse(remove_path=True)
            elif key == 'middle mouse down':
                # Handle middle click, adjust the method or parameters as needed
                print("Middle click on ground")
                
        if key == "space":
            print(self.editor_cam.position)
            print(self.editor_cam.rotation) 
            print(camera.fov)

        if key == "x":
            move(targets)


            
    def update(self):
        if mouse.hovered_entity == self.ground:
            if held_keys['left mouse']:
                self.click_mouse(add_path=True)
            if held_keys['right mouse']:
                self.editor_cam.rotate_key = None
                self.click_mouse(remove_path=True)
            else:
                self.editor_cam.rotate_key = 'right mouse'

            
    def create_grid_texture(self):
        
        img = Image.new('RGB', (self.grid_size_in_pixels, self.grid_size_in_pixels), 
                        color='white')
        pixels = img.load()

        
        for x in range(self.grid_size_in_pixels):
            for z in range(self.grid_size_in_pixels):
                if x % self.cell_size == 0 or z % self.cell_size == 0:
                    pixels[ x, z] = (0, 255, 0)  # Grid lines are green

        # Save the image to a bytes buffer instead of a file
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        self.in_memory_texture = buffer

    def apply_texture_to_ground(self):
        if self.in_memory_texture:
            # Load the image from the in-memory buffer
            self.in_memory_texture.seek(0)  # Ensure the buffer's read pointer is at the start
            image = Image.open(self.in_memory_texture)
            
            # Ensure the image is in RGBA mode
            image = image.convert('RGBA')
            
            # Convert the PIL image to a format Ursina can use
            texture = Texture(image)
            self.ground.texture = texture
        else:
            print("No texture in memory to apply.")

    def update_grid_texture(self, cell_x, cell_z, color_to_change_to):
        
        img = Image.open(self.in_memory_texture)
        pixels = img.load()

        cell_size = self.cell_size
        for x in range(cell_x * cell_size, (cell_x + 1) * cell_size):
            for z in range(cell_z * cell_size, (cell_z + 1) * cell_size):
                if x % cell_size == 0 or z % cell_size == 0:
                    continue
                pixels[x, z] = color_to_change_to  

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        self.in_memory_texture = buffer
        
    def save_texture_to_disk(self, filename=r'EDGE/game_templates/tower/assets/grid_texture.png'):
        self.in_memory_texture
        if self.in_memory_texture:
            with open(filename, 'wb') as f:
                f.write(self.in_memory_texture.getvalue())
        else:
            print("No texture in memory to save.")

    def click_mouse(self, add_path=False, remove_path=False):
        local_x = mouse.world_point[0] - self.ground.position.x + (self.ground.scale_x / 2)
        local_z = mouse.world_point[2] - self.ground.position.z + (self.ground.scale_z / 2)
        
        # Adjust local_x and local_z to be in terms of the texture size
        texture_ratio_x = self.grid_size_in_pixels / self.ground.scale_x
        texture_ratio_z = self.grid_size_in_pixels / self.ground.scale_z
        
        # Scale local_x and local_z to texture coordinates
        texture_x = int(local_x * texture_ratio_x)
        texture_z = int(local_z * texture_ratio_z)
        
        # Invert texture_z to account for potential y-axis inversion
        texture_z = self.grid_size_in_pixels - texture_z - 1
        
        # Ensure texture_x and texture_z are within the bounds of the texture
        texture_x = max(0, min(self.grid_size_in_pixels - 1, texture_x))
        texture_z = max(0, min(self.grid_size_in_pixels - 1, texture_z))

        pt(local_x, local_z, texture_z, texture_z)

        if add_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=(255, 255, 0))  # Yellow
        elif remove_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=(255, 255, 255))  # White (or original color)

        self.apply_texture_to_ground()
    




if __name__ == "__main__":
    app = Ursina(
    # development_mode=False
    )
    
    Level_Editor = Level_Editor(grid_cells=20, texture_resolution=800)

    app.run()


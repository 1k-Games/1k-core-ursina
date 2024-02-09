from print_tricks import pt

pt.c('------- tower ---------')


from print_tricks import pt

from PIL import Image
import io

from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from enemy import move


Entity.default_shader = bls
pt(Entity.default_shader)

class Grid_Editor(Entity):
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
        pt(self.cell_size)
        # pt(ratio_grid_to_grid_size_in_pixels)
        # pt(self.grid_size_in_pixels)
        
        self.path_locations = set()


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
        model_x = mouse.world_point[0] - self.ground.position.x + (self.ground.scale_x / 2)
        model_z = mouse.world_point[2] - self.ground.position.z + (self.ground.scale_z / 2)
        
        # Calculate the size of each cell in terms of the model's scale
        cell_grid_ratio_x = self.ground.scale_x / self.grid_cells
        cell_grid_ratio_z = self.ground.scale_z / self.grid_cells
        
        # Calculate cell position by dividing the model position by the cell size
        cell_pos_x = int(model_x / cell_grid_ratio_x) + 1
        cell_pos_z = int(model_z / cell_grid_ratio_z) + 1

        # Create Vec3 for the cell position
        cell_position = Vec3(cell_pos_x, 0, cell_pos_z)

        if add_path:
            if cell_position in self.path_locations:
                return
            self.path_locations.add(cell_position)
        else:
            if not cell_position in self.path_locations:
                return
            self.path_locations.discard(cell_position)
            

        texture_ratio_x = self.grid_size_in_pixels / self.ground.scale_x
        texture_ratio_z = self.grid_size_in_pixels / self.ground.scale_z
        
        texture_x = int(model_x * texture_ratio_x)
        texture_z = int(model_z * texture_ratio_z)
        ## Invert 
        texture_z = self.grid_size_in_pixels - texture_z - 1
        
        
        # Ensure texture_x and texture_z are within the bounds of the texture
        texture_x = max(0, min(self.grid_size_in_pixels - 1, texture_x))
        texture_z = max(0, min(self.grid_size_in_pixels - 1, texture_z))

        pt(model_x, model_z, cell_pos_x, cell_pos_z, texture_x, texture_z)

        if add_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=(255, 255, 0))  # Yellow
        
        elif remove_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=(255, 255, 255))  # White (or original color)
        
        self.apply_texture_to_ground()

    def update_path(self, model_x, model_z, path_type='add'):
        ...
        new_point = Vec3(model_x, 0, model_z)  # Using Vec3 for compatibility with Ursina's distance check
        
        # # Check for existing points within cell_size distance
        # for point in self.path_locations:
        #     existing_point = Vec3(point[0], 0, point[1])
        #     if distance(new_point, existing_point) < self.cell_size:
        #         return False
        
        # if path_type == 'add':
        #     self.path_locations.append((model_x, model_z))
        #     self.reorganize_path_locations(new_point)
        # elif path_type == 'remove':
        #     if (model_x, model_z) in self.path_locations:
        #         self.path_locations.remove((model_x, model_z))
        # else:
        #     print(f"Unknown path type: {path_type}")

    def reorganize_path_locations(self, new_point):
        if len(self.path_locations) <= 1:
            return  # No need to reorganize if there's only one or no points
        
        # Convert path_locations to Vec3 for distance calculations
        path_locations_vec3 = [Vec3(point[0], 0, point[1]) for point in self.path_locations]
        
        # Start reorganization from the last added point
        sorted_locations = [new_point]
        remaining_points = set(path_locations_vec3)
        remaining_points.remove(new_point)
        
        while remaining_points:
            last_point = sorted_locations[-1]
            closest_point, min_distance = None, float('inf')
            
            for point in remaining_points:
                dist = distance(last_point, point)
                if dist < min_distance:
                    closest_point, min_distance = point, dist
            
            sorted_locations.append(closest_point)
            remaining_points.remove(closest_point)
        
        # Convert Vec3 back to tuples and update path_locations
        self.path_locations = [(point.x, point.z) for point in sorted_locations]

def run():
    grid_editor = Grid_Editor(grid_cells=10, texture_resolution=800)
    grid_editor.save_texture_to_disk()

if __name__ == "__main__":
    app = Ursina(
        title='Tower',
    # development_mode=False
    )
    
    run()
    
    app.run()


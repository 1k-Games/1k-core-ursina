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
        
        # pt(self.cell_size)
        # pt(ratio_grid_to_grid_size_in_pixels)
        # pt(self.grid_size_in_pixels)
        
        self.path_locations = set()
        self.path_locations_ordered = []


        self.in_memory_texture = None
        self.ground = Entity(model='cube', scale=ground_scale, collider='box')
        
        self.create_grid_texture()
        self.apply_texture_to_ground()

        self.editor_cam = EditorCamera()
        self.editor_cam.position = Vec3(1, 22, -19)
        self.editor_cam.rotation = Vec3(50, -1.3, 0)
        self.sky = Sky(texture = "sky_sunset")
        
        self.camera_rotation_active = False

    def input(self, key):

        if mouse.hovered_entity == self.ground:
            if key == 'left mouse down':
                self.click_mouse(add_path=True)
                
            elif key == 'right mouse down':
                # Attempt to remove a path. If successful, ensure camera does not rotate.
                if self.click_mouse(remove_path=True):
                    self.camera_rotation_active = False
                    self.editor_cam.rotate_key = None  # Disable camera rotation
                else:
                    # If not removing a path (clicking on an empty cell), enable camera rotation.
                    self.camera_rotation_active = True
                    self.editor_cam.rotate_key = 'right mouse'
            elif key == 'right mouse up':
                # When the right mouse button is released, you can choose to disable rotation.
                self.camera_rotation_active = False
                self.editor_cam.rotate_key = None  # Ensure camera rotation is disabled
                    
            elif key == 'middle mouse down':

                print("Middle click on ground")
                
        if key == "space":
            print(self.editor_cam.position)
            print(self.editor_cam.rotation) 
            print(camera.fov)

        if key == "x":
            self.path_locations_ordered = self.order_path_locations(self.path_locations)
            world_positions = [self.cell_to_world_position(cell_pos) for cell_pos in self.path_locations_ordered]

            pt(self.path_locations_ordered)
            pt(world_positions)
            move(world_positions)

    def update(self):
        if mouse.hovered_entity == self.ground and not self.camera_rotation_active:
            if held_keys['left mouse']:
                self.click_mouse(add_path=True)
            if held_keys['right mouse']:
                self.click_mouse(remove_path=True)

    def order_path_locations(self, path_locations):
        if not path_locations:
            return []

        # Find the starting point with the lowest x and z values
        starting_point = min(path_locations, key=lambda loc: (loc[0], loc[1]))
        path_locations_list = list(path_locations)
        path_locations_list.remove(starting_point)

        ordered_locations = [starting_point]

        # Iterate until all locations are ordered
        while path_locations_list:
            last_loc = ordered_locations[-1]
            # Find the closest location to the last location in ordered_locations
            closest_loc, closest_dist = None, float('inf')
            for loc in path_locations_list:
                dist = distance_2d(last_loc, loc)  # Assuming distance is an appropriate function or method
                if dist < closest_dist:
                    closest_loc, closest_dist = loc, dist
            ordered_locations.append(closest_loc)
            path_locations_list.remove(closest_loc)

        pt(path_locations, ordered_locations)
        return ordered_locations

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

        cell_position = (cell_pos_x, cell_pos_z)

        if add_path:
            if cell_position in self.path_locations:
                return False
            self.path_locations.add(cell_position)
        else:
            if not cell_position in self.path_locations:
                return False
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
        
        return True

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

    def cell_to_world_position(self, cell_position):
        # Calculate the size of each cell in terms of the model's scale
        cell_grid_ratio_x = self.ground.scale_x / self.grid_cells
        cell_grid_ratio_z = self.ground.scale_z / self.grid_cells
        
        # Convert cell position back to world position
        world_x = (cell_position[0] - 0.5) * cell_grid_ratio_x + self.ground.position.x - (self.ground.scale_x / 2)
        world_z = (cell_position[1] - 0.5) * cell_grid_ratio_z + self.ground.position.z - (self.ground.scale_z / 2)
        
        # Assuming the y position is the same as the ground's y position
        world_y = self.ground.position.y
        
        return Vec3(world_x, world_y, world_z)

def run():
    grid_editor = Grid_Editor(grid_cells=10, texture_resolution=100)
    grid_editor.save_texture_to_disk()

if __name__ == "__main__":
    app = Ursina(
        title='Tower',
    # development_mode=False
    )
    
    run()
    
    app.run()


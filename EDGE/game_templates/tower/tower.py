from print_tricks import pt
pt.easy_imports('main.py')


from PIL import Image
import io
import json

from ursina import *
from engine.ai.enemy import move
import placeable_turrets

pt.c('------- tower ---------')


class Grid_Editor(Entity):
    def __init__(self, *args, 
                grid_cells=20, 
                ground_scale=(20, .11, 20), 
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
        
        self.editor_cam = EditorCamera()
        self.editor_cam.position = Vec3(1, 22, -19)
        self.editor_cam.rotation = Vec3(50, -1.3, 0)
        self.sky = Sky(texture = "sky_sunset")
        
        self.camera_rotation_active = False
        self.path_location_color = color.red
        self.trail_color = color.gray
        self.grid_background_color = color.white
        
        self.create_grid_texture()
        self.apply_texture_to_ground()
        self.create_ui()
        
        self.load_and_run_from_slot(1)

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
            # self.draw_path_trail()
            
            # pt(self.path_locations_ordered)
            # pt(world_positions)
            move(world_positions)
            # invoke(move, world_positions, delay=1)

    def update(self):
        if mouse.hovered_entity == self.ground and not self.camera_rotation_active:
            if held_keys['left mouse']:
                self.click_mouse(add_path=True)
            if held_keys['right mouse']:
                self.click_mouse(remove_path=True)

    def load_and_run_from_slot(self, slot):
        if self.load_from_slot(slot):
            self.path_locations_ordered = self.order_path_locations(self.path_locations)
            self.run_move_enemy_command()

    def run_move_enemy_command(self):
        if self.path_locations_ordered:
            world_positions = [self.cell_to_world_position(cell_pos) for cell_pos in self.path_locations_ordered]
            move(world_positions)

    def create_ui(self):
        save_menu = self.create_expandable_menu('Save', Vec2(-0.8, 0.45), self.save_to_slot, 7)
        
        load_menu = self.create_expandable_menu('Load', Vec2(-0.7, 0.45), self.load_from_slot, 7)

        clear_button = self.create_expandable_menu('Clear', Vec2(-0.6, 0.45), self.clear, 0)

    def create_expandable_menu(self, title, position, action, slots=7):
        menu = Entity(parent=camera.ui)
        main_button = Button(text=title, parent=menu, 
            position=position, 
            scale=Vec2(0.1, 0.1))
        
        # Placeholder for expandable slot buttons
        slot_buttons = []
        for i in range(1, slots + 1):
            slot_button = Button(text=str(i), parent=menu, 
                position=position + Vec2(0, -0.1 * i), 
                scale=Vec2(0.2, 0.1))
            
            # Modify the on_click function to also toggle the slots visibility after performing the action
            def on_click_action(slot=i):
                action(slot)
                toggle_slots()  # Call toggle_slots to hide the sub-buttons after an action
            
            slot_button.on_click = Func(on_click_action)
            slot_button.enabled = False  # Initially hidden
            slot_buttons.append(slot_button)
        
        def toggle_slots():
            # Check if any button is enabled, then disable all
            if any(button.enabled for button in slot_buttons):
                for button in slot_buttons:
                    button.enabled = False
            else:
                for button in slot_buttons:
                    button.enabled = True
        
        if title == 'Clear':
            main_button.on_click = Func(self.clear_texture_and_points)
        else:
            main_button.on_click = Func(toggle_slots)
            
        return menu

    def save_to_slot(self, slot):
        self.save_points_and_texture(slot)

    def load_from_slot(self, slot):
        self.load_points_and_texture(slot)
    
    def clear(self):
        self.clear_texture_and_points()
        
    def save_points_and_texture(self, slot=1):
        points_filename = f'path_points_{slot}.json'
        texture_filename = f'grid_texture_{slot}.png'
        # Save points
        with open(points_filename, 'w') as f:
            json.dump(list(self.path_locations), f)
        
        # Save texture
        self.save_texture_to_disk(texture_filename)

    def load_points_and_texture(self, slot=1):
        points_filename = f'path_points_{slot}.json'
        texture_filename = f'grid_texture_{slot}.png'
        # Check if points file exists
        if not os.path.exists(points_filename):
            print(f"{points_filename} does not exist.")
            return False
        # Load points
        with open(points_filename, 'r') as f:
            self.path_locations = set(tuple(point) for point in json.load(f))
            self.path_locations_ordered = self.order_path_locations(self.path_locations)
        
        # Check if texture file exists
        if not os.path.exists(texture_filename):
            print(f"{texture_filename} does not exist.")
            return False
        # Load texture
        with open(texture_filename, 'rb') as f:
            self.in_memory_texture = io.BytesIO(f.read())
            self.apply_texture_to_ground()

    def clear_texture_and_points(self):
        self.path_locations = set()
        self.path_locations_ordered = []

        self.create_grid_texture()
        self.apply_texture_to_ground()
    
    def cell_to_texture_position(self, cell_position):
        """Convert cell position to texture (pixel) position, inverting the Z-axis."""
        texture_x = int(cell_position[0] * self.cell_size + self.cell_size / 2)
        # Invert the Z-axis for PIL image coordinates
        texture_z = self.grid_size_in_pixels - int(cell_position[1] * self.cell_size + self.cell_size / 2)
        return texture_x, texture_z

    def draw_path_trail(self):
        self.in_memory_texture.seek(0)
        img = Image.open(self.in_memory_texture)
        pixels = img.load()

        # Draw the trail
        for i in range(len(self.path_locations_ordered) - 1):
            start_cell = self.path_locations_ordered[i]
            end_cell = self.path_locations_ordered[i + 1]

            start_x, start_z = self.cell_to_texture_position(start_cell)
            end_x, end_z = self.cell_to_texture_position(end_cell)

            self.draw_line(pixels, start_x, start_z, end_x, end_z)
            self.draw_circle(pixels, start_x, start_z, 8)
            self.draw_circle(pixels, end_x, end_z, 8)

        # Redraw the original points on top of the trail
        for cell in self.path_locations_ordered:
            x, z = self.cell_to_texture_position(cell)
            self.redraw_original_point(pixels, x, z)

        # Save and apply the updated texture
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        self.in_memory_texture = buffer
        self.apply_texture_to_ground()

    def redraw_original_point(self, pixels, x, z):
        """Draws the original path point on top of the trail."""
        original_point_color = int(self.path_location_color[0] * 255), int(self.path_location_color[1] * 255), int(self.path_location_color[2] * 255)  # White, or choose the color that represents the original points
        radius = 1  # Smaller radius to ensure visibility
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    pixels[x + dx, z + dy] = original_point_color

    def draw_line(self, pixels, x0, y0, x1, y1):
        """Draws a line from (x0, y0) to (x1, y1) with a given radius and color gradient."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        self.draw_circle(pixels, x, y, 12) ## Beginning Point Circle 
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                self.draw_circle(pixels, x, y, 12)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                self.draw_circle(pixels, x, y, 12)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        # self.draw_circle(pixels, x, y, 8) ## End Point Circle

    def draw_circle(self, pixels, x0, y0, radius):
        """Draws a circle of a given radius around a point (x0, y0) with a color gradient."""
        trail_color = (int(self.trail_color[0] * 255), int(self.trail_color[1] * 255), int(self.trail_color[2] * 255))
        background_color = (int(self.grid_background_color[0] * 255), int(self.grid_background_color[1] * 255), int(self.grid_background_color[2] * 255))
        for x in range(x0 - radius, x0 + radius + 1):
            for y in range(y0 - radius, y0 + radius + 1):
                if (x - x0)**2 + (y - y0)**2 <= radius**2:
                    # Calculate gradient ratio based on distance from the center
                    distance = ((x - x0)**2 + (y - y0)**2)**0.23
                    ratio = 1 - (distance / radius)  # Invert ratio for correct gradient direction
                    # Mix colors based on the ratio
                    mixed_color = self.mix_colors(trail_color, background_color, ratio)
                    if 0 <= x < self.grid_size_in_pixels and 0 <= y < self.grid_size_in_pixels:
                        pixels[x, y] = mixed_color

    def mix_colors(self, color1, color2, ratio):
        """Mixes two colors together with a given ratio. Closer to 1 means more of color1."""
        return tuple(int(c1 * ratio + c2 * (1 - ratio)) for c1, c2 in zip(color1, color2))

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

        # pt(path_locations, ordered_locations)
        return ordered_locations

    def create_grid_texture(self, draw_grid_lines=False):
        img = Image.new('RGB', (self.grid_size_in_pixels, self.grid_size_in_pixels), 
                        color=(int(self.grid_background_color[0] * 255), 
                               int(self.grid_background_color[1] * 255), 
                               int(self.grid_background_color[2] * 255)
                                )
                        )
        if draw_grid_lines:
            pixels = img.load()
            for x in range(self.grid_size_in_pixels):
                for z in range(self.grid_size_in_pixels):
                    if x % self.cell_size == 0 or z % self.cell_size == 0:
                        pixels[x, z] = (0, 255, 0)  # Grid lines are green

        # Save the image to a bytes buffer instead of a file
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        self.in_memory_texture = buffer

    def update_grid_texture(self, cell_x, cell_z, color_to_change_to, draw_grid_lines=False):
        color_to_change_to = (int(color_to_change_to[0] * 255), 
                              int(color_to_change_to[1] * 255), 
                              int(color_to_change_to[2] * 255), 255)
        
        img = Image.open(self.in_memory_texture)
        pixels = img.load()

        cell_size = self.cell_size
        for x in range(cell_x * cell_size, (cell_x + 1) * cell_size):
            for z in range(cell_z * cell_size, (cell_z + 1) * cell_size):
                if draw_grid_lines and (x % cell_size == 0 or z % cell_size == 0):
                    continue
                pixels[x, z] = color_to_change_to  

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

    def mix_colors(self, color1, color2, ratio):
        """Mixes two colors together with a given ratio."""
        return tuple(int(c1 * ratio + c2 * (1 - ratio)) for c1, c2 in zip(color1, color2))

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

        # pt(model_x, model_z, cell_pos_x, cell_pos_z, texture_x, texture_z)

        if add_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=self.path_location_color)  
        
        elif remove_path:
            self.update_grid_texture(texture_x // self.cell_size, texture_z // self.cell_size, color_to_change_to=self.grid_background_color)
        
        self.apply_texture_to_ground()
        
        return True

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

def run(grid_cells=55, texture_resolution=333):
    grid_editor = Grid_Editor(grid_cells=grid_cells, texture_resolution=texture_resolution)
    grid_editor.save_texture_to_disk()

if __name__ == "__main__":
    app = Ursina(
        title='Tower',
    # development_mode=False
    )
    
    Entity(model='cube', texture='temp_symbol')

    
    run(grid_cells=400, texture_resolution=444)
    
    app.run()


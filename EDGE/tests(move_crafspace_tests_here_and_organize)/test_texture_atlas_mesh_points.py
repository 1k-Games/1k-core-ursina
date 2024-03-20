'''
- Quads working
    - slight offset might be happening though. As some circles on the xz plate are not just
    rotated, but also slightly above the xy plane. 
- Triangles are distorted very badly. 
'''
from print_tricks import pt
from ursina import *
import random

class CustomMesh(Entity):
    def __init__(self, texture_atlas, 
                mode='triangle', 
                double_sided=True, 
                spacing='uniform', 
                spacing_range=(1, 1, 1), 
                planes=['xy'], 
                shape='quad',
                point_count=9,
                **kwargs):
        super().__init__(double_sided=double_sided, **kwargs)
        self.texture_atlas = texture_atlas
        self.point_count = point_count  # For the 3x3 grid
        self.vertices = []
        self.triangles = []
        self.uvs = []

        if spacing == 'uniform':
            self.point_positions = [Vec3(x * spacing_range[0], y * spacing_range[1], z * spacing_range[2]) 
                                    for z in range(-1, 2) for y in range(-1, 2) for x in range(-1, 2)]
        elif spacing == 'random':
            self.point_positions = [Vec3(   
                random.uniform(-spacing_range[0], spacing_range[0]), 
                random.uniform(-spacing_range[1], spacing_range[1]), 
                random.uniform(-spacing_range[2], spacing_range[2])) for _ in range(self.point_count)]

        self.generate_mesh(mode, planes, shape)
        self.model = Mesh(vertices=self.vertices, triangles=self.triangles, uvs=self.uvs, mode=mode)
        self.texture = texture_atlas

    def generate_mesh(self, mode, planes, shape):
        for i, position in enumerate(self.point_positions):
            for plane in planes:
                if shape == 'quad':
                    self.add_quad(position, i, plane)
                elif shape == 'triangle':
                    self.add_triangle(position, i, plane)

    def add_quad(self, position, index, plane):
        half_size = 0.1  # Fixed size for simplicity
        if plane == 'xy':
            vertices = [
                Vec3(-half_size, -half_size, 0) + position,
                Vec3(half_size, -half_size, 0) + position,
                Vec3(half_size, half_size, 0) + position,
                Vec3(-half_size, half_size, 0) + position,
            ]
        elif plane == 'zy':
            vertices = [
                Vec3(0, -half_size, -half_size) + position,
                Vec3(0, half_size, -half_size) + position,
                Vec3(0, half_size, half_size) + position,
                Vec3(0, -half_size, half_size) + position,
            ]
        elif plane == 'xz':
            vertices = [
                Vec3(-half_size, 0, -half_size) + position,
                Vec3(half_size, 0, -half_size) + position,
                Vec3(half_size, 0, half_size) + position,
                Vec3(-half_size, 0, half_size) + position,
            ]
        else:
            raise ValueError(f"Unsupported plane: {plane}")

        self.vertices.extend(vertices)

        quad_start = len(self.vertices) - 4
        self.triangles.extend([quad_start, quad_start + 1, quad_start + 2, quad_start + 2, quad_start + 3, quad_start])

        # Calculate UVs based on the 3x3 grid position
        row = index // 3
        col = index % 3
        u_offset = col / 3
        v_offset = 1 - (row + 1) / 3

        self.uvs.extend([
            (u_offset, v_offset + 1/3),
            (u_offset + 1/3, v_offset + 1/3),
            (u_offset + 1/3, v_offset),
            (u_offset, v_offset),
        ])

    def add_triangle(self, position, index, plane):
        half_size = 0.1  # Fixed size for simplicity
        grid_size = 3  # Assuming a 3x3 grid in the texture atlas

        # Calculate which grid cell to use based on the index
        grid_x = index % grid_size
        grid_y = index // grid_size

        # Calculate UV coordinates for the selected grid cell
        uv_size = 1 / grid_size
        uv_bottom_left = (grid_x * uv_size, grid_y * uv_size)
        uv_bottom_right = ((grid_x + 1) * uv_size, grid_y * uv_size)
        uv_top_center = ((grid_x + 0.5) * uv_size, (grid_y + 1) * uv_size)

        if plane == 'xy':
            vertices = [
                position + Vec3(-half_size, -half_size, 0),
                position + Vec3(half_size, -half_size, 0),
                position + Vec3(0, half_size, 0),
            ]
            uvs = [
                uv_bottom_left,
                uv_bottom_right,
                uv_top_center,
            ]
        elif plane == 'zy':
            vertices = [
                position + Vec3(0, -half_size, -half_size),
                position + Vec3(0, half_size, -half_size),
                position + Vec3(0, 0, half_size),
            ]
            uvs = [
                uv_bottom_left,
                uv_bottom_right,
                uv_top_center,
            ]
        elif plane == 'xz':
            vertices = [
                position + Vec3(-half_size, 0, -half_size),
                position + Vec3(half_size, 0, -half_size),
                position + Vec3(0, 0, half_size),
            ]
            uvs = [
                uv_bottom_left,
                uv_bottom_right,
                uv_top_center,
            ]
        else:
            raise ValueError(f"Unsupported plane: {plane}")

        self.vertices.extend(vertices)
        self.uvs.extend(uvs)

        tri_start = len(self.vertices) - 3
        self.triangles.extend([tri_start, tri_start + 1, tri_start + 2])

if __name__ == '__main__':
    
    
    app = Ursina()
    texture_atlas = 'texture_atlas_spheres.png'
    custom_mesh = CustomMesh(
        texture_atlas=texture_atlas, 
        spacing='random', 
        spacing_range=(2, 2, 2), 
        double_sided=True,
        planes=['xy', 'zy', 'xz'], 
        # shape='triangle',
        shape='quad',
        # point_count=33,
        point_count=222333,
        )
    EditorCamera()
    app.run()
    
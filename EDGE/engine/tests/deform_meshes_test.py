from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import floor, ceil


def distance_3d(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5


def find_related_vertices(x, y, z, distance=1):
    related_vertices = []
    for x_offset in range(-distance, distance + 1):
        for y_offset in range(-distance, distance + 1):
            for z_offset in range(-distance, distance + 1):
                x_neighbor = x + x_offset
                y_neighbor = y + y_offset
                z_neighbor = z + z_offset
                if 0 <= x_neighbor < w and 0 <= y_neighbor < d and 0 <= z_neighbor < h:
                    related_vertices.append((x_neighbor, y_neighbor, z_neighbor))
    return related_vertices


app = Ursina()

hit_plane = Entity(model='plane', collider='box', scale=100, alpha=.2, visible=False)
cursor = Entity(model='sphere', color=color.azure, scale=.1)

w, h, d = 16, 16, 16
centering_offset = Vec2(-.5, -.5)

terrain = Entity(model=Mesh(vertices=[], triangles=[], uvs=[], colors=[]), scale=(w, d, h), y=-.01, texture='grass', collider='box')
terrain.scale *= 5

i = 0
for z in range(h):
    for x in range(w):
        for y in range(d):
            terrain.model.vertices.append(Vec3(x / w + centering_offset.x, y / d, z / h + centering_offset.y))
            terrain.model.uvs.append((x / w, z / h))

            if x > 0 and z > 0 and y > 0:
                terrain.model.triangles.append((i, i - 1, i - w - 1, i - w - 0, i - w * h - 1, i - w * h - 0))

            i += 1

terrain.model.generate()

terrain.model.height_values = [[[0 for x in range(w)] for y in range(h)] for z in range(d)]
ec = EditorCamera(rotation_smoothing=0, enabled=1, rotation=(30, 30, 0))

strength = 5


def update():
    if mouse.world_point:
        cursor.position = mouse.world_point

        x_idx = int(cursor.x / (terrain.scale_x / w) + w / 2)
        y_idx = int(cursor.y / (terrain.scale_y / d) + d / 2)
        z_idx = int(cursor.z / (terrain.scale_z / h) + h / 2)

        neighbors = find_related_vertices(x_idx, y_idx, z_idx, distance=3)

        for x, y, z in neighbors:
            brush_falloff = 1 - (distance_3d((x_idx, y_idx, z_idx), (x, y, z)) / 4)

            if not held_keys['shift']:
                if not held_keys['alt']:
                    terrain.model.height_values[x][y][z] += strength * brush_falloff * time.dt
                else:
                    terrain.model.height_values[x][y][z] -= strength * brush_falloff * time.dt

        terrain.model.vertices = []
        terrain.model.colors = []

        for z, depth in enumerate(terrain.model.height_values):
            for x, row in enumerate(depth):
                for y, height in enumerate(row):
                    terrain.model.vertices.append(Vec3(x / w, terrain.model.height_values[x][y][z], z / h) + Vec3(centering_offset.x, 0, centering_offset.y))
                    terrain.model.colors.append(hsv(0, 0, 1 - (terrain.model.height_values[x][y][z] * 1)))

        terrain.model.generate()


player = Entity(model='cube')


def input(key):
    if key == 'tab':
        ec.enabled = not ec.enabled
        player.enabled = not player.enabled


DirectionalLight().look_at(Vec3(-.5, -1, -1))
app.run()

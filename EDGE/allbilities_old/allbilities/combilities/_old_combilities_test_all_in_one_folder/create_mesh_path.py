import warnings 

from print_tricks import pt
from ursina import * 

from math import radians
from ursina import distance
from math import atan2, pi

from PIL import Image, ImageDraw





def remove_close_vertices(vertices, threshold):
    unique_vertices = [vertices[0]]
    for vertex in vertices[1:]:
        if distance(vertex, unique_vertices[-1]) > threshold:
            unique_vertices.append(vertex)
    return unique_vertices





def generate_star_points(arms, radius=1):
    points = []
    angle_step = 360 / (arms * 2)
    for i in range(arms * 2):
        angle = radians(i * angle_step)
        if i % 2 == 0:
            points.append(Vec2(cos(angle) * radius, sin(angle) * radius))
        else:
            points.append(Vec2(cos(angle) * radius / 2, sin(angle) * radius / 2))
    return points


class Mesh_Creator:
    """
    Create a 3D mesh from a list of vertices and cross-section shape(s).

    Args:
        vertices (list): A list of Vec3 points that define the path of the mesh.
        height (float, optional): The height of the cross-section. If only height is provided, width is set to the same value.
        width (float, optional): The width of the cross-section. If only width is provided, height is set to the same value.
        diameter (float, optional): The diameter of the cross-section. If diameter is provided and neither height nor width is specified, both are set to the value of diameter.
        num_sides (int, optional): The number of sides for the cross-section. If provided, a regular polygon with this number of sides will be used as the cross-section. Ignored if custom_shapes is provided.
        custom_shapes (list or dict, optional): Either a list of Vec2 points defining a custom cross-section shape or a dictionary where keys are indices and values are lists of Vec2 points defining custom cross-section shapes at those indices. Overrides num_sides if provided.
        rotation (int, optional): The rotation of the cross-section in degrees.
        interpolate (bool, optional): Whether to interpolate the height and width values between vertices.
        debug_uvs (bool, optional): If set to True, a UV map will be generated for debugging purposes.

    Returns:
        tuple: Contains four lists: the new vertices, the triangles (which define the faces of the mesh), the UV coordinates for texturing, and the normals for each vertex.

    Code Breakdown:
        1 - Initializes empty lists for the new vertices, triangles, UV coordinates, and normals of the mesh.
        2 - Loops over each vertex in the input list.
        3 - Selects the shape associated with the largest key that is less than or equal to the current index from the custom_shapes dictionary. This shape is then scaled by the height and width at the current index.
        4 - If the number of vertices in the current shape is less than num_sides, it duplicates some vertices until the length of scaled_shape matches num_sides.
        5 - Calculates the base index for the current cross-section.
        6 - Loops over each side of the cross-section.
        7 - Calculates a new vertex by adding the scaled shape to the current vertex and appends it to the new_vertices list.
        8 - Calculates the UV coordinates for the new vertex and appends them to the new_uvs list.
        9 - Calculates the normal of the new vertex and appends it to the new_normals list.
        10 - If the current vertex is not the last one, it generates the triangles that connect the current cross-section to the next one and appends them to the triangles list.

    The result of this code is a 3D mesh that follows the path defined by the input vertices, with a cross-section at each vertex defined by the custom_shapes, height, and width parameters.
    """

    
    def convert_model_to_cross_sections(self):
        ...
    def create_mesh_data(self, 
        vertices, 
        height=None, 
        width=None, 
        diameter=1, 
        num_sides=8, 
        custom_shapes=None, 
        rotation=0, 
        interpolate=True,
        debug_uvs=False
        ):

        # If only height is provided, set width to the same value
        if height is not None and width is None:
            width = height

        # If only width is provided, set height to the same value
        if width is not None and height is None:
            height = width

        # If dimension is provided and neither height nor width is specified, set both to the value of dimension
        if diameter is not None and height is None and width is None:
            height = diameter
            width = diameter
            
            
        height_radius = self.interpolate_dimension(height, vertices, interpolate)
        width_radius = self.interpolate_dimension(width, vertices, interpolate)
        
        if custom_shapes is None:
            num_sides = num_sides if num_sides is not None else 4  # Default to a square (cube) cross-section
            custom_shapes = {i: [Vec2(cos(radians(j * 360 / num_sides + rotation)), sin(radians(j * 360 / num_sides + rotation))) for j in range(num_sides)] for i in range(len(vertices))}
        elif isinstance(custom_shapes, list):
            num_sides = len(custom_shapes)
            custom_shapes = {i: custom_shapes for i in range(len(vertices))}
        else:
            num_sides = max(len(shape) for shape in custom_shapes.values())  # Get the maximum length of the custom shapes in the dictionary
            custom_shapes = {i: [Vec2(v.x * cos(radians(rotation)) - v.y * sin(radians(rotation)), v.x * sin(radians(rotation)) + v.y * cos(radians(rotation))) for v in shape] for i, shape in custom_shapes.items()}

        new_vertices, triangles, new_uvs, new_normals = [], [], [], []

        for i, vertex in enumerate(vertices):
            # Select the shape associated with the largest key that is less than or equal to the current index
            shape_key = max(k for k in custom_shapes.keys() if k <= i)
            scaled_shape = [Vec2(v.x * width_radius[i], v.y * height_radius[i]) for v in custom_shapes[shape_key]]
            # If the number of vertices in the current shape is less than num_sides, duplicate some vertices
            while len(scaled_shape) < num_sides:
                scaled_shape.append(scaled_shape[-1])

            base_index = i * num_sides
            for j in range(num_sides):
                new_vertex = Vec3(vertex.x + scaled_shape[j].x, vertex.y + scaled_shape[j].y, vertex.z)
                new_vertices.append(new_vertex)

                u = j / num_sides
                v = i / len(vertices)
                new_uvs.append(Vec2(u, v))

                normal = (new_vertex - vertex).normalized()
                new_normals.append(normal)

            if i < len(vertices) - 1:
                for j in range(num_sides):
                    next_j = (j + 1) % num_sides
                    triangles.extend([
                        [base_index + num_sides + next_j, base_index + next_j, base_index + j],
                        [base_index + num_sides + j, base_index + num_sides + next_j, base_index + j]
                    ])




        front_center_vertex = Vec3(vertices[0].x, vertices[0].y, vertices[0].z)
        new_vertices.append(front_center_vertex)
        front_center_index = len(new_vertices) - 1
        for i in range(num_sides):
            next_i = (i + 1) % num_sides
            triangles.append([front_center_index, i, next_i])

        back_center_vertex = Vec3(vertices[-1].x, vertices[-1].y, vertices[-1].z)
        new_vertices.append(back_center_vertex)
        back_center_index = len(new_vertices) - 1
        base_index = (len(vertices) - 1) * num_sides
        for i in range(num_sides):
            next_i = (i + 1) % num_sides
            triangles.append([back_center_index, base_index + next_i, base_index + i])

        if debug_uvs:
            self.debug_uv_map(triangles, new_uvs)
        
        return new_vertices, triangles, new_uvs, new_normals
    
    def interpolate_dimension(self, dimension, vertices, interpolate=True):
        """
        Interpolate dimension values based on the type of input and convert them to radius.

        Args:
            dimension (int, float, list, dict): The dimension (height or width) to be used for the mesh.
            vertices (list): The list of vertices for the mesh.
            interpolate (bool): Whether to interpolate between the dimension values.

        Returns:
            list: A list of interpolated dimensions (radius) for each vertex.
        """
        if isinstance(dimension, (int, float)):  # if a single dimension is provided
            return [(dimension / 2)] * len(vertices)  # create a list with the same dimension for all vertices

        elif isinstance(dimension, list):  # if a list of dimensions is provided
            dimension = [d / 2 for d in dimension]  # convert dimensions to radius
            if len(dimension) == 3:  # if a list of three dimensions is provided
                if interpolate:
                    dimension = [dimension[0]] + [dimension[0] + (dimension[1] - dimension[0]) * (i / (len(vertices) // 2)) for i in range(1, len(vertices) // 2)] + \
                        [dimension[1] + (dimension[2] - dimension[1]) * (i / (len(vertices) // 2)) for i in range(len(vertices) // 2)]
                else:
                    dimension = [dimension[0]] * (len(vertices) // 3) + [dimension[1]] * (len(vertices) // 3) + [dimension[2]] * (len(vertices) - 2 * (len(vertices) // 3))
            elif len(dimension) != len(vertices):
                raise ValueError("The length of the dimension list must match the length of the vertices list.")
            return dimension

        elif isinstance(dimension, dict):  # if a dictionary of dimensions is provided
            keys = sorted(dimension.keys())
            full_dimension = []
            for i in range(len(keys) - 1):
                if interpolate:
                    for j in range(keys[i], keys[i+1]):
                        t = (j - keys[i]) / (keys[i+1] - keys[i])  # calculate interpolation factor
                        d = (dimension[keys[i]] / 2) * (1 - t) + (dimension[keys[i+1]] / 2) * t  # interpolate dimension and convert to radius
                        full_dimension.append(d)
                else:
                    full_dimension.extend([(dimension[keys[i]] / 2)] * (keys[i+1] - keys[i]))
            full_dimension.append(dimension[keys[-1]] / 2)
            dimension = full_dimension

        if isinstance(dimension, list) and len(dimension) < len(vertices):
            dimension += [dimension[-1]] * (len(vertices) - len(dimension))
        return dimension
    

    def adjust_model_to_path_with_multiple_clones_of_parts_of_model(self, model, path_vertices):
        distances = [distance(path_vertices[i], path_vertices[i+1]) for i in range(len(path_vertices)-1)]

        total_distance = sum(distances)
        
        new_triangles = []
        
        original_vertices = model.vertices.copy()
        
        for i, dist in enumerate(distances):
            closest_vertices = [v for v in original_vertices if v[2] < dist]
            
            for v in closest_vertices:
                model.vertices.append((v[0], v[1], v[2] + dist))
            
            for t in model.triangles:
                new_triangles.append([t[0] + i*len(closest_vertices), t[1] + i*len(closest_vertices), t[2] + i*len(closest_vertices)])
        
        model.triangles = new_triangles
        model.generate()
        return model


    def adjust_model_to_path_close(self, model, path_vertices):
        distances = [distance(path_vertices[i], path_vertices[i+1]) for i in range(len(path_vertices)-1)]
        total_distance = sum(distances)
        new_triangles = []
        model.vertices = [(v[0] * total_distance, v[1] * total_distance, v[2] * total_distance) for v in model.vertices]
        original_vertices = model.vertices.copy()

        vertices_per_section = len(model.vertices) // len(path_vertices)

        for i, dist in enumerate(distances):
            closest_vertices = [v for v in original_vertices if v[2] < dist]
            for v in closest_vertices:
                model.vertices.append((v[0], v[1], v[2] + dist))
            for t in model.triangles:
                new_triangles.append([t[0] + i*len(closest_vertices), t[1] + i*len(closest_vertices), t[2] + i*len(closest_vertices)])

            # Calculate the indices of the vertices in this section
            start_index = i * vertices_per_section
            end_index = start_index + vertices_per_section

            # Calculate the center point of this section
            section_vertices = model.vertices[start_index:end_index]
            section_center = Vec3(sum(vertex[0] for vertex in section_vertices) / len(section_vertices),
                                sum(vertex[1] for vertex in section_vertices) / len(section_vertices),
                                sum(vertex[2] for vertex in section_vertices) / len(section_vertices))

            # Calculate the displacement for this section
            displacement = path_vertices[i] - section_center

            # Adjust the vertices in this section
            for j in range(start_index, end_index):
                model.vertices[j] = tuple(Vec3(*model.vertices[j]) + displacement)

        model.triangles = new_triangles
        model.generate()
        return model



    def adjust_model_to_path_no_adjustment_yet(self, model, path_vertices):
        distances = [distance(path_vertices[i], path_vertices[i+1]) for i in range(len(path_vertices)-1)]

        total_distance = sum(distances)
            
        new_triangles = []
            
        # Scale the vertices in the z direction
        # model.vertices = [(v[0], v[1], v[2] * total_distance) for v in model.vertices]
        # Scale in all directions
        model.vertices = [(v[0] * total_distance, v[1] * total_distance, v[2] * total_distance) for v in model.vertices]

        original_vertices = model.vertices.copy()
            
        # # Scale the vertices in the z direction
        # original_vertices = [(v[0], v[1], v[2] * total_distance) for v in original_vertices]
            
        for i, dist in enumerate(distances):
            # Find the closest vertices to the right of this point
            closest_vertices = [v for v in original_vertices if v[2] < dist]
                
            # Duplicate the closest vertices and place them at this distance
            for v in closest_vertices:
                model.vertices.append((v[0], v[1], v[2] + dist))
                
            # Adjust the triangles to account for the new vertices
            for t in model.triangles:
                new_triangles.append([t[0] + i*len(closest_vertices), t[1] + i*len(closest_vertices), t[2] + i*len(closest_vertices)])
            
        model.triangles = new_triangles
        # pt(model.vertices)
        model.generate()
        return model
    

    def debug_uv_map(self, triangles, new_uvs):
        # Define the resolution of the image
        width, height = 1024, 1024

        # Create a new image with the defined resolution
        img = Image.new('RGB', (width, height))

        # Create a draw object
        draw = ImageDraw.Draw(img)

        # Iterate over the triangles
        for triangle in triangles:
            # Check if the indices in triangle are within the range of new_uvs
            if all(index < len(new_uvs) for index in triangle):
                # Get the UV coordinates of the vertices of the triangle
                uv1 = new_uvs[triangle[0]]
                uv2 = new_uvs[triangle[1]]
                uv3 = new_uvs[triangle[2]]

                # Scale the UV coordinates to match the image resolution
                x1, y1 = int(uv1.x * (width - 1)), int(uv1.y * (height - 1))
                x2, y2 = int(uv2.x * (width - 1)), int(uv2.y * (height - 1))
                x3, y3 = int(uv3.x * (width - 1)), int(uv3.y * (height - 1))

                # Draw the triangle
                draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill='white', outline='black')
        # Save the image
        img.save('uv_map.png')

        # Display the image
        img.show()

if __name__ == '__main__':
    test_path_vertices = [Vec3(-0.005, -0.005, -0.005), Vec3(0.005, -0.005, -0.005), Vec3(0.005, 0.005, -0.005), Vec3(-0.005, 0.005, -0.005), Vec3(-0.005, -0.005, 0.005), Vec3(0.005, -0.005, 0.005), Vec3(0.005,
        0.005, 0.005), Vec3(-0.005, 0.005, 0.005), Vec3(-0.005, -0.005, -0.005), Vec3(0.005, -0.005, -0.005), Vec3(0.005, 0.005, -0.005), Vec3(-0.005, 0.005, -0.005), Vec3(-0.005, -0.005, 0.005),
        Vec3(0.005, -0.005, 0.005), Vec3(0.005, 0.005, 0.005), Vec3(-0.005, 0.005, 0.005), Vec3(-0.005, 0.106964, 0.0264391), Vec3(0.005, 0.106964, 0.0264391), Vec3(0.005, 0.116964, 0.0264391),
        Vec3(-0.005, 0.116964, 0.0264391), Vec3(-0.005, 0.106964, 0.0364391), Vec3(0.005, 0.106964, 0.0364391), Vec3(0.005, 0.116964, 0.0364391), Vec3(-0.005, 0.116964, 0.0364391), Vec3(-0.005,
        0.217521, 0.12036), Vec3(0.005, 0.217521, 0.12036), Vec3(0.005, 0.227521, 0.12036), Vec3(-0.005, 0.227521, 0.12036), Vec3(-0.005, 0.217521, 0.13036), Vec3(0.005, 0.217521, 0.13036),
        Vec3(0.005, 0.227521, 0.13036), Vec3(-0.005, 0.227521, 0.13036), Vec3(-0.005, 0.325279, 0.275583), Vec3(0.005, 0.325279, 0.275583), Vec3(0.005, 0.335279, 0.275583), Vec3(-0.005, 0.335279,
        0.275583), Vec3(-0.005, 0.325279, 0.285583), Vec3(0.005, 0.325279, 0.285583), Vec3(0.005, 0.335279, 0.285583), Vec3(-0.005, 0.335279, 0.285583), Vec3(-0.005, 0.527032, 0.761379),
        Vec3(0.005, 0.527032, 0.761379), Vec3(0.005, 0.537032, 0.761379), Vec3(-0.005, 0.537032, 0.761379), Vec3(-0.005, 0.527032, 0.771379), Vec3(0.005, 0.527032, 0.771379), Vec3(0.005, 0.537032,
        0.771379), Vec3(-0.005, 0.537032, 0.771379), Vec3(-0.005, 0.61849, 1.08584), Vec3(0.005, 0.61849, 1.08584), Vec3(0.005, 0.62849, 1.08584), Vec3(-0.005, 0.62849, 1.08584), Vec3(-0.005,
        0.61849, 1.09584), Vec3(0.005, 0.61849, 1.09584), Vec3(0.005, 0.62849, 1.09584), Vec3(-0.005, 0.62849, 1.09584), Vec3(-0.005, 0.702107, 1.45947), Vec3(0.005, 0.702107, 1.45947),
        Vec3(0.005, 0.712107, 1.45947), Vec3(-0.005, 0.712107, 1.45947), Vec3(-0.005, 0.702107, 1.46947), Vec3(0.005, 0.702107, 1.46947), Vec3(0.005, 0.712107, 1.46947), Vec3(-0.005, 0.712107,
        1.46947), Vec3(-0.005, 0.841724, 2.33484), Vec3(0.005, 0.841724, 2.33484), Vec3(0.005, 0.851724, 2.33484), Vec3(-0.005, 0.851724, 2.33484), Vec3(-0.005, 0.841724, 2.34484), Vec3(0.005,
        0.841724, 2.34484), Vec3(0.005, 0.851724, 2.34484), Vec3(-0.005, 0.851724, 2.34484), Vec3(-0.005, 0.895969, 2.82558), Vec3(0.005, 0.895969, 2.82558), Vec3(0.005, 0.905969, 2.82558),
        Vec3(-0.005, 0.905969, 2.82558), Vec3(-0.005, 0.895969, 2.83558), Vec3(0.005, 0.895969, 2.83558), Vec3(0.005, 0.905969, 2.83558), Vec3(-0.005, 0.905969, 2.83558), Vec3(-0.005, 0.938883,
        3.3436), Vec3(0.005, 0.938883, 3.3436), Vec3(0.005, 0.948883, 3.3436), Vec3(-0.005, 0.948883, 3.3436), Vec3(-0.005, 0.938883, 3.3536), Vec3(0.005, 0.938883, 3.3536), Vec3(0.005, 0.948883,
        3.3536), Vec3(-0.005, 0.948883, 3.3536), Vec3(-0.005, 0.988712, 4.43518), Vec3(0.005, 0.988712, 4.43518), Vec3(0.005, 0.998712, 4.43518), Vec3(-0.005, 0.998712, 4.43518), Vec3(-0.005,
        0.988712, 4.44518), Vec3(0.005, 0.988712, 4.44518), Vec3(0.005, 0.998712, 4.44518), Vec3(-0.005, 0.998712, 4.44518), Vec3(-0.005, 0.995, 4.995), Vec3(0.005, 0.995, 4.995), Vec3(0.005,
        1.005, 4.995), Vec3(-0.005, 1.005, 4.995), Vec3(-0.005, 0.995, 5.005), Vec3(0.005, 0.995, 5.005), Vec3(0.005, 1.005, 5.005), Vec3(-0.005, 1.005, 5.005), Vec3(-0.005, 0.988712, 5.55482),
        Vec3(0.005, 0.988712, 5.55482), Vec3(0.005, 0.998712, 5.55482), Vec3(-0.005, 0.998712, 5.55482), Vec3(-0.005, 0.988712, 5.56482), Vec3(0.005, 0.988712, 5.56482), Vec3(0.005, 0.998712,
        5.56482), Vec3(-0.005, 0.998712, 5.56482), Vec3(-0.005, 0.938883, 6.6464), Vec3(0.005, 0.938883, 6.6464), Vec3(0.005, 0.948883, 6.6464), Vec3(-0.005, 0.948883, 6.6464), Vec3(-0.005,
        0.938883, 6.6564), Vec3(0.005, 0.938883, 6.6564), Vec3(0.005, 0.948883, 6.6564), Vec3(-0.005, 0.948883, 6.6564), Vec3(-0.005, 0.895969, 7.16442), Vec3(0.005, 0.895969, 7.16442),
        Vec3(0.005, 0.905969, 7.16442), Vec3(-0.005, 0.905969, 7.16442), Vec3(-0.005, 0.895969, 7.17442), Vec3(0.005, 0.895969, 7.17442), Vec3(0.005, 0.905969, 7.17442), Vec3(-0.005, 0.905969,
        7.17442), Vec3(-0.005, 0.841724, 7.65516), Vec3(0.005, 0.841724, 7.65516), Vec3(0.005, 0.851724, 7.65516), Vec3(-0.005, 0.851724, 7.65516), Vec3(-0.005, 0.841724, 7.66516), Vec3(0.005,
        0.841724, 7.66516), Vec3(0.005, 0.851724, 7.66516), Vec3(-0.005, 0.851724, 7.66516), Vec3(-0.005, 0.702107, 8.53053), Vec3(0.005, 0.702107, 8.53053), Vec3(0.005, 0.712107, 8.53053),
        Vec3(-0.005, 0.712107, 8.53053), Vec3(-0.005, 0.702107, 8.54053), Vec3(0.005, 0.702107, 8.54053), Vec3(0.005, 0.712107, 8.54053), Vec3(-0.005, 0.712107, 8.54053), Vec3(-0.005, 0.61849,
        8.90416), Vec3(0.005, 0.61849, 8.90416), Vec3(0.005, 0.62849, 8.90416), Vec3(-0.005, 0.62849, 8.90416), Vec3(-0.005, 0.61849, 8.91416), Vec3(0.005, 0.61849, 8.91416), Vec3(0.005, 0.62849,
        8.91416), Vec3(-0.005, 0.62849, 8.91416), Vec3(-0.005, 0.527032, 9.22862), Vec3(0.005, 0.527032, 9.22862), Vec3(0.005, 0.537032, 9.22862), Vec3(-0.005, 0.537032, 9.22862), Vec3(-0.005,
        0.527032, 9.23862), Vec3(0.005, 0.527032, 9.23862), Vec3(0.005, 0.537032, 9.23862), Vec3(-0.005, 0.537032, 9.23862), Vec3(-0.005, 0.325279, 9.71442), Vec3(0.005, 0.325279, 9.71442),
        Vec3(0.005, 0.335279, 9.71442), Vec3(-0.005, 0.335279, 9.71442), Vec3(-0.005, 0.325279, 9.72442), Vec3(0.005, 0.325279, 9.72442), Vec3(0.005, 0.335279, 9.72442), Vec3(-0.005, 0.335279,
        9.72442), Vec3(-0.005, 0.217521, 9.86964), Vec3(0.005, 0.217521, 9.86964), Vec3(0.005, 0.227521, 9.86964), Vec3(-0.005, 0.227521, 9.86964), Vec3(-0.005, 0.217521, 9.87964), Vec3(0.005,
        0.217521, 9.87964), Vec3(0.005, 0.227521, 9.87964), Vec3(-0.005, 0.227521, 9.87964), Vec3(-0.005, -0.005, 9.995), Vec3(0.005, -0.005, 9.995), Vec3(0.005, 0.005, 9.995), Vec3(-0.005, 0.005,
        9.995), Vec3(-0.005, -0.005, 10.005), Vec3(0.005, -0.005, 10.005), Vec3(0.005, 0.005, 10.005), Vec3(-0.005, 0.005, 10.005)
    ]

    test_path_vertices = remove_close_vertices(test_path_vertices, threshold=0.1)

    app = Ursina()

    scenarios = [
        {"num_sides": 4},
        
        {"num_sides": 4, "rotation": 45},
        
        {"num_sides": 8},
        
        {"custom_shapes": generate_star_points(4), "height": 0.5, "width":0.5},
        
        {"custom_shapes": generate_star_points(4), "rotation": 45, "height": 0.5, "width":0.5},
        
        {"custom_shapes": {0: generate_star_points(4), 8: generate_star_points(7)}, "rotation": 45, 
            "height": 0.5, "width":0.5},
        
        {"num_sides": 5, "custom_shapes": generate_star_points(7), "height": 0.5, "width":0.5},
        
        {"num_sides": 3, "diameter": 0.5, 'rotation': 90},
        
        {"num_sides": 3, "height": 0.5, 'rotation': -90},
        
        {"height": [0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4],
            "width": [0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4]},
        
        {"height": {0: 0.1, len(test_path_vertices) // 2: 1.0, len(test_path_vertices) - 1: 0.1},
            "width": {0: 0.1, len(test_path_vertices) // 2: 1.0, len(test_path_vertices) - 1: 0.1}},
        
        {"height": [0.1, 1.0, 0.1],
            "width": [0.1, 1.0, 0.1]},
        
        {"interpolate": False, "height": [0.2, 1.0, 0.2]},
        
        {"height": [0.1, 0.0, 0.1], "interpolate": False},
        
        {"interpolate": True, "height": [0.2, 0.0, 0.2]},
        
        {"height": {0: 1.0, 10: 2.0, len(test_path_vertices) // 2: 2.0, len(test_path_vertices) - 1: 1.0},
            "width": {0: 2.0, 10: 1.0, len(test_path_vertices) // 2: 0.5, len(test_path_vertices) - 1: 1.0}}
    ]
    
    c = Mesh_Creator()
    spacing = 1.5
    for i, scenario in enumerate(scenarios):
        new_vertices, triangles, new_uvs, new_normals = c.create_mesh_data(test_path_vertices, **scenario)

        mesh = Mesh(vertices=new_vertices, triangles=triangles, uvs=new_uvs, normals=new_normals, mode='triangle')
        path_mesh = Mesh(vertices=test_path_vertices, mode='point', thickness=.005)
        wireframe_mesh = Mesh(vertices=new_vertices, triangles=triangles, mode='line')
        points_mesh = Mesh(vertices=new_vertices, mode='point', thickness=.005, render_points_in_3d=True)

        box_entity = Entity(model=mesh, texture='brick', texture_scale=(1,3), color=color.azure, double_sided=False, x=i*spacing)
        path_entity = Entity(model=path_mesh, color=color.yellow, always_on_top=True, x=i*spacing)
        wireframe_entity = Entity(model=wireframe_mesh, color=color.red, x=i*spacing)
        points_entity = Entity(model=points_mesh, color=color.blue, x=i*spacing)

    # # # Add a light source
    # # light = DirectionalLight(parent=scene, x=10, y=10, z=10, shadows=True)
    



    arrow = load_model("arrow1", use_deepcopy=True)
    curved_arrow_model = c.adjust_model_to_path(arrow, test_path_vertices)
    curved_arrow = Entity(model=curved_arrow_model, double_sided=True, x=-11, z=10)




    
    EditorCamera()
    app.run()
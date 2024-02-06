from ursina import *
from print_tricks import pt
app = Ursina()

''' NOTE: Supposed to help me add points to models for collision detection and LOD's

TODO 1:
- Currently my logic is flawed I believe when generating new verts @ gen_new_verts()
- It should be taking the 1st and 2nd verts, finding the midpoint, adding it to a list, then finding the 2nd and 3rd verts, finding their midpoint
etc. But when I compare the quad.model.vertices with the new_verts I don't quite get that. 

TODO 2:
- Once I can complete generating the correct vertices, I then need to gen 
the correct uvs or normals or both, so I can texture and shade the models and actually
see them in 3d. 

'''



def hd(iterable):
    seen = set()
    for x in iterable:
        # if x[0] in 
        for i in x:
            if x[i] in seen[0]:
                pt(x)
                return True
            seen.add(x)
        return False

def method_B():

    test_tuple = (("A", "B"), ("C", "D"), ("E", "A"))

    for count, x in enumerate(test_tuple):
        for i in test_tuple:
            if x[count] in test_tuple[count]:
                pt('yes')
                pt(x[0])
                pt(i)
            else:
                pt('no')

def gen_new_verts(Entity):
    qv = quad.model.vertices
    
    new_verts = []
    vert_pairs = []
    pair = 1
    
    for vert in qv:
        # get verts
        x = vert[0]
        y = vert[1]
        z = vert[2]
        
        if pair == 1: 
            # if this is the first pair in the group:
            # vert_pairs.append((x, y, z))
            vert_pairs = [(x, y, z)]
            pair = 2
            
        elif pair == 2:
            # if there is already one pair in the group:
            # get the first x,y,z of the pair
            x1 = vert_pairs[0][0]
            y1 = vert_pairs[0][1]
            z1 = vert_pairs[0][2]
            
            # get the midpoint by adding the first pair and the 2nd then /2
            mid_x = (x1 + x) / 2 
            mid_y = (y1 + y) / 2 
            mid_z = (z1 + z) / 2 

            # reset the vert_pairs to just this second one (to establish this as the new first pair)
            # NOTE TODO is this doing anything? Or should we do this above under "if pair ==1:" ???
            # vert_pairs = [(x, y, z)]

            # add the first points of the pair, the new generated mid points, and the 2nd points of the pair
            new_verts.append((x1, y1, z1))
            new_verts.append((mid_x, mid_y, mid_z))
            new_verts.append((x, y, z))
            pair = 1
            

    pt(quad.model.vertices,
        new_verts,
        quad.model.triangles,
        quad.model.normals,
        quad.model.uvs)
    return new_verts

quad = Entity(model = load_model("cube", use_deepcopy=True))
qv = quad.model.vertices

new_verts = gen_new_verts(quad)

newquad = Entity(
    model = Mesh(
        vertices=new_verts, 
        triangles=None, 
        colors=None, 
        uvs=None, 
        normals=None, 
        static=True, 
        mode='triangle', 
        thickness=1
        ), 
    position = (2, 2, 2), 
    double_sided = True,
    )

# newquad.model.generate_normals()
# newquad.model.generate()

# pt.ex()

EditorCamera()
app.run()
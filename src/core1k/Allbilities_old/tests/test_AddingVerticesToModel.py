from ursina import *
#from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import *
import sys
sys.path.append("C:\.PythonProjects\Print Tricks")
from print_tricks import pt

from ursina.shaders import lit_with_shadows_shader

from math import sqrt

''' MINIMAL TEST DESIGNED TO ADD NEW VERTICES TO EXISTING MODEL '''
blah = 0
 
app = Ursina()

'''Combined code from:
1 http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html (for the t=__ function, and the base coords)

2 https://gist.github.com/scurest/3c67b60e900f4142436730eef8b68f92 (for the refinement method) (and WIP, for separate sphere creation function to call refinement method.)

3 https://www.alexisgiard.com/icosahedron-sphere/ (for calculating UVs from pre-exising vertices, see my gen_UVs() function)

4 (not yet) - http://www.mvps.org/directx/articles/spheremap.htm NOTE Not yet used, but could use it maybe for better uv mapping

5 (not yet) - http://codescrib.blogspot.com/ - For getting better refinements than the current (4 subdivisions everytime). Instead, can choose much more precisely how many triangles to generate. 

6 (not yet) - https://stackoverflow.com/questions/18578943/automatically-generating-uv-coordinates-algorithms - For different ways to simply calculate UV's using different methods. 

7 (not yet) - SEVERAL refinement methods, multiple ways to control how much to refine the sphere. All written out very plainly. https://www.opengl.org.ru/docs/pg/0208.html

8 (not yet) - How to manually UV unwrap, intelligently - https://web.archive.org/web/20170609143444/http://kiwi.atmos.colostate.edu/BUGS/geodesic/text.html

9 (superhedral) - guy built universe generator, thinking about same stuff I am https://superhedral.com/, though never completed. 

'''
yPos = 0
def startup():
    # Icosphere.create_Planet('self', 2)
    # Icosphere.create_Planet('self')

    ico = Icosphere()
    # ico.refine()
    global pl
    pl = ico.create_Planet(0)
    print(' what is pl? ')
    print(type(pl))
    print(pl)
class Icosphere:
    colors = (color.red, color.blue, color.lime, color.black)

    def vert(self, co, uv):
        mag = sqrt(sum([x**2 for x in co]))
        normalized = [x/mag for x in co]
        self.positions.append(normalized)
        self.uvs.append(uv)

    def __init__(self):
        """Build a regular icosahedron."""
        self.positions = []
        self.uvs = []
        self.tris = []
        ##### Create the 12 icosahedron vertices:
        t = (1. + math.sqrt(5.0)) / 2.0

        self.vert([ t,-1, 0], [0.0, 0.32379180882521663]  )
        self.vert([ t, 1, 0], [0.0, 0.6762081911747834]   )
        self.vert([-t,-1, 0], [0.5, 0.32379180882521663]  )
        self.vert([-t, 1, 0], [0.5, 0.6762081911747834]   )
        self.vert([-1, 0, t], [0.3381040955873917, 0.5]   )
        self.vert([ 1, 0, t], [0.16189590441260832, 0.5]  )
        self.vert([-1, 0,-t], [-0.3381040955873917, 0.5]  )
        self.vert([ 1, 0,-t], [-0.16189590441260832, 0.5] )
        self.vert([ 0, t,-1], [-0.25, 0.8237918088252166] )
        self.vert([ 0, t, 1], [0.25, 0.8237918088252166]  )
        self.vert([ 0,-t,-1], [-0.25, 0.17620819117478337])
        self.vert([ 0,-t, 1], [0.25, 0.17620819117478337] )

        ##### Triangles, in 4 groups of 5 each:
        self.tris = (
            ## 5 faces around point 0
            (0, 11, 5),
            (0, 5, 1),
            (0, 1, 7),
            (0, 7, 10),
            (0, 10, 11),
            ## adjacent faces to point 0
            (1, 5, 9),
            (5, 11, 4),
            (11, 10, 2),
            (10, 7, 6),
            (7, 1, 8),
            ## faces around point 3
            (3, 9, 4),
            (3, 4, 2),
            (3, 2, 6),
            (3, 6, 8),
            (3, 8, 9), 
            ## faces adjacent to p3
            (4, 9, 5),
            (2, 4, 11),
            (6, 2, 10),
            (8, 6, 7),
            (9, 8, 1)
        )

        self.norms = ((0,0,-1),) * len(self.positions)

        # UV_List = []
        # for verts in self.positions:
        #     # pt(verts)
        #     x = verts[0]
        #     y = verts[1]
        #     z = verts[2]
        #     thisUV = Icosphere.gen_UVs(x,y,z)
        #     UV_List.append(thisUV)
        # # print(UV_List)


    def refine(self):
        pt('refine')
        midpoint_cache = {}

        def midpoint(v1, v2):
            v1, v2 = sorted((v1, v2))

            if (v1, v2) in midpoint_cache:
                return midpoint_cache[(v1, v2)]

            midpos = [(x+y)/2 for x,y in zip(self.positions[v1], self.positions[v2])]
            miduv = [(x+y)/2 for x,y in zip(self.uvs[v1], self.uvs[v2])]
            self.vert(midpos, miduv)
            index = len(self.positions) - 1

            midpoint_cache[(v1, v2)] = index

            return index

        new_tris = []

        for tri in self.tris:
            #    /\           /\
            #   /  \   ==>   /__\
            #  /    \  ==>  /\  /\
            # /_____ \     /__\/__\
            a = midpoint(tri[0], tri[1])
            b = midpoint(tri[1], tri[2])
            c = midpoint(tri[2], tri[0])

            new_tris.append([tri[0], a, c])
            new_tris.append([tri[1], b, a])
            new_tris.append([tri[2], c, b])
            new_tris.append([a, b, c])

        self.tris = new_tris

        # global yPos
        # yPos +=3
        newPos = (-3,yPos,0)
        # e = Entity(model=Mesh(vertices=self.positions, triangles=self.tris, uvs=self.uvs), position =newPos, texture='muse_uv_01.png', tile_set=(100,100))

        return self.planet.model
        pass
    def gen_UVs(x,y,z):
        u = (math.atan2(z,x) / (2. * math.pi))
        v = (math.asin(y) / math.pi) + 0.5 

        return u,v
    def create_Planet(self, refinements=0):
        # Build an icosphere

        for _ in range(0, refinements):
            self.refine()
        
        self.planet = Entity(model=Mesh(vertices=self.positions, triangles=self.tris, uvs=self.uvs), position =(0,0,0), texture='muse_uv_01.png',
            collision=True, collider='sphere', on_click=touched)
        
        # project_uvs(model, aspect_ratio=1, direction='forward', regenerate=False)   
        # e.model.project_uvs()
        # points = Entity(model=Mesh(vertices=self.positions, mode='point', thickness=.01), color=color.red)
        # lines = Entity(model=Mesh(vertices=self.positions, triangles=self.tris, mode='line', thickness=2), color=color.cyan)
        

        return self.planet

    def planetTouched(self):
        global blah
        pt('planetTouched')
        
        verts1 = self.planet.model.vertices
        tris1 = self.planet.model.triangles
        uvs1 = self.planet.model.uvs
        norms1 = self.planet.model.normals 

        for i in range(1):
            newData = self.refine()
        pt(newData)
        # self.planet.model = newData
        # self.planet.model.generate()
        pass

        '''Create test cube'''
        verts = (
            ### bottom
            (-1,0,1), 
            (1,0,1), 
            (1, 0,-1), 
            (-1,0,-1), 
            ### top
            (-1,2,1), 
            (1,2,1), 
            (1, 2,-1), 
            (-1,2,-1),
            ### back
            (-1, 0, -1),
            (1, 0, -1), 
            (-1, 2, -1),
            (1,2,-1)
            )
        tris = (
            ## bottom
            0,1,2,
            0,2,3,
            ## top
            5,4,6,
            6,4,7,
            ## side R
            8,7,9,
            9,7,10
            )

        uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
        norms = ((0,0,-1),) * len(verts)

        # verts = self.planet.model.vertices
        # pt(verts)
        # tris = self.planet.model.triangles
        # uvs = self.planet.model.uvs
        # norms = self.planet.model.normals 

        pt(blah)
        print(blah)
        if blah == 0:
            pt('inside blah 0')
            self.planet.model.vertices = verts 
            self.planet.model.triangles = tris
            self.planet.model.uvs = uvs 
            self.planet.model.normals = norms
            self.planet.model.generate()
            blah = 1

        elif blah == 1:
            pt('inside blah 1')
            self.planet.model.vertices = verts1
            self.planet.model.triangles = tris1
            self.planet.model.uvs = uvs1
            self.planet.model.normals = norms1
            self.planet.model.generate()
            blah = 0
    pass

def update():
    # global pl
    # ve = pl.model.vertices[0][0]
    # ve +=.1
    # pt(ve)
    # pl.model.vertices[0][0] = ve
    # pl.model.generate()
    # Wait(1)
    pass

def touched():
        global pl
        pt('planetTouched')
        
        verts = pl.model.vertices
        tris = pl.model.triangles
        uvs = pl.model.uvs
        norms = pl.model.normals 

        for i in range(1):
            newData = AddMeshDetails.refine(level=3, ent=pl)
        # pt(newData)
        verts = newData[0]
        tris = newData[1]
        uvs = newData[2]
        norms = newData[3]
        pl.model = newData
        # self.planet.model.generate()
        pass
class AddMeshDetails:

    def vert(co, uv):
        positions=[]
        uvs = []
        mag = sqrt(sum([x**2 for x in co]))
        normalized = [x/mag for x in co]
        positions.append(normalized)
        uvs.append(uv)
        return positions, uvs

 
    def refine(level, ent=type(Entity)):
        pt('refine')
        em = ent.model
        global positions
        positions = em.vertices
        global uvs
        uvs = em.uvs
        tris = em.triangles
        norms = em.normals
        midpoint_cache = {}

        def midpoint(v1, v2):
            global positions
            global uvs
            v1, v2 = sorted((v1, v2))

            if (v1, v2) in midpoint_cache:
                return midpoint_cache[(v1, v2)]

            midpos = [(x+y)/2 for x,y in zip(positions[v1], positions[v2])]
            miduv = [(x+y)/2 for x,y in zip(uvs[v1], uvs[v2])]
            positions, uvs = AddMeshDetails.vert(midpos, miduv)
            index = len(positions) - 1

            midpoint_cache[(v1, v2)] = index

            return index

        new_tris = []

        for tri in tris:
            #    /\           /\
            #   /  \   ==>   /__\
            #  /    \  ==>  /\  /\
            # /_____ \     /__\/__\
            a = midpoint(tri[0], tri[1])
            b = midpoint(tri[1], tri[2])
            c = midpoint(tri[2], tri[0])

            new_tris.append([tri[0], a, c])
            new_tris.append([tri[1], b, a])
            new_tris.append([tri[2], c, b])
            new_tris.append([a, b, c])

        tris = new_tris

        # global yPos
        # yPos +=3

        return positions, tris, uvs, norms
        pass



















class CreateShapes:

    def create_spheres_old(self): 
        ''' the original. not sure how it's supposed to work but when it creates the pos=[x for v], it gets rid of   all internal lists of points, and just has it as one extremely long list)'''
        pt('create spheres')
        # Build an icosphere

        icosphere = Icosphere()
        for _ in range(0, 4):
            icosphere.refine()
        pos = [x for v in icosphere.positions for x in v]
        pt(pos)
        uvs = [x for v in icosphere.uvs for x in v]
        indices = [i for tri in icosphere.tris for i in tri]

        # assert(len(indices) < 2**16) # Make sure we can use u16 for the index data

        pass
    def modify_sphere(self):
        ### modify an existing sphere

        pass
class create_more_detail():
    ### This could be thought of as "create more detailed lods, etc"

    pass

class create_planet_system():
    def createBasePlanet(self):
        self.planet = CreateShapes.create_spheres('self', refinements=0)
        self.planet.collision = True
        self.planet.collider  = 'sphere'
        self.planet.on_click = create_planet_system.hit_getInfo
    def refine_existing(self, ent):
        en = ent.model
        verts = ent.vertices 
        tris = ent.triangles
        uvs = ent.uvs 
        norms = ent.normals
        midpoint_cache = {}


        def midpoint(v1, v2):
            v1, v2 = sorted((v1, v2))

            if (v1, v2) in midpoint_cache:
                return midpoint_cache[(v1, v2)]

            midpos = [(x+y)/2 for x,y in zip(self.positions[v1], self.positions[v2])]
            miduv = [(x+y)/2 for x,y in zip(self.uvs[v1], self.uvs[v2])]
            self.vert(midpos, miduv)
            index = len(self.positions) - 1

            midpoint_cache[(v1, v2)] = index

            return index

        new_tris = []

        for tri in self.tris:
            #    /\           /\
            #   /  \   ==>   /__\
            #  /    \  ==>  /\  /\
            # /_____ \     /__\/__\
            a = midpoint(tri[0], tri[1])
            b = midpoint(tri[1], tri[2])
            c = midpoint(tri[2], tri[0])

            new_tris.append([tri[0], a, c])
            new_tris.append([tri[1], b, a])
            new_tris.append([tri[2], c, b])
            new_tris.append([a, b, c])

        self.tris = new_tris

        pass
    def hit_getInfo(self):
        print('hit_getInfo')
        for _ in range(0, 4):
        # for _ in range(0):
            create_planet_system.refine_existing('self', self.planet)
            self.planet.model.generate()
    def doAction():
        print('hit1')     
    pass
class hitDetection():
    # def getInfo():
    #     print('hit')
    #     icosphere = Icosphere()
    #     global planet
    #     for _ in range(0, 4):
    #     # for _ in range(0):
    #         icosphere.refine()
    #         planet.model.generate()
         
    #     pass
    pass

startup()
# app.run()

if __name__ == '__main__':
    
    #### Controllers, Cameras, App Run
    nowController = EditorCamera(move_speed=15)
    nowController.y = 0
    nowController.rotation_x = 0
    camera.clip_plane_far = 100000
    camera.fov = 70

    mouse.enabled = True

    app.run() 

















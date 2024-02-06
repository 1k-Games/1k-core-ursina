import sys

from ursina.entity import Entity
from ursina.mesh import Mesh
from ursina.scene import instance as scene
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay
from ursina.vec3 import Vec3
from math import sqrt, inf, dist
from copy import copy
from ursina.hit_info import HitInfo
from ursina import ursinamath, color
from ursina.ursinastuff import destroy, invoke


_line_model = Mesh(vertices=[Vec3(0,0,0), Vec3(0,0,1)], mode='line', thickness=2)

_linecaster = Entity(add_to_scene_entities=False)
_linecaster._picker = CollisionTraverser()  # Make a traverser
_linecaster._pq = CollisionHandlerQueue()  # Make a handler
_linecaster._pickerNode = CollisionNode('_linecaster')
_linecaster._pickerNode.set_into_collide_mask(0)
_linecaster._pickerNP = _linecaster.attach_new_node(_linecaster._pickerNode)
_linecaster._picker.addCollider(_linecaster._pickerNP, _linecaster._pq)
_line = CollisionRay()
_line.setOrigin(Vec3(0,0,0))
_line.setDirection(Vec3(0,0,1))
_linecaster._pickerNode.addSolid(_line)


def linecast(
    origin, 
    destination, 
    distance=None, 
    traverse_target:Entity=scene, 
    ignore:list=None, 
    debug=False, 
    debug_time=.06, 
    color=color.white):
    
    if not ignore:
        ignore = []

    if distance is None:
        distance = dist(origin, destination)

    _linecaster.position = origin
    _linecaster.look_at(destination)

    if debug:
        temp = Entity(
            position=origin, 
            color=color, 
            model=copy(_line_model), 
            add_to_scene_entities=False,
            scale=Vec3(1,1,distance), 
            always_on_top=False,
        )
        temp.look_at(destination)
        destroy(temp, debug_time)

    _linecaster._picker.traverse(traverse_target)

    if _linecaster._pq.get_num_entries() == 0:
        _linecaster.hit = HitInfo(hit=False, distance=distance)
        return _linecaster.hit

    _linecaster._pq.sort_entries()
    entries = _linecaster._pq.getEntries()
    entities = [e.get_into_node_path().parent for e in entries]

    entries = [
        e for i, e in enumerate(entries)
        if entities[i] in scene.collidables
        and entities[i] not in ignore
        and ursinamath.distance(_linecaster.world_position, e.get_surface_point(render)) <= distance
        ]

    if len(entries) == 0:
        return HitInfo(hit=False)

    _linecaster.collision = entries[0]
    nP = _linecaster.collision.get_into_node_path().parent
    point = Vec3(*_linecaster.collision.get_surface_point(nP))
    world_point = Vec3(*_linecaster.collision.get_surface_point(render))

    hit_info = HitInfo(hit=True)
    hit_info.entities = [e.get_into_node_path().parent.getPythonTag('Entity') for e in entries]
    hit_info.entity = hit_info.entities[0]

    hit_info.point = point
    hit_info.world_point = world_point
    hit_info.distance = ursinamath.distance(_linecaster.world_position, hit_info.world_point)

    hit_info.normal = Vec3(*_linecaster.collision.get_surface_normal(_linecaster.collision.get_into_node_path().parent).normalized())
    hit_info.world_normal = Vec3(*_linecaster.collision.get_surface_normal(render).normalized())

    return hit_info

if __name__ == '__main__':
    '''
    linecast:
    
    Cast a ray from a specified origin to a destination point. 
    The length of the ray is either the distance between the origin and destination or a specified distance. 
    Returns a HitInfo object that contains information about what it hit. 
    Note that the ray will only interact with entities that have a collider.
    
    Use optional *traverse_target* to only be able to hit a specific entity and its children/descendants.
    Use optional *ignore* list to ignore certain entities.
    Setting debug to True will draw the line on screen.
    
    The following is an example of how you might use this function to detect intersecting through a wall:
    '''

    from ursina import *
    app = Ursina()

    class Player(Entity):
        def update(self):
            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                ).normalized()
            self.position += self.direction * 5 * time.dt
            
            
            hit_info = linecast(self.world_position + (self.up * .5), destination.world_position, 
                ignore=(self, destination), 
                debug=True
            )
            
            if hit_info.hit:
                print('Hit: ', hit_info.entity.name)

    player = Player(model='cube', origin_y=-.5, color=color.orange)
    destination = Entity(model = 'cube', parent = player, position = (4, .5, 0), scale = 0.5)
    wall = Entity(name='wall', model='cube', collider='box', scale_y=3, color=color.azure, position=(3,1.5,2))
    camera.y = 1
    
    EditorCamera()
    app.run()





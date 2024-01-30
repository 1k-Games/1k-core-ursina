'''
    Working:
        -Light_Position_Entity
        -Light_Position_Entity_Model
        
    Not Working:
        -Light_Entity
        -Light_Entity_Model
        
        '''

from print_tricks import *

from panda3d.core import NodePath
from ursina.vec3 import Vec3
from ursina.vec4 import Vec4

try:
    from ursina.scene import instance as scene
except:
    pass

class BaseEntity(NodePath):
    def __init__(self, parent=scene, **kwargs):
        super().__init__(self.__class__.__name__)
        self.parent = parent

    @property
    def parent(self):
        return self.getParent()

    @parent.setter
    def parent(self, value):
        if value is not None:
            self.reparentTo(value)
            parent_scale = self.getParent().getScale()
            self.setScale(1 / parent_scale[0], 1 / parent_scale[1], 1 / parent_scale[2])
            
class Light_Position_Entity(BaseEntity):
    def __init__(self, position=None, world_position=None, **kwargs):
        super().__init__(**kwargs)
        if position is not None:
            self.position = position
        if world_position is not None:
            self.world_position = world_position

    @property
    def position(self):
        return Vec3(*self.getPos())

    @position.setter
    def position(self, value):
        self.setPos(value[0], value[1], value[2])

    @property
    def world_position(self):
        return Vec3(*self.getPos(scene))

    @world_position.setter
    def world_position(self, value):
        self.setPos(scene, value[0], value[1], value[2])

class Light_Position_Model_Entity(Light_Position_Entity):
    def __init__(self, model=None, texture=None, color=None, **kwargs):
        from panda3d.core import NodePath
        from direct.actor.Actor import Actor
        
        super().__init__(**kwargs)
        
        self.actor = Actor()
        if model is not None:
            self.actor.loadModel('models/box')
        if texture is not None:
            self.actor.setTexture(texture)
        if color is not None:
            self.actor.setColor(color)
        self.actor.reparentTo(self)

    @property
    def model(self):
        return self.actor.getModel()

    @model.setter
    def model(self, value):
        self.actor.loadModel(value)

    @property
    def texture(self):
        return self.actor.getTexture()

    @texture.setter
    def texture(self, value):
        self.actor.setTexture(value)

    @property
    def color(self):
        return self.actor.getColor()

    @color.setter
    def color(self, value):
        self.actor.setColor(value)
        
class Light_Entity(BaseEntity):
    def __init__(self, position=Vec3(0,0,0), rotation=Vec3(0,0,0), scale=Vec3(1,1,1), world_position=Vec3(0,0,0), world_rotation=Vec3(0,0,0), world_scale=Vec3(1,1,1), **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.world_position = world_position
        self.world_rotation = world_rotation
        self.world_scale = world_scale

    @property
    def position(self):
        return Vec3(*self.getPos())

    @position.setter
    def position(self, value):
        self.setPos(value[0], value[1], value[2])

    @property
    def rotation(self):
        return Vec3(*self.getHpr())

    @rotation.setter
    def rotation(self, value):
        self.setHpr(value[0], value[1], value[2])

    @property
    def scale(self):
        return Vec3(*self.getScale())

    @scale.setter
    def scale(self, value):
        self.setScale(value[0], value[1], value[2])

    @property
    def world_position(self):
        return Vec3(*self.getPos(scene))

    @world_position.setter
    def world_position(self, value):
        self.setPos(scene, value[0], value[1], value[2])

    @property
    def world_rotation(self):
        return Vec3(*self.getHpr(scene))

    @world_rotation.setter
    def world_rotation(self, value):
        self.setHpr(scene, value[0], value[1], value[2])

    @property
    def world_scale(self):
        return Vec3(*self.getScale(scene))

    @world_scale.setter
    def world_scale(self, value):
        original_parent = self.getParent()
        self.reparentTo(scene)
        self.setScale(value[0], value[1], value[2])
        self.reparentTo(original_parent)


class Light_Entity_Model(Light_Entity):
    def __init__(self, model='models/box', texture=None, color=Vec4(1,1,1,1), **kwargs):
        from panda3d.core import NodePath
        from direct.actor.Actor import Actor
        
        super().__init__(**kwargs)
        
        self.actor = Actor()
        self.actor.loadModel(model)
        if texture is not None:
            self.actor.setTexture(texture)
        self.actor.setColor(color)
        self.actor.reparentTo(self)

    @property
    def model(self):
        return self.actor.getModel()

    @model.setter
    def model(self, value):
        self.actor.loadModel(value)

    @property
    def texture(self):
        return self.actor.getTexture()

    @texture.setter
    def texture(self, value):
        self.actor.setTexture(value)

    @property
    def color(self):
        return self.actor.getColor()

    @color.setter
    def color(self, value):
        self.actor.setColor(value)
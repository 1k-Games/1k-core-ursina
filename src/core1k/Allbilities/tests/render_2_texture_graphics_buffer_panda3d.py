''''''


from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

base = ShowBase()

altBuffer = base.win.makeTextureBuffer("hello", 256, 256)

altRender = NodePath("new render")

altCam = base.makeCamera(altBuffer)
altCam.reparentTo(altRender)
altCam.setPos(0, -10, 0)

teapot = base.loader.loadModel('teapot')
teapot.reparentTo(altRender)
teapot.setPos(0, 0, -1)
teapot.hprInterval(1.5, (360, 360, 360)).loop()

cube = base.loader.loadModel('models/box')  # Load the cube model
cube.setPos(0, 15, 0)
cube.reparentTo(base.render)
cube.setTexture(altBuffer.getTexture(), 1)  # Apply the texture to the cube

base.run()
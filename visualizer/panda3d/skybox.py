from panda3d.core import TextureStage, TexGenAttrib


class SkyBox:

    def __init__(self, base):
        self.base = base
        self.skybox_scale = 10000
        self.sky_box = None

        cube_map = loader.loadCubeMap('./textures/skybox/blue_#.png')
        self.sky_box = loader.loadModel('./models/inverted_box.glb')
        self.sky_box.setPos(self.base.cam, 0, 0, 0)
        self.sky_box.setScale(self.skybox_scale)
        self.sky_box.setBin('background', 0)
        self.sky_box.setDepthWrite(0)
        self.sky_box.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)
        self.sky_box.setTexture(cube_map, 1)
        self.sky_box.reparentTo(render)

        self.recenter_skybox_task = self.base.taskMgr.add(self.update_skybox, 'recenter_skybox')

    def update_skybox(self, task):
        self.sky_box.setPos(self.base.cam, 0, 0, 0)
        return task.cont

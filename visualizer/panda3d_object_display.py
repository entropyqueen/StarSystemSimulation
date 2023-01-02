import collections

from astropy import units as u
from direct.gui.OnscreenText import TextNode
from panda3d.core import LPoint3f, PointLight, AmbientLight, TextureStage, LineSegs, NodePath, LVecBase4f
import math

from utils import hex_to_rgb_norm
import config

class ObjectDisplay:

    def __init__(self, star_system_obj, model_path='./models/sphere.glb',
                 textures=None, units=u.AU, realist_view=False):

        self.zoom_factor = config.DEFAULT_ZOOM

        self.units = units
        self.realist_view = realist_view
        # Grab data from StarSystemObject
        self.obj = star_system_obj
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()
        self.history_size = config.HISTORY_SIZE
        self.history_points = collections.deque([], self.history_size)
        self.history_steps_ctr = 0
        self.history = []

        self.designation_name = self.obj.name.lower().replace(" ", "_")

        # Init object
        self.pos = self.compute_display_pos()
        self.obj_node_path = render.attachNewNode(f'{self.designation_name}_trajectory')
        self.obj_model = loader.loadModel(model_path)
        self.obj_model.reparentTo(self.obj_node_path)
        self.obj_model.setP(90)

        if not config.HIDE_LABEL:
            self.label = TextNode(f'{self.obj.name}')
            self.label.setText(f'{self.obj.name}')
            self.label_node_path = render.attachNewNode(self.label)
            self.label_node_path.setPos(self.obj_node_path, -0.5, -self.scale, self.scale)
            self.label_node_path.setScale(config.LABEL_SIZE)
            self.label_node_path.setBillboardPointEye(-10, fixed_depth=True)
            self.label_node_path.reparentTo(self.obj_node_path)

        ts = TextureStage('ts')
        if textures is not None:
            if 'color' in textures:
                color_map = loader.loadTexture(textures['color'])
                ts.setMode(TextureStage.MModulate)
                self.obj_model.setTexture(ts, color_map)
        else:
            self.obj_model.setColor(*hex_to_rgb_norm(self.obj.color))

        glow_map = loader.loadTexture('textures/black.jpg')  # a tiny black image
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MGlow)

        if self.obj.is_star:
            self.light = PointLight(f'{self.designation_name}_light')
            self.light.setColorTemperature(self.obj.temp)
            self.light_node_path = self.obj_node_path.attachNewNode(self.light)
            self.light_node_path.setPos(*self.pos)

            alight = AmbientLight('alight')
            alnp = self.obj_node_path.attachNewNode(alight)
            self.obj_model.setLight(alnp)

            glow_map = loader.loadTexture('textures/white.jpg')  # a tiny black image
            ts = TextureStage('ts')
            ts.setMode(TextureStage.MGlow)
            self.obj_model.setTexture(ts, glow_map)
        else:
            self.light = None
            self.obj_model.setTexture(ts, glow_map)

        self.label_node_path.setTexture(ts, glow_map)

        self.obj_node_path.setShaderAuto()

        # Init position and size
        self.obj_node_path.setScale(self.scale)
        self.obj_node_path.setPos(*self.pos)

    def convert_distances(self, dist):
        """
        Takes an astropy quantity and returns a quantity less value, normalized for the display
        """
        if self.realist_view:
            return float(dist.to(self.units) / self.units)
        return float(dist.to(self.units) / self.units)

    def compute_display_pos(self):
        if self.realist_view:
            return LPoint3f(*[self.convert_distances(x) * self.zoom_factor for x in self.obj.position])
        # When not realist view, don't zoom on distances because it's a fucking mess
        return LPoint3f(*[self.convert_distances(x) / 10 for x in self.obj.position])

    def compute_scale(self):
        if config.STANDARDIZE_BODY_SIZES:
            return config.STANDARD_BODY_SIZE
        size = self.radius * 2 * self.zoom_factor
        if self.realist_view:
            return size
        return config.DEFAULT_BODY_SIZES + math.log10(size)

    def delete_history_lines(self):
        # destroy previous points
        for x in self.history:
            x.removeNode()

    def delete_history(self):
        self.delete_history_lines()
        self.history_points.clear()

    def handle_history(self):
        self.history_steps_ctr += 1
        if self.history_steps_ctr == config.HISTORY_STEP:
            self.history_steps_ctr = 0

            self.history_points.appendleft(self.pos)
            self.delete_history_lines()

            if len(self.history_points) >= 2:
                for i, p in enumerate(self.history_points):
                    if i + 1 == len(self.history_points):
                        continue
                    lines = LineSegs()
                    lines.moveTo(p)
                    lines.drawTo(self.history_points[i + 1])
                    lines.setColor(*hex_to_rgb_norm(self.obj.color), 1)
                    lines.setThickness(0)
                    node = lines.create()
                    np = NodePath(node)
                    np.reparentTo(render)
                    self.history.append(np)

    def update(self):
        self.pos = self.compute_display_pos()
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()

        if config.HISTORY_ON:
            self.handle_history()
        self.obj_model.setScale(self.scale)
        self.obj_node_path.setPos(*self.pos)

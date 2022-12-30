
from direct.gui.OnscreenText import TextNode

from astropy import units as u
from panda3d.core import LPoint3f, TextureStage
import math

from utils import hex_to_rgb_norm
import config

class ObjectDisplay:

    def __init__(self, star_system_obj, model_path='./models/sphere.glb', texture_path=None, units=u.AU, realist_view=False):
        # Set zoom
        self.zoom_factor = config.DEFAULT_ZOOM

        self.units = units
        self.realist_view = realist_view
        # Grab data from StarSystemObject
        self.obj = star_system_obj
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()

        self.designation_name = self.obj.name.lower().replace(" ", "_")

        # Init object
        self.pos = self.compute_display_pos()
        self.obj_node_path = render.attachNewNode(f'{self.designation_name}_trajectory')
        self.obj_model = loader.loadModel(model_path)
        self.obj_model.reparentTo(self.obj_node_path)
        self.obj_model.setR(-90)

        if texture_path is not None:
            self.obj_texture = loader.loadTexture(texture_path)
            self.obj_model.setTexture(self.obj_texture, 1)
        else:
            self.obj_model.setColor(*hex_to_rgb_norm(self.obj.color))

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
        return LPoint3f(*[self.convert_distances(x) for x in self.obj.position])

    def compute_scale(self):
        size = self.radius * 2 * self.zoom_factor
        if self.realist_view:
            return size
        return config.DEFAULT_BODY_SIZES + math.log10(size)

    def update(self):
        self.pos = self.compute_display_pos()
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()

        self.obj_model.setScale(self.scale)
        self.obj_node_path.setPos(*self.pos)

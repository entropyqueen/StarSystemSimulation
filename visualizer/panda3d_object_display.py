
from direct.gui.OnscreenText import TextNode

from astropy import units as u
from panda3d.core import LPoint3f

from utils import hex_to_rgb_norm
import config

class ObjectDisplay:

    def __init__(self, star_system_obj, model_path='./models/sphere.glb', units=u.AU, texture_path=''):
        # Set zoom
        self.zoom_factor = config.DEFAULT_ZOOM

        self.units = units
        # Grab data from StarSystemObject
        self.obj = star_system_obj
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()

        self.label_text = self.obj.name.lower().replace(" ", "_")

        # Init object
        self.pos = self.compute_display_pos()
        self.obj_node_path = render.attachNewNode(f'{self.label_text}_trajectory')
        self.obj_model = loader.loadModel(model_path)
        self.obj_model.setColor(*hex_to_rgb_norm(self.obj.color))
        # self.obj_texture = loader.loadTexture(texture_path)
        # self.obj_model.setTexture(self.obj_texture, 1)
        self.obj_model.reparentTo(self.obj_node_path)

        self.label = TextNode(f'{self.label_text}')
        self.label.setText(f'{self.obj.name}')
        self.label_node_path = aspect2d.attachNewNode(self.label)
        self.label_node_path.setPos(self.obj_node_path, -0.5, -0.5, self.scale)
        self.label_node_path.setScale(0.4)
        self.label_node_path.reparentTo(self.obj_node_path)
        self.label_node_path.setBillboardPointEye()

        # Init position and size
        self.obj_node_path.setScale(self.scale)
        self.obj_node_path.setPos(*self.pos)

    def convert_distances(self, dist):
        """
        Takes an astropy quantity and returns a quantity less value, normalized for the display
        """

        return float(dist.to(self.units) / self.units)

    def compute_display_pos(self):
        return LPoint3f(*[self.convert_distances(x) * self.zoom_factor for x in self.obj.position])

    def compute_scale(self):
        return self.radius * 2 * self.zoom_factor

    def update(self):
        self.pos = self.compute_display_pos()
        self.radius = self.convert_distances(self.obj.radius)
        self.scale = self.compute_scale()

        self.obj_model.setScale(self.scale)
        self.obj_node_path.setPos(*self.pos)
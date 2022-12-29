from astropy import units as u
from utils import hex_to_rgb_norm

class ObjectDisplay:

    def __init__(self, star_system_obj, model_path='./models/sphere.glb', texture_path=''):
        self.obj = star_system_obj
        self.pos = [x for x in self.obj.position / u.AU]
        self.obj_trajectory = render.attachNewNode(f'{self.obj.name.lower().replace(" ", "_")}_trajectory')
        self.obj_model = loader.loadModel(model_path)
        self.obj_model.setColor(*hex_to_rgb_norm(self.obj.color))
        # self.obj_texture = loader.loadTexture(texture_path)
        # self.obj_model.setTexture(self.obj_texture, 1)
        self.obj_model.reparentTo(self.obj_trajectory)

        self.obj_trajectory.setPos(*self.pos)
        self.obj_model.setScale(self.obj.radius.to(u.AU) / u.AU)

    def update(self):
        self.pos = [x for x in self.obj.position / u.AU]
        self.obj_trajectory.setPos(*self.pos)

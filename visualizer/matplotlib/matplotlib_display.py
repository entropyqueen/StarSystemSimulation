from astropy import units as u
import matplotlib.pyplot as plt

import config
from loader.loader import StarSystemLoader
from physics.universe import Universe, StarSystemObject


class MatplotlibDisplay:

    def __init__(self, star_system_path):

        self.size = config.SIM_SIZE
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(config.FIG_SIZE, config.FIG_SIZE),
        )
        self.fig.tight_layout()

        self.universe = Universe()
        self.bodies = []
        ss_loader = StarSystemLoader(self.universe)
        system, self.units, load_config = ss_loader.load(star_system_path)
        for obj in system:
            self.add_object(BodyView(obj))
        try:
            self.size = load_config['matplotlib_sim_size']
        except KeyError:
            pass

    def run(self):
        while True:
            self.universe.update()
            self.draw_all()

    def add_object(self, body):
        if not isinstance(body, BodyView) or not isinstance(body.obj, StarSystemObject):
            raise
        self.bodies.append(body)

    def draw_all(self):

        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))

        # Display simulation date
        for obj in sorted(self.bodies, key=lambda item: item.obj.position[0]):
            obj.update(self.units['d_unit'])

            self.ax.plot(
                *obj.pos,
                marker="o",
                markersize=10,
                color=obj.obj.color
            )
            self.ax.plot(
                obj.pos[0],
                obj.pos[1],
                -self.size / 2,
                marker="o",
                markersize=10,
                color=(0, 0, 0),
            )
            self.ax.text(
                obj.pos[0] + (0.015 * 10 / 2),
                obj.pos[1] + (0.015 * 10 / 2),
                obj.pos[2],
                obj.obj.name
            )
        # Slow down time ... :3
        plt.pause(config.FRAME_RATE)
        self.ax.clear()


class BodyView:

    def __init__(self, obj):
        self.obj = obj
        self.pos = (0, 0, 0)

    @staticmethod
    def convert_distance(dist, units):
        return float(dist.to(units) / units)

    def update(self, d_unit):
        self.pos = [self.convert_distance(x, d_unit) for x in self.obj.position]


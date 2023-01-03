from astropy import units as u
import matplotlib.pyplot as plt

import config
from loader.loader import StarSystemLoader
from physics.universe import Universe, StarSystemObject


class MatplotlibDisplay:

    def __init__(self):

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
        self.units = u.AU
        self.bodies = []
        ss_loader = StarSystemLoader(self.universe)
        system = ss_loader.load('sol')
        for obj in system:
            self.add_object(BodyView(self, obj))

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
            obj.draw()
        # Slow down time ... :3
        plt.pause(config.FRAME_RATE)
        self.ax.clear()


class BodyView:

    def __init__(self, base, obj):
        self.base = base
        self.obj = obj
        self.pos = (0, 0, 0)

    def convert_distance(self, dist):
        return float(dist.to(self.base.units) / self.base.units)

    def draw(self):
        pos = [self.convert_distance(x) for x in self.obj.position]

        self.base.ax.plot(
            *pos,
            marker="o",
            markersize=10,
            color=self.obj.color
        )
        self.base.ax.plot(
            pos[0],
            pos[1],
            -self.base.size / 2,
            marker="o",
            markersize=10,
            color=(0, 0, 0),
        )
        self.base.ax.text(
            pos[0] + (0.015 * 10 / 2),
            pos[1] + (0.015 * 10 / 2),
            pos[2],
            self.obj.name
        )

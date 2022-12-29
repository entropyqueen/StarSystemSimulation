from astropy import units as u
import matplotlib.pyplot as plt

import config
from physics.star_system import StarSystemBody


class MatplotlibVisualizer:

    def __init__(self, size):

        self.size = size
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(config.FIG_SIZE, config.FIG_SIZE),
        )
        self.bodies = []
        self.fig.tight_layout()

    def add_object(self, body):
        if not isinstance(body, StarSystemBody):
            raise
        self.bodies.append(body)

    def draw_all(self):

        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))

        # Display simulation date
        for obj in sorted(self.bodies, key=lambda item: item.position[0]):
            obj.display.draw()
        # Slow down time ... :3
        plt.pause(config.FRAME_RATE)
        self.ax.clear()

class BodyView:

    def __init__(self, body, name, position, radius, colour, universe_display):
        self.name = name
        self.position = position
        self.radius = radius
        self.colour = colour
        self.universe_display = universe_display
        self.universe_display.add_object(body)

    def draw(self):
        self.universe_display.ax.plot(
            *self.position,
            marker="o",
            markersize=self.radius,
            color=self.colour
        )
        self.universe_display.ax.plot(
            self.position[0],
            self.position[1],
            -self.universe_display.size / 2,
            marker="o",
            markersize=self.radius / 2,
            color=(0, 0, 0),
        )
        self.universe_display.ax.text(
            self.position[0] / u.AU + (0.015 * self.radius / 2),
            self.position[1] / u.AU + (0.015 * self.radius / 2),
            self.position[2] / u.AU,
            self.name
        )
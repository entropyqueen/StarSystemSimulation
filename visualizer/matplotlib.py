from astropy import units as u
import matplotlib.pyplot as plt
import config
from physics.star_system import Universe, StarSystemBody


class MatplotlibVisualizer(Universe):

    def __init__(self, size=10):
        super().__init__(self, size)

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(config.FIG_SIZE, config.FIG_SIZE),
        )
        self.fig.tight_layout()

    def run(self):
        super().run()
        self.draw_all()

    def draw_all(self):

        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))

        # Display simulation date
        for body in sorted(self.bodies, key=lambda item: item.position[0]):
            body.draw()
        # Slow down time ... :3
        plt.pause(config.FRAME_RATE)
        self.ax.clear()

class StarSystemBodyView(StarSystemBody):

    def __init__(
            self,
            universe,
            mass,
            position=(0, 0, 0),
            velocity=(0, 0, 0),
            colour='black',
            name='object',
            radius=10,
    ):
        super().__init__(universe, mass, position, velocity, colour, name, radius)

    def draw(self):
        self.universe.ax.plot(
            *self.position,
            marker="o",
            markersize=self.radius,
            color=self.colour
        )
        self.universe.ax.plot(
            self.position[0],
            self.position[1],
            -self.universe.size / 2,
            marker="o",
            markersize=self.radius / 2,
            color=(0, 0, 0),
        )
        self.universe.ax.text(
            self.position[0] / u.AU + (0.015 * self.radius / 2),
            self.position[1] / u.AU + (0.015 * self.radius / 2),
            self.position[2] / u.AU,
            self.name
        )
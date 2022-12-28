import math
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy import constants as c

import config


class StarSystem:

    def __init__(self, size):
        self.size = size  # size of the graph in AU
        self.bodies = []
        self.dt = config.SIM_DT
        self.iterations = 0
        self.date = config.SIM_START_DATE

        # plot stuf
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(config.FIG_SIZE, config.FIG_SIZE),
        )
        self.fig.tight_layout()

        # used to print first csv line only once
        self.csv = False

    def __repr__(self):
        obj = []
        for b in self.bodies:
            obj.append(repr(b))
        return ''.join(obj)

    def __str__(self):
        obj = []
        for i, b in enumerate(self.bodies):
            obj.append(f'Body: #{i}\n{str(b)}')
        return '\n------------\n'.join(obj)

    def to_csv(self):
        if not self.csv:
            s = 'body_name,position,velocity,acceleration,time\n'
            self.csv = True
        else:
            s = ''
        for b in self.bodies:
            s += f'{b.name},' \
                 f'{str(np.linalg.norm(b.position) / u.AU)},' \
                 f'{str(np.linalg.norm(b.velocity) / (u.AU / u.d))},' \
                 f'{str(np.linalg.norm(b.acc) / (u.AU / u.d ** 2))},' \
                 f'{str(self.iterations * self.dt) / u.d}\n'
        return s

    def run(self):
        self.update_all()
        self.draw_all()

    def add_body(self, body):
        self.bodies.append(body)

    def update_all(self):
        self.iterations += 1
        self.date += config.SIM_DT
        for body in self.bodies:
            body.update_position(self.dt)

    def draw_all(self):
        # set axis boundaries in AU
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))

        # Display simulation date
        for body in sorted(self.bodies, key=lambda item: item.position[0]):
            body.draw()
        # Slow down time ... :3
        plt.pause(config.FRAME_RATE)
        self.ax.clear()


class StarSystemBody:

    def __init__(
            self,
            star_system,
            mass,
            position=(0, 0, 0),
            velocity=(0, 0, 0),
            colour='black',
            name='object',
            radius=10,
    ):
        # Setting physical properties
        self.star_system = star_system
        self.mass = mass
        self.position = np.array(position, dtype=np.double) * u.AU
        self.velocity = np.array(velocity, dtype=np.double) * u.AU / u.d
        self.acc = np.zeros(3, dtype=np.double) * u.AU / (u.d ** 2)

        self.radius = radius
        self.colour = colour
        self.name = name

        self.star_system.add_body(self)

    def __repr__(self):
        s = f'<{self.name}, {self.mass}, pos:{self.position},vel:{self.velocity},acc:\t{self.acc}'
        return s

    def __str__(self):
        s = f'{self.name}: (mass: {self.mass})\n' \
            f'position:\t{np.linalg.norm(self.position):.3e}\n' \
            f'velocity:\t{np.linalg.norm(self.velocity):.3e}\n' \
            f'accel:\t\t{np.linalg.norm(self.acc):.3e}\n' \
            f'f:\t\t\t{np.linalg.norm(self.acc * self.mass).to(u.N):.3e}'
        return s

    def draw(self):
        self.star_system.ax.plot(
            *self.position,
            marker="o",
            markersize=self.radius,
            color=self.colour
        )
        self.star_system.ax.plot(
            self.position[0],
            self.position[1],
            -self.star_system.size / 2,
            marker="o",
            markersize=self.radius / 2,
            color=(0, 0, 0),
        )
        self.star_system.ax.text(
            self.position[0] / u.AU + (0.015 * self.radius / 2),
            self.position[1] / u.AU + (0.015 * self.radius / 2),
            self.position[2] / u.AU,
            self.name
        )

    # COMPUTE ACCELERATION
    def calculate_acceleration(self, other):
        dst = np.linalg.norm(other.position - self.position)  # distance in AU
        unit_v = (other.position - self.position) / dst
        f = ((c.G * self.mass * other.mass) / (dst ** 2)) * unit_v
        if config.DEBUG:
            print(f'F between {self.name} and {other.name}: {np.linalg.norm(f).to(u.N):.2e}')
        return (f / self.mass).to(u.AU / u.d ** 2)

    # INTEGRATE THE POSITIONS OF BODIES
    def update_position(self, dt):
        acc = 0
        for body in self.star_system.bodies:
            if self == body:
                continue
            acc += self.calculate_acceleration(body)
        self.velocity += acc * dt
        self.position += self.velocity * dt
        self.acc = acc

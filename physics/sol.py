import numpy as np
from astroquery.jplhorizons import Horizons
from astropy import units as u

from physics.star_system import StarSystemBody
from utils import convert_K_to_RGB
from config import SIM_START_DATE


"""
Coordinates and velocities are gathered from Horizons
Units:
 Distances in AU 
 Speeds in AU / d
 Masses in Earth's mass
"""


class Sun(StarSystemBody):
    def __init__(self, universe, display_class= None):
        self.name = 'Sun'
        b = Horizons(id='Sun', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            333030 * u.Mearth, position, velocity,
            name=self.name, radius=20, colour=convert_K_to_RGB(5778),
            display_class=display_class,
        )


class Mercury(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Mercury'
        b = Horizons(id='Mercury bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.055 * u.Mearth, position, velocity,
            name=self.name, radius=7, colour='#708090',
            display_class=display_class,
        )


class Venus(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Venus'
        b = Horizons(id='Venus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.815 * u.Mearth, position, velocity,
            name=self.name, radius=10, colour='#ffffe0',
            display_class=display_class,
        )


class Earth(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Earth'
        b = Horizons(id='399', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            1 * u.Mearth, position, velocity, name
            =self.name, radius=10, colour='#287AB8',
            display_class=display_class,
        )


class Moon(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Moon'
        b = Horizons(id='301', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.074 * u.Mearth, position, velocity,
            name=self.name, radius=4, colour='#7d7d7d',
            display_class=display_class,
        )


class Mars(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Mars'
        b = Horizons(id='Mars bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.107 * u.Mearth, position, velocity,
            name=self.name, radius=7, colour='#69340f',
            display_class=display_class,
        )


class Ceres(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Ceres'
        b = Horizons(id='Ceres', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.00016 * u.Mearth, position, velocity
            , name=self.name, radius=5, colour='#9d97a4',
            display_class=display_class,
        )


class Jupiter(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Jupiter'
        b = Horizons(id='Jupiter bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            317.8 * u.Mearth, position, velocity,
            name=self.name, radius=15, colour='#bcafb2',
            display_class=display_class,
        )


class Saturn(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Saturn'
        b = Horizons(id='Saturn bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            95.16 * u.Mearth, position, velocity,
            name=self.name, radius=14, colour='#a68a60',
            display_class=display_class,
        )


class Uranus(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Uranus'
        b = Horizons(id='Uranus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            14.54 * u.Mearth, position, velocity,
            name=self.name, radius=13, colour='#d1e7e7',
            display_class=display_class,
        )


class Neptune(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Neptune'
        b = Horizons(id='Neptune bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            17.15 * u.Mearth, position, velocity,
            name=self.name, radius=13, colour='#5b5ddf',
            display_class=display_class,
        )


class Pluto(StarSystemBody):

    def __init__(self, universe, display_class=None):
        self.name = 'Pluto'
        b = Horizons(id='Pluto bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.00218 * u.Mearth, position, velocity,
            name=self.name, radius=5, colour='#fff1d5', display_class=display_class,
        )

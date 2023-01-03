import numpy as np
from astroquery.jplhorizons import Horizons
from astropy import units as u

from physics.universe import StarSystemObject
from config import SIM_START_DATE

"""
Coordinates and velocities are gathered from Horizons
Units:
 Distances in AU 
 Speeds in AU / d
 Masses in Earth's mass
"""

model_map = {
    'Saturn': 'models/saturn.glb',
}

texture_map = {
    'Neptune': {'color': 'textures/2k_neptune.jpg'},
    'Ceres': {'color': 'textures/2k_ceres_fictional.jpg'},
    'Earth': {
        'color': 'textures/2k_earth_daymap.jpg',
        'specular': 'textures/2k_earth_specular_map.tif',
        'normal': 'textures/2k_earth_normal_map.tif',
    },
    'Mars': {'color': 'textures/2k_mars.jpg'},
    'Moon': {'color': 'textures/2k_moon.jpg'},
    'Sun': {'color': 'textures/2k_sun.jpg'},
    'Uranus': {'color': 'textures/2k_uranus.jpg'},
    'Venus': {'color': 'textures/2k_venus_atmosphere.jpg'},
    'Jupiter': {'color': 'textures/2k_jupiter.jpg'},
    'Mercury': {'color': 'textures/2k_mercury.jpg'},
    'Pluto': {'color': 'textures/2k_pluto.jpg'},
}


def create_Sol_system(universe):
    return [
        Sun(universe),
        # Sun2(universe),
        Mercury(universe),
        Venus(universe),
        Earth(universe),
        # Moon(universe),  # The Moon doesn't behave accordingly with the current position and velocity...
        Mars(universe),
        Ceres(universe),
        Jupiter(universe),
        Saturn(universe),
        Uranus(universe),
        Neptune(universe),
        Pluto(universe),
    ]

class Sun(StarSystemObject):
    def __init__(self, universe, display_class=None):
        self.name = 'Sun'
        b = Horizons(id='Sun', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        temp = 5778
        super().__init__(
            universe,
            333030 * u.Mearth, position, velocity,
            name=self.name, radius=1. * u.Rsun,
            is_star=True, temp=5778
        )


class Sun2(StarSystemObject):
    """
    TEST PURPOSES :D
    """
    def __init__(self, universe, display_class=None):
        self.name = 'Sun2'
        b = Horizons(id='2', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array((1, 1, 1), dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            333030 * u.Mearth, position, velocity,
            name=self.name, radius=1. * u.Rsun,
            is_star=True, temp=6800
        )


class Mercury(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Mercury'
        b = Horizons(id='Mercury bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.055 * u.Mearth, position, velocity,
            name=self.name, radius=0.385 * u.Rearth, color='#708090'
        )


class Venus(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Venus'
        b = Horizons(id='Venus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.815 * u.Mearth, position, velocity,
            name=self.name, radius=0.923 * u.Rearth, color='#ffffe0'
        )


class Earth(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Earth'
        b = Horizons(id='399', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            1 * u.Mearth, position, velocity,
            name=self.name, radius=1 * u.Rearth, color='#287ab8'
        )


class Moon(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Moon'
        b = Horizons(id='301', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.074 * u.Mearth, position, velocity,
            name=self.name, radius=1737 * u.km, color='#7d7d7d'
        )


class Mars(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Mars'
        b = Horizons(id='Mars bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.107 * u.Mearth, position, velocity,
            name=self.name, radius=0.532 * u.Rearth, color='#69340f'
        )


class Ceres(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Ceres'
        b = Horizons(id='Ceres', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.00016 * u.Mearth, position, velocity,
            name=self.name, radius=469. * u.km, color='#9d97a4'
        )


class Jupiter(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Jupiter'
        b = Horizons(id='Jupiter bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            317.8 * u.Mearth, position, velocity,
            name=self.name, radius=1. * u.Rjup, color='#bcafb2'
        )


class Saturn(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Saturn'
        b = Horizons(id='Saturn bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            95.16 * u.Mearth, position, velocity,
            name=self.name, radius=9.1402 * u.Rearth, color='#a68a60'
        )


class Uranus(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Uranus'
        b = Horizons(id='Uranus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            14.54 * u.Mearth, position, velocity,
            name=self.name, radius=4.007 * u.Rearth, color='#d1e7e7'
        )


class Neptune(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Neptune'
        b = Horizons(id='Neptune bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            17.15 * u.Mearth, position, velocity,
            name=self.name, radius=3.883 * u.Rearth, color='#5b5ddf'
        )


class Pluto(StarSystemObject):

    def __init__(self, universe, display_class=None):
        self.name = 'Pluto'
        b = Horizons(id='Pluto bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(
            universe,
            0.00218 * u.Mearth, position, velocity,
            name=self.name, radius=0.1868 * u.Rearth, color='#fff1d5'
        )

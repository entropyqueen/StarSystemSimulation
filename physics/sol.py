import numpy as np
from astroquery.jplhorizons import Horizons
from astropy import units as u

from utils import convert_K_to_RGB
from config import SIM_START_DATE
from visualizer.matplotlib import StarSystemBodyView

"""
Coordinates and velocities are gathered from Horizons
Units:
 Distances in AU 
 Speeds in AU / d
 Masses in Earth's mass
"""


class Sun(StarSystemBodyView):
    def __init__(self, universe):
        self.name = 'Sun'
        b = Horizons(id='Sun', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 333030 * u.Mearth, position, velocity, name=self.name, radius=20)
        self.colour = convert_K_to_RGB(5778)


class Mercury(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Mercury'
        b = Horizons(id='Mercury bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.055 * u.Mearth, position, velocity, name=self.name, radius=7)
        self.colour = '#708090'


class Venus(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Venus'
        b = Horizons(id='Venus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.815 * u.Mearth, position, velocity, name=self.name, radius=10)
        self.colour = '#ffffe0'


class Earth(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Earth'
        b = Horizons(id='399', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 1 * u.Mearth, position, velocity, name=self.name, radius=10)
        self.colour = '#287AB8'


class Moon(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Moon'
        b = Horizons(id='301', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.074 * u.Mearth, position, velocity, name=self.name, radius=4)
        self.colour = '#7d7d7d'


class Mars(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Mars'
        b = Horizons(id='Mars bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.107 * u.Mearth, position, velocity, name=self.name, radius=7)
        self.colour = '#69340f'


class Ceres(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Ceres'
        b = Horizons(id='Ceres', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.00016 * u.Mearth, position, velocity, name=self.name, radius=5)
        self.colour = '#9d97a4'


class Jupiter(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Jupiter'
        b = Horizons(id='Jupiter bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 317.8 * u.Mearth, position, velocity, name=self.name, radius=15)
        self.colour = '#bcafb2'


class Saturn(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Saturn'
        b = Horizons(id='Saturn bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 95.16 * u.Mearth, position, velocity, name=self.name, radius=14)
        self.colour = '#a68a60'


class Uranus(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Uranus'
        b = Horizons(id='Uranus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 14.54 * u.Mearth, position, velocity, name=self.name, radius=13)
        self.colour = '#d1e7e7'


class Neptune(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Neptune'
        b = Horizons(id='Neptune bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 17.15 * u.Mearth, position, velocity, name=self.name, radius=13)
        self.colour = '#5b5ddf'


class Pluto(StarSystemBodyView):

    def __init__(self, universe):
        self.name = 'Pluto'
        b = Horizons(id='Pluto bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super().__init__(universe, 0.00218 * u.Mearth, position, velocity, name=self.name, radius=5)
        self.colour = '#fff1d5'

import numpy as np
from astroquery.jplhorizons import Horizons

from star_system import StarSystemBody
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
    def __init__(self, sol):
        self.name = 'Sun'
        b = Horizons(id='Sun', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Sun, self).__init__(sol, 333030, position, velocity, name=self.name, radius=20)
        self.colour = convert_K_to_RGB(5778)


class Mercury(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Mercury'
        b = Horizons(id='Mercury bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Mercury, self).__init__(sol, 0.055, position, velocity, name=self.name, radius=7)
        self.colour = '#708090'


class Venus(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Venus'
        b = Horizons(id='Venus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Venus, self).__init__(sol, 0.815, position, velocity, name=self.name, radius=10)
        self.colour = '#ffffe0'


class Earth(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Earth'
        b = Horizons(id='399', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Earth, self).__init__(sol, 1, position, velocity, name=self.name, radius=10)
        self.colour = '#287AB8'


class Moon(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Moon'
        b = Horizons(id='301', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Moon, self).__init__(sol, 1, position, velocity, name=self.name, radius=4)
        self.colour = '#7d7d7d'


class Mars(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Mars'
        b = Horizons(id='Mars bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Mars, self).__init__(sol, 1, position, velocity, name=self.name, radius=7)
        self.colour = 'chocolate'


class Ceres(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Ceres'
        b = Horizons(id='Ceres', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Ceres, self).__init__(sol, 1, position, velocity, name=self.name, radius=5)
        self.colour = '#9d97a4'


class Jupiter(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Jupiter'
        b = Horizons(id='Jupiter bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Jupiter, self).__init__(sol, 1, position, velocity, name=self.name, radius=15)
        self.colour = '#bcafb2'


class Saturn(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Saturn'
        b = Horizons(id='Saturn bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Saturn, self).__init__(sol, 1, position, velocity, name=self.name, radius=14)
        self.colour = '#a68a60'


class Uranus(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Uranus'
        b = Horizons(id='Uranus bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Uranus, self).__init__(sol, 1, position, velocity, name=self.name, radius=13)
        self.colour = '#d1e7e7'


class Neptune(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Neptune'
        b = Horizons(id='Neptune bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Neptune, self).__init__(sol, 1, position, velocity, name=self.name, radius=13)
        self.colour = '#5b5ddf'


class Pluto(StarSystemBody):

    def __init__(self, sol):
        self.name = 'Pluto'
        b = Horizons(id='Pluto bary', location="@sun", epochs=SIM_START_DATE.jd).vectors()
        position = np.array([np.double(b[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        velocity = np.array([np.double(b[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        super(Pluto, self).__init__(sol, 1, position, velocity, name=self.name, radius=5)
        self.colour = '#fff1d5'


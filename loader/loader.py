import yaml
from yaml.loader import SafeLoader
from astroquery.jplhorizons import Horizons
from astropy import units as u
import numpy as np

import config
from physics.universe import StarSystemObject


class LoadException(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)

class StarSystemLoader:

    def __init__(self, universe):
        self.universe = universe

    @staticmethod
    def load_from_Horizons(nasa_id, location_ref):
        h = Horizons(id=nasa_id, location=location_ref, epochs=config.SIM_START_DATE.jd).vectors()
        pos = np.array([np.double(h[xi]) for xi in ['x', 'y', 'z']], dtype=np.double)
        vel = np.array([np.double(h[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.double)
        return pos, vel

    @staticmethod
    def convert(units, value):
        return value * units

    @staticmethod
    def get_values(data, unit):
        return np.array([float(x.strip()) for x in data.split(',')], dtype=np.double) * unit

    def load_system(self, data, d_unit, m_unit, t_unit):
        system = []

        for i, obj in enumerate(data['system']):
            try:
                obj_name = obj['name']
            except KeyError:
                raise LoadException(f'Object #{i} requires a name.')
            try:
                obj_mass = obj['mass'] * m_unit
            except KeyError:
                raise LoadException(f'{obj_name}: a mass is required.')
            try:
                is_star = obj['is_star']
            except KeyError:
                is_star = False
            try:
                obj_temp = obj['temperature']
            except KeyError:
                if is_star:
                    raise LoadException(f'{obj_name} is a star and requires a temperature (in Kelvin)')
                else:
                    obj_temp = 0
            try:
                obj_radius = obj['radius'] * d_unit
            except KeyError:
                obj_radius = 5000 * u.km
            try:
                obj_color = obj['color']
            except KeyError:
                obj_color = (0.8, 0, 0.8)

            try:
                textures = obj['texture']
            except KeyError:
                textures = {}
            try:
                model = obj['model']
            except KeyError:
                model = './models/sphere.glb'

            try:
                if obj['position'] == 'get_from_nasa_Horizons' or obj['velocity'] == 'get_from_nasa_Horizons':
                    nasa_id = obj['horizons_id']
                    location_ref = obj['horizons_location_ref']
                    pos, vel = self.load_from_Horizons(nasa_id, location_ref)
                    if obj['position'] == 'get_from_nasa_Horizons':
                        obj_pos = self.convert(u.AU, np.array(pos, dtype=np.double))
                    else:
                        obj_pos = self.get_values(obj['position'], d_unit)

                    if obj['velocity'] == 'get_from_nasa_Horizons':
                        obj_vel = self.convert(u.AU / u.d, vel)
                    else:
                        obj_vel = self.get_values(obj['velocity'], d_unit / t_unit)
                else:
                    obj_pos = self.get_values(obj['position'], d_unit)
                    obj_vel = self.get_values(obj['velocity'], d_unit / t_unit)
            except KeyError:
                raise LoadException(f'{obj_name} requires a position and velocity')

            sso = StarSystemObject(
                self.universe, obj_mass, obj_pos, obj_vel,
                name=obj_name, radius=obj_radius,
                is_star=is_star, temp=obj_temp, color=obj_color,
            )
            system.append(LoadedObject(sso, textures, model))
        return system

    def load(self, system_path):

        with open(system_path) as f:
            data = yaml.load(f, Loader=SafeLoader)

        try:
            d_unit = getattr(u,  data['units']['distance'])
            m_unit = getattr(u,  data['units']['mass'])
            t_unit = getattr(u,  data['units']['time'])
            units = {'d_unit': d_unit, 'm_unit': m_unit, 't_unit': t_unit}
        except KeyError:
            raise LoadException('distance, mass and time units are required.')
        except AttributeError as e:
            raise LoadException(f'{e}')

        system = self.load_system(data, d_unit, m_unit, t_unit)

        load_config = {}
        if 'config' in data:
            load_config = data['config']
        if 'dt' in load_config:
            self.universe.dt = load_config['dt'] * t_unit

        return system, units, load_config


class LoadedObject:

    def __init__(self, star_system_object, textures, model_path):
        self.sso = star_system_object
        self.textures = textures
        self.model_path = model_path

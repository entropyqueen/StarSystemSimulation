import sys
sys.path.append("physics/build/")
print(sys.path)
from PyCppInterface import PyCppInterface, StarSystemObjectCpp

import numpy as np
from astropy import units as u

import config
from utils import convert_K_to_RGB


class Universe:

    def __init__(self):
        self.objects = []
        self.dt = config.SIM_DT
        self.iterations = 0
        self.date = config.SIM_START_DATE
        self.str_date = self.date.strftime("%Y/%m/%d")

        # used to print first csv line only once
        self.csv = False

    def __repr__(self):
        obj = []
        for b in self.objects:
            obj.append(repr(b))
        return ''.join(obj)

    def __str__(self):
        obj = []
        for i, b in enumerate(self.objects):
            obj.append(f'Body: #{i}\n{str(b)}')
        return '\n------------\n'.join(obj)

    def to_csv(self):
        if not self.csv:
            s = 'body_name,position,velocity,acceleration,time\n'
            self.csv = True
        else:
            s = ''
        for b in self.objects:
            s += f'{b.name},' \
                 f'{str(np.linalg.norm(b.position) / u.AU)},' \
                 f'{str(np.linalg.norm(b.velocity) / (u.AU / u.d))},' \
                 f'{str(np.linalg.norm(b.acc) / (u.AU / u.d ** 2))},' \
                 f'{str(self.iterations * self.dt) / u.d}\n'
        return s

    def run(self):
        self.update()

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        self.iterations += 1
        self.date += self.dt
        self.str_date = self.date.strftime("%Y/%m/%d")
        for obj in self.objects:
            obj.update_position(self.dt)


class StarSystemObject:

    def __init__(
            self,
            universe,
            mass,
            position=np.array([0, 0, 0], dtype=np.double) * u.km,
            velocity=np.array([0, 0, 0], dtype=np.double) * (u.km / u.h),
            color='#000000',
            name='object',
            radius=10 * u.km,
            period=0 * u.h,
            obliquity=0,
            is_star=False,
            temp=5000 * u.K,
            d_unit=u.m,
            t_unit=u.s,
            m_unit=u.kg,
    ):
        # Setting physical properties
        self.universe = universe
        self.d_unit = d_unit
        self.t_unit = t_unit
        self.m_unit = m_unit
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acc = np.zeros(3, dtype=np.double)

        self.f = 0

        self.radius = radius
        self.period = period
        self.obliquity = obliquity
        self.color = color
        if is_star:
            self.color = convert_K_to_RGB(temp)
        self.name = name
        self.is_star = is_star
        self.temp = temp

        self.universe.add_object(self)

    def __repr__(self):
        s = f'<{self.name}, {self.mass}, pos:{self.position},vel:{self.velocity},acc:\t{self.acc}'
        return s

    def __str__(self):
        s = f'{self.name}: (mass: {self.mass})\n' \
            f'coords:\t{self.position:}\n' \
            f'distance:\t{np.linalg.norm(self.position):.3e}\n' \
            f'velocity:\t{np.linalg.norm(self.velocity):.3e}\n' \
            f'accel:\t\t{np.linalg.norm(self.acc):.3e}\n' \
            f'f:\t\t\t{np.linalg.norm(self.acc * self.mass).to(u.N):.3e}'
        return s

    def update_position(self, dt):

        # prepare call to cpp implementation
        lst = []
        for o in self.universe.objects:
            print(o.velocity)
            lst.append(StarSystemObjectCpp(
                o.mass.to(u.kg).value,
                o.position.to(u.m).value,
                o.velocity.to(u.m / u.s).value,
            ))

        # Call cpp implementation
        pycppiface = PyCppInterface(lst)
        pycppiface.update_position(dt.to(u.s).value)
        lst = pycppiface.get_lst()

        # convert from cpp implementation
        for i, o in enumerate(lst):
            self.universe.objects[i].position = (o.pos * u.m).to(self.d_unit)
            self.universe.objects[i].velocity = (o.vel * (u.m / u.s)).to(self.d_unit/self.t_unit)

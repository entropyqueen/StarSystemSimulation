import matplotlib.pyplot as plt

from visualizer.matplotlib import MatplotlibVisualizer, BodyView

from physics.star_system import Universe
from physics.sol import *

import config

if __name__ == '__main__':

    # u = Universe(PandaVisualizer, 10)
    display = MatplotlibVisualizer(10)
    u = Universe(display, 10)

    # Load Universe passing viewer'
    #       Universe class shall register it's update() method to viewer
    # Load planets passing viewer
    #   planets will have a RenderObject or similar that will store:
    #       obj_orbit = u.main_star.attachNewNode(f'orbit_{self.name}')
    #       obj = loader.loadModel('./models/sphere')
    #       obj_tex = loader.loadTexture('./textures/') ?
    #       obj.setTexture(obj_tex, 1)
    #       obj.reparentTo(u.sun.obj_orbit)
    #       obj.setPos(coordinates)
    #       obj.setScale(factor * base_scale)
    # or StarStystemBody will have a render_to object ? // le render to permet
    # de changer de moteur d'affichage, l'idée étant d'avoir un truc générique
    # en terme de physique, mais pouvoir choisir si je le veux dans matplotlib
    # ou dans panda3d, ou autre, whatever ce qu'on implem.

    # Size in AU
    sun = Sun(u, BodyView)
    Mercury(u, BodyView)
    Venus(u, BodyView)
    Earth(u, BodyView)
    Moon(u, BodyView)
    Mars(u, BodyView)
    Ceres(u, BodyView)
    Jupiter(u, BodyView)
    Saturn(u, BodyView)
    Uranus(u, BodyView)
    Neptune(u, BodyView)
    Pluto(u, BodyView)

    i = config.MAX_DAYS
    while i:
        if config.VERBOSE:
            print('===============================================================')
            print(f'Simulation Day #{config.MAX_DAYS - i}')
            print(str(u))

        if config.CSV:
            with open(config.CSV_OUTPUT, 'w') as f:
                f.write(u.to_csv())
        u.run()
        i -= 1

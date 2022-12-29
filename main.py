import matplotlib.pyplot as plt

from visualizer import Visualizer
from star_system import StarSystem
from sol import *

import config


if __name__ == '__main__':

    viewer = Visualizer()
    # Load Universe passing viewer'
    #       Universe class shall register it's update() method to viewer
    # Load planets passing viewer
    #   planets will have a RenderObject or similar that will store:
    #       obj_orbit = universe.main_star.attachNewNode(f'orbit_{self.name}')
    #       obj = loader.loadModel('./models/sphere')
    #       obj_tex = loader.loadTexture('./textures/') ?
    #       obj.setTexture(obj_tex, 1)
    #       obj.reparentTo(universe.sun.obj_orbit)
    #       obj.setPos(coordinates)
    #       obj.setScale(factor * base_scale)
    # or StarStystemBody will have a render_to object ? // le render to permet
    # de changer de moter d'affichage, l'idée étant d'avoir un truc générique
    # en terme de physique, mais pouvoir choisir si je le veux dans matplotlib
    # ou dans panda3d, ou autre, whatever ce qu'on implem.
    viewer.run()

    plt.style.use('dark_background')

    # Size in AU
    Sol = StarSystem(10)

    sun = Sun(Sol)
    planets = (
        Mercury(Sol),
        Venus(Sol),
        Earth(Sol),
        Moon(Sol),
        Mars(Sol),
        Ceres(Sol),
        Jupiter(Sol),
        Saturn(Sol),
        Uranus(Sol),
        Neptune(Sol),
        Pluto(Sol),
    )

    i = config.MAX_DAYS
    while i:
        if config.verbose:
            print('===============================================================')
            print(f'Simulation Day #{config.MAX_DAYS - i}')
            print(str(Sol))

        if config.csv:
            with open(config.csv_output, 'w') as f:
                f.write(Sol.to_csv())
        Sol.run()
        i -= 1

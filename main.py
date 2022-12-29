import matplotlib.pyplot as plt

from visualizer import Visualizer
from star_system import StarSystem
from sol import *

import config


if __name__ == '__main__':

    viewer = Visualizer()
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

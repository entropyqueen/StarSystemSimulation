# from visualizer.matplotlib import MatplotlibVisualizer, BodyView

import config
from visualizer.panda3d.visualizer import Visualizer

if __name__ == '__main__':

    # display = MatplotlibVisualizer(10)
    display = Visualizer(realist_view=config.REALIST_VIEW)
    display.run()

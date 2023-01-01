import matplotlib.pyplot as plt

# from visualizer.matplotlib import MatplotlibVisualizer, BodyView

import config
from visualizer.panda3d import PandaVisualizer

if __name__ == '__main__':

    # display = MatplotlibVisualizer(10)
    display = PandaVisualizer(realist_view=config.REALIST_VIEW)
    display.run()

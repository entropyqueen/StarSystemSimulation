import argparse

from visualizer.matplotlib.matplotlib_display import MatplotlibDisplay
from visualizer.panda3d.panda3d_display import Panda3dDisplay
from visualizer.text.text_display import TextDisplay

if __name__ == '__main__':

    disp = {
        'panda3d': Panda3dDisplay,
        'matplotlib': MatplotlibDisplay,
        'text': TextDisplay,
    }

    parser = argparse.ArgumentParser(description='4S: Star System Simulator Sandbox')
    parser.add_argument('display', metavar='DISPLAY', choices=disp.keys(),
                        help='Choose which display method to use')
    args = parser.parse_args()

    display = disp[args.display]()
    display.run()

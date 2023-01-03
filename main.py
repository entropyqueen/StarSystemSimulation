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
    parser.add_argument(
        '--display', '-d', metavar='DISPLAY', choices=disp.keys(), default='text',
        help='Choose which display method to use'
    )
    parser.add_argument(
        'star_system_path', metavar='FILE',
        help='File path of the star system to render, for example: ./star_systems/sol.yml'
    )
    args = parser.parse_args()

    display = disp[args.display](args.star_system_path)
    display.run()

import config
from loader.loader import StarSystemLoader
from physics.universe import Universe


class TextDisplay:
    """
    Simple text display
    """

    def __init__(self):
        self.universe = Universe()
        ss_loader = StarSystemLoader(self.universe)
        ss_loader.load('sol')

    def run(self):

        while True:

            self.universe.update()

            print('===============================================================')
            print(str(self.universe))

            if config.CSV:
                with open(config.CSV_OUTPUT, 'w') as f:
                    f.write(self.universe.to_csv())

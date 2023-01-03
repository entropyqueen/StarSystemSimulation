import config
from loader.loader import StarSystemLoader
from physics.universe import Universe


class TextDisplay:
    """
    Simple text display
    """

    def __init__(self, star_system_path):
        self.universe = Universe()
        ss_loader = StarSystemLoader(self.universe)
        ss_loader.load(star_system_path)

    def run(self):
        while True:
            self.universe.update()
            print('===============================================================')
            print(str(self.universe))

            if config.CSV:
                with open(config.CSV_OUTPUT, 'w') as f:
                    f.write(self.universe.to_csv())

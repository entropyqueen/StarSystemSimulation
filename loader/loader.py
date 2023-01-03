from loader.sol import create_Sol_system


class StarSystemLoader:

    def __init__(self, universe):
        self.universe = universe

    def load(self, name):
        system = create_Sol_system(self.universe)
        return system

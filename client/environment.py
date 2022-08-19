from shared.simulation import SimulationTime

class Environment(SimulationTime):
    initial_player = None
    network = None

    def __init__(self, *a, **kw):
        SimulationTime.__init__(self, *a, **kw)
        self.observers = []

    def set_initial_player(self, player):
        self.initial_player = player

    def set_network(self, network):
        self.network = network

    def add_observer(self, observer):
        self.observers.append(observer)

    def create_player(self, position, speed):
        pass
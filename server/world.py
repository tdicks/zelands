import random
from twisted.application.service import Service
from shared.simulation import SimulationTime

class GameService(Service):
    def __init__(self, world):
        self.world = world

    def startService(self):
        self.world.start()

    def stopService(self):
        self.world.stop()

class World(SimulationTime):
    def __init__(self, random=random, granularity=1, platform_clock = None):
        SimulationTime.__init__(self, granularity, platform_clock)
        self.random = random
        self.players = []

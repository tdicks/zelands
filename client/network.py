from twisted.protocols.amp import(
    AMP, Command, Integer, Float, Argument
)

from shared.network import *
from client.environment import Environment

class NetworkController(AMP):

    environment = None

    def __init__(self, clock):
        self.modelObjects = {}
        self.clock = clock

    def introduce(self):
        d = self.callRemote(Introduce)
        def introduce_callback(box):
            granularity = box['granularity']
            self.environment = Environment(granularity, self.clock)
            self.environment.set_network(self)
            return self.environment
        d.addCallback(introduce_callback)
        return d
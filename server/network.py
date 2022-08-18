from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
#from server.events import EventHandler
#from profiles import ProfileManager


"""
Here be the brains for the server communicating with the client
"""

class GameServer(AMP):

    def __init__(self, world, clock=reactor):
        self.world = world
        self.clock = clock
        self.players = {}

class GameServerFactory(ServerFactory):
    def __init__(self, world, config):
        self.config = config
        self.world = world

        self.max_clients = config['max_clients']

    def buildProtocol(self, addr):
        return GameServer(self.world)
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
#from server.events import EventHandler
#from profiles import ProfileManager
from shared.network import Introduce

"""
Here be the brains for the server communicating with the client
"""

class GameServer(AMP):

    def __init__(self, world, clock=reactor):
        self.world = world
        self.clock = clock
        self.players = {}

    def introduce(self):
        player = self.world.create_player()
        ident = self.ident_for_player(player)
        v = player.get_position()
        self.player = player
        return {"granularity": self.world.granularity,
                "identifier": ident,
                "x": v.x,
                "y": v.y}
    Introduce.responder(introduce)

    def ident_for_player(self, player):
        self.players[id(player)] = player
        return id(player)

    def player_for_ident(self, ident):
        return self.players[ident]

class GameServerFactory(ServerFactory):
    def __init__(self, world, config):
        self.config = config
        self.world = world

        self.max_clients = config['max_clients']

    def buildProtocol(self, addr):
        return GameServer(self.world)

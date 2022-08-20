from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
#from server.events import EventHandler
#from profiles import ProfileManager
from shared.network import *
from pygame.math import Vector2

"""
Here be the brains for the server communicating with the client
"""

class GameServer(AMP):
    """
    GameServer AMP protocol
    An instance of this class is spawned for each connected client
    """
    def __init__(self, world, clock=reactor):
        self.world = world
        self.clock = clock
        self.player = None

    def connectionLost(self, reason):
        self.world.remove_client(self)

    def resp_player_connected(self):
        """
        Responder for the player connecting to the server
        We just given them an identity and add them to our world for now until they spawn
        """
        player = self.world.create_player(self)
        ident = self.world.ident_for_player(player)
        self.player = player
        return {"granularity": self.world.granularity,
                "identifier": ident}
    PlayerConnected.responder(resp_player_connected)

    def resp_player_initial_spawn(self):
        """
        Responder for the player who has requested their initial spawn
        This is where we spawn them into the world at the specified position
        """
        self.player.spawn()
        ident = self.world.ident_for_player(self.player)
        v = self.player.get_position()
        return {"identifier": ident,
                "x": v.x,
                "y": v.y,
                "status": self.player.get_status().encode('utf')}
    PlayerInitialSpawn.responder(resp_player_initial_spawn)

    def resp_player_moved(self, x, y, status):
        """
        Responder for the client saying their player has moved. 
        Save their new position in our world and tell everyone else
        """
        self.player.set_position(Vector2(x, y))
        self.player.set_status(status)
        self.world.update_player_positions()
        return {}
    PlayerMoved.responder(resp_player_moved)

class GameServerFactory(ServerFactory):
    """
    This factory creates a GameServer AMP class instance for each
    connecting client.

    The world exists at this level so that a common environment can persist between clients
    """
    def __init__(self, world, config):
        self.config = config
        self.world = world

        self.max_clients = config['max_clients']

    def buildProtocol(self, addr):
        protocol = GameServer(self.world)
        self.world.clients.append(protocol)
        return protocol

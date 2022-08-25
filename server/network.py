from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP, CommandLocator
#from server.events import EventHandler
#from profiles import ProfileManager
from shared.network import *
from pygame.math import Vector2
from shared.events import EventManager

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
        self.player_id = None
        self.events = EventManager()

    def connectionMade(self):
        # Add this protocol to the world's client list
        self.world.add_client(self)
        # Make the world subscribe to all our events so that things actually happen.
        self.world.subscribe_events(self)

        #self.callRemote(PlayerSpawn, x=200, y=200, orientation='down')

    def connectionLost(self, reason):
        # remove the client connection from the world
        self.world.remove_client(self)
        # remove all the world's subscribed events for this client
        self.world.unsubscribe_events(self)

#
#   Define the instructions the protocol can call on the client
#

    def update_entity_position(self, entity_id, x, y, orientation):
        d = self.callRemote(EntityMoved,
            entity_id, x, y, orientation
        )

#
#   Define all our responders on this protocol
#

    @PlayerConnected.responder
    def player_connected(self, client_id):
        self.events.trigger('player_connected', self, client_id)
        return {'client_id': client_id}

    @PlayerDisconnected.responder
    def player_disconnected(self):
        self.events.trigger('player_disconnected', self)
        return {}

    @PlayerClientReady.responder
    def player_client_ready(self):
        self.events.trigger('player_client_ready', self)
        return {}

    @PlayerMoved.responder
    def player_moved(self, x, y, orientation):
        self.events.trigger('player_moved', self, x, y, orientation)
        return {}

    @PlayerMoving.responder
    def player_moving(self, x, y):
        self.events.trigger('player_moving', self, x, y)
        return {}

    @PlayerItemEquipped.responder
    def player_item_equipped(self, item_id, slot):
        self.events.trigger('player_item_equipped', self, item_id, slot)
        pass

    @PlayerPrimaryAction.responder
    def player_primary_action(self):
        self.events.trigger('player_primary_action', self)
        pass

    @PlayerSecondaryAction.responder
    def player_secondary_action(self):
        self.events.trigger('player_secondary_action', self)
        pass

    @PlayerTertiaryAction.responder
    def player_tertiary_action(self):
        self.events.trigger('player_tertiary_action', self)
        pass

    @PlayerItemCollected.responder
    def player_item_collected(self, item_id):
        self.events.trigger('player_item_collected', self, item_id)
        pass

    @PlayerItemDropped.responder
    def player_item_dropped(self, item_id):
        self.events.trigger('player_item_dropped', self, item_id)
        pass


#
#   Old responders I need to delete
#
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
    #PlayerConnected.responder(resp_player_connected)

    def resp_player_spawn(self):
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
    #PlayerSpawn.responder(resp_player_spawn)

    def resp_player_moved(self, x, y, status):
        """
        Responder for the client saying their player has moved. 
        Save their new position in our world and tell everyone else
        """
        self.player.set_position(Vector2(x, y))
        self.player.set_status(status)
        self.world.update_player_positions()
        return {}
    #PlayerMoved.responder(resp_player_moved)

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
        return protocol
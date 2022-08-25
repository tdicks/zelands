from statistics import mode
from twisted.protocols.amp import(
    AMP, Command, Integer, Float, Argument, CommandLocator
)

from pygame.math import Vector2
from client.player import Player

from shared.network import *
from client.environment import Environment
from shared.events import EventManager
import client.events as event

class NetworkController(AMP):

    def __init__(self, clock):
        self.clock = clock
        self.granularity = None
        self.events = EventManager()


    def set_environment(self, environment):
        self.environment = environment

    """
    Call the PlayerConnected command on the server to say we're here
    """
    def join_server(self):
        d = self.callRemote(PlayerConnected, client_id=b'123123asdasd')
        def connected(client_id):
            return True

        d.addCallback(connected)
        return d

    def send_client_ready(self):
        return self.callRemote(PlayerClientReady)

    """
    def player_initial_spawn(self):
        d = self.callRemote(PlayerInitialSpawn)
        def spawned(data):
            position = Vector2(data['x'], data['y'])
            self.environment = Environment(self.granularity, self.clock)
            self.environment.set_network(self)
            self.create_initial_player(self.environment, data['identifier'], position, data['status'])
            return self.environment
        d.addCallback(spawned)
        return d

    def set_entity_position(self, identifier, x, y, status):
        entity = self.object_by_identifier(identifier)
        entity.set_position(Vector2(x, y))
        entity.set_status(status)
    UpdateEntityPosition.responder(set_entity_position)

    def other_player_spawned(self, identifier, entity):
        self.environment.create_entity(identifier, entity)
        self.add_model_object(identifier, entity)
    """

    # Model observers

    def ob_entity_moved(self, entity):
        """
        Observe when the player entity moves and send an
        update to the server
        """
        v = entity.get_position()
        d = self.callRemote(PlayerMoved,
            x = v.x,
            y = v.y,
            status = entity.status.encode('utf-8')
        )


#
#   Senders
#   (Put these here so we have abstraction)
#

    def send_player_moved(self, x, y, orientation):
        self.callRemote(PlayerMoved,
            x=x,
            y=y,
            orientation=orientation
        )

    def send_player_moving(self, x, y):
        self.callRemote(PlayerMoving,
            x=x,
            y=y
        )

#
# Responders
# NOTE: All responders must return ~something~
# If there is no return value required, just return {}
# Otherwise, Twisted will complain about NoneType object has no attribute 'copy'
#

    @PlayerSpawn.responder
    def player_spawn(self, x, y, orientation):
        #self.ev
        return {}

    @PlayerCreated.responder
    def player_created(self, player_id):
        self.environment.create_player(player_id)
        return {}

    @EntityCreated.responder
    def entity_created(self, entity_id, data):
        # Don't create an entity if it's the player
        if entity_id != self.environment.player_entity_id:
            self.environment.create_server_entity(entity_id)
            self.environment.update_entity(entity_id, data)
        return {}

    @EntityDamaged.responder
    def entity_damaged(self, entity_id):
        pass

    @EntityDespawned.responder
    def entity_despawned(self, entity_id):
        pass

    @EntityDied.responder
    def entity_died(self, entity_id, killer_id, item_id):
        pass

    @EntityItemEquipped.responder
    def entity_item_equipped(self, entity_id, item_id):
        pass

    @EntityMoved.responder
    def entity_moved(self, entity_id, x, y, orientation):
        self.environment.move_entity(entity_id,
        x, y, orientation)
        return {}

    @EntityMoving.responder
    def entity_moving(self, entity_id, x, y):
        self.environment.direct_entity(entity_id, x, y)
        return {}

    @EntityPrimaryAction.responder
    def entity_primary_action(self, entity_id):
        pass

    @EntitySecondaryAction.responder
    def entity_secondary_action(self, entity_id):
        pass

    @EntityTertiaryAction.responder
    def entity_tertiary_action(self, entity_id):
        pass

    @EntityRemoved.responder
    def entity_removed(self, entity_id):
        pass

    @EntitySpawned.responder
    def entity_spawned(self, entity_id):
        pass

    @EntityUpdated.responder
    def entity_updated(self, entity_id, data):
        pass
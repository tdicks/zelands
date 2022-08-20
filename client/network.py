from statistics import mode
from twisted.protocols.amp import(
    AMP, Command, Integer, Float, Argument
)

from pygame.math import Vector2

from shared.network import *
from client.environment import Environment

class NetworkController(AMP):

    environment = None

    def __init__(self, clock):
        self.model_objects = {}
        self.clock = clock
        self.granularity = None

    def add_model_object(self, identifier, model_object):
        self.model_objects[identifier] = model_object

    def object_by_identifier(self, identifier):
        return self.model_objects[identifier]

    def identifier_by_object(self, model_object):
        for identifier, object in self.model_objects.items():
            if object is model_object:
                return identifier

    def create_initial_player(self, environment, identifier, position, status):
        player = environment.create_player(position, status)
        environment.set_initial_player(player)
        player.add_observer(self)
        self.add_model_object(identifier, player)

    def create_entity(self, environment, identifier, position, status):
        pass#entity 

    """
    Call the PlayerConnected command on the server to say we're here
    """
    def join_server(self):
        d = self.callRemote(PlayerConnected)
        def connected(data):
            self.granularity = data['granularity']
        d.addCallback(connected)
        return d

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

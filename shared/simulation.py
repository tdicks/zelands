from twisted.internet.task import LoopingCall, Clock
from shared.events import EventManager
from shared.entity import Entity

"""
Base class for simulating a game environment for both client and server
The server World and the client Environment classes inherit from this for their respective purposes.

The server World is an overall game world where the server is aware of everything going on.
The client Environment is a subset of the world which the client manages.

The entity dictionary is used by both subclasses so is defined here, alongside some helper methods.
"""

class SimulationTime(Clock):

    _call = None

    """
    This dict is shared between the world and each client environment through
    various event triggers. 
    All the keys are identical between client and server, and the server
    tells the client what to add, update, and remove from the dict. In turn,
    the client is responsible for rendering the entities in the dict.
    """
    entities = {}

    def __init__(self, granularity, platform_clock):
        Clock.__init__(self)
        self.granularity = granularity
        self.platform_clock = platform_clock
        self.events = EventManager()

    def _update(self, frames):
        self.advance(1.0 * frames / self.granularity)

    def start(self):
        self._call = LoopingCall.withCount(self._update)
        self._call.clock = self.platform_clock
        self._call.start(1.0 / self.granularity, now=False)

    def stop(self):
        self._call.stop()

    def add_entity(self, entity_id, entity):
        """
        Add an entity to the dictionary under the specified ID
        
        The entity_id is the server's id() for the entity object.
        """
        if not self.entity_exists(entity_id):
            self.entities[entity_id] = entity
            #self._update_entity_attributes(entity_id, entity)
            self.events.trigger('entity_added', entity_id, entity)

    def remove_entity(self, entity_id):
        """
        Delete an entity from the dictionary by ID
        """
        if self.entity_exists(entity_id):
            del self.entities[entity_id]
            self.events.trigger('entity_removed', entity_id)

    def entity_exists(self, entity_id):
        if entity_id in self.entities.keys():
            return True
        else:
            return False


    def update_entity(self, entity_id, data):
        """
        Update properties on the entity using the data dict provided.
        Only properties that exist on the entity will be affected.
        """
        print(type(data))
        if type(data) is not dict:
            return
        if self.entity_exists(entity_id):
            entity = self.entities[entity_id]
            #for k, v in data.items():
                #if hasattr(entity, k):
                    #setattr(entity, k, v)
            self.events.trigger('entity_updated', entity_id, data)

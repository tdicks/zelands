"""
Networking module which has shared requests/responses etc
"""
import jsons
from urllib import response
from twisted.protocols.amp import (
    Command, Integer, Float, String, Argument
)
import shared.entity as entity

from pygame.math import Vector2

jsons.set_deserializer(jsons.default_object_deserializer, entity.Entity)
jsons.set_serializer(jsons.default_object_serializer, entity.Entity)
jsons.set_deserializer(jsons.default_object_deserializer, Vector2)
jsons.set_serializer(jsons.default_object_serializer, Vector2)

class Object(Argument):
    """
    Encodes an Entity into json and back.
    """

    def toString(self, obj):
        """
        Convert the object to json
        """

        if obj is not None:
            try:
                return jsons.dumps(obj, strip_privates=True).encode()
            except Exception as e:
                print('Could not dump obj to json: ' + str(e))
        else:
            raise Exception("obj was None")

    def fromString(self, json_str):
        """
        Convert the json back to object
        """

        try:
            obj = jsons.loads(json_str)
        except Exception as e:
            print('Could not load json to obj: ' + str(e))

        return obj       

"""
Client to Server commands
"""

class PlayerConnected(Command):
    """
    Client to Server
    Client provides a client_id which the server uses
    to lookup the client's info.

    If client_id is a blank string or not found, the server will respond with a new client_id
    which the client should save.

    If the client_id is found, the server will return the same ID back.
    """

    arguments = [(b'client_id', String())]

    response = [(b'client_id', String())]

class PlayerDisconnected(Command):
    """
    Client to Server
    Client tells the server they are logging off.
    Gives the server a chance to clear down information.
    """

class PlayerMoved(Command):
    """
    Sent by the client to the server when the client's player
    entity moves position.

    Note: this is when the player's entity has been force moved.
            Use PlayerMoving for changes in direction.
    """
    arguments = [(b'x', Integer()),
                 (b'y', Integer()),
                 (b'orientation', String())]

class PlayerMoving(Command):
    """
    Sent by the client to the server when the client's player
    entity is going in a direction other than 0,0.
    """
    arguments = [(b'x', Float()),
                 (b'y', Float())]

class PlayerItemEquipped(Command):
    """
    Sent by the client to the server when the player equips an item
    """
    arguments = [(b'item_id', Integer()),
                 (b'slot', Integer())]

class PlayerPrimaryAction(Command):
    """
    Sent by the client to the server when the player does their primary action
    """

class PlayerSecondaryAction(Command):
    """
    Sent by the client to the server when the player does their secondary action
    """

class PlayerTertiaryAction(Command):
    """
    Sent by the client to the server when the player does their tertiary action
    """

class PlayerItemCollected(Command):
    """
    Sent by the client to the server when the player picks up an item
    """
    arguments = [(b'item_id', Integer())]

class PlayerItemDropped(Command):
    """
    Sent by the client to the server when the player drops an item
    """
    arguments = [(b'item_id', Integer())]

class PlayerClientReady(Command):
    """
    Sent by the client to the server when the client is fully initialised and ready to do stuff
    """
    requiresAnswer = False

"""
Server to Client commands
"""

class ShowMessage(Command):
    """
    Sent by the server to the client to show a message on the screen
    """
    arguments = [(b'message', String())]

class PlayerSpawn(Command):
    """
    Sent by the server to the client to advise their player has spwaned in the world.
    Client needs to kick into action and start doing play!
    """
    arguments = [(b'x', Integer()),
                (b'y', Integer()),
                (b'orientation', String())]

    requiresAnswer = False

class PlayerCreated(Command):
    """
    Sent by the server to the client when the server has created the client's player entity.
    The client should go ahead and create their local player but not spawn it yet.
    """
    arguments = [(b'player_id', Integer())]

class EntityCreated(Command):
    """
    Sent by the server to the client when a new entity has been created on the server.
    The client should also create this entity and add it to its entity table.

    The entity is only created in memory, EntitySpawned tells the client to spawn the entity
    into the game environment.
    """
    arguments = [(b'entity_id', Integer()),
                 (b'data', Object())]

class EntitySpawned(Command):
    """
    Sent by the server to the client when an entity has spawned in the world
    """
    arguments = [(b'entity_id', Integer()),
                 (b'x', Integer()),
                 (b'y', Integer()),
                 (b'orientation', String())]

class EntityDespawned(Command):
    """
    Sent by the server to the client when the server removes an entity from play, but keeps it in the 
    entities table. 
    
    The client needs to "hide" an entity from the game, but keep it in the entities table for later use.
    """
    arguments = [(b'entity_id', Integer())]

class EntityMoved(Command):
    """
    Sent by the server to the client when an entity has moved (x or y, or orientation)
    """
    arguments = [(b'entity_id', Integer()),
                 (b'x', Integer()),
                 (b'y', Integer()),
                 (b'orientation', String())]

class EntityMoving(Command):
    """
    Sent by the server to the client when an entity has changed direction
    (other than 0,0)
    """
    arguments = [(b'entity_id', Integer()),
                 (b'x', Float()),
                 (b'y', Float())]

class EntityRemoved(Command):
    """
    Sent by the server to the client when an entity has been removed from the world.
    The client should remove this entity from the entities table immediately and forget it exists
    
    Removing the entity should also make it stop rendering!
    """
    arguments = [(b'entity_id', Integer())]

class EntityDied(Command):
    """
    Sent by the server to the client when an entity (mob or player) dies.
    
    Client just needs to play a death animation and anything else related to a dead entity.
    The server will send another instruction when the entity should be removed or respawned."""
    arguments = [(b'entity_id', Integer())]

class EntityDamaged(Command):
    """
    Sent by the server to the client when an entity takes damage.
    
    Client should render an appropriate "ouch" animation. Any pushback is handled by further EntityMoved commands.
    """
    arguments = [(b'entity_id', Integer())]

class EntityItemEquipped(Command):
    """
    Sent by the server to the client when an entity equips an item.
    
    Client just needs to render the item onto the entity, and perhaps update an entity record with the new item ID
    """
    arguments = [(b'entity_id', Integer()),
                 (b'item_id', Integer())]

class EntityPrimaryAction(Command):
    """
    Sent by the server to the client when an entity does its primary action
    """
    arguments = [(b'entity_id', Integer())]

class EntitySecondaryAction(Command):
    """
    Sent by the server to the client when an entity does its secondary action
    """
    arguments = [(b'entity_id', Integer())]

class EntityTertiaryAction(Command):
    """
    Sent by the server to the client when an entity does its tertiary action
    """
    arguments = [(b'entity_id', Integer())]

class EntityUpdated(Command):
    """
    Sent by the server to the client when an entity is updated.
    
    Cient should update the properties on the entity to the values provided.
    """
    arguments = [(b'entity_id', Integer()),
                 (b'data', Object())]
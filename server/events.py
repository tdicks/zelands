from server.player import Player
from shared.network import *

#
#   Event handlers for the Zelands server side
#

class WorldEventHandler:
    """
    Handles events that occur in the server world
    """

    def __init__(self, world):
        self.world = world

#   Player events
#   (events called due to player interactions)

    def player_connected(self, client, client_id):
        # Client has connected
        # Let's just boot them right into the game.
        pass
        

    def player_disconnected(self, client):
        # A client has told us they're disconnecting
        # Save their stuff, update entity table, tell other players, goodbye and goodnight
        pass

    def player_client_ready(self, client):
        player = Player()
        client.player_id = id(player)
        client.player = player
        self.world.add_entity(client.player_id, player)
        client.callRemote(PlayerCreated,
            player_id=client.player_id
        )
        client.callRemote(PlayerSpawn,
            x=200,
            y=200,
            orientation=b'down'
        )

    def player_moved(self, client, x, y, orientation):
        entity_id = id(client.player)
        self.world.announce_entity_moved(entity_id, x, y, orientation)

    def player_moving(self, client, x, y):
        entity_id = client.player_id
        self.world.announce_entity_moving(entity_id, x, y)

    def player_item_equipped(self, client, item_id, slot):
        # A client's player has equipped an item
        # Update entity table and inform other clients so they can render appropriately
        pass

    def player_primary_action(self, client):
        # A player has performed the primary action for an item
        # Call the item's primary action handler and do something about it
        pass

    def player_secondary_action(self, client):
        # A player has performed the secondary action for an item
        # Call the item's secondary action handler and do something about it
        pass

    def player_item_collected(self, client, item_id):
        # A player has picked up an item
        # Remove it from the world, and add it to their inventory on the server
        pass

    def player_item_dropped(self, client, item_id):
        # A player has dropped an item
        # Remove it from their inventory and spawn the item in the world
        pass

    #   Entity events
    #   (events called due to actions in the game world)

    def entity_created(self, entity_id, data):
        self.world.announce_entity_created(entity_id, data)

    def entity_removed(self, entity_id):
        # the world has removed an entity, tell clients to remove
        # the entity from their entities table
        pass 

    def entity_spawned(self, entity_id, x, y, orientation):
        # When an entity spawns in the world, tell all the clients
        # so they can render it
        # The entity must be created first!!
        pass

    def entity_despawned(self, entity_id):
        # The world has removed an entity from play but the entity still
        # exists in the table
        # Usually used for death and respawning
        # The entity must be created first!!
        pass

    def entity_moved(self, entity_id, x, y, orientation):
        self.world.announce_entity_moved(entity_id, x, y, orientation)

    def entity_died(self, entity_id):
        # An entity has died or been killed in the world, tell all the clients about it
        # so they can render appropriate animations
        pass

    def entity_damaged(self, entity_id):
        # An entity has taken damage of some kind. tell clients so they can render
        # an "ouch" animation
        pass

    def entity_item_equipped(self, entity_id, item_id):
        # An entity has equipped an item. Tell clients so they can render the item on the
        # entity
        pass

    def entity_primary_action(self, entity_id):
        # An entity has performed its primary action
        pass

    def entity_secondary_action(self, entity_id):
        # An entity has performed its secondary action
        pass

    def entity_updated(self, entity_id, data):
        # An entity's properties have been updated
        # tell all the clients
        pass

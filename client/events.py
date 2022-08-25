#
#   Event handlers for the Zelands server side
#

class EnvironmentEventHandler:
    """
    Handles events that occur in the client's game environment
    """

    def __init__(self, environment):
        self.environment = environment
        self.client = environment.client

    def player_moved(self, player):
        pos = player.get_position()
        x = pos.x
        y = pos.y
        self.client.send_player_moved(
            x,
            y,
            player.orientation.encode()
        )

    def player_moving(self, player):
        dir = player.get_direction()
        x = dir.x
        y = dir.y
        self.client.send_player_moving(
            x,
            y
        )

#   Player events
#   (events called due to player interactions)

    def player_created(self):
        # The server has created our player entity
        # do what we need to do on our side to set
        # up the player
        pass

    def player_spawn(self, client, client_id):
        # Spawn the player's entity in the game
        pass

    #   Entity events
    #   (events called due to actions in the game world)

    def entity_created(self, entity_id, data):
        # The world has created an item, tell clients to add
        # the entity to their entities table
        pass

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
        # the world has moved an entity, tell all the clients about it
        pass

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

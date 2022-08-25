import random
from twisted.application.service import Service
from shared.network import *
from shared.simulation import SimulationTime

import pygame
from pygame.math import Vector2
from server.player import Player
from server.events import WorldEventHandler

class GameService(Service):
    def __init__(self, world):
        self.world = world

    def startService(self):
        self.world.start()

    def stopService(self):
        self.world.stop()

class World(SimulationTime):
    """
    Shared world environment where all clients and entities are tracked.

    The world reacts to certain events that happen during gameplay.
    """
    def __init__(self, random=random, granularity=1, platform_clock = None):
        SimulationTime.__init__(self, granularity, platform_clock)
        self.random = random

        pygame.init()
        pygame.display.set_mode((800,600))

        self.clients = []

        """
        Set up the world's event handler 
        """
        self.event_handler = WorldEventHandler(self)


        """
        Set up the world's version of the level
        (not yet implemented)
        """
        self.level = None

        """
        Subscribe to the events we emit ourselves as the world.
        """
        self.subscribe_world_events()

    def subscribe_events(self, client):
        """
        Subscribe to all the client's command events that we're interested in.
        Which is pretty much all of them...

        The events module contains the business logic to process what happens.
        """
        client.events.on('player_connected', self.event_handler.player_connected)
        client.events.on('player_disconnected', self.event_handler.player_disconnected)
        client.events.on('player_moved', self.event_handler.player_moved)
        client.events.on('player_moving', self.event_handler.player_moving)
        client.events.on('player_client_ready', self.event_handler.player_client_ready)
        # ... and add the rest...

    def unsubscribe_events(self, client):
        """
        Unsubscribe from all the client's events
        """
        client.events.remove(
            self.event_handler.player_connected,
            self.event_handler.player_disconnected,
            self.event_handler.player_moved,
            self.event_handler.player_moving,
            self.event_handler.player_client_ready
        )

    def subscribe_world_events(self):
        """
        Subscribe to the world's own events such as entity dict changes.
        """
        # Entity dict events. These trigger the server to inform clients
        # of entity dict adds, updates, and removals
        self.events.on('entity_added', self.event_handler.entity_created)
        self.events.on('entity_updated', self.event_handler.entity_updated)
        self.events.on('entity_removed', self.event_handler.entity_removed)
        self.events.on('entity_moved', self.event_handler.entity_moved)

    def create_player(self, client):
        player = Player()
        client.player = player
        client.player_id = id(player)
        return player

    def get_players(self):
        players = []
        for client in self.clients:
            players.append(client.player)
        return players

    def ident_for_player(self, search_player):
        for player in self.get_players():
            if player is search_player:
                return id(player)

    def get_client_by_player_id(self, player_id):
        for client in self.clients:
            if id(client.player) == player_id:
                return client


    def add_client(self, client):
        self.clients.append(client)

    def get_client(self, search_client):
        for client in self.clients:
            if client is search_client:
                return client
    
    def remove_client(self, client):
        self.clients.remove(client)

    def player_for_ident(self, ident):
        return self.get_players()[ident]


#
#   Announcement definitions
#

    def announce_entity_created(self, entity_id, data):
        # If the created entity was a player associated with a clinet,
        # Skip them from this broadcast
        skip_client = self.get_client_by_player_id(entity_id)
        self.broadcast_except(skip_client, EntityCreated, 
            entity_id = entity_id,
            data = data)
        pass

    def announce_entity_updated(self, entity_id, data):
        pass

    def announce_entity_removed(self, entity_id):
        pass

    def announce_entity_moved(self, entity_id, x, y, orientation):
        skip_client = self.get_client_by_player_id(entity_id)
        self.broadcast_except(skip_client, EntityMoved,
            entity_id = entity_id,
            x = x,
            y = y,
            orientation = orientation)

    def announce_entity_moving(self, entity_id, x, y):
        skip_client = self.get_client_by_player_id(entity_id)
        self.broadcast_except(skip_client, EntityMoving,
            entity_id = entity_id,
            x = x,
            y = y)

    def broadcast(self, command, *args, **kwargs):
        for client in self.clients:
            client.callRemote(command, *args, **kwargs)

    def broadcast_except(self, skip_clients, command, *args, **kwargs):
        if type(skip_clients) is not list:
            skip_clients = [skip_clients]
        for client in self.clients:
            if not client in skip_clients:
                client.callRemote(command, *args, **kwargs)
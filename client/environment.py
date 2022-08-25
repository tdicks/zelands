from shared.simulation import SimulationTime
from shared.entity import Entity
from client.player import Player
from client.events import EnvironmentEventHandler

import pygame

class Environment(SimulationTime):
    initial_player = None
    client = None
    level = None

    def __init__(self, *a, **kw):
        SimulationTime.__init__(self, *a, **kw)
        self.observers = []
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()

        self.event_handler = None

        """
        Keep track of our player sprite ID as some game 
        events won't actually apply to this.
        """
        self.player_entity_id = None

    def set_level(self, level):
        self.level = level

    def set_initial_player(self, player):
        self.initial_player = player

    def set_event_handler(self, handler):
        self.event_handler = handler

    def set_client(self, client):
        """
        Add an instance of the network client so the environment
        can call methods on it
        """
        self.client = client

    def add_observer(self, observer):
        self.observers.append(observer)

    def create_player(self, player_id):
        self.player = Player()
        self.player.import_assets()
        self.player_entity_id = player_id
        self.player.add(self.all_sprites)
        self.add_entity(player_id, self.player)
        self.player.events.on('entity_moved', self.event_handler.player_moved)
        self.player.events.on('entity_moving', self.event_handler.player_moving)
        return self.player

    def create_server_entity(self, entity_id):
        ent = Entity()
        ent.import_assets()
        ent.server_entity_id = entity_id
        ent.add(self.all_sprites)
        self.add_entity(entity_id, ent)
        return ent 

    # Consider renaming this function to place_entity
    # Plus all the other associated stuff
    def move_entity(self, entity_id, x, y, orientation):
        if self.entity_exists(entity_id):
            entity = self.entities[entity_id]
            entity.set_position((x, y))
            entity.set_orientation(orientation)

    def direct_entity(self, entity_id, x, y):
        """
        Make an entity start moving in a particular direction
        """
        if self.entity_exists(entity_id):
            entity = self.entities[entity_id]
            entity.set_direction(x, y)

    def run(self, dt):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
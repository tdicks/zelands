from shared.simulation import SimulationTime
from shared.entity import Entity
from client.player import Player

import pygame

class Environment(SimulationTime):
    initial_player = None
    network = None
    level = None

    def __init__(self, *a, **kw):
        SimulationTime.__init__(self, *a, **kw)
        self.observers = []
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

    def set_level(self, level):
        self.level = level

    def set_initial_player(self, player):
        self.initial_player = player

    def set_network(self, network):
        self.network = network

    def add_observer(self, observer):
        self.observers.append(observer)

    def create_player(self, position, status):
        self.player = Player((400,300), self.all_sprites)
        return self.player

    def create_entity(self, position, status):
        ent = Entity(position, self.all_sprites)
        return ent 

    def run(self, dt):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
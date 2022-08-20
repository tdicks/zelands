import random
from twisted.application.service import Service
from shared.network import UpdateEntityPosition
from shared.simulation import SimulationTime

from pygame.math import Vector2
from server.player import Player

class GameService(Service):
    def __init__(self, world):
        self.world = world

    def startService(self):
        self.world.start()

    def stopService(self):
        self.world.stop()

class World(SimulationTime):
    """
    Shared world environment where all players and entities are tracked
    """
    def __init__(self, random=random, granularity=1, platform_clock = None):
        SimulationTime.__init__(self, granularity, platform_clock)
        self.random = random
        self.clients = []

    def create_player(self, client):
        player = Player(Vector2(0, 0))
        self.get_client(client).player = player
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

    def get_client(self, search_client):
        for client in self.clients:
            if client is search_client:
                return client
    
    def remove_client(self, client):
        self.clients.remove(client)

    def player_for_ident(self, ident):
        return self.get_players()[ident]

    def update_player_positions(self):
        for client in self.clients:
            for player in self.get_players():
                if client.player is not player:
                    identifier = self.ident_for_player(player)
                    v = player.get_position()
                    pl_status = player.get_status()
                    if type(pl_status) != bytes:
                        pl_status = pl_status.encode()
                    client.callRemote(UpdateEntityPosition,
                        identifier = identifier,
                        x = v.x,
                        y = v.y,
                        status = pl_status)
                    #self.update_entity_position(player)

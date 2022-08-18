from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
from twisted.internet import reactor

from shared.network import (
    PlayerConnected, PlayerDisconnected, SetDirectionOf, SetMyDirection,
    RemovePlayer
)

class GameServer(AMP):

    def __init__(self, world, clock=reactor):
        self.world = world
        self.clock = clock
        self.players = {}
        self.player = None

    def playerCreated(self, player):
        self.notifyPlayerCreated(player)
        player.addObserver(self)

    def playerRemoved(self, player):
        identifier = self.identifierForPlayer(player)
        self.callremote(RemovePlayer, identifier = identifier)
        del self.players[identifier]

    def notifyPlayerCreated(self, player):
        v = self.getPosition()
        self.callRemote(NewPlayer,
            identifier=self.identifierForPlayer(player),
            x=v.x, y=v.y, z=v.z, speed=player.speed)

    def sendExistingState(self):
        self.sendExistingPlayers()

    def sendExistingPlayers(self):

        for player in self.world.getPlayers():
            if player is not self.player:
                self.notifyPlayerCreated(player)
                player.addObserver(self)
        self.world.addObserver(self)

    def directionChanged(self, player):
        v = player.getPosition()
        self.callRemote(SetDirectionOf,
            identifier = self.identifierForPlayer(player),
            direction=player.direction,
            x=v.x, y=v.y, z=v.z,
            orientation=player.orientation.y)

    def setMyDirection(self, direction, y):
        self.player.orientation.y = y
        self.player.setDirection(direction)
        v = self.player.getPosition()
        return {'x': v.x, 'y': v.y, 'z': v.z}
    SetMyDirection.responder(setMyDirection)

    def identifierForPlayer(self, player):
        self.players[id(player)] = player
        return id(player)

    def playerForIdentifier(self, identifier):
        return self.players[identifier]

    def connectionLost(self, reason):
        self.world.removePlayer(self.player)

class GameServerFactory(ServerFactory):
    def __init__(self, world):
        self.world = world

    def buildProtocol(self, ignored):
        return GameServer(self.world)
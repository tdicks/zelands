# The websocket server gets fired up and attached to this

import yaml
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from events import EventHandler
from profiles import ProfileManager
from random import random

class ClientManager(LineReceiver):

    def __init__(self, factory):
        self.setLineMode()
        self.factory = factory
        self.sid = len(self.factory.clients) + 1
        self.rcon_auth = False
        self.profile_manager = ProfileManager()
        self.event_handler = EventHandler()
        self.state = "NOAUTH"

    def sendLine(self, line):
        LineReceiver.sendLine(self, line.encode('utf-8'))

    def connectionMade(self):
        print("Client %i connected" % (self.sid))
        self.factory.clients[self.sid] = self

    def connectionLost(self, reason):
        if (self.sid in self.factory.clients):
            del self.factory.clients[self.sid]
        print("Client %i disconnected" % (self.sid))

    def lineReceived(self, data):
        response = self.event_handler.handle_data(self, data)
        if (response != None):
            self.sendLine(response)

class GameServerFactory(Factory):
    def __init__(self, config):
        self.config = config
        self.clients = {}

    def buildProtocol(self, addr):
        return ClientManager(self)

with open('config/server.yaml', 'r') as file:
    config = yaml.safe_load(file)

reactor.listenTCP(config['network']['listen_port'], GameServerFactory(config))
reactor.run()
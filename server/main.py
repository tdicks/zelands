# The websocket server gets fired up and attached to this

import yaml
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from events import EventHandler
from profiles import ProfileManager

class GameServerProtocol(LineReceiver):

    def __init__(self, factory):
        self.setLineMode()
        self.factory = factory
        self.sid = self.factory.generate_sid()
        self.rcon_auth = False
        self.profile_manager = ProfileManager(self)
        self.event_handler = EventHandler(self)
        self.state = "NOAUTH"

    def send(self, data):
        LineReceiver.sendLine(self, data.encode('utf-8'))

    def connectionMade(self):
        if len(self.factory.clients) >= self.factory.max_clients:
            self.transport.loseConnection()
            return

        print("Client %i connected" % (self.sid))
        self.factory.clients[self.sid] = self

    def connectionLost(self, reason):
        if (self.sid in self.factory.clients):
            print("Client %i disconnected" % (self.sid))
            del self.factory.clients[self.sid]

    def lineReceived(self, data):
        response = self.event_handler.handle_data(data)
        if (response != None):
            self.send(response)

class GameServerFactory(Factory):
    def __init__(self, config):
        self.config = config
        self.clients = {}
        self.last_sid = 0
        self._max_sid = 9000
        self.max_clients = config['max_clients']

    def buildProtocol(self, addr):
        return GameServerProtocol(self)

    def generate_sid(self):
        self.last_sid = self.last_sid + 1
        if self.last_sid > self._max_sid:
            self.last_sid = 0
        return self.last_sid

    def send_all(self, data):
        for cl in self.clients:
            self.clients[cl].send(data)

with open('config/server.yaml', 'r') as file:
    config = yaml.safe_load(file)

reactor.listenTCP(config['network']['listen_port'], GameServerFactory(config))
reactor.run()
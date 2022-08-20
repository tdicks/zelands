import yaml
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from twisted.protocols.policies import ProtocolWrapper, WrappingFactory
from client.view import Window
from client.network import NetworkController
from client.level import Level

class ConnectionNotificationWrapper(ProtocolWrapper):

    def makeConnection(self, transport):
        ProtocolWrapper.makeConnection(self, transport)
        self.factory.connectionNotification.callback(self.wrappedProtocol)

class ConnectionNotificationFactory(WrappingFactory):
    protocol = ConnectionNotificationWrapper
    def __init__(self, realFactory):
        WrappingFactory.__init__(self, realFactory)
        self.connectionNotification = Deferred()

class UI(object):
    
    config = None
    protocol = None

    def __init__(self, reactor=reactor, windowFactory=Window):
        self.reactor = reactor
        self.windowFactory = windowFactory

    def connect(self, host, port):
        clientFactory = ClientFactory()
        clientFactory.protocol = lambda: NetworkController(
            self.reactor
        )
        factory = ConnectionNotificationFactory(clientFactory)
        self.reactor.connectTCP(host, port, factory)
        return factory.connectionNotification

    def join_server(self, protocol):
        self.protocol = protocol
        return self.protocol.join_server()

    def server_joined(self, thing):
        # We've joined the server, now tell the server we want to spawn
        # and create our environment
        return self.protocol.player_initial_spawn()

    def player_initial_spawn(self, environment):
        self.window = self.windowFactory(self.reactor)
        self.window.config = self.config
        self.window.environment = environment
        environment.start()
        return self.window.go()

    def start(self, host, port):
        d = self.connect(host, port)
        d.addCallback(self.join_server)
        d.addCallback(self.server_joined)
        d.addCallback(self.player_initial_spawn)
        return d




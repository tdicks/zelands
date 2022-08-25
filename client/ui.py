import yaml
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from twisted.protocols.policies import ProtocolWrapper, WrappingFactory
from client.view import Window
from client.network import NetworkController
from client.level import Level
from client.environment import Environment
from client.events import EnvironmentEventHandler

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
    environment = None

    def __init__(self, reactor=reactor, windowFactory=Window):
        self.reactor = reactor
        self.windowFactory = windowFactory

    def connect(self, host, port):
        clientFactory = ClientFactory()
        clientFactory.protocol = lambda: NetworkController(
            clock=self.reactor
        )
        factory = ConnectionNotificationFactory(clientFactory)
        self.reactor.connectTCP(host, port, factory)
        return factory.connectionNotification

    def join_server(self, protocol):
        self.protocol = protocol
        return self.protocol.join_server()

    def create_environment(self, thing):
        # We've joined the server, now create our environment and
        # introduce the environment and network client to each other
        self.environment = Environment(platform_clock=self.reactor, granularity=100)
        self.environment.set_client(self.protocol)
        self.protocol.set_environment(self.environment)
        self.environment.set_event_handler(EnvironmentEventHandler(self.environment))
        self.environment.start()
        #return self.protocol.player_initial_spawn()

    def start_ui(self, thing):
        self.window = self.windowFactory(self.reactor)
        self.window.config = self.config
        self.window.environment = self.environment
        self.protocol.send_client_ready()
        return self.window.go()

    #def client_ready(self, thing):
    #    return self.protocol.send_client_ready()

    def do_error(self, someting):
        print(someting)

    def start(self, host, port):
        d = self.connect(host, port)
        d.addBoth(self.join_server)
        d.addCallback(self.create_environment)
        d.addCallback(self.start_ui)
        #d.addCallback(self.client_ready)
        return d




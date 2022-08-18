from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from twisted.protocols.policies import ProtocolWrapper, WrappingFactory
#from client.main import Game
from client.network import NetworkController

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
    
    def __init__(self, reactor=reactor):
        self.reactor = reactor

    def connect(self, host, port):
        clientFactory = ClientFactory
        clientFactory.protocol = lambda: NetworkController(
            self.reactor
        )
        factory = ConnectionNotificationFactory(clientFactory)
        self.reactor.connectTCP(host, port, factory)
        return factory.connectionNotification

    def introduce(self, protocol):
        self.protool = protocol
        return self.protool.introduce()

    def start(self, host, port):
        d = self.connect(host, port)
        d.addCallback(self.introduce)
        d.addCallback(self.got_introduced)
        return d




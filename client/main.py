# Main piece of code that combines the game client, the UI, and the server

from client.ui import UI
from twisted.internet import reactor
from client.environment import Environment

class GameClient():
    reactor = None
    uiFactory = None

    def __init__(self, config):
        self.reactor = reactor
        #self.environment = Environment(platform_clock=reactor, granularity=100)
        self.uiFactory = UI
        self.uiFactory.config = config
        #self.uiFactory.environment = self.environment
        self.config = config
        

    def run(self, host, port):
        d = self.uiFactory().start(host, port)
        d.addCallback(lambda ignored: self.reactor.stop())
        self.reactor.run()

    def main(self):
        host = "localhost"
        port = 19820
        self.run(host, port)
        
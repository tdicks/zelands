# Main piece of code that combines the game client, the UI, and the server

from client.ui import UI
from twisted.internet import reactor

class NetworkClient():
    reactor = None
    uiFactory = None

    def __init__(self):
        self.reactor = reactor
        self.uiFactory = UI

    def run(self, host, port):
        d = self.uiFactory().start(host, port)
        d.addCallback(lambda ignored: self.reactor.stop())
        self.reactor.run()

    def main(self):
        host = "localhost"
        port = 19820
        self.run(host, port)
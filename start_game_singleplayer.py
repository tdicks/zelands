
import yaml
from client.main import GameClient
from os.path import join
from zope.interface import implementer, provider


from server.network import GameServerFactory
from server.world import World
from server.network import GameServerFactory

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.logger import globalLogPublisher, Logger, ILogObserver, eventAsText

@provider(ILogObserver)
def simpleObserver(event):
    print(eventAsText(event))

log = Logger()

globalLogPublisher.addObserver(simpleObserver)

with open("config/server.yaml", 'r') as file:
    server_config = yaml.safe_load(file)

world = World(granularity = 100, platform_clock = reactor)

endpoint = TCP4ServerEndpoint(reactor, 19820)
endpoint.listen(GameServerFactory(world, server_config))

with open('config/client.yaml', 'r') as file:
    config = yaml.safe_load(file)

GameClient(config).main()




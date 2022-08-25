import yaml
import os
from zope.interface import implementer

from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer
from twisted.plugin import IPlugin
from twisted.python import usage


from server.network import GameServerFactory
from server.world import World
from server.network import GameServerFactory

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

# This is a headless dedicated server
# Set the video driver to dummy so pygame doesn't show a window
os.environ['SDL_VIDEODRIVER'] = 'dummy'

with open("config/server.yaml", 'r') as file:
    config = yaml.safe_load(file)

world = World(granularity = 100, platform_clock = reactor)

endpoint = TCP4ServerEndpoint(reactor, 19820)
endpoint.listen(GameServerFactory(world, config))
reactor.run()
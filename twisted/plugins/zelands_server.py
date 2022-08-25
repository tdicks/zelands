import yaml
import os
from zope.interface import implementer

from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer
from twisted.plugin import IPlugin
from twisted.python import usage

# This is a headless dedicated server
# Set the video driver to dummy so pygame doesn't show a window
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class Options(usage.Options):
    optParameters = [
        ('config', 'c', "config/server.yaml", 'Optional config file to run the server under')
    ]

@implementer(IPlugin, IServiceMaker)
class ZelandsServiceMaker(object):

    tapname = "zelands_server"
    description = "Zelands Server"
    options = Options
    
    def makeService(self, options):
        # Steal most of this from the ~game-hackers repo
        from pygame.image import load
        from server.network import GameServerFactory
        from server.world import GameService, World
        
        from twisted.internet import reactor
        from twisted.python.filepath import FilePath
        from twisted.application.service import MultiService
        from twisted.protocols.policies import TrafficLoggingFactory

        with open(options['config'], 'r') as file:
            config = yaml.safe_load(file)

        world = World(granularity = 100, platform_clock = reactor)
        service = MultiService()
        factory = GameServerFactory(world, config)

        tcp = TCPServer(config['network']['listen_port'], factory)
        tcp.setName(config['service']['tcp_service_name'])
        tcp.setServiceParent(service)

        gameservice = GameService(world)
        gameservice.setName(config['service']['game_service_name'])
        gameservice.setServiceParent(service)

        return service

service_maker = ZelandsServiceMaker()

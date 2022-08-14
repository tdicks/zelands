# The websocket server gets fired up and attached to this

import yaml
from websocket import WebSocketServer
from events import EventHandler

class GameServer:

    def __init__(self):
        self.server = None
        self.event_handler = None
        self.config = None

    def start(self):
        address = self.config['network']['listen_addr']
        port = self.config['network']['listen_port']
        self.server = WebSocketServer(address, port)
        self.server.event_handler = EventHandler()

if __name__ == "__main__":
    gs = GameServer()
    with open('config/server.yaml', 'r') as file:
        gs.config = yaml.safe_load(file)
    gs.start()
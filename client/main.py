# Insane in the main game!

import pygame
import yaml
import sys
import os
from pygame.locals import *
from threading import Thread
from twisted.internet.task import LoopingCall
from events import EventHandler
from level import Level
from client import NetworkClient

class Game:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self.config = None
        self.size = None
        self.event_handler = None
        self.network_client = None

    def on_init(self):
        pygame.init()
        pygame.display.set_caption(self.config["window"]["title"])
        self.size = self.width, self.height = self.config['window']['width'], self.config['window']['height']
        self._display_surface = pygame.display.set_mode(self.size,HWSURFACE)
        self.clock = pygame.time.Clock()
        self.level = Level()
        self._running = True
        self.event_handler = EventHandler(self)
        self.network_client = NetworkClient(self)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.event_handler.handle(event)

    def on_loop(self):
        dt = self.clock.tick() / 1000
        self.level.run(dt)
        pygame.display.update()
       
    
    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        #while(self._running):
        for event in pygame.event.get():
            self.on_event(event)

        self.on_loop()
        self.on_render()
        #self.on_cleanup()

if __name__ == "__main__":
    game = Game()
    with open('config/client.yaml', 'r') as file:
        game.config = yaml.safe_load(file)
    tick = LoopingCall(game.on_execute())
    tick.start(1.0 / 60)
    #game.network_client.start()
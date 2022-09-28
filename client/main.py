# Insane in the main game!

import pygame
import yaml
import sys
from os import path
from pygame.locals import *
from events import EventHandler
from level import Level
from player import *

# added fps to be used by clock.tick to slow bullet rate
FPS = 60
class Game:
    def __init__(self):
        self._running = True
        self.playing = False
        self._display_surface = None
        self.config = None
        self.size = None
        self.event_handler = None

    def on_init(self):
        pygame.init()
        pygame.display.set_caption(self.config["window"]["title"])
        self.size = self.width, self.height = self.config['window']['width'], self.config['window']['height']
        self._display_surface = pygame.display.set_mode(self.size,HWSURFACE)
        
        self.clock = pygame.time.Clock()
        self.level = Level()
        self._running = True
        self.event_handler = EventHandler(self)
        self.game_paused = False


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.event_handler.handle(event)

    def on_loop(self):
        dt = self.clock.tick(FPS) / 1000
        self.level.run(dt)
        pygame.display.update()
    
    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()
        exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    game = Game()
    with open(path.join('config','client.yaml'), 'r') as file:
        game.config = yaml.safe_load(file)
    game.on_execute()
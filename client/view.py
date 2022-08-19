# Insane in the main game!

#from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import pygame
import yaml
import sys
import os
from pygame.locals import *
#from events import EventHandler
from client.level import Level
from client.player import *

from twisted.internet.task import LoopingCall
from twisted.internet import reactor

"""
Class that deals with the game window and callbacks for events
"""

class Window:
    def __init__(self, clock=reactor, display=pygame.display, event=pygame.event):
        self._running = True
        self._display_surface = None
        self._display_loop = None
        self._input_loop = None
        self._update_loop = None
        self.display = display
        self.config = None
        self.clock = clock
        self.pg_clock = pygame.time.Clock()
        self.size = None
        self.event = event
        self.event_handler = None

    def go(self):
        pygame.init()
        self.display.init()
        self.display.set_caption(self.config["window"]["title"])
        self.size = self.width, self.height = self.config['window']['width'], self.config['window']['height']
        self.level = Level()
        self.screen = self.display.set_mode(self.size, HWSURFACE)
        self._display_loop = LoopingCall(self.display_loop)
        self._display_loop.start(1 / 60, now=False)
        self._input_loop = LoopingCall(self.handle_input)
        finished_deferred = self._input_loop.start(0.04, now=False)
        finished_deferred.addCallback(lambda ign: self._display_loop.stop())
        finished_deferred.addCallback(lambda ign: self.display.quit())

        return finished_deferred

    def stop(self):
        if self._update_loop is not None:
            self._update_loop.stop()
        self._input_loop.stop()
        pygame.quit()

    def handle_input(self):
        for event in self.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        print(event)
        if event.type == pygame.QUIT:
            self.stop()
        """
        elif self.controller is not None:
            if event.type == pygame.KEYDOWN:
                self.controller.key_down(event.key)
            elif event.type == pygame.KEYUP:
                self.controller.key_up(event.key)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.event.get_grab():
                    self.controller.mouse_motion(
                        event.pos, event.rel, event.buttons
                    )
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.event.set_grab(not pygame.event.get_grab())
                pygame.mouse.set_visible(not pygame.mouse.set_visible(True))
        """
    def display_loop(self):
        dt = self.pg_clock.tick() / 1000
        self.level.run(dt)
        pygame.display.update()
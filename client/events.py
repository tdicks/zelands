import pygame

class EventHandler:

    def __init__(self, game):
        self.game = game
        self.key_down = KeyDown()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_down.handle(event)
        


class KeyDown:
    def handle(self, event):
        pass

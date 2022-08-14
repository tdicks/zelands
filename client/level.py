import pygame
from player import Player


class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
    
        self.setup()
    
    def setup(self):
        self.player = Player((400,300), self.all_sprites)

    def run(self,dt):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
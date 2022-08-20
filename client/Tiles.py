import pygame, os
from Settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','rocksprite.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

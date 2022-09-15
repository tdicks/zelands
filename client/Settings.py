import pygame, os
pygame.mixer.init()

FPS = 60
WIDTH, HEIGHT = int(1280), int(980)
TILESIZE = 56
#BGM = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'SOM31.mp3'))
FONT = os.path.join('assets','8-BIT WONDER.TTF')

WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
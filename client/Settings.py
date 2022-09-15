import pygame, os
pygame.mixer.init()

FPS = 60
WIDTH, HEIGHT = int(1280), int(980)
TILESIZE = 56
#BGM = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'SOM31.mp3'))
FONT = os.path.join('client','menu','8-BIT WONDER.TTF')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
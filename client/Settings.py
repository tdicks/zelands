import pygame, os
pygame.mixer.init()
FPS = 60
WIDTH, HEIGHT = int(1280), int(720)
TILESIZE = 64
BGM = pygame.mixer.Sound(os.path.join('Assets', 'RSPTN.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
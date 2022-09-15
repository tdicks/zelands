from re import X
from typing import Type
import os
import pygame
import random
pygame.init()
font_name = os.path.join('client','menu','cambriab.TTF')
font = pygame.font.Font(font_name, 14)
fsize = 12
WHITE = (255,255,255)

def debug(info, x = 10, y = 10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info),True, (255, 255, 255))
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, 'black', debug_rect.inflate(10,10))
    display_surface.blit(debug_surf,debug_rect)

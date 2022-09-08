from re import X
from typing import Type
import pygame
import random
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info),True, (255, 255, 255))
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, 'black', debug_rect)
    display_surface.blit(debug_surf,debug_rect)

print(5 + 6 % 3 * 3)
a = 6 % 3
b = 3 * 3
print(5 + a * 3)
print(5 + 6 % b)


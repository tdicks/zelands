import pygame
from os.path import join
from Settings import TILESIZE,WHITE,BLACK
import time
import textwrap
from debug import debug as db
pygame.init()

#font settings for floating text:
font_name = join('client','menu','cambriab.TTF')
size = 20
font = pygame.font.Font(font_name, size)
fsize = 12
WHITE = (255,255,255)


#sprite loading / modification functions
def load_collision_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def load_usable_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 1.5, rect.height* 1.5)
    return image, rect, hitbox, info_range

def load_walkable_tile(lst,pos):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    return image, rect

def load_weapon(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 3, rect.height* 3)
    return image, rect, hitbox, info_range

def load_player(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image, (TILESIZE - image.get_width()/4,TILESIZE))
    rect = image.get_rect(center = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def tile_rotate(image,amount):
    return pygame.transform.rotate(image,amount)

# in-game functions

def outline_text(in_text,sprite_topleft,displacement, colour):
    i = displacement
    displacement_list = [(-i,-i),(-i, i),(i,i),(i,-i)]
    display_surface = pygame.display.get_surface()
    font = pygame.font.Font(font_name, size)
    text_colour = colour
    for d in displacement_list:
        for i,item in enumerate(in_text):
            text_surface = font.render(item,True, text_colour)
            text_rect = text_surface.get_rect(bottomleft = (sprite_topleft[0] + d[0], sprite_topleft[1] + (i * 20)+ d[1]))
            display_surface.blit(text_surface, text_rect) 
        

def floating_text(in_text, sprite_topleft, colour, better):
    text_colour = colour
    display_surface = pygame.display.get_surface()
    for i,item in enumerate(in_text):
        if i > 3:
            if better[i-4] == -1:
                text_colour = (255,0,0)
            if better[i-4] == 1:
                text_colour = (0,255,0)
        else: 
            text_colour = (255,255,255)
    
        text_surface = font.render(item,True, text_colour)
        text_rect = text_surface.get_rect(bottomleft = (sprite_topleft[0], sprite_topleft[1] + (i * 20)))
        display_surface.blit(text_surface, text_rect)    

# Camera functions
def zoom_keys(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        self.zoomscale += 0.1
    if keys[pygame.K_e]:
        self.zoomscale -= 0.1
    
    if self.zoomscale > 1.6:
        self.zoomscale = 1.6
    if self.zoomscale < 0.5:
        self.zoomscale = 0.5
    self.zoomscale = round(self.zoomscale, 1)
    #time.sleep(0.1)

import pygame,os
from Settings import TILESIZE

def load_collision_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(os.path.join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def load_usable_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(os.path.join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 1.5, rect.height* 1.5)
    return image, rect, hitbox, info_range

def load_walkable_tile(lst,pos):
    image = pygame.image.load(os.path.join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    return image, rect

def load_player(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(os.path.join(*lst)).convert_alpha()
    image = pygame.transform.scale(image, (TILESIZE - image.get_width()/4,TILESIZE))
    rect = image.get_rect(center = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def load_weapon(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(os.path.join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 3, rect.height* 3)
    return image, rect, hitbox, info_range

def tile_rotate(image,amount):
    return pygame.transform.rotate(image,amount)

def actual_mouse_loc():
    mouse_x, mouse_y = pygame.mouse.get_pos()
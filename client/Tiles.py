import pygame, os
from Settings import *
from shared_functions import (load_collision_tile, load_weapon,
load_walkable_tile, load_usable_tile, tile_rotate)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','green_SMG.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -((self.image.get_height()/2) - 3))


class Corner_Wall(pygame.sprite.Sprite):
    def __init__(self, pos,rotation, groups):
        super().__init__(groups)
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','walls','wall1_32_topleft.png'],pos,hitbox_x=0,hitbox_y=0)
        self.image = tile_rotate(self.image,90 * rotation)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos,rotation, groups):
        super().__init__(groups)
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','walls','wall1_32_top.png'],pos)
        self.image = tile_rotate(self.image, rotation * 90)


class Broken_Wall(pygame.sprite.Sprite):
    def __init__(self, pos,rotation, groups):
        super().__init__(groups)
        if rotation == 0:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','Bwall1_32_top.png')).convert_alpha()
        if rotation == 1:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','Bwall1_32_right.png')).convert_alpha()
        if rotation == 2:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','Bwall1_32_bottom.png')).convert_alpha()
        if rotation == 3:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','Bwall1_32_left.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        if rotation == 2:
            self.hitbox = self.rect.inflate(0,0)
        else:
            self.hitbox = self.rect.inflate(0,-10)


class Treasure(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','objects','chest.png'],pos,0,-20)


class Half_Wall(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','halfwall1_32.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-25)


class Future_Floor1(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','floors','floorboard_32.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)


class Future_Floor2(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','floors','floorboard2_32.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)


class Wood_Floor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect = load_walkable_tile(['assets','sprites','caves_env','floors','floorboard_32.png'],pos)


class SMG_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, rarity, gun_info, groups):
        super().__init__(groups)
        self.gun_details = gun_info.information.items() 
        if rarity == 'white':
            self.image, self.rect, self.hitbox, self.info_range = load_weapon(['assets','sprites','white_SMG.png'],pos)
        if rarity == 'green':
            self.image, self.rect, self.hitbox, self.info_range = load_weapon(['assets','sprites','green_SMG.png'],pos)
        if rarity == 'blue':
            self.image, self.rect, self.hitbox, self.info_range = load_weapon(['assets','sprites','blue_SMG.png'],pos)
        if rarity == 'purple':
            self.image, self.rect, self.hitbox, self.info_range = load_weapon(['assets','sprites','purple_SMG.png'],pos)
        if rarity == 'gold':
            self.image, self.rect, self.hitbox, self.info_range = load_weapon(['assets','sprites','gold_SMG.png'],pos)

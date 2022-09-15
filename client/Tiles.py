import pygame, os
from settings import *
from shared_functions import (load_collision_tile, load_weapon,
load_walkable_tile, load_usable_tile, tile_rotate)

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
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','walls','Bwall1_32_top.png'],pos)
        self.image = tile_rotate(self.image, rotation * 90)

class Treasure(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','objects','chest.png'],pos,0,-20)

class Half_Wall(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect, self.hitbox = load_collision_tile(['assets','sprites','caves_env','walls','halfwall1_32.png'],pos)

class Future_Floor1(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect = load_walkable_tile(['assets','sprites','caves_env','floors','floorboard_32.png'],pos)

class Future_Floor2(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image, self.rect = load_walkable_tile(['assets','sprites','caves_env','floors','floorboard2_32.png'],pos)

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

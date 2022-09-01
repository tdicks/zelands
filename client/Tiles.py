import pygame, os
from Settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','objects','pillar_64_192.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE*3))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -self.image.get_height()/2)

class Corner_Wall(pygame.sprite.Sprite):
    def __init__(self, pos,rotation, groups):
        super().__init__(groups)
        if rotation == 0:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_topleft.png')).convert_alpha()
        if rotation == 1:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_topright.png')).convert_alpha()
        if rotation == 2:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_bottomleft.png')).convert_alpha()
        if rotation == 3:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_bottomright.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos,rotation, groups):
        super().__init__(groups)
        if rotation == 0:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_top.png')).convert_alpha()
        if rotation == 1:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_right.png')).convert_alpha()
        if rotation == 2:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_bottom.png')).convert_alpha()
        if rotation == 3:
            self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','walls','wall1_32_left.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        if rotation == 2:
            self.hitbox = self.rect.inflate(0,0)
        else:
            self.hitbox = self.rect.inflate(0,-10)

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
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','objects','chest.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-15)

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
        self.image = pygame.image.load(os.path.join('assets','sprites','caves_env','floors','floorboard_32.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
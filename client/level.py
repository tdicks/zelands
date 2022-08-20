import random
import time

import pygame
from Settings import *
from Tiles import Tile
from player import Player
import pygame.sprite
import time

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

class Generator:
    def __init__(self):
        self.blank = ' '

    def map_generation(grid=20,seed_number=random.randint(0,10000)): # uses a default grid size of 20 and a random integer for the seed number if not specified
        map_base = [['X' for i in range(0, grid)] for j in range(0, grid)] # saturates a 20 x 20 grid with 'X'
        random.seed(seed_number)
        for i in range(1, grid-1):           #
            for j in range(1, grid-1):       #   these 3 lines take the rows and columns 1 tile in from each side a saturates them as '_' (free space)
                map_base[i][j] = '_'     #
                if i in range(2,grid-2) and j in range(2,grid-2):
                    if 'X' in [map_base[i - 1][j], map_base[i + 1][j], map_base[i][j - 1], map_base[i][j + 1]]:
                        if random.randint(1,1000) % 6 == 0: # increses the chance of like-objects spawning if there is another present in any adjacent tile
                            map_base[i][j] = 'X'
                # lines 25-28 place objects in the free spaces if a random number is perfectly divisable
                if random.randint(1, 1000) % 17 == 0:
                    map_base[i][j] = 'X'
                if random.randint(1, 1000) % 73 == 0:
                    map_base[i][j] = 'T'
            # rows 30 - 36 checks the map for empty tiles and appends them to a list as tuples then selects the player start location
        open_ground = []
        for r_index, row in enumerate(map_base):
            for col_index, text in enumerate(row):
                if text == '_':
                    open_ground.append((r_index,col_index))
        map_x,map_y = random.choice(open_ground)
        map_base[map_x][map_y] = 'P'
        for row in map_base: # prints map to console for debugging
            print(row)
        return map_base

class Level:
    def __init__(self, dt):
        valid = False
        while not valid:
            try:
                self.gridsize = int(input('enter map size [0 for default] : '))
                valid = True
            except (TypeError,ValueError):
                print('Should be an interger')
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obst_sprites = pygame.sprite.Group()
        if self.gridsize == 0:
            self.map = Generator.map_generation()
        else:
            self.map = Generator.map_generation(self.gridsize)
        self.dt = dt
        self.create_map()

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(self.dt)

    def create_map(self):
        for row_indx, row in enumerate(self.map):
            for col_indx, col in enumerate(row):
                x = col_indx * TILESIZE # TILESIZE is stored in Settings.py
                y = row_indx * TILESIZE
                if col == 'X':
                    Tile((x,y), [self.visible_sprites, self.obst_sprites]) # Tile is a member of both 'visible...' and 'obst...'
            for col_indx, col in enumerate(row):
                x = col_indx * TILESIZE # TILESIZE is stored in Settings.py
                y = row_indx * TILESIZE        
                if col == 'P':
                    print(f'x: {x}    y: {y}')
                    Player((x,y), [self.visible_sprites], self.obst_sprites) # Player is a member of 'visible...' and only references 'obst...'

#class Level:
#    def __init__(self):
#
        # get display surface
#        self.display_surface = pygame.display.get_surface()

        # sprite groups
#        self.all_sprites = pygame.sprite.Group()
    
#        self.setup()
    
#    def setup(self):
#        self.player = Player((400,300), self.all_sprites)

#   def run(self,dt):
#        self.display_surface.fill('white')
#        self.all_sprites.draw(self.display_surface)
#        self.all_sprites.update(dt)
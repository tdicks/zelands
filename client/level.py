import random

from items import SMG 
from camera import SpritesByLayerCamera
import pygame
from Settings import TILESIZE
from Tiles import *
from player import Player
import pygame.sprite
from data_stores import level_tile_lib
from debug import debug as dbug

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000



class Generator:
    def __init__(self):
        self.blank = ' '

    def map_generation(grid=20,seed_number=random.randint(0,10000)): # uses a default grid size of 20 and a random integer for the seed number if not specified
        map_base = [['__' for i in range(0, grid)] for j in range(0, grid)] # saturates a 20 x 20 grid with '__' - (double underscore [to adjust map output to 2 characters])
        random.seed(seed_number)
        for i in range(1, grid-1):           #
            for j in range(1, grid-1):       #   these 3 lines take the rows and columns 1 tile in from each side a saturates them as '_' (free space)
                map_base[i][j] = '__'     #
                if i in range(2,grid-2) and j in range(2,grid-2):
                    if 'HW' in [map_base[i - 1][j], map_base[i + 1][j], map_base[i][j - 1], map_base[i][j + 1]]:
                        if random.randint(1,1000) % 6 == 0: # increses the chance of like-objects spawning if there is another present in any adjacent tile
                            map_base[i][j] = 'HW'
                    if random.randint(1, 1000) % 13 == 0:
                        map_base[i][j] = 'HW'
                    if random.randint(1, 1000) % 31 == 0:
                        map_base[i][j] = 'TR'
        map_base[0][0] = 'CWTL'
        map_base[0][-1] = 'CWTR'
        map_base[-1][0] = 'CWBL'
        map_base[-1][-1] = 'CWBR'
        for i in range(1,grid -1):
            map_base[0][i] = 'TW'
            map_base[i][0] = 'LW'
            map_base[-1][i] = 'BW'
            map_base[i][-1] = 'RW'
            # rows 30 - 36 checks the map for empty tiles and appends them to a list as tuples then selects the player start location
        open_ground = []
        for r_index, row in enumerate(map_base):
            for col_index, text in enumerate(row):
                if text == '__' and r_index in range(2,grid-2) and col_index in range(2,grid-2):
                    open_ground.append((r_index,col_index))
        map_x,map_y = random.choice(open_ground)
        map_base[map_x][map_y] = 'P'
        #for row in map_base: # prints map to console for debugging
            #print(row)
        return map_base

class Level:
    def __init__(self, dt):
        valid = True
        while not valid:
            try:
                self.gridsize = int(input('enter map size [0 for default] : '))
                valid = True
            except (TypeError,ValueError):
                print('Should be an interger')
        self.gridsize = 14
        self.visible_sprites = SpritesByLayerCamera()
        self.visible_floor_sprites = pygame.sprite.Group()
        self.obst_sprites = pygame.sprite.Group()

        # region Map_Creation
        self.map1 = Generator.map_generation(self.gridsize,random.randint(1,2345))
        self.map2 = Generator.map_generation(self.gridsize,random.randint(1,5324))
        self.map3 = Generator.map_generation(self.gridsize,random.randint(1,6278))
        self.map4 = Generator.map_generation(self.gridsize,random.randint(1,3445))
        self.map5 = Generator.map_generation(self.gridsize,random.randint(1,2235))
        self.map6 = Generator.map_generation(self.gridsize,random.randint(1,5876))
        self.map7 = Generator.map_generation(self.gridsize,random.randint(1,5785))
        self.map8 = Generator.map_generation(self.gridsize,random.randint(1,8793))
        self.map9 = Generator.map_generation(self.gridsize,random.randint(1,9374))
        self.maps = [self.map1, self.map2, self.map3, self.map4,self.map5,
                    self.map6, self.map7, self.map8, self.map9]
        # endregion
        # region Base_X,Y for each room
        self.co_ord_list = []
        for i in range(0,4):    
            for j in range(0,5):
                co_ords = [TILESIZE * self.gridsize * i,TILESIZE * self.gridsize * j]
                self.co_ord_list.append(co_ords)
        self.room_coords = self.room_layout()

        # endregion
        self.dt = dt
        self.create_map()
        self.create_player()

    def room_layout(self):
        self.__layout_selection = random.choice(['layout1','layout2','layout3','layout4','layout5',
                        'layout6','layout7','layout8','layout9','layout10','layout11','layout12','layout13'])
        self.map_layout = level_tile_lib[self.__layout_selection]
        self.layout_tuples = []
        count = 0
        for row in self.map_layout:
            for room in row:
                count += 1
                if room == 'X':
                    continue
                else:
                    x_origin = self.co_ord_list[count-1][0]
                    y_origin = self.co_ord_list[count-1][1]
                    self.layout_tuples.append((x_origin,y_origin))                
        return self.layout_tuples
        

    def run(self):
        self.visible_floor_sprites.update()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(self.dt)

    def create_map(self):
        guns = []
        count = 0
        for map, origin in zip(self.maps,self.room_coords):
            count += 1
            x_origin = origin[0]
            y_origin = origin[1]
            for row_indx, row in enumerate(map):
                for col_indx, col in enumerate(row):
                    x = x_origin + (col_indx * TILESIZE) # TILESIZE is stored in Settings.py
                    y = y_origin + (row_indx * TILESIZE)
                    # during the following 'if' statements the number following co-ordinates (x,y) is a rotation value
                    # 0 = north , 1 = east, 2 = south, 3 = west
                    if col == 'TW':
                        if random.randint(1,20) % 13 == 0:
                            Broken_Wall((x,y), 0, [self.visible_sprites, self.obst_sprites])
                        else:
                            Wall((x,y), 0, [self.visible_sprites, self.obst_sprites])
                    if col == 'RW':
                        if random.randint(1,20) % 13 == 0:
                            Broken_Wall((x,y), 3, [self.visible_sprites, self.obst_sprites])
                        else:
                            Wall((x,y), 3, [self.visible_sprites, self.obst_sprites])
                    if col == 'BW':
                        if random.randint(1,20) % 13 == 0:
                            Broken_Wall((x,y), 2, [self.visible_sprites, self.obst_sprites])
                        else:
                            Wall((x,y), 2, [self.visible_sprites, self.obst_sprites])
                    if col == 'LW':
                        if random.randint(1,20) % 13 == 0:
                            Broken_Wall((x,y), 1, [self.visible_sprites, self.obst_sprites])
                        else:
                            Wall((x,y), 1, [self.visible_sprites, self.obst_sprites])
                    if col == '__' or col == 'P' or col == 'TR' or col == 'HW' :
                        if random.randint(1,15) % 6 == 0:
                            Future_Floor2((x,y), [self.visible_sprites]) # draw ground tile on open ground AND player spawn location
                        else:
                            Future_Floor1((x,y), [self.visible_sprites])
                    if col == 'HW':
                        Half_Wall((x,y), [self.visible_sprites, self.obst_sprites])
                    if col == 'CWTL':
                        Corner_Wall((x,y), 0, [self.visible_sprites, self.obst_sprites])
                    if col == 'CWTR':
                        Corner_Wall((x,y), 3, [self.visible_sprites, self.obst_sprites])
                    if col == 'CWBL':
                        Corner_Wall((x,y), 1, [self.visible_sprites, self.obst_sprites]) 
                    if col == 'CWBR':
                        Corner_Wall((x,y), 2, [self.visible_sprites, self.obst_sprites])
                    if col == 'TR':
                        if random.randint(0,19) % 3 == 0:
                            Treasure((x,y), [self.visible_sprites, self.obst_sprites])
                        else:
                            gun = SMG()
                            guns.append(gun)
                            #print('This is my gun ::', gun.information())
                            SMG_Tile((x,y), gun.weapon_rarity, gun, [self.visible_sprites, self.obst_sprites]) # Tile is a member of both 'visible...' and 'obst...'
                for col_indx, col in enumerate(row):
                    x = x_origin + (col_indx * TILESIZE) # TILESIZE is stored in Settings.py
                    y = y_origin + (row_indx * TILESIZE)        
                    if col == 'P':
                            player_spawn = (x,y)
                    #
                #
            #
        self.stored_spawn = Player(player_spawn, [self.visible_sprites], self.obst_sprites) # Player is a member of 'visible...' and only references 'obst...'

    def create_player(self):
        self.player = self.stored_spawn
        self.stored_spawn



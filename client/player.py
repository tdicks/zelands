
from turtle import speed, width
import pygame
import math
import os
from Settings import TILESIZE
from Tiles import *
from shared_functions import load_player, floating_text, outline_text
from support import *
from debug import debug as db

display = pygame.display.set_mode((800,600))

# create bullet list
player_bullets = []

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group,obstacle_sprites):
        super().__init__(group)
        
        #self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image, self.rect, self.hitbox = load_player(['assets','sprites','mario.png'], pos)
        self.obstacle_sprites = obstacle_sprites
        self.weapon_load_count = 0

        # movement attributes

		# general setup
        #self.image = self.animations[self.status][self.frame_index]
        #self.rect = self.image.get_rect(center = pos)

		# movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 4

    def inventory(self):
        """character storage using two library variables \'slot1\' and \'slot2\'"""
        self.slot1 = {
            'Weapon Level': 2,
            'Weapon Type': 'SMG',
            'Weapon Rarity': 'purple',
            'Weapon Manufacturer': 'Judicium',
            'Damage': 16,
            'Accuracy': 65,
            'Clip Size': 54,
            'Reload': 16,
            'Ammo Capacity': 647
            }
        self.slot2 = {
            'Weapon Level': 1,
            'Weapon Type': 0,
            'Weapon Rarity': 0,
            'Weapon Manufacturer': 0,
            'Damage': 0,
            'Accuracy': 0,
            'Clip Size': 0,
            'Reload': 0,
            'Ammo Capacity': 0
            }
        while self.weapon_load_count < 1:
            self.held_weapon = self.slot1.items()
            self.weapon_load_count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if self.slot1['Weapon Level'] == None:
                pass
            else:
                self.held_weapon = self.slot1.items()
        if keys[pygame.K_2]:
            if self.slot2['Weapon Level'] == None:
                pass
            else:
                self.held_weapon = self.slot2.items()
        
        for i, item in enumerate(self.held_weapon):
            db(item,10, i * 20)

    def import_assets(self):
        #key pairs for all possible animations
        self.animations = {'up': [],'down': [],'left': [], 'right': [],'up_idle': [], 'down_idle': [],'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = os.path.join('assets','sprites','character', animation)
            self.animations[animation] = import_folder(full_path)
    
    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))

    def input(self):     
        keys = pygame.key.get_pressed()
        # will need to change the keys to use the config file but struggle with this one.
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        
        self.facing = self.status

        # Only needed to check direction of player in terminal
        # print(self.direction)
        
    def pew(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_bullets.append(PlayerBullet(self.pos.x, self.pos.y, mouse_x, mouse_y))

        for bullet in player_bullets:
            bullet.main(display)

    def get_status(self):

        # checks if player is in a state of movement if its not it appends the status with _idle 
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def true_mouse_location(self):
        """finds the mouse location in the world based 
        off of the player location and mouse location 
        within the screen"""
        self.plyr_x, self.plyr_y = self.rect.center
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.true_mouse_x = (self.plyr_x - (display.get_width() / 2)) + self.mouse_x
        self.true_mouse_y = (self.plyr_y - (display.get_height() / 2)) + self.mouse_y
        return self.true_mouse_x, self.true_mouse_y

    def move(self,dt):
        # normalizing a vector to stop double movement speed while moving diagonally. Sorry Tim :(
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')

        # vertical movement
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        self.item_info_range()


    def spriteinfo(self, sprite):
        """adds mouse-over information for item sprites when within their \'info_range\' distance"""
        self.true_mouse_x, self.true_mouse_y = self.true_mouse_location()
        self.display_surface = pygame.display.get_surface()
        placement = self.mouse_x - 32, self.mouse_y - 184
        if self.hitbox.colliderect(sprite.info_range) and sprite.rect.collidepoint(self.true_mouse_x,self.true_mouse_y):
            details_list = []
            text_list = []
            held_info = []
            better = []
            for i,detail in enumerate(sprite.gun_details):
                dkey, dvalue = detail
                if dkey in details_list:
                    continue
                else:
                    details_list.append((dkey, dvalue))
                    text_list.append(f"{dkey} {dvalue}")
                
                if dkey == 'Weapon Rarity':
                    colour = dvalue

            for i,detail in enumerate(self.held_weapon):
                hkey, hval = detail
                if hkey in held_info:
                    continue
                else:
                    held_info.append((hkey, hval))
                
            for i in range(4,9):
                held_value,pickup_value = held_info[i][1],details_list[i][1]
                try:
                    print(held_value,   pickup_value)
                    if held_value > pickup_value:   
                        better.append(-1)
                    if held_value == pickup_value:
                        better.append(0)
                    if held_value < pickup_value:
                        better.append(1)
                    else:
                        better.append('null')
                except:
                    pass

            displacement = 2
            outline_text(text_list, placement, displacement, 'black')
            floating_text(text_list, placement, colour, better)
        

    def item_info_range(self):
        for sprite in self.obstacle_sprites:
            if isinstance(sprite, SMG_Tile):
                                self.spriteinfo(sprite)
 

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            count = 0
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
        
    
    def update(self, dt):
        self.input()
        self.pew()
        self.get_status()
        self.move(dt)
        self.true_mouse_location()
        self.inventory()
        #self.animate(dt)
        

# bullet creation
class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.lifetime = 50
        self.bullet_velocity = 15
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.bullet_velocity
        self.y_vel = math.sin(self.angle) * self.bullet_velocity
        self.radius = 5

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.radius)
        self.lifetime -= 1
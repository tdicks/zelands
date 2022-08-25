from turtle import speed, width
import pygame
import math
import os
from client.support import *
from shared.entity import Entity
display = pygame.display.set_mode((800,600))
test = 0

"""
Player entity which supports local input
"""

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
       
    def input(self):
        global test
        
        keys = pygame.key.get_pressed()
        # will need to change the keys to use the config file but struggle with this one.
        if keys[pygame.K_w]:
            # up
            self.direction.y = -1
            test = test + 1
            #print(test)
        elif keys[pygame.K_s]:
            # down
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            # left
            self.direction.x = -1
        elif keys[pygame.K_d]:
            # right
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        # Only needed to check direction of player in terminal
        #print(self.direction)
        
        # get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        #check if mouse is pressed
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            # add bullet to bullet list
            player_bullets.append(PlayerBullet(self.pos.x, self.pos.y, mouse_x, mouse_y))
        for bullet in player_bullets:
            bullet.main(display)



    def update(self, dt):
        # Do the input processing and then the superclass update
        self.input()
        super().update(dt)

        


# create bullet list
player_bullets = []

# bullet creation
class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.bullet_velocity = 3
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.bullet_velocity
        self.y_vel = math.sin(self.angle) * self.bullet_velocity

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x, self.y), 3)

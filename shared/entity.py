from turtle import speed, width
import pygame
import math
import os
from client.support import *

"""
Base entity class
Supports basic movement and animation
"""
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
       
        self.observers = []

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

		# general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

		# movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

    def import_assets(self):
        # key pairs for all possible animations
        self.animations = {'up': [],'down': [],'left': [], 'right': [],'up_idle': [], 'down_idle': [],'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = os.path.join('assets','sprites','character', animation)
            self.animations[animation] = import_folder(full_path)
    
    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def apply_status(self):
        # checks if player is in a state of movement if its not it appends the status with _idle 
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
    def move(self,dt):
        # normalizing a vector to stop double movement speed while moving diagonally. Sorry Tim :(
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

        for observer in self.observers:
            observer.ob_entity_moved(self)

    def update(self, dt):
        self.apply_status()
        self.move(dt)
        self.animate(dt)

    def add_observer(self, observer):
        self.observers.append(observer)

    def get_position(self):
        return self.pos

    def set_position(self, position):
        self.pos = position

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status
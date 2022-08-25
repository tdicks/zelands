from turtle import speed, width
import pygame
import math
import os
from client.support import *
from shared.events import EventManager

"""
Base entity class
Supports basic movement and animation
"""
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       
        self.callbacks = {}

        self.import_assets()
        self.orientation = 'down'
        self.frame_index = 0

        self._layer = 2

		# general setup
        self.image = self.animations[self.orientation][self.frame_index]
        self.rect = self.image.get_rect(center = (0,0))
        self.events = EventManager()

		# movement attributes
        self.direction = pygame.math.Vector2()
        # Used to control entity_moving trigger
        self.previous_direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

        self.moving = False

        self.server_entity_id = None

    def import_assets(self):
        # key pairs for all possible animations
        self.animations = {'up': [],'down': [],'left': [], 'right': [],'up_idle': [], 'down_idle': [],'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = os.path.join('assets','sprites','character', animation)
            self.animations[animation] = import_folder(full_path)
    
    def animate(self,dt):

        animation = self.orientation
        if self.is_idle:
            animation = animation + "_idle"

        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[animation]):
            self.frame_index = 0
        self.image = self.animations[animation][int(self.frame_index)]

    def idle_check(self):
        """
        Keep the is_idle property up to date depending on whether the
        entity is moving or not.
        """
        if self.direction.magnitude() == 0:
            self.is_idle = True
        else:
            self.is_idle = False
        
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

        # check if our direction has changed, including 0,0 (stopped)
        if self.direction.x != self.previous_direction.x or \
            self.direction.y != self.previous_direction.y:

            # Moving also changes our orientation, so set it here
            if self.direction.y == -1:
                self.orientation = 'up'
            elif self.direction.y == 1:
                self.orientation = 'down'
            elif self.direction.x == -1:
                self.orientation = 'left'
            elif self.direction.x == 1:
                self.orientation = 'right'

            # it has, so trigger the entity_moving event
            self.events.trigger('entity_moving', self)
        
        # Have to set the x and y attributes directly otherwise
        # python just adds a reference to the original Vector() object
        # and then the direction check doesn't work!
        self.previous_direction.x = self.direction.x
        self.previous_direction.y = self.direction.y


    def update(self, dt):
        self.idle_check()
        self.move(dt)
        self.animate(dt)

    def set_direction(self, x, y):
        """
        Set the direction the entity is heading towards.
        Up:     y=-1
        Down:   y=1
        Left:   x=-1
        Right:  x=1
        Stop:   x=0, y=0

        The client will render the entity's movement, the server
        just tells the client which direction go to in.
        """
        self.direction.x = x
        self.direction.y = y

    def get_direction(self):
        return self.direction

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        pass

    # No use for these at the moment...
    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_orientation(self):
        return self.orientation

    def set_orientation(self, orientation):
        """
        Forcibly set the orientation of the entity
        """
        self.orientation = orientation

class Missile(object):
    """
    Base class for bullets, magic missiles, arrows, and any other types of airborne pain delivery.
    """

    velocity = None
    base_dmg = 0

    def __init__(self):
        pass

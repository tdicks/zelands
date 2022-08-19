from turtle import speed, width
import pygame
import math
import os
from support import *

display = pygame.display.set_mode((800, 600))

# create bullet list
player_bullets = []


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group,obstacle_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = pygame.image.load(os.path.join('assets', 'mario.png'))
        self.rect = self.image.get_rect(center=pos)
        self.obstacle_sprites = obstacle_sprites

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

    def import_assets(self):
        # key pairs for all possible animations
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'up_idle': [], 'down_idle': [],
                           'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = os.path.join('assets', 'sprites', 'character', animation)
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

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

        # Only needed to check direction of player in terminal
        # print(self.direction)

        # get mouse position

        # for event in pygame.event.get():

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

    def move(self, dt):
        # normalizing a vector to stop double movement speed while moving diagonally. Sorry Tim :(
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.pew()
        self.get_status()
        self.move(dt)
        self.animate(dt)


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
        self.x_vel = math.cos(self.angle) * self.bullet_velocity
        self.y_vel = math.sin(self.angle) * self.bullet_velocity
        self.radius = 5

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.radius)
        self.lifetime -= 1
        """def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: #moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: #moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom"""


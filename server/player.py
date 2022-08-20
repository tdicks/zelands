"""
Server-side repesentation of a player
"""

from shared.entity import Entity
from pygame.math import Vector2

class Player(Entity):
    def __init__(self, position, status='down_idle'):
        self.pos = position
        self.status = status
    
    def spawn(self):
        self.set_position(Vector2(200, 200))
        #self.move()
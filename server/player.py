"""
Server-side repesentation of a player
"""

from shared.entity import Entity
from pygame.math import Vector2

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)

    
    def spawn(self):
        self.set_position(Vector2(200, 200))
        self.orientation = "down"
        self.events.trigger('player_spawn')
        #self.move()
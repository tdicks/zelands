"""
Server-side repesentation of a player
"""

class Player(object):
    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position
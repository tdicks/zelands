"""
Network client for zelands
"""

from pygame import Vector2
from twisted.protocols.amp import AMP
from shared.network import (
  SetDirectionOf, SetMyDirection
)

class NetworkController(AMP):
  """
  Controller which handles AMP commands from the server
  and makes state changes in the local environment
  """

  def __init__(self, clock):
    self.clock = clock
    self.modelObjects = {}

  def addModelObject(self, identifier, modelObject):
    self.modelObjects[identifier] = modelObject
    modelObject.addObserver(self)

  def directionChanged(self, modelObject):
    """
    Send an instruction to the server that the local player has changed direction
    """

    d = self.callRemote(
      SetMyDirection,
      direction=modelObject.direction, y=modelObject.orientation.y)
    d.addCallback(self._gotNewPosition, modelObject)
    
  def _gotNewPosition(self, position, player):
    player.setPosition(Vector2(position['x'], position['y']))
from twisted.protocols.amp import (
  AMP, Command, Integer, Float, Argument, String
)

class PlayerConnected(Command):
  """
  (Server to client)
  Client has connected to the server
  """
  response = [('sid', Integer()),
              ('name', String())]

class PlayerDisconnected(Command):
  """
  (Server to client)
  Client has disconnected from the server
  """
  response = [('sid', Integer()),
              ('name', String())]

class RemovePlayer(Command):
  arguments = [('identifier', Integer())]

class SetMyDirection(Command):
  """
  (Client to server)
  Client has moved position/direction in the game
  """

  arguments =  [('direction', String())]

  response = [('x', Float()),
              ('y', Float())]

class SetDirectionOf(Command):
  """
  (Server to client)
  Sets the direction of a player
  """

  arguments = [('identifier', Integer()),
               ('direction', String()),
               ('x', Float()),
               ('y', Float())]
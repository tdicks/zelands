"""
Networking module which has shared requests/responses etc
"""

from urllib import response
from twisted.protocols.amp import (
    Command, Integer, Float, String, Argument
)


class PlayerConnected(Command):
    """
    Sent by the client to the server when connected.
    (clent to server)
    """
    response = [(b'identifier', Integer()),
                (b'granularity', Integer())]

class PlayerInitialSpawn(Command):
    """
    Sent by the client to the server requesting an initial spawn
    """
    response = [(b'identifier', Integer()),
                (b'x', Integer()),
                (b'y', Integer()),
                (b'status', String())]

class PlayerMoved(Command):
    """
    Sent by the client to the server when the client's player
    entity moves position
    """
    arguments = [(b'x', Integer()),
                 (b'y', Integer()),
                 (b'status', String())]

class UpdateEntityPosition(Command):
    """
    Sent by the server to the client telling them that another
    player has moved
    """
    arguments = [(b'identifier', Integer()),
                 (b'x', Integer()),
                 (b'y', Integer()),
                 (b'status', String())]
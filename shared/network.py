"""
Networking module which has shared requests/responses etc
"""

from twisted.protocols.amp import (
    Command, Integer, Float, String, Argument
)


"""
Sent by the client to the server when connected.
(clent to server)
"""
class Introduce(Command):
    response = [(b'identifier', Integer()),
                (b'granularity', Integer()),
                (b'x', Integer()),
                (b'y', Integer())]

"""
class SetMyPosition(Command):
    arguments = [(b'')]
"""
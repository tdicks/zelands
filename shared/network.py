"""
Networking module which has shared requests/responses etc
"""

from twisted.protocols.amp import (
    Command, Integer, Float, String, Argument
)

class Introduce(Command):
    response = [(b'identifier', Integer()),
                (b'granularity', Integer()),
                (b'x', Integer()),
                (b'y', Integer())]
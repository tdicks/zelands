# Definitions of various event types used by both client and server

from enum import Enum

class Message(Enum):
  ClientConnected = "clientconnected"         # New client has joined the server
  ClientDisconnected = "clientdisconnected"   # Client has left the server
  ClientPlayerAction = "clientplayeraction"   # A client's player has done something (moved, shot etc)
  ServerStateUpdate = "serverstateupdate"     # A server state update has been issued to clients
  ServerMoveUpdate = "servermoveupdate"

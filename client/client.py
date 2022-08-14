# Gameserver client
# This module handles interaction between the game client and the game server

import socketio

sock = socketio.Client()

class Client:
  
  socket = None
  
  def __init__(self):
    self.socket = sock
    
  @sock.event
  def message(data):
    pass

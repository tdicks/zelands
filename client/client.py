# Gameserver client
# This module handles interaction between the game client and the game server

import socketio

class Client:
  
  socket = None
  
  def __init__(self):
    self.socket = socketio.Client()
    
  @socket.event
  def message(data):
    pass

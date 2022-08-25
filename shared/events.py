# Event handling module
# Used by both client and server to allow triggering of events
# which objects can request callbacks to.
from enum import Enum

class Event(Enum):
    ClientConnected = "client-connected"         # New client has joined the server
    ClientDisconnected = "client-disconnected"   # Client has left the server
    ClientPlayerAction = "client-player-action"   # A client's player has done something (moved, shot etc)
    ServerStateUpdate = "serverstateupdate"     # A server state update has been issued to clients
    ServerMoveUpdate = "servermoveupdate"

class EventManager:
    """
    Event subscription and triggering class

    On an event manager instance, call evtmgr.on('my-event', my_callback)

    When 'my-event' is triggered, the my_callback function will be executed.

    To trigger events, call evtmgr.trigger('my-event'). All the callbacks will be executed.
    """

    def __init__(self):
      self.callbacks = {}

    def on(self, event, callback):
      """
      Add a function to be called when the specified event is triggered by the entity.
      """
      if event not in self.callbacks:
          self.callbacks[event] = [callback]
      else:
          self.callbacks[event].append(callback)

    def trigger(self, event, *argv):
      """
      Triggers the callbacks for all subscribers of the specified event
      """
      if event in self.callbacks:
          for callback in self.callbacks[event]:
            try:
                callback(*argv)
            except BaseException as e:
              print('Caught exception in callback: ' + str(e))

    def remove(self, *callbacks):
      """
      Removes a callback from all events
      """

      # Loop through all the events
      # For each callback provided, check
      # if it exists in the callbacks list
      # and remove it if it does.
      for event in self.callbacks.keys():
        for search_cb in callbacks:
          if search_cb in self.callbacks[event]:
            self.callbacks[event].remove(search_cb)
        
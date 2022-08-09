from http.client import NON_AUTHORITATIVE_INFORMATION
import socketio

class Server:
    pass

    socket = None

    def __init__(self):
        self.socket = socketio.AsyncServer(async_mode='asgi')

    @socket.event
    def connect(sid, sock):
        pass

    @socket.event
    def disconnect(sid):
        pass

    @socket.event
    def get_name(sid):
        pass

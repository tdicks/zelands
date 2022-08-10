from http.client import NON_AUTHORITATIVE_INFORMATION
import socketio
import eventlet
from eventlet import wsgi

sock = socketio.Server(async_mode='eventlet')

class WebSocketServer:
    
    def __init__(self, _listen_addr, _listen_port):
        self.socket = sock
        self.event_handler = None
        self.app = socketio.WSGIApp(self.socket)
        wsgi.server(eventlet.listen((_listen_addr, _listen_port)), self.app)

    @sock.event
    def connect(sid, sock):
        pass

    @sock.event
    def disconnect(sid):
        pass

    # Send everything that doesn't already have a handler to our own EventHandler
    @sock.on('*')
    def catch_all(self, event, sid, data):
        self.event_handler.handle(event, sid, data)

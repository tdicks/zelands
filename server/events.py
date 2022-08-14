import json
from typing import Union
import sys
import os

sys.path.append(os.getcwd())

from shared.requests import *

class EventHandler:
    def __init__(self, client):
        self.client = client
        pass

    def json_response(self, response):
        if type(response) == str:
            return json.dumps({"message": response})
        else:
            return json.dumps(response)

    def handle_data(self, bytes):
        try:
            request = json.loads(bytes)
            if not request.keys() >= {"type", "data"}:
                return self.json_response("Missing type and/or data keys")

            reqtype = request['type']
            data = request['data']

            if reqtype == 'player_auth':
                if data.keys() >= {"username", "password"}:
                    username = data['username']
                    password = data['password']
                    return self.player_auth(username, password)

            if reqtype == 'rcon_auth':
                password = data['password']
                return self.rcon_auth(password)

            if reqtype == 'rcon_command':
                command = data['command']
                return self.rcon_command(command)

            if reqtype == "player_move":
                if data.keys() >= {"status", "direction"}:
                    status = data['status']
                    direction = data['direction']
                    self.player_move(status, direction)

        except:
            print(sys.exc_info())
            return self.json_response("Invalid JSON, command, or missing parameters")

    def player_auth(self, username, password):
        if username=='tom' and password=='pass':
            self.client.load_profile()

    def player_move(self, status, direction):
        data = {"type": "player_move", "data": {
            "sid": self.client.sid,
            "status": status,
            "direction": direction
        }}
        self.client.factory.send_all(self.json_response(data))

    def rcon_auth(self, password):
        if password == self.client.factory.config['rcon_password']:
            self.client.rcon_auth = True
            return self.json_response('Authenticated!')

    def rcon_command(self, command):
        if not self.client.rcon_auth:
            return self.json_response("No RCON auth")

        if command == 'status':
            clients = []
            for i in self.client.factory.clients:
                cl = self.client.factory.clients[i]
                row = {}
                row["sid"] = cl.sid
                row["ip"] = "%s:%s" % (cl.transport.client[0], cl.transport.client[1])
                row["rcon"] = cl.rcon_auth
                clients.append(row)
            return json.dumps(clients)
            
        if command.startswith("kick"):
            id = int(command.split(' ')[1])
            if id in self.client.factory.clients.keys():
                self.client.factory.clients[id].transport.loseConnection()
                return self.json_response("SID kicked")
            else:
                return self.json_response("SID not found")

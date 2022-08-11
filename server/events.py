import json
import sys

class EventHandler:
    def __init__(self):
        pass

    def handle_data(self, client, datastr):
        try:
            data = json.loads(datastr)
            payload = data['payload']

            if payload == 'player_auth':
                return self.player_auth(client, payload['username'], payload['password'])

            if payload == 'rcon_cmd':
                return self.rcon_command(client, data['cmd'])

            if payload == 'rcon_auth':
                return self.rcon_auth(client, data['password'])
        except:
            print(sys.exc_info()[0])
            return json.dumps("Invalid JSON, command, or missing parameters")


    def player_auth(self, client, username, password):
        if username=='tom' and password=='pass':
            client.load_profile()

    def rcon_auth(self, client, password):
        if password == client.factory.config['rcon_password']:
            client.rcon_auth = True

    def rcon_command(self, client, command):
        if not client.rcon_auth:
            return "No RCON auth"
        if command == 'status':
            clients = []
            for i in client.factory.clients:
                cl = client.factory.clients[i]
                row = {}
                row["sid"] = cl.sid
                row["ip"] = "%s:%s" % (cl.transport.client[0], cl.transport.client[1])
                row["rcon"] = cl.rcon_auth
                clients.append(row)
            return json.dumps(clients)
        if command.startswith("kick"):
            id = int(command.split(' ')[1])
            if id in client.factory.clients.keys():
                client.factory.clients[id].transport.loseConnection()
                return "SID kicked"
            else:
                return "SID not found"

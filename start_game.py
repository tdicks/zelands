import sys
import yaml
from client.main import GameClient

with open('config/client.yaml', 'r') as file:
    config = yaml.safe_load(file)

GameClient(config).main()
import sys
import yaml
from client.main import NetworkClient

with open('config/client.yaml', 'r') as file:
    config = yaml.safe_load(file)

NetworkClient(config).main()
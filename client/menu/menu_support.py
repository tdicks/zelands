import yaml,os

def read_yaml():
    config = None
    # Read YAML file
    with open(os.path.join('config','client.yaml'), 'r') as file:
        config = yaml.safe_load(file)
    print(config['controls'])

read_yaml()
import yaml

def getConfig(file = 'config.yml'):
    with open(file ,'r') as stream:
        ports = yaml.safe_load(stream)
    return ports

import os
import configparser

class PropertyResolver:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('app/properties.ini')
        print(config.sections())
        self.url = os.environ.get('WEBSITE', config.get('DEFAULT', 'website'))
        self.rabbit = os.environ.get('RABBIT', config.get('DEFAULT', 'rabbit'))

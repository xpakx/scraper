import os
import configparser

class PropertyResolver:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('app/properties.ini')
        print(config.sections())
        self.url = os.environ.get('WEBSITE_URL', config.get('DEFAULT', 'website'))
import os
import configparser

class PropertyResolver:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('app/properties.ini')
        print(config.sections())
        self.url = os.environ.get('WEBSITE_URL', config.get('DEFAULT', 'website_url'))
        self.rabbit = os.environ.get('RABBIT_HOST', config.get('DEFAULT', 'rabbit_host'))
        self.rabbit_port = os.environ.get('RABBIT_PORT', config.get('DEFAULT', 'rabbit_port'))

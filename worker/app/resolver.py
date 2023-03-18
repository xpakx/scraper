import os
import configparser

class PropertyResolver:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('app/properties.ini')
        print(config.sections())
        self.user_id = os.environ.get('USER_ID', config.get('DEFAULT', 'user_id'))
        self.url = 'https://citystrides.com/users/' + self.user_id
        self.rabbit = os.environ.get('RABBIT_HOST', config.get('DEFAULT', 'rabbit_host'))
        self.rabbit_port = os.environ.get('RABBIT_PORT', config.get('DEFAULT', 'rabbit_port'))

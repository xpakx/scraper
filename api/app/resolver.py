import os
import configparser

class PropertyResolver:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('app/properties.ini')
        self.rabbit = os.environ.get('RABBIT_HOST', config.get('DEFAULT', 'rabbit_host'))
        self.rabbit_port = int(os.environ.get('RABBIT_PORT', config.get('DEFAULT', 'rabbit_port')))
        self.db_url = os.environ.get("DB_URL", config.get('DEFAULT', 'db_url'))
        self.initial_data_file = os.environ.get("INITIAL_DATA_FILE", config.get('DEFAULT', 'initial_data_file'))

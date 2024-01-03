import configparser
import os

APP_NAME = 'FeedSphere'
APP_VERSION = '1.0.0-SNAPSHOT'
MINIMAL_CLIENT_VERSION = '1.0.0-SNAPSHOT'

INI_FILE = os.path.join(os.path.dirname(__file__), '../conf/development.ini')

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

HOST = CONFIG['server']['host']
PORT = CONFIG['server']['port']

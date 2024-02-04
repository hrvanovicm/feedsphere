import configparser
import os
import sys

APP_NAME = 'FeedSphere'
APP_VERSION = '1.0.0-SNAPSHOT'

PROD_INI_FILE = os.path.join(os.path.dirname(__file__), '../conf/production.ini')
DEV_INI_FILE = os.path.join(os.path.dirname(__file__), '../conf/development.ini')
INI_FILE = DEV_INI_FILE if '--development' in sys.argv else PROD_INI_FILE

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

APP_KEY = CONFIG['app']['key']

HOST = CONFIG['server']['host']
PORT = CONFIG['server']['port']


def reload_conf():
    global APP_KEY, HOST, PORT
    CONFIG.read(INI_FILE)

    APP_KEY = CONFIG['app']['key']

    HOST = CONFIG['server']['host']
    PORT = CONFIG['server']['port']

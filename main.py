from client import Client
from config import Config

# Obsłużenie pliku konfiguracyjnego
config = Config('config.json')

# Serwer MQTT
Client(config)
from client import Client
from config import Config
from gui.utils import show_error

try:
    # Obsłużenie pliku konfiguracyjnego
    config = Config('config.json')

    # Serwer MQTT
    Client(config)
except Exception as err:
    show_error(f'Wystąpił błąd. {err}')
import json
from tkinter import messagebox

from utils import show_error, dict_raise_duplicates, test_config
from client import Client

import paho.mqtt.client as mqtt

# Ładowanie pliku konfiguracyjnego config.json
try:
    with open('config.json', encoding='utf-8') as file:
        config = json.load(file, object_pairs_hook=dict_raise_duplicates)
except FileNotFoundError:
    show_error('Nie znaleziono pliku konfiguracyjnego config.json.')
except json.decoder.JSONDecodeError as err:
    show_error(f'Nie można odkodować pliku konfiguracyjnego config.json.\n{err}')
except ValueError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\nKlucz {err} powtórzył się.')

try:
    test_config(config)
except KeyError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\n{err}')
except ValueError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\n{err}')

# Serwer MQTT
Client(config)
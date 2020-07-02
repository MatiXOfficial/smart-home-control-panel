import json
from tkinter import messagebox

from utils import show_error, dict_raise_duplicates
from client import Client
from gui.input_frame import InputFrame

import paho.mqtt.client as mqtt

# Ładowanie pliku konfiguracyjnego config.json
try:
    with open('config.json', encoding='utf-8') as file:
        config = json.load(file, object_pairs_hook=dict_raise_duplicates)
except FileNotFoundError:
    show_error('Nie znaleziono pliku konfiguracyjnego config.json.')
except json.decoder.JSONDecodeError:
    show_error('Błąd w pliku konfiguracyjnym config.json.')
except ValueError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\nKlucz {err} powtórzył się.')

if 'nazwa' not in config:
    config['nazwa'] = InputFrame('Podaj nazwę').start_and_return()

if 'adres' not in config:
    config['adres'] = InputFrame('Podaj adres serwera').start_and_return()

# Serwer MQTT
Client(config)
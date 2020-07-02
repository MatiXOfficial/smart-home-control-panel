import json
from tkinter import messagebox

from main_frame import MainFrame
from utils import show_error, dict_raise_duplicates
from client import Client

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
    config['nazwa'] = input('Podaj nazwę: ')

if 'adres' not in config:
    config['adres'] = input('Podaj adres serwera: ')

# Serwer MQTT
Client(config)
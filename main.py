import json
from tkinter import messagebox

from main_frame import MainFrame
from utils import show_error, dict_raise_duplicates

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

# Połączenie z serwerem mqtt
try:
    client = mqtt.Client(config['nazwa'])
    client.connect(config['adres'])
except KeyError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\nBrak pola {err}.')
except ConnectionRefusedError:
    show_error('Nie można nawiązać połączenia z serwerem MQTT.')

client.loop_start()

# Główne okno pilota
MainFrame(config, client)

client.loop_stop()
client.disconnect()
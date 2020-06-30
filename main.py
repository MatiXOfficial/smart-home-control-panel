import json
from tkinter import messagebox

from gui.main_frame import MainFrame
from utils import show_error, dict_raise_duplicates


try:
    with open('config.json', encoding='utf-8') as file:
        config = json.load(file, object_pairs_hook=dict_raise_duplicates)

except FileNotFoundError:
    show_error('Nie znaleziono pliku konfiguracyjnego config.json.')
except json.decoder.JSONDecodeError:
    show_error('Błąd w pliku konfiguracyjnym config.json.')
except ValueError as err:
    show_error(f'Błąd w pliku konfiguracyjnym config.json.\nKlucz {err} powtórzył się.')


MainFrame(config)
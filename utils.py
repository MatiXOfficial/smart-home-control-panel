import tkinter as tk
from gui.input_frame import InputFrame

def show_error(error_message):
    '''
    Funkcja pomocnicza wyświetlająca okno z błędem.
    '''
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror('Błąd', error_message)
    exit()


def dict_raise_duplicates(pairs):
    '''
    Zwraca wyjątek gdy w pairs znajdują się duplikaty kluczy.
    W przeciwnym wypadku tworzy słownik na podstawie pairs.
    '''
    result = {}
    for key, val in pairs:
        if key in result:
            raise ValueError(key)
        else:
            result[key] = val
    return result

# Sprawdza poprawność słownika config oraz standaryzuje go w celu poprawnego działania programu.
def test_config(config):
    if 'nazwa' not in config:
        config['nazwa'] = InputFrame('Podaj nazwę').start_and_return()

    if 'adres' not in config:
        config['adres'] = InputFrame('Podaj adres serwera').start_and_return()

    config['topics'] = {}
    for room, devices in config['urządzenia'].items():
        for device, options in devices.items():
            if 'temat' not in options:
                if room in config['topics'] and device in config['topics'][room]:
                    raise ValueError(f'Nie można ustawić domyślnego tematu dla {room}: {device}. Urządzenie o temacie {room}/{device} jest już w pliku konfiguracyjnym.')

                options['temat'] = f'{room}/{device}'
            else:
                topic_room, topic_device = options['temat'].split('/')
                if topic_room in config['topics'] and topic_device in config['topics'][topic_room]:
                    raise ValueError(f'Zły temat w {room}: {device}. Urządzenie o tym temacie jest już w pliku konfiguracyjnym.')

                if topic_room not in config['topics']:
                    config['topics'][topic_room] = {}
                config['topics'][topic_room][topic_device] = {}
                config['topics'][topic_room][topic_device]['room'] = room
                config['topics'][topic_room][topic_device]['device'] = device

            if 'typ' not in options:
                options['typ'] = 'przełącznik'
            elif options['typ'] == 'suwak':
                if 'min' not in options:
                    options['min'] = 1
                else:
                    options['min'] = int(options['min'])
                if 'max' not in options:
                    raise KeyError(f'Brak wartości max w {room}: {device}.')
                else:
                    options['max'] = int(options['max'])                  
                if options['min'] >= options['max']:
                    raise ValueError(f'Wartość max powinna być większa od wartości min w {room}: {device}.')
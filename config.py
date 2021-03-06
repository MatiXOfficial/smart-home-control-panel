import json
from gui.utils import show_error
from gui.input_frame import InputFrame

class Config:
    '''
    Klasa obsługująca konfigurację pilota.
    '''
    def __init__(self, path):
        # Ładowanie pliku konfiguracyjnego config.json
        try:
            with open('config.json', encoding='utf-8') as file:
                self.data = json.load(file, object_pairs_hook=self.dict_raise_duplicates)
        except FileNotFoundError:
            show_error('Nie znaleziono pliku konfiguracyjnego config.json.')
        except json.decoder.JSONDecodeError as err:
            show_error(f'Nie można odkodować pliku konfiguracyjnego config.json.\n{err}')
        except ValueError as err:
            show_error(f'Błąd w pliku konfiguracyjnym config.json.\nKlucz {err} powtórzył się.')

        # Sprawdzanie poprawności załadowanej konfiguracji
        try:
            self._test_config_correct()
        except KeyError as err:
            show_error(f'Błąd w pliku konfiguracyjnym config.json.\n{err}')
        except ValueError as err:
            show_error(f'Błąd w pliku konfiguracyjnym config.json.\n{err}')

    # Metody zwracające elementy konfiguracji.
    @property
    def address(self):
        return self.data['adres']

    @property
    def name(self):
        return self.data['nazwa']      

    @property
    def temp(self):
        return self.data['temperatura'] 

    @property
    def rooms(self):
        return self.data['pokoje']

    def room(self, room):
        return self.data['pokoje'][room]

    def device(self, room, device):
        return self.data['pokoje'][room][device]

    @property
    def pub(self):
        '''
        Przedrostek dodawany do tematu przy każdym użyciu publish
        '''
        return self.data['publikacja']

    @property
    def sub(self):
        '''
        Przedrostek dodawany do tematu przy każym użyciu subscribe
        '''
        return self.data['subskrypcja']

    def is_temp_set(self):
        '''
        Zwraca True jeśli ustawiono kontrolę temperatury w słowniku.
        '''
        if self.temp is not None:
            return True
        else:
            return False

    def get_room_device(self, room, device):
        '''
        Zwraca nazwę pokoju i urządzenia potrzebne do tematu wykorzystując ew. wpis z topics.
        '''
        if room in self.data['topics'] and device in self.data['topics'][room]:
            old_room = room
            room = self.data['topics'][old_room][device]['room']
            device = self.data['topics'][old_room][device]['device']
        return room, device

    def add_device_state(self, room, device, mode, state):
        '''
        Dodaje stan początkowy do konfiguracji, jeśli dane urządzenie zostało podane w pliku config.json.
        '''
        if room in self.data['pokoje']:
            if device in self.data['pokoje'][room]:
                self.data['pokoje'][room][device][mode] = state

    def get_device_state(self, room, device, mode, default_value):
        '''
        Pobiera stan ze słownika. Jeśli nie ma, zwraca default_value
        '''
        if mode in self.data['pokoje'][room][device]:
            return self.data['pokoje'][room][device][mode]
        else:
            return default_value

    def add_temp_state(self, temp):
        '''
        Dodaje stan początkowy do temperatury, jeżeli została ona określona w pliku config.json.
        '''
        if self.is_temp_set():
            self.data['temperatura']['start'] = temp

    def get_temp_state(self):
        '''
        Pobiera stan początkowy temperatury ze słownika.
        '''
        return self.data['temperatura']['start']

    def _test_config_correct(self):
        '''
        Sprawdza poprawność słownika config oraz standaryzuje go w celu poprawnego działania programu.
        '''
        # Ewentualne uzupełnienie nazwy, adresu oraz przedrostków
        if 'nazwa' not in self.data:
            self.data['nazwa'] = InputFrame('Podaj nazwę').start_and_return()

        if 'adres' not in self.data:
            self.data['adres'] = InputFrame('Podaj adres serwera').start_and_return()

        if 'publikacja' not in self.data:
            self.data['publikacja'] = 'cmd'

        if 'subskrypcja' not in self.data:
            self.data['subskrypcja'] = 'var'

        # Ewentualne uzupełnienie albo sprawdzenie poprawności słownika temperatury
        if 'temperatura' not in self.data:
            self.data['temperatura'] = None
        else:
            if 'min' not in self.data['temperatura']:
                self.data['temperatura']['min'] = 15
            if 'max' not in self.data['temperatura']:
                self.data['temperatura']['max'] = 30
            if 'krok' not in self.data['temperatura']:
                self.data['temperatura']['krok'] = 0.5
            if 'start' not in self.data['temperatura']:
                self.data['temperatura']['start'] = (self.data['temperatura']['min'] + self.data['temperatura']['max']) / 2

            if self.data['temperatura']['min'] >= self.data['temperatura']['max']:
                show_error('Wartość max powinna być większa od wartości min w ustawieniach temperatury.')
            if self.data['temperatura']['krok'] <= 0:
                show_error('Wartość kroku w ustawieniach temperatury powinna być dodatnia.')
            if self.data['temperatura']['start'] < self.data['temperatura']['min']:
                show_error('Wartość początkowa temperatury nie może być mniejsza od wartości minimalnej.')
            if self.data['temperatura']['start'] > self.data['temperatura']['max']:
                show_error('Wartość początkowa temperatury nie może być większa od wartości maksymalnej.')

        # Utworzenie słownika, w którym będą tematy urządzeń
        self.data['topics'] = {}

        # Testowanie wszystkich pokoi
        for room, devices in self.data['pokoje'].items():
            for device, options in devices.items():
                # Ustawienie domyślnego tematu albo wybranego przez użytkownika
                if 'temat' not in options:
                    if room in self.data['topics'] and device in self.data['topics'][room]:
                        raise ValueError(f'Nie można ustawić domyślnego tematu dla {room}: {device}. Urządzenie o temacie {room}/{device} jest już w pliku konfiguracyjnym.')

                    options['temat'] = f'{room}/{device}'
                else:
                    topic_room, topic_device = options['temat'].split('/')
                    if topic_room in self.data['topics'] and topic_device in self.data['topics'][topic_room]:
                        raise ValueError(f'Zły temat w {room}: {device}. Urządzenie o tym temacie jest już w pliku konfiguracyjnym.')

                    if topic_room not in self.data['topics']:
                        self.data['topics'][topic_room] = {}
                    self.data['topics'][topic_room][topic_device] = {}
                    self.data['topics'][topic_room][topic_device]['room'] = room
                    self.data['topics'][topic_room][topic_device]['device'] = device

                # Ustawienie domyślnego typu albo sprawdzenie poprawności typu wybranego przez użytkownika
                if 'typ' not in options or options['typ'] == 'przełącznik':
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
                elif options['typ'] == 'tv':
                    if 'kanały' not in options:
                        show_error(f'W {room}: {device} należy podać liczbę kanałów.')
                    elif options['kanały'] <= 0:
                        show_error(f'Niedodatnia liczba kanałów w {room}: {device}.')

                    if "max głośność" not in options:
                        options['max głośność'] = 100
                    elif options['max głośność'] <= 0:
                        show_error(f'Niedodatnia maksymalna głośność w {room}: {device}.')
                elif options['typ'] == 'roleta':
                    pass
                else:
                    show_error(f"Zły typ: {options['typ']}.")

    @staticmethod
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
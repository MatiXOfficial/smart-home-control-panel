import tkinter as tk
from tkinter import ttk

from gui.tv_frame import TvFrame
from gui.utils import center_window

import math
from time import sleep

class MainFrame:
    '''
    Główne okno z pilotem sterującym inteligentym domem.
    '''
    def __init__(self, config, client):

        # Ustawienia okna
        self.root = tk.Tk()
        self.root.title('Pilot')
        self.root.iconbitmap('icon.ico')

        center_window(self.root)

        self.client = client

        # Słownik przycisków, suwaków itd.
        self.widgets = {}
        
        # Budowa zakładek i ramki z tekstem (_info_frame)
        self.config = config
        self._info_frame()
        self.load_config()
    
        # Ustawienie minimalnej wielkości okna na wielkość okna po zbudowaniu zakładek i ramki z tekstem
        self.root.update()
        self.root.minsize(self.root.winfo_width() + 20, self.root.winfo_height())

    # Rozpoczyna pętlę - wizualizacja okienka
    def start_loop(self):
        self.root.mainloop()
 
    def load_config(self):
        '''
        Funkcja ładująca konfigurację, tworzy zakładki i przyciski.
        '''
        # Ewentualne tworzenie panelu do zmiany temperatury
        if self.config.is_temp_set():
            self._add_temp_panel()

        # Tworzenie i wypełnianie zakładek
        tab_control = ttk.Notebook()

        for room, devices in self.config.rooms.items():
            # Zakładka
            tab = ttk.Frame(tab_control)
            tk.Grid.columnconfigure(tab, 0, weight=1)
            self.widgets[room] = {}

            # Wypisanie nazwy pokoju
            label_title = ttk.Label(tab, text=room, font=('default', 20))
            label_title.grid(row=0, column=0, columnspan=4, padx=30, pady=10)

            was_not_button = False
            # Wypisanie nazw urządzeń, stworzenie przycisków, suwaków itp.
            for i, device in enumerate(devices.keys()):
                label_device = ttk.Label(tab, text=device, font=('default', 15))
                label_device.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

                if device not in self.widgets[room]:
                    self.widgets[room][device] = {}

                # Przycisk On/Off
                if self.config.device(room, device)['typ'] == 'przełącznik':
                    self._add_button(tab, room, device, i + 1)

                # Suwak
                elif self.config.device(room, device)['typ'] == 'suwak':
                    self._add_button(tab, room, device, i + 1)
                    self._add_slider(tab, room, device, i + 1)
                    was_not_button = True

                # Tv
                elif self.config.device(room, device)['typ'] == 'tv':
                    self._add_button(tab, room, device, i + 1)
                    self._add_tv(tab, room, device, i + 1)
                    was_not_button = True

                # Roleta
                elif self.config.device(room, device)['typ'] == 'roleta':
                    self._add_blind_menu(tab, room, device, i + 1)
                    was_not_button = True

            if was_not_button:
                tk.Grid.columnconfigure(tab, 2, weight=1)
            else:
                tk.Grid.columnconfigure(tab, 1, weight=1)

            tab_control.add(tab, text=room)

        tab_control.pack(expand=True, fill='both', side='top')

    def _info_frame(self):
        '''
        Funkcja tworzy ramkę do wyświetlania informacji.
        '''
        frame = ttk.Frame(self.root)

        self.label_info = ttk.Label(frame, text=f'Połączono z {self.config.address} jako {self.config.name}.')
        # button_options = ttk.Button(frame, text='Ustawienia')

        self.label_info.pack(side='left')
        # button_options.pack(side='right')

        frame.pack(fill='both', side='bottom')

    # Funkcje obsługujące panel temperatury
    def _add_temp_panel(self):
        '''
        Rysuje panel temperatury
        '''
        frame = ttk.Frame(self.root)

        state = self.config.get_temp_state()
        self.temp = state
        self.temp_label = ttk.Label(frame, text=f'Temperatura: {self.temp}°C')

        button_up = ttk.Button(frame, text=f"+{self.config.temp['krok']}°C", width=8,
                               command = lambda x='up' : self._temp_command(x))
        button_down = ttk.Button(frame, text=f"-{self.config.temp['krok']}°C", width=8,
                                 command = lambda x='down' : self._temp_command(x))

        self.temp_label.pack(side='left', padx=4)
        button_up.pack(side='left', padx=3)
        button_down.pack(side='left', padx=3)

        frame.pack(anchor='w', pady=3)

    def _temp_command(self, mode):
        '''
        Funkcja obsługująca przyciski zmiany temperatury
        '''
        if mode == 'up':
            new_temp = self.temp + self.config.temp['krok']
            if new_temp > self.config.temp['max']:
                return
        else: # if mode == 'up'
            new_temp = self.temp - self.config.temp['krok']
            if new_temp < self.config.temp['min']:
                return

        self.client.publish(f"{self.config.pub}/temp", f'{new_temp}', retain=True)

    def change_temp_state(self, new_temp):
        self.temp = float(new_temp)
        self.temp_label['text'] = f'Temperatura: {self.temp}°C'
        self.label_info['text'] = f'Zmieniono temperaturę na {self.temp}°C.'

    # Funkcje obsługujące przyciski On/Off
    def _add_button(self, tab, room, device, row):
        '''
        Rysuje przycisk w zakładce.
        '''
        state = self.config.get_device_state(room, device, 'button', 'Off')
        self.widgets[room][device]['button'] = tk.Button(tab, command=lambda x=room, y=device : self._button_command(x, y),
                                                         bd=1, relief=tk.GROOVE, width=6)
        if state == 'Off':
            self.widgets[room][device]['button'].config(text='Off', fg='white', bg='#bcbcbc')
        else:
            self.widgets[room][device]['button'].config(text='On', fg='white', bg='#007aff')

        self.widgets[room][device]['button'].grid(row=row, column=1, padx=2, sticky='w')


    def _button_command(self, room, device):
        '''
        Funkcja obsługująca przyciski On/Off
        '''
        if self.widgets[room][device]['button']['text'] == 'Off':
            self.client.publish(f"{self.config.pub}/{self.config.device(room, device)['temat']}/button", 'On', retain=True)
        else:
            self.client.publish(f"{self.config.pub}/{self.config.device(room, device)['temat']}/button", 'Off', retain=True)

    def change_button_state(self, room, device, state):
        '''
        Funkcja zmieniająca stan przycisków On/Off (na podstawie komunikatu z serwera)
        '''
        room, device = self.config.get_room_device(room, device)

        if state == 'Off':
            self.widgets[room][device]['button'].config(text='Off', fg='white', bg='#bcbcbc')
            self.label_info['text'] = f'Wyłączono {room}: {device}'
        else:
            self.widgets[room][device]['button'].config(text='On', fg='white', bg='#007aff')
            if self.config.device(room, device)['typ'] == 'przełącznik':
                self.label_info['text'] = f'Włączono {room}: {device}'
            elif self.config.device(room, device)['typ'] == 'suwak':
                state = self.widgets[room][device]['slider'].get()
                self.label_info['text'] = f'Włączono {room}: {device} i ustawiono na {state}.'
            elif self.config.device(room, device)['typ'] == 'tv':
                channel = self.widgets[room][device]['tv'].get_channel()
                volume = self.widgets[room][device]['tv'].get_volume()
                self.label_info['text'] = f'Włączono {room}: {device}, kanał: {channel}, głośność: {volume}.'

    # Funkcje obsługujące suwaki
    def _add_slider(self, tab, room, device, row):
        '''
        Rysuje suwak w zakładce.
        '''
        min_val = self.config.device(room, device)['min']
        max_val = self.config.device(room, device)['max']
        state = self.config.get_device_state(room, device, 'slider', min_val)

        self.widgets[room][device]['slider'] = tk.Scale(tab, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                                                        tickinterval=math.ceil((max_val - min_val) / 6 * math.log10(max_val)))
        self.widgets[room][device]['slider'].set(state)
        self.widgets[room][device]['slider'].bind("<ButtonRelease-1>", lambda x, y=room, z=device : self._slider_command(x, y, z))

        self.widgets[room][device]['slider'].grid(row=row, column=2, padx=5, sticky='w')

    def _slider_command(self, state, room, device):
        '''
        Funkcja obsługująca suwaki
        '''
        state = self.widgets[room][device]['slider'].get()
        self.client.publish(f"{self.config.pub}/{self.config.device(room, device)['temat']}/slider", f'{state}', retain=True)

    def change_slider_state(self, room, device, state):
        '''
        Funkcja zmieniająca stan suwaka (na podstawie komunikatu z serwera)
        '''
        room, device = self.config.get_room_device(room, device)
        self.widgets[room][device]['slider'].set(int(state))
        if self.widgets[room][device]['button']['text'] == 'On':
            self.label_info['text'] = f'Ustawiono {room}: {device} na {state}.'

    # Funkcje obsługujące tv
    def _add_tv(self, tab, room, device, row):
        '''
        Rysuje przyciski odpowiedzialne za zmianę kanału i głośności telewizora.
        '''
        channels = self.config.device(room, device)['kanały']
        max_volume = self.config.device(room, device)['max głośność']
        start_channel = self.config.get_device_state(room, device, 'channel', 1)
        start_volume = self.config.get_device_state(room, device, 'volume', 0)

        self.widgets[room][device]['tv'] = TvFrame(tab, self.client, f'{room}/{device}', channels, 
                                                   max_volume, start_channel, start_volume, self.config.pub)

        self.widgets[room][device]['tv'].grid(row=row, column=2)
        
    def change_channel_state(self, room, device, state):
        self.widgets[room][device]['tv'].change_channel(int(state))
        if self.widgets[room][device]['button']['text'] == 'On':
            self.label_info['text'] = f'Ustawiono kanał w {room}: {device} na {state}.'

    def change_volume_state(self, room, device, state):
        self.widgets[room][device]['tv'].change_volume(int(state))
        if self.widgets[room][device]['button']['text'] == 'On':
            self.label_info['text'] = f'Ustawiono głośność w {room}: {device} na {state}.'

    # Funkcje obsługujące rolety
    def _add_blind_menu(self, tab, room, device, row):
        '''
        Rysuje przyciski odpowiedzialne opuszczanie i podnoszenie rolet.
        '''
        frame = ttk.Frame(tab)

        self.widgets[room][device]['blind_up'] = ttk.Button(frame, text='\u25B2', width=4, 
                                        command=lambda x=room, y=device, z='up' : self._blind_command(x, y, z))
        self.widgets[room][device]['blind_down'] = ttk.Button(frame, text='\u25BC', width=4, 
                                        command=lambda x=room, y=device, z='down' : self._blind_command(x, y, z))

        self.widgets[room][device]['blind_up'].pack()
        self.widgets[room][device]['blind_down'].pack()

        frame.grid(row=row, column=1, padx=2, pady=2, sticky='we')

    def _blind_command(self, room, device, mode):
        '''
        Funkcja obsługująca przyciski podnoszące i opuszczające rolety
        '''
        self.client.publish(f"{self.config.pub}/{self.config.device(room, device)['temat']}/blind", mode, retain=False)
        
        if mode == 'up':
            self.label_info['text'] = f'Podnoszę {room}: {device}.'
        else:
            self.label_info['text'] = f'Opuszczam {room}: {device}.'

    def change_blind_state(self, room, device, state):
        '''
        Funkcja wyświetla komunikat o podniesieniu/opuszczeniu rolet (na podstawie komunikatu z serwera)
        '''
        if state == 'up':
            self.label_info['text'] = f'Podniesiono {room}: {device}.'
        else: # if state == 'down'
            self.label_info['text'] = f'Opuszczono {room}: {device}.'
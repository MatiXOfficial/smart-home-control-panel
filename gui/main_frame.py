import tkinter as tk
from tkinter import ttk

class MainFrame:
    '''
    Główne okno z pilotem sterującym inteligentym domem.
    '''
    def __init__(self, config, client):

        self.root = tk.Tk()
        self.root.title('Pilot')
        self.root.iconbitmap('images/icon.ico')

        self.client = client

        # Słownik przycisków
        self.buttons = {}
        
        self.config = config
        self._info_frame()
        self.load_config()
    
        self.root.update()
        self.root.minsize(self.root.winfo_width() + 20, self.root.winfo_height())

    # Rozpoczyna pętlę - wizualizacja okienka
    def start_loop(self):
        self.root.mainloop()

    # Funkcja ładująca konfigurację, tworzy zakładki i przyciski.
    def load_config(self):
        # Tworzenie i wypełnianie zakładek
        tab_control = ttk.Notebook()

        for room, lamps in self.config['urządzenia'].items():
            tab = ttk.Frame(tab_control)
            tk.Grid.columnconfigure(tab, 0, weight=1)
            tk.Grid.columnconfigure(tab, 1, weight=1)
            self.buttons[room] = {}

            # Wypisanie nazwy pokoju
            label_title = ttk.Label(tab, text=room, font=('default', 20))
            label_title.grid(row=0, column=0, columnspan=2, padx=30, pady=10)

            # Wypisanie nazw lamp, stworzenie przycisków
            for i, lamp in enumerate(lamps.keys()):
                label_lamp = ttk.Label(tab, text=lamp, font=('default', 15))
                if 'state' in self.config['urządzenia'][room][lamp]:
                    state = self.config['urządzenia'][room][lamp]['state']
                else:
                    state = 'Off'

                self.buttons[room][lamp] = tk.Button(tab, command=lambda x=room, y=lamp: self._button_command(x, y),
                                                     bd=1, relief=tk.GROOVE, width=6)
                if state == 'Off':
                    self.buttons[room][lamp].config(text='Off', fg='white', bg='#bcbcbc')
                else:
                    self.buttons[room][lamp].config(text='On', fg='white', bg='#007aff')

                label_lamp.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')
                self.buttons[room][lamp].grid(row=i+1, column=1, padx=2, sticky='w')

            tab_control.add(tab, text=room)

        tab_control.pack(expand=True, fill='both', side='top')

    # Funkcja obsługująca przyciski
    def _button_command(self, room, device):
        if self.buttons[room][device]['text'] == 'Off':
            self.client.publish(self.config['urządzenia'][room][device]['temat'], 'On', retain=True)
        else:
            self.client.publish(self.config['urządzenia'][room][device]['temat'], 'Off', retain=True)

    # Funkcja zmieniająca stan przycisków
    def change_button_state(self, room, device, state):
        if room in self.config['topics'] and device in self.config['topics'][room]:
            old_room = room
            room = self.config['topics'][old_room][device]['room']
            device = self.config['topics'][old_room][device]['device']

        if state == 'Off':
            self.buttons[room][device].config(text='Off', fg='white', bg='#bcbcbc')
            self.label_info['text'] = f'Wyłączono {room}: {device}'
        else:
            self.buttons[room][device].config(text='On', fg='white', bg='#007aff')
            self.label_info['text'] = f'Włączono {room}: {device}'

    # Funkcja tworzy ramkę do wyświetlania informacji.
    def _info_frame(self):
        frame = ttk.Frame(self.root)

        self.label_info = ttk.Label(frame, text=f'Połączono z {self.config["adres"]} jako {self.config["nazwa"]}.')
        button_options = ttk.Button(frame, text='Ustawienia')

        self.label_info.pack(side='left')
        button_options.pack(side='right')

        frame.pack(fill='both', side='bottom')
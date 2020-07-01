import tkinter as tk
from tkinter import ttk
import json


class MainFrame:
    '''
    Główne okno z pilotem sterującym inteligentym domem.
    '''
    def __init__(self, config):

        self.root = tk.Tk()
        # self.root.resizable(0, 0)
        self.root.title('Pilot')

        # Style przycisków
        style = ttk.Style()
        style.configure('On.TButton', foreground='#007aff', background='#007aff')
        style.configure('Off.TButton')

        # Słownik przycisków
        self.buttons = {}
        
        self.load_config(config)
        self._info_frame()
    
        self.root.mainloop()

    def load_config(self, config):
        '''
        Funkcja ładująca config, tworzy zakładki i przyciski.
        '''
        # Tworzenie i wypełnianie zakładek
        tab_control = ttk.Notebook()

        for room, lamps in config.items():
            tab = ttk.Frame(tab_control)
            self.buttons[room] = {}

            # Wypisanie nazwy pokoju
            label_title = ttk.Label(tab, text=room, font=('default', 20))
            label_title.grid(row=0, column=0, columnspan=2, padx=30, pady=10)

            # Wypisanie nazw lamp, stworzenie przycisków
            for i, lamp in enumerate(lamps):
                label_lamp = ttk.Label(tab, text=lamp, font=('default', 15))

                self.buttons[room][lamp] = ttk.Button(tab, text='Off', command=lambda x=room, y=lamp: self._button_command(x, y), style='Off.TButton')

                label_lamp.grid(row=i+1, column=0, padx=10, pady=5)
                self.buttons[room][lamp].grid(row=i+1, column=1, padx=10)

            tab_control.add(tab, text=room)

        tab_control.pack(expand=True, fill='both')

    def _button_command(self, room, lamp):
        '''
        Funkcja obsługująca przyciski
        '''
        if self.buttons[room][lamp]['text'] == 'Off':
            self.buttons[room][lamp]['text'] = 'On'
            self.buttons[room][lamp]['style'] = 'On.TButton'
            self.label_info['text'] = f'Włączono {room}: {lamp}'
        else:
            self.buttons[room][lamp]['text'] = 'Off'
            self.buttons[room][lamp]['style'] = 'Off.TButton'
            self.label_info['text'] = f'Wyłączono {room}: {lamp}'

    def _info_frame(self):
        '''
        Funkcja tworzy ramkę do wyświetlania informacji.
        '''
        frame = ttk.Frame(self.root)

        self.label_info = ttk.Label(frame)
        # button_options = ttk.Button(frame, text='Ustawienia')

        self.label_info.pack(side='left')
        # button_options.pack(side='right')

        frame.pack(fill='both')
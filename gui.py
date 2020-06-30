import tkinter as tk
from tkinter import ttk
import json


with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

root = tk.Tk()

# Słownik przycisków
buttons = {}

# Style przycisków
style = ttk.Style()
style.configure('On.TButton', foreground='#007aff', background='#007aff')
style.configure('Off.TButton')

# Funkcje obsługujące wydarzenia
def button_command(room, lamp):
    if buttons[room][lamp]['text'] == 'Off':
        buttons[room][lamp]['text'] = 'On'
        buttons[room][lamp]['style'] = 'On.TButton'
    else:
        buttons[room][lamp]['text'] = 'Off'
        buttons[room][lamp]['style'] = 'Off.TButton'

# Tworzenie i wypełnianie zakładek
tab_control = ttk.Notebook()

for room, lamps in config.items():
    tab = ttk.Frame(tab_control)
    buttons[room] = {}

    # Wypisanie nazwy pokoju
    label_title = ttk.Label(tab, text=room, font=('default', 40))
    label_title.grid(row=0, column=0, columnspan=2, padx=30, pady=10)

    # Wypisanie nazw lamp, stworzenie przycisków
    for i, lamp in enumerate(lamps):
        label_lamp = ttk.Label(tab, text=lamp, font=('default', 20))

        buttons[room][lamp] = ttk.Button(tab, text='Off', command=lambda x=room, y=lamp: button_command(x, y), style='Off.TButton')

        label_lamp.grid(row=i+1, column=0, padx=20, pady=5)
        buttons[room][lamp].grid(row=i+1, column=1, padx=10)

    tab_control.add(tab, text=room)

tab_control.pack(expand=True, fill='both')


root.mainloop()
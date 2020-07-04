import tkinter as tk
from tkinter import messagebox

def show_error(error_message):
    '''
    Funkcja pomocnicza wyświetlająca okno z błędem.
    '''
    root = tk.Tk()
    center_window(root)
    root.withdraw()
    messagebox.showerror('Błąd', error_message)
    exit()

def center_window(root):
    '''
    Ustawia okno na środku ekranu.
    '''
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    position_right = int(root.winfo_screenwidth() / 3 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 3 - window_height / 2)

    root.geometry(f'+{position_right}+{position_down}')
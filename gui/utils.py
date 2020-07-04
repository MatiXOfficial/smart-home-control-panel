import tkinter as tk
from tkinter import messagebox

def show_error(error_message):
    '''
    Funkcja pomocnicza wyświetlająca okno z błędem.
    '''
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('Błąd', error_message)
    exit()
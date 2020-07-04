import tkinter as tk

def show_error(error_message):
    '''
    Funkcja pomocnicza wyświetlająca okno z błędem.
    '''
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror('Błąd', error_message)
    exit()
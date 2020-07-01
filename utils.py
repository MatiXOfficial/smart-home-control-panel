import tkinter as tk

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
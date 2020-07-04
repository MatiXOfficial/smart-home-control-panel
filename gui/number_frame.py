import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from gui.utils import center_window

class NumberFrame:
    '''
    Okno pozwalające na wprowadzenie numeru.
    '''
    def __init__(self, min, max):

        # Uruchomienie okna
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.title('')
        self.root.iconbitmap('icon.ico')
        self.root.resizable(False, False)

        center_window(self.root)

        self.min = min
        self.max = max

        # Zmienna z wpisywaną liczbą jako string
        self.number = '-'

        # Tekst wyświetlający aktualnie podaną liczbę
        self.label = ttk.Label(self.root, text=self.number, font=('default', 25))

        # Przyciski - cyfry
        button_7 = tk.Button(self.root, text='7', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('7'))
        button_8 = tk.Button(self.root, text='8', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('8'))
        button_9 = tk.Button(self.root, text='9', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('9'))

        button_4 = tk.Button(self.root, text='4', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('4'))
        button_5 = tk.Button(self.root, text='5', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('5'))
        button_6 = tk.Button(self.root, text='6', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('6'))

        button_1 = tk.Button(self.root, text='1', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('1'))
        button_2 = tk.Button(self.root, text='2', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('2'))
        button_3 = tk.Button(self.root, text='3', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('3'))

        button_0 = tk.Button(self.root, text='0', font=('default', 15), relief=tk.GROOVE, padx=10, command=lambda : self._button_number_command('0'))

        # Przyciski specjalne
        button_clear = tk.Button(self.root, text='C', font=('default', 15), relief=tk.GROOVE, padx=9, command=self._button_clear_command)

        # Ramka z opcjami: ok i cancel
        frame = ttk.Frame(self.root)

        button_ok = ttk.Button(frame, text='Ok', command=self._button_ok_command)
        button_cancel = ttk.Button(frame, text='Anuluj', command=self._button_cancel_command)

        button_ok.pack(side='left', anchor='center', padx=5)
        button_cancel.pack(side='right', anchor='center', padx=5)

        # Umiejscowienie w oknie
        self.label.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

        button_7.grid(row=1, column=0, padx=5, pady=1)
        button_8.grid(row=1, column=1, padx=1, pady=1)
        button_9.grid(row=1, column=2, padx=5, pady=1)

        button_4.grid(row=2, column=0, padx=1, pady=1)
        button_5.grid(row=2, column=1, padx=1, pady=1)
        button_6.grid(row=2, column=2, padx=1, pady=1)

        button_1.grid(row=3, column=0, padx=1, pady=1)
        button_2.grid(row=3, column=1, padx=1, pady=1)
        button_3.grid(row=3, column=2, padx=1, pady=1)

        button_clear.grid(row=4, column=0, padx=1, pady=1)
        button_0.grid(row=4, column=1, padx=1, pady=1)

        frame.grid(row=5, column=0, columnspan=3, pady=5)

    def start_and_return(self):
        self.root.mainloop()
        if self.number is None or self.number == '-':
            return None
        return int(self.number)

    def _button_number_command(self, digit):
        if self.number == '-':
            self.number = digit
        else:
            self.number = self.number + digit
        self.label['text'] = self.number

    def _button_clear_command(self):
        self.number = '-'
        self.label['text'] = self.number

    def _button_ok_command(self):
        if self.number == '-':
            messagebox.showwarning('Ostrzeżenie', 'Nie wprowadzono liczby. Spróbuj jeszcze raz.')
        elif int(self.number) < self.min:
            messagebox.showwarning('Ostrzeżenie', 'Wprowadzono za małą liczbę. Spróbuj jeszcze raz.')
            self._button_clear_command()
        elif int(self.number) > self.max:
            messagebox.showwarning('Ostrzeżenie', 'Wprowadzono za dużą liczbę. Spróbuj jeszcze raz.')
            self._button_clear_command()
        else:
            self.root.quit()
            self.root.destroy()

    def _button_cancel_command(self):
        self.number = None
        self.root.destroy()
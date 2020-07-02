import tkinter as tk
from tkinter import ttk

class InputFrame():
    '''
    Okno pozwalające na wprowadzenie tekstu.
    '''
    def __init__(self, text):

        self.root = tk.Tk()
        self.root.title('Pilot')
        self.root.iconbitmap('images/icon.ico')
        self.root.resizable(False, False)

        label = ttk.Label(self.root, text=f'  {text}: ')

        self.text_var = tk.StringVar()
        entry = ttk.Entry(self.root, textvariable=self.text_var)

        button_ok = ttk.Button(self.root, text='Ok', command=self._command_ok)
        button_cancel = ttk.Button(self.root, text='Anuluj', command=self._command_cancel)

        label.grid(row=0, column=0, pady=5)
        entry.grid(row=0, column=1, padx=5)
        button_ok.grid(row=1, column=0, pady=5)
        button_cancel.grid(row=1, column=1)

    def start_and_return(self):
        self.root.mainloop()
        return self.text_var.get()

    def _command_ok(self):
        self.root.destroy()

    def _command_cancel(self):
        self.root.destroy()
        exit()
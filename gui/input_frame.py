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
        self.root.protocol("WM_DELETE_WINDOW", exit)

        label = ttk.Label(self.root, text=f'  {text}: ')

        self.text_var = tk.StringVar()
        entry = ttk.Entry(self.root, textvariable=self.text_var)

        frame_buttons = ttk.Frame(self.root)
        button_ok = ttk.Button(frame_buttons, text='Ok', command=self._command_ok)
        button_cancel = ttk.Button(frame_buttons, text='Anuluj', command=self._command_cancel)

        button_ok.pack(side='left', anchor='center', padx=10)
        button_cancel.pack(side='right', anchor='center', padx=10)

        label.grid(row=0, column=0, pady=5)
        entry.grid(row=0, column=1, padx=5)
        frame_buttons.grid(row=1, column=0, columnspan=2, pady=2)

    def start_and_return(self):
        self.root.mainloop()
        return self.text_var.get()

    def _command_ok(self):
        self.root.destroy()

    def _command_cancel(self):
        self.root.destroy()
        exit()
import tkinter as tk
from tkinter import ttk

from gui.number_frame import NumberFrame

class TvFrame:

    def __init__(self, tab, client, topic, channels, max_volume, start_channel, start_volume, pub):

        self.root = ttk.Frame(tab)

        self.client = client
        self.topic = topic
        self.channels = channels
        self.max_volume = max_volume
        self.pub = pub

        # Kanał
        self.channel = int(start_channel)
        label_channel_info = ttk.Label(self.root, text='Kanał: ')

        button_channel_up = ttk.Button(self.root, text='\u25B2', command=self._button_channel_up, width=4)
        button_channel_down = ttk.Button(self.root, text='\u25BC', command=self._button_channel_down, width=4)

        self.button_channel_value = tk.Button(self.root, text=str(self.channel), width=3, font=('Arial', 15), relief=tk.GROOVE,
                                              command=self._button_channel_value)

        label_channel_info.grid(row=0, column=0, rowspan=2)
        button_channel_up.grid(row=0, column=1)
        button_channel_down.grid(row=1, column=1)
        self.button_channel_value.grid(row=0, column=2, rowspan=2, padx=2)

        # Głośność
        self.volume = int(start_volume)
        label_volume_info = ttk.Label(self.root, text='Głośność: ')

        button_volume_up = ttk.Button(self.root, text='\u25B2', command=self._button_volume_up, width=4)
        button_volume_down = ttk.Button(self.root, text='\u25BC', command=self._button_volume_down, width=4)

        self.button_volume_value = tk.Button(self.root, text=str(self.volume), width=3, font=('Arial', 15), relief=tk.GROOVE,
                                             command=self._button_volume_value)

        label_volume_info.grid(row=0, column=3, rowspan=2)
        button_volume_up.grid(row=0, column=4)
        button_volume_down.grid(row=1, column=4)
        self.button_volume_value.grid(row=0, column=5, rowspan=2, padx=2)

    def grid(self, row, column):
        self.root.grid(row=row, column=column, padx=5, sticky='w')

    def get_channel(self):
        return self.channel

    def get_volume(self):
        return self.volume

    def _button_channel_up(self):
        if self.channel < self.channels:
            self.client.publish(f"{self.pub}/{self.topic}/channel", self.channel + 1, retain=True)

    def _button_channel_down(self):
        if self.channel > 1:
            self.client.publish(f"{self.pub}/{self.topic}/channel", self.channel - 1, retain=True)

    def _button_volume_up(self):
        if self.volume < self.max_volume:
            self.client.publish(f"{self.pub}/{self.topic}/volume", self.volume + 1, retain=True)

    def _button_volume_down(self):
        if self.volume > 0:
            self.client.publish(f"{self.pub}/{self.topic}/volume", self.volume - 1, retain=True)

    def _button_channel_value(self):
        channel = NumberFrame(1, self.channels + 1).start_and_return()
        if channel is not None:
            self.channel = channel
            self.client.publish(f"{self.pub}/{self.topic}/channel", self.channel, retain=True)
    
    def _button_volume_value(self):
        volume = NumberFrame(0, self.max_volume).start_and_return()
        if volume is not None:
            self.volume = volume
            self.client.publish(f"{self.pub}/{self.topic}/volume", self.volume, retain=True)

    def change_channel(self, channel):
        self.channel = channel
        self.button_channel_value['text'] = str(self.channel)

    def change_volume(self, volume):
        self.volume = volume
        self.button_volume_value['text'] = str(self.volume)
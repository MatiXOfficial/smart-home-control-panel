import paho.mqtt.client as mqtt

from utils import show_error
from gui.main_frame import MainFrame

class Client:

    def __init__(self, config):
        self.config = config
        self.client = mqtt.Client(self.config['nazwa'])

        try:
            self.client.connect(self.config['adres'])
        except:
            show_error('Nie można nawiązać połączenia z serwerem MQTT.')

        self.client.loop_start()

        # Subskrybcja określonych tematów
        for room, lamps in config['urządzenia'].items():
            for lamp in lamps.keys():
                self.client.subscribe(f"{room}/{lamp}")

        self.client.on_message = self._on_message_start

        self.main_frame = MainFrame(self.config, self.client)
        self.client.on_message = self._on_message_normal
        self.main_frame.start_loop()

        self.client.loop_stop()
        self.client.disconnect()

    def _on_message_start(self, client, userdata, message):
        '''
        Callout wykonujący się po otrzymaniu wiadomości z serwera.
        Służy do odebrania wiadomości zatrzymanych na serwerze w celu odtworzenia aktulanego stanu.
        '''
        room, device = message.topic.split('/')
        state = (message.payload.decode("utf-8"))
        if room in self.config['urządzenia']:
            if device in self.config['urządzenia'][room]:
                self.config['urządzenia'][room][device]['state'] = state

    def _on_message_normal(self, client, userdata, message):
        '''
        Callout wykonujący się po otrzymaniu wiadomości z serwera.
        Reakcja na zmiany w trakcie działania programu.
        '''
        room, device = message.topic.split('/')
        self.main_frame.change_button_state(room, device, str(message.payload.decode("utf-8")))
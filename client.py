import paho.mqtt.client as mqtt

from gui.utils import show_error
from gui.main_frame import MainFrame

class Client:

    def __init__(self, config):
        self.config = config
        self.client = mqtt.Client(self.config.name)

        # Próba połączenia
        try:
            self.client.connect(self.config.address)
        except:
            show_error('Nie można nawiązać połączenia z serwerem MQTT.')

        self.client.loop_start()

        # Subskrybcja określonych tematów
        for room, devices in self.config.rooms.items():
            for device in devices.keys():
                if self.config.device(room, device)['typ'] == 'przełącznik':
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/button")
                elif self.config.device(room, device)['typ'] == 'suwak':
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/button")
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/slider")
                elif self.config.device(room, device)['typ'] == 'tv':
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/button")
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/channel")
                    self.client.subscribe(f"{self.config.sub}/{self.config.device(room, device)['temat']}/volume")

        # Obsłużenie zatrzymanych wiadomości (retained)
        self.client.on_message = self._on_message_start

        # Uruchomienie okna i zmiana obsługi wiadomości na tryb związany z gui
        self.main_frame = MainFrame(self.config, self.client)
        self.client.on_message = self._on_message_normal
        self.main_frame.start_loop()

        # Zakończenie działania po wyłączeniu okna
        self.client.loop_stop()
        self.client.disconnect()

    def _on_message_start(self, client, userdata, message):
        '''
        Callout wykonujący się po otrzymaniu wiadomości z serwera.
        Służy do odebrania wiadomości zatrzymanych na serwerze w celu odtworzenia aktulanego stanu.
        '''
        _, room, device, mode = message.topic.split('/')
        state = (message.payload.decode("utf-8"))
        room, device = self.config.get_room_device(room, device)
        self.config.add_device_state(room, device, mode, state)

    def _on_message_normal(self, client, userdata, message):
        '''
        Callout wykonujący się po otrzymaniu wiadomości z serwera.
        Reakcja na zmiany w trakcie działania programu.
        '''
        _, room, device, mode = message.topic.split('/')
        if mode == 'button':
            self.main_frame.change_button_state(room, device, str(message.payload.decode("utf-8")))
        elif mode == 'slider':
            self.main_frame.change_slider_state(room, device, str(message.payload.decode("utf-8")))
        elif mode == 'channel':
            self.main_frame.change_channel_state(room, device, str(message.payload.decode("utf-8")))
        elif mode == 'volume':
            self.main_frame.change_volume_state(room, device, str(message.payload.decode("utf-8")))

import serial
import time

class MaestroController:
    def __init__(self, port='/dev/ttyACM0', baudrate=57600, timeout=1):
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Donner le temps à la connexion série de s'établir

    def set_target(self, channel, target):
        """
        Configure la position cible pour un canal donné.

        :param channel: Numéro du canal (0-23).
        :param target: Largeur d'impulsion en quarts de microsecondes (4000-8000).
        """
        command = bytearray([0x84, channel, target & 0x7F, (target >> 7) & 0x7F])
        self.serial_port.write(command)

    def disconnect(self):
        """Ferme le port série."""
        self.serial_port.close()

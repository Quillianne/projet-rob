import serial
import time
import numpy as np
class PololuController:
    def __init__(self, port='/dev/ttyACM0', baudrate=57600, timeout=1):
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Donner le temps à la connexion de s'établir

    def set_target(self, channel, target):
        """
        Configure la position cible pour un canal donné.
        
        :param channel: Le canal à contrôler (entre 0 et 23 pour une Maestro).
        :param target: La largeur d'impulsion cible en quarts de microsecondes (min 4000, max 8000).
        """
        command = bytearray([0x84, channel, target & 0x7F, (target >> 7) & 0x7F])
        self.serial_port.write(command)

    def set_motor_speed(self, left_speed, right_speed):
        """
        Contrôle les deux moteurs en définissant leur vitesse.

        :param left_speed: Vitesse du moteur gauche (-1.0 à 1.0).
        :param right_speed: Vitesse du moteur droit (-1.0 à 1.0).
        """
        # Convertir les vitesses en largeur d'impulsion (4000 à 8000 correspond à -100% à +100%).
        left_target = int(5000 + 1000 * left_speed)
        right_target = int(6000 - 1000 * right_speed)

        #left_target = int(6000 + 2000 * left_speed)
        #right_target = int(6000 + 2000 * left_speed)

        # S'assurer que les valeurs sont dans les limites autorisées.
        left_target = max(4000, min(8000, left_target))
        right_target = max(4000, min(8000, right_target))
        print("Left Target: ", left_target)
        # Envoi des commandes aux canaux correspondants.
        self.set_target(0, left_target)  # Canal 0 pour le moteur gauche.
        self.set_target(1, right_target)  # Canal 1 pour le moteur droit.

    def disconnect(self):
        """Ferme le port série."""
        self.serial_port.close()

if __name__ == "__main__":
    # Initialisation du contrôleur Pololu
    pololu = PololuController(port='/dev/ttyACM0')

    try:
        # Test des moteurs
        #print("Déplacement en avant...")
        #pololu.set_motor_speed(-0.75, 0.25)  # Les deux moteurs à 100% de leur vitesse maximale.
        #time.sleep(2)

        #print("Déplacement en avant...")
        #pololu.set_motor_speed(-0.625, 0.125)  # Les deux moteurs à 50%% de leur vitesse maximale.
        #time.sleep(2)

        #print("Rotation sur place...")
        #pololu.set_motor_speed(-0.375, 0.5)  # Tourne sur place (moteur gauche recule, droit avance).
        #time.sleep(2)

        # for i in np.arange(-1, 1, 0.1):  # Utilisation de np.arange pour des pas décimaux
        #     print(f"Fonctionne avec {i}")
        #     pololu.set_motor_speed(i, i)  # Définir la vitesse du moteur gauche
        #     time.sleep(2)

            #print("Arrêt...")
            #pololu.set_motor_speed(-0.5, 0)  # stop les moteurs
            #time.sleep(1)
        pololu.set_motor_speed(0, -0.5)
    finally:
        pololu.disconnect()
        print("Connexion terminée.")

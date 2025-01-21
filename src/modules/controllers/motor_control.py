from modules.controllers.maestro_controller import MaestroController

class MotorControl:
    def __init__(self, port='/dev/ttyACM0'):
        self.controller = MaestroController(port)

    def set_motor_speed(self, left_speed, right_speed):
        """
        Définit la vitesse des moteurs gauche et droit en utilisant vos formules spécifiques.

        :param left_speed: Vitesse du moteur gauche (-1.0 à 1.0).
        :param right_speed: Vitesse du moteur droit (-1.0 à 1.0).
        """
        # Utilisation des formules de calibration spécifiques
        left_target = int(5050 + 10 * left_speed)  # Ajustement pour le moteur gauche
        right_target = int(5985 - 10 * right_speed)  # Ajustement pour le moteur droit

        # Vérifier les limites (4000-8000)
        left_target = max(4000, min(8000, left_target))
        right_target = max(4000, min(8000, right_target))

        # Envoyer les commandes aux moteurs via la Pololu
        self.controller.set_target(0, left_target)  # Canal 0 : moteur gauche
        self.controller.set_target(1, right_target)  # Canal 1 : moteur droit

    def stop(self):
        """
        Arrête les moteurs en envoyant une vitesse de 0.
        """
        self.set_motor_speed(0, 0)

    def disconnect(self):
        """Déconnecte le contrôleur Pololu."""
        self.controller.disconnect()

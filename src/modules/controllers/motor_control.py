import logging
from modules.controllers.maestro_controller import MaestroController

# Configuration de base pour le logging
logging.basicConfig(
    level=logging.DEBUG,  # Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format des logs
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)

class MotorControl:
    def __init__(self, port='/dev/ttyACM0'):
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger spécifique à cette classe
        self.logger.info("Initialisation du contrôleur Maestro sur le port %s", port)
        self.controller = MaestroController(port)

    def set_motor_speed(self, left_speed, right_speed):
        """
        Définit la vitesse des moteurs gauche et droit en utilisant vos formules spécifiques.

        :param left_speed: Vitesse du moteur gauche (-1.0 à 1.0).
        :param right_speed: Vitesse du moteur droit (-1.0 à 1.0).
        """
        self.logger.debug("Définition de la vitesse des moteurs : gauche=%s, droite=%s", left_speed, right_speed)

        # Utilisation des formules de calibration spécifiques
        left_target = int(6000 + 20 * left_speed)  # Ajustement pour le moteur gauche
        right_target = int(6000 - 20 * right_speed)  # Ajustement pour le moteur droit

        # Vérifier les limites (4000-8000)
        left_target = max(4000, min(8000, left_target))
        right_target = max(4000, min(8000, right_target))

        # Logs des cibles calculées
        # self.logger.info(f"Commandes calculées : gauche={left_target}, droite={right_target}")

        # Envoyer les commandes aux moteurs via la Pololu
        self.controller.set_target(0, left_target)  # Canal 0 : moteur gauche
        self.controller.set_target(1, right_target)  # Canal 1 : moteur droit
        self.logger.debug("Commandes envoyées : gauche=%s, droite=%s", left_target, right_target)

    def stop(self):
        """
        Arrête les moteurs en envoyant une vitesse de 0.
        """
        self.logger.info("Arrêt des moteurs")
        self.set_motor_speed(0, 0)

    def disconnect(self):
        """Déconnecte le contrôleur Pololu."""
        self.logger.info("Déconnexion du contrôleur Maestro")
        self.controller.disconnect()

import serial
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,  # Niveau de log configuré à DEBUG pour capturer tous les événements
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format détaillé
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)

class IMUSensor:
    def __init__(self, port="/dev/ttyUSB2", baudrate=57600, timeout=2):
        """
        Initialisation de l'IMU avec les paramètres de connexion série.

        :param port: Port série où l'IMU est connecté.
        :param baudrate: Débit en bauds pour la communication.
        :param timeout: Délai d'attente pour les données.
        """
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger dédié
        self.logger.info("Initialisation de l'IMU sur le port %s avec un baudrate de %d.", port, baudrate)

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """
        Établit la connexion série avec l'IMU.
        """
        try:
            self.connection = serial.Serial(
                self.port, self.baudrate, timeout=self.timeout
            )
            self.logger.info("Connexion série établie avec succès sur %s à %d bps.", self.port, self.baudrate)
        except serial.SerialException as e:
            self.logger.error("Erreur lors de l'établissement de la connexion série : %s", e)
            raise

    def read_data(self):
        """
        Lit et analyse les données de l'IMU.

        :return: Tuple (yaw, pitch, roll) ou None si les données sont invalides.
        """
        if not self.connection or not self.connection.is_open:
            self.logger.warning("Tentative de lecture sans connexion série active.")
            return None

        try:
            line = self.connection.read_until(b'\n').decode('ascii', errors='replace').strip()
            if line and line.startswith('#YPR'):
                ypr_data = line.split("#YPR=")[1]
                yaw, pitch, roll = map(float, ypr_data.split(','))
                self.logger.debug("Données reçues : yaw = %.2f, pitch = %.2f, roll = %.2f", yaw, pitch, roll)
                return yaw, pitch, roll
            else:
                self.logger.warning("Données reçues invalides ou non reconnues : %s", line)
        except ValueError as ve:
            self.logger.warning("Erreur de parsing des données : %s", ve)
        except serial.SerialException as se:
            self.logger.error("Erreur de lecture série : %s", se)

        return None

    def close(self):
        """
        Ferme la connexion série proprement.
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            self.logger.info("Connexion série fermée.")

# Exemple d'utilisation autonome
if __name__ == "__main__":
    imu = IMUSensor(port="/dev/ttyUSB2", baudrate=57600)

    try:
        imu.connect()
        logging.info("Lecture des données IMU en cours...")
        while True:
            data = imu.read_data()
            if data:
                yaw, pitch, roll = data
                print(f"yaw = {yaw}, pitch = {pitch}, roll = {roll}")
    except KeyboardInterrupt:
        logging.info("Interruption par l'utilisateur.")
    except Exception as e:
        logging.error("Erreur inattendue : %s", e)
    finally:
        imu.close()

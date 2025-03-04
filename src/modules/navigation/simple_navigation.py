import logging
from modules.sensors.imu import IMUSensor
from modules.controllers.motor_control import MotorControl
import json
import time

# Configuration de base pour le logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

class SimpleNavigation:
    def __init__(self, imu_port="/dev/ttyUSB2", motor_port="/dev/ttyACM0", kp_forward=1.0, kp_turn=1.0):
        """
        Initialise les capteurs, les moteurs et les paramètres de navigation.

        :param imu_port: Port pour l'IMU.
        :param motor_port: Port pour le contrôleur de moteurs.
        :param kp_forward: Gain proportionnel pour l'asservissement en mode forward.
        :param kp_turn: Gain proportionnel pour l'asservissement en mode turn.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initialisation de la navigation simple avec asservissement IMU.")
        
        # Initialiser l'IMU et le contrôleur moteur
        self.imu = IMUSensor(port=imu_port,baudrate=57600)
        self.motor_control = MotorControl(port=motor_port)

        # Gains proportionnels
        self.kp_forward = kp_forward
        self.kp_turn = kp_turn

        # Connexion au matériel
        try:
            self.imu.connect()
            self.logger.info("IMU connectée avec succès.")
        except Exception as e:
            self.logger.error("Erreur lors de la connexion à l'IMU : %s", e)
            raise

    def forward(self, duration=5):
        """
        Fait avancer le robot tout droit en maintenant le cap via l'asservissement.

        :param duration: Temps maximal d'avancement (en secondes).
        """
        self.logger.info("Début de l'avance tout droit avec asservissement (kp=%.2f).", self.kp_forward)
        start_time = time.time()

        # Lire l'orientation initiale
        data = self.imu.read_data()
        if not data:
            self.logger.error("Impossible de lire les données de l'IMU pour avancer.")
            return
        
        target_yaw, _, _ = data

        while time.time() - start_time < duration:
            data = self.imu.read_data()
            if not data:
                self.logger.warning("Données IMU indisponibles pendant l'avancement.")
                continue

            yaw, _, _ = data
            error = target_yaw - yaw

            # Normalisation de l'erreur entre -180 et 180
            if error > 180:
                error -= 360
            elif error < -180:
                error += 360

            # Calcul de la correction proportionnelle
            correction = self.kp_forward * error
            left_speed = 50 - correction
            right_speed = 50 + correction

            # Limiter les vitesses entre -100 et 100
            left_speed = max(-100, min(100, left_speed))
            right_speed = max(-100, min(100, right_speed))

            self.motor_control.set_motor_speed(left_speed, right_speed)
            self.logger.debug("Correction appliquée : gauche=%.2f, droite=%.2f", left_speed, right_speed)

            time.sleep(0.1)  # Pause pour éviter de saturer le capteur

        # Arrêter les moteurs après avoir atteint la durée
        self.motor_control.stop()
        self.logger.info("Avancement terminé.")

    def turn(self, relative_angle):
        """
        Fait tourner le robot d'un angle relatif donné.

        :param relative_angle: Angle à tourner (positif pour horaire, négatif pour anti-horaire).
        """
        self.logger.info("Début de la rotation relative de %.2f° avec kp=%.2f.", relative_angle, self.kp_turn)

        # Lire l'orientation initiale
        data = self.imu.read_data()
        if not data:
            self.logger.error("Impossible de lire les données de l'IMU pour tourner.")
            return

        initial_yaw, _, _ = data
        target_yaw = (initial_yaw + relative_angle) % 360

        while True:
            data = self.imu.read_data()
            if not data:
                self.logger.warning("Données IMU indisponibles pendant la rotation.")
                continue

            yaw, _, _ = data
            error = target_yaw - yaw

            # Normalisation de l'erreur entre -180 et 180
            if error > 180:
                error -= 360
            elif error < -180:
                error += 360
            print(initial_yaw, yaw, target_yaw)
            self.logger.debug("Erreur actuelle : %.2f°", error)

            # Si l'orientation cible est atteinte, arrêter la rotation
            if abs(error) <= 2:  # Tolérance fixe de 2 degrés
                self.motor_control.stop()
                self.logger.info("Rotation terminée. Orientation actuelle : %.2f°", yaw)
                break

            # Appliquer des vitesses proportionnelles pour tourner sur place
            offset = 30
            correction = self.kp_turn * abs(error) + offset
            print("erreur en degres :", error)
            if error > 0:
                self.motor_control.set_motor_speed(correction, -correction)
            else:
                self.motor_control.set_motor_speed(-correction, correction)
            # Limiter les vitesses entre -100 et 100
            correction = max(-100, min(100, correction))

            time.sleep(0.1)  # Pause pour éviter des mises à jour trop rapides

    def stop(self):
        """
        Arrête les moteurs immédiatement.
        """
        self.motor_control.stop()
        self.logger.info("Arrêt immédiat des moteurs.") 

    def handle_request(self, json_request):
        """
        Traite une requête JSON et effectue les actions correspondantes.

        :param json_request: Une chaîne JSON contenant l'action à effectuer.
        :return: Un dictionnaire contenant le statut et les détails de l'action.
        """
        try:
            # Parser la requête JSON
            request = json.loads(json_request)
            action = request.get("action")
            value = request.get("value")
            self.logger.info("Requête reçue : action=%s, value=%s", action, value)

            # Effectuer l'action spécifiée
            if action == "forward":
                self.forward()
                return {"status": "success", "message": "Avancé tout droit."}
            
            elif action == "turn_left":
                self.turn(relative_angle=-value)
                return {"status": "success", "message": f"Tourné à gauche de {value}°."}
            
            elif action == "turn_right":
                self.turn(relative_angle=value)
                return {"status": "success", "message": f"Tourné à droite de {value}°."}
            
            elif action == "stop":
                self.stop()
                return {"status": "success", "message": "Arrêt immédiat."}
            
            else:
                self.logger.warning("Action non reconnue : %s", action)
                return {"status": "error", "message": f"Action inconnue : {action}"}
        
        except json.JSONDecodeError as e:
            self.logger.error("Erreur de parsing JSON : %s", e)
            return {"status": "error", "message": "Format JSON invalide."}
        
        except Exception as e:
            self.logger.error("Erreur inattendue : %s", e)
            return {"status": "error", "message": f"Erreur inattendue : {e}"}

    def shutdown(self):
        """
        Ferme les connexions et arrête les moteurs proprement.
        """
        self.logger.info("Arrêt de la navigation simple.")
        self.motor_control.stop()
        self.imu.close()
        self.motor_control.disconnect()


# Exemple d'utilisation autonome
if __name__ == "__main__":
    navigator = SimpleNavigation(imu_port="/dev/ttyUSB2", motor_port="/dev/ttyACM0", kp_forward=1.5, kp_turn=1.2)

    try:
        # Exemple de requête JSON
        example_request = '{"action": "forward", "value": null}'
        response = navigator.handle_request(example_request)
        print("Réponse :", response)

        # Une autre requête
        example_request = '{"action": "turn_right", "value": 90}'
        response = navigator.handle_request(example_request)
        print("Réponse :", response)
    
    except KeyboardInterrupt:
        logging.info("Interruption par l'utilisateur.")
    except Exception as e:
        logging.error("Erreur inattendue : %s", e)
    finally:
        navigator.shutdown()

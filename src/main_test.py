import logging
import time
from modules.sensors.kinect import KinectSensor
from modules.navigation.simple_navigation import SimpleNavigation
from modules.api.vision_api import VisionAPI

def main():
    # Configuration globale du logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Main")

    try:
        # Initialisation du capteur Kinect
        logger.info("Initialisation du capteur Kinect...")
        kinect = KinectSensor(output_dir="kinect_images")
        frames = kinect.get_frames()
        if not frames:
            logger.error("Aucune frame capturée depuis le Kinect.")
            return

        # Sauvegarde des frames capturées
        kinect.save_frames(frames)
        # Optionnel : Affichage de la frame couleur
        # if "color" in frames:
        #     kinect.display_frame(frames["color"], window_name="Kinect Color Frame")

        # Initialisation de la VisionAPI et envoi de la requête avec l'image capturée
        logger.info("Envoi de la requête à l'API Vision...")
        vision_api = VisionAPI(api_key="env", prompt="import_txt")
        image_path = "kinect_images/raw_color.png"
        response_api = vision_api.send_request(image_path=image_path)
        if not response_api:
            logger.error("Échec de la requête à l'API Vision.")
            return

        # Extraction du JSON propre depuis la réponse de l'API
        json_response = vision_api.return_clean_json(response_api)
        if not json_response:
            logger.error("Impossible d'extraire un JSON valide de la réponse API.")
            return

        logger.info("Réponse API extraite : %s", json_response)

        # Initialisation du système de navigation simple
        logger.info("Initialisation du système de navigation...")
        navigator = SimpleNavigation(
            imu_port="/dev/ttyUSB2",
            motor_port="/dev/ttyACM0",
            kp_forward=1.5,
            kp_turn=1.2
        )

        # Envoi de la commande de navigation extraite de l'API
        nav_response = navigator.handle_request(json_response)
        logger.info("Réponse de la navigation : %s", nav_response)

        # Pause pour laisser le temps aux actions de s'exécuter
        time.sleep(2)

    except Exception as e:
        logger.error("Une erreur est survenue : %s", e)
    finally:
        # Arrêt propre du système de navigation
        try:
            if 'navigator' in locals():
                navigator.shutdown()
        except Exception as shutdown_error:
            logger.error("Erreur lors de l'arrêt de la navigation : %s", shutdown_error)
        logger.info("Programme terminé proprement.")

if __name__ == "__main__":
    main()

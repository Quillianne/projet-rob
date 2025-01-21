import cv2
import ktb
import logging
import os

class KinectSensor:
    def __init__(self, output_dir="output"):
        """
        Initialise le capteur Kinect et configure le répertoire de sortie.
        
        :param output_dir: Répertoire où les images seront enregistrées.
        """
        self.kinect = ktb.Kinect()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Crée le dossier de sortie si nécessaire
        logging.info(f"Répertoire de sortie configuré : {self.output_dir}")

    def get_frames(self):
        """
        Capture les images couleur et profondeur du Kinect.
        
        :return: Un dictionnaire contenant les frames (raw_color, raw_depth, color, depth).
        """
        try:
            frames = {
                "raw_color": self.kinect.get_frame(ktb.RAW_COLOR),
                "raw_depth": self.kinect.get_frame(ktb.RAW_DEPTH),
                "color": self.kinect.get_frame(ktb.COLOR),
                "depth": self.kinect.get_frame(ktb.DEPTH),
            }
            logging.info("Frames capturées avec succès.")
            return frames
        except Exception as e:
            logging.error(f"Erreur lors de la capture des frames : {e}")
            return None
        
    def get_raw_color(self):
        """
        Capture les images couleur et profondeur du Kinect.
        
        :return: Un dictionnaire contenant les frames (raw_color, raw_depth, color, depth).
        """
        try:
            frames = {
                "raw_color": self.kinect.get_frame(ktb.RAW_COLOR),
            }
            logging.info("Frames capturées avec succès.")
            return frames
        except Exception as e:
            logging.error(f"Erreur lors de la capture des frames : {e}")
            return None        

    def save_frames(self, frames):
        """
        Enregistre les frames capturées dans des fichiers image.
        
        :param frames: Dictionnaire contenant les frames à sauvegarder.
        """
        try:
            if not frames:
                logging.warning("Aucune frame à enregistrer.")
                return

            for key, frame in frames.items():
                filename = os.path.join(self.output_dir, f"{key}.png")
                cv2.imwrite(filename, frame)
                logging.info(f"Frame {key} enregistrée sous {filename}")
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement des frames : {e}")

    def display_frame(self, frame, window_name="Kinect Frame"):
        """
        Affiche une frame spécifique dans une fenêtre.
        
        :param frame: Image à afficher.
        :param window_name: Titre de la fenêtre.
        """
        try:
            cv2.imshow(window_name, frame)
            cv2.waitKey(0)  # Attend qu'une touche soit pressée
            cv2.destroyAllWindows()
            logging.info(f"Frame affichée : {window_name}")
        except Exception as e:
            logging.error(f"Erreur lors de l'affichage de la frame : {e}")



# Exemple d'utilisation autonome
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    kinect_sensor = KinectSensor(output_dir="kinect_images")

    try:
        frames = kinect_sensor.get_frames()
        kinect_sensor.save_frames(frames)
        if "color" in frames:
            kinect_sensor.display_frame(frames["color"], window_name="Color Frame")
    except KeyboardInterrupt:
        logging.info("Interruption par l'utilisateur.")
    except Exception as e:
        logging.error(f"Erreur inattendue : {e}")


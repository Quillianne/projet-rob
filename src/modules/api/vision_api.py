import base64
import os
import logging
from openai import OpenAI

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

class VisionAPI:
    def __init__(self, api_key, prompt):
        """
        Initialise le client OpenAI, le prompt et l'historique.

        :param api_key: Clé API pour OpenAI.
        :param prompt: Prompt à utiliser pour toutes les requêtes.
        """
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger dédié
        self.logger.info("Initialisation de VisionAPI.")

        if api_key == "env":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                self.logger.error("Clé API OpenAI non trouvée dans les variables d'environnement.")
                raise ValueError("Clé API OpenAI non trouvée.")

        if prompt == "import_txt":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(script_dir, "prompt.txt")
            try:
                with open(prompt_path, "r") as file:
                    prompt = file.read()
                self.logger.info("Prompt chargé depuis le fichier : %s", prompt_path)
            except FileNotFoundError:
                self.logger.error("Fichier prompt.txt introuvable.")
                raise

        self.client = OpenAI(api_key=api_key)
        self.prompt = prompt
        self.history = [{"role": "user", "content": prompt}]
        self.logger.info("Client OpenAI initialisé avec succès.")

    @staticmethod
    def encode_image(image_path=None, image_data=None):
        """
        Encode une image en base64 à partir d'un fichier ou d'une donnée brute.

        :param image_path: Chemin vers l'image à encoder.
        :param image_data: Données binaires de l'image.
        :return: Image encodée en base64 (string).
        """
        if image_path:
            try:
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                logging.debug("Image encodée avec succès depuis le fichier : %s", image_path)
                return encoded_image
            except FileNotFoundError:
                logging.error("Fichier image introuvable : %s", image_path)
                raise
        elif image_data:
            logging.debug("Encodage d'une image à partir des données binaires.")
            return base64.b64encode(image_data).decode("utf-8")
        else:
            logging.error("Aucune image fournie pour l'encodage.")
            raise ValueError("Aucune image fournie pour l'encodage.")

    def send_request(self, image_path=None, image_data=None):
        """
        Envoie une requête à l'API avec une image.

        :param image_path: Chemin de l'image à envoyer.
        :param image_data: Données binaires de l'image.
        :return: Réponse de l'API.
        """
        if not image_path and not image_data:
            self.logger.error("Aucune image fournie pour l'envoi de la requête.")
            raise ValueError("Vous devez fournir une image_path ou une image_data.")

        try:
            base64_image = self.encode_image(image_path, image_data)
        except Exception as e:
            self.logger.error("Erreur lors de l'encodage de l'image : %s", e)
            return None

        image_message = {
            "role": "user",
            "content": [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}]
        }

        self.history.append(image_message)
        self.logger.info("Envoi de la requête à l'API OpenAI.")

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.history,
            )
            assistant_response = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": assistant_response})
            self.logger.info("Réponse reçue avec succès de l'API OpenAI.")
            return assistant_response
        except Exception as e:
            self.logger.error("Erreur lors de la requête à l'API OpenAI : %s", e)
            return None

    def clear_history(self):
        """
        Vide l'historique des messages et réinitialise avec le prompt initial.
        """
        self.history = [{"role": "user", "content": self.prompt}]
        self.logger.info("Historique des messages réinitialisé.")

    def return_clean_json(self, response):
        """
        Extrait le contenu JSON propre de la réponse de l'API.

        :param response: Réponse brute de l'API.
        :return: Contenu JSON sous forme de chaîne de caractères.
        """
        try:
            json_data = response.split("```json\n")[1].split("\n```")[0]
            self.logger.debug("Extraction du JSON réussie.")
            return json_data
        except IndexError:
            self.logger.warning("Impossible d'extraire un JSON valide de la réponse.")
            return None


# Test de la classe
if __name__ == "__main__":
    logging.info("Démarrage du programme principal.")

    try:
        api = VisionAPI(api_key="env", prompt="import_txt")
        response = api.send_request(image_path="raw_color.png")
        
        if response:
            clean_json = api.return_clean_json(response)
            if clean_json:
                print("Réponse extraite :", clean_json)
            else:
                logging.warning("La réponse n'a pas pu être extraite sous forme de JSON.")
        else:
            logging.error("Échec de la requête à l'API.")
    except Exception as e:
        logging.error("Une erreur inattendue s'est produite : %s", e)

    logging.info("Fin du programme.")

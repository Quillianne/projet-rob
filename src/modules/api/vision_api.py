import base64
from openai import OpenAI

class VisionAPI:
    def __init__(self, api_key, prompt):
        """
        Initialise le client OpenAI, le prompt, et l'historique.
        :param api_key: Clé API pour OpenAI.
        :param prompt: Prompt à utiliser pour toutes les requêtes.
        """
        self.client = OpenAI(api_key=api_key)
        self.prompt = prompt
        self.history = []  # Historique des messages (questions/réponses)
        
        # Ajouter le prompt au début de l'historique
        self.history.append({"role": "user", "content": prompt})

    @staticmethod
    def encode_image(image_path):
        """
        Encode une image en base64.
        :param image_path: Chemin vers l'image à encoder.
        :return: Image encodée en base64 (string).
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def send_request(self, image_path):
        """
        Envoie une requête à l'API avec une image.
        :param image_path: Chemin de l'image à envoyer.
        :return: Réponse de l'API.
        """
        # Encoder l'image
        base64_image = self.encode_image(image_path)
        
        # Construire le message pour l'image
        image_message = {
            "role": "user",
            "content": {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            },
        }

        # Ajouter l'image à l'historique
        self.history.append(image_message)

        # Envoyer la requête avec l'historique complet
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
        )

        # Ajouter la réponse à l'historique
        assistant_response = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_response})

        # Retourner uniquement la réponse
        return assistant_response

    def clear_history(self):
        """
        Vide l'historique des messages et réinitialise avec le prompt initial.
        """
        self.history = [{"role": "user", "content": self.prompt}]

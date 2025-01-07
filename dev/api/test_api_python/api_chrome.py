from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Chemin vers le chromedriver
driver_path = "/home/yasmine/Documents/projet/copilotrob/drivers/chromedriver-linux64/chromedriver"  # Remplace ce chemin par celui où tu as téléchargé le chromedriver

options = Options()
# Ajouter des options (par exemple, mode sans tête si tu ne veux pas que la fenêtre du navigateur apparaisse)
options.headless = True  # Si tu veux exécuter sans afficher le navigateur

# Créer un Service avec le chemin de chromedriver
service = Service(driver_path)

# Initialiser le navigateur avec le Service
driver = webdriver.Chrome(service=service, options=options)

try:
    # Ouvrir la page de connexion OpenAI
    #driver.get("https://platform.openai.com/playground/chat?models=gpt-4")
    driver.get("https://auth.openai.com/authorize?audience=https%3A%2F%2Fapi.openai.com%2Fv1&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjEuMjEuMCJ9&client_id=DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD&device_id=2b94a6d4-680a-4f77-af2b-6c48e7deee62&issuer=https%3A%2F%2Fauth.openai.com&max_age=0&nonce=VlhpbVNWbDNiLXBmaW9zaFE3cS1iLkY3TkRvcTFMNVpsZHAzNzlJdGN2Tw%3D%3D&redirect_uri=https%3A%2F%2Fplatform.openai.com%2Fauth%2Fcallback&response_mode=query&response_type=code&scope=openid+profile+email+offline_access&state=RER0R29LMW5VNmZ3bjZ4R0JsbWpCakxPWmZjdmdTWTZSdXNvdktDR0NhSQ%3D%3D&flow=treatment")
    time.sleep(40)

    # Remplir les champs de connexion
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys("yasmine.raoux@ensta-bretagne.org")  # Remplace par ton email
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("@Mbp7tw;sxqY")  # Remplace par ton mot de passe

    # Soumettre le formulaire
    password_field.send_keys(Keys.RETURN)
    time.sleep(60)  # Attendre que la connexion soit effectuée

    # Maintenant que tu es connecté, tu peux faire des requêtes avec Selenium ou OpenAI API.
    print("Connexion réussie!")

except Exception as e:
    print("Erreur de connexion:", e)


try:
    # Étape 1 : Ouvrir la page web qui interagit avec l'API ChatGPT
    driver.get("https://platform.openai.com/playground/chat?models=gpt-4")

    # Étape 2 : Localiser et uploader l'image
    time.sleep(3)  # Attendre que la page se charge
    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")  # Sélecteur pour l'input de fichier
    upload_input.send_keys("photos/prote_1.jpeg")  # Spécifie le chemin vers l'image à envoyer

    # Étape 3 : Attendre que ChatGPT traite l'image et génère une commande
    time.sleep(10)  # Attendre 10 secondes pour le traitement, ajuster si nécessaire
    response_element = driver.find_element(By.CSS_SELECTOR, "élément_qui_affiche_les_commandes")  # Sélecteur du texte de réponse
    commands = response_element.text
    print("Commandes reçues par ChatGPT :", commands)

    # Étape 4 : Utilisation des commandes dans ton robot
    if "forward" in commands:
        distance = int(commands.split(" ")[1])  # Extraire la distance
        print(f"Avancer de {distance} mètres")
    elif "turn left" in commands:
        angle = int(commands.split(" ")[2])  # Extraire l'angle
        print(f"Tourner à gauche de {angle} degrés")

except Exception as e:
    print("Erreur :", e)
finally:
    driver.quit()  # Ferme le navigateur après l'exécution du script

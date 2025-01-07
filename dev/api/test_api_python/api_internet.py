from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import os

# Chemin vers le geckodriver
driver_path = "photos/geckodriver"  # Remplace ce chemin par celui où se trouve le geckodriver sur ton système

# Configuration des options de Firefox
options = Options()
# Spécifie le chemin du profil que tu veux utiliser
profile_path = "/home/yasmine/snap/firefox/common/.mozilla/firefox/u4i2txkj.tahlesoufs"
options.set_preference("profile", profile_path)

# Créer un Service avec le chemin de geckodriver
service = Service(driver_path)

# # Initialiser le navigateur avec le Service et les options
# driver = webdriver.Firefox(service=service, options=options)

try:
    driver = webdriver.Firefox(service=service, options=options)
except Exception as e:
    print("Erreur lors du lancement de Firefox avec le profil :", e)

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

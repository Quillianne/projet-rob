
# Autonomous guidance using OpenAI

Ce projet Python vise à contrôler un robot roulant équipé de divers capteurs (RPLIDAR, Kinect, IMU, etc.) et d'un contrôleur de moteurs Pololu Maestro, tout en utilisant CHATGPT pour la navigation et l'évitement d'obstacles.

## Membres du groupe :
- Maxime Lefèvre
- Robin Vidal
- Kilian Barantal
- Yasmine Raoux


Lien vers le fichier google docs contenant l'avancement du projet par séances :
https://docs.google.com/document/d/1WdZpqYGWUWTXwZNBJJRWHQwiuqZebqBb8ohJc7dD8aI/edit?usp=sharing

## 🗂️ Suivi de l'avancement  

Cette section explique les icônes utilisées pour indiquer l'état d'avancement des tâches du projet :  

| Icône | État                        | Description                                      |
|-------|-----------------------------|--------------------------------------------------|
| ✅    | **Terminé et testé**         | La tâche est terminée et a été complètement testée. |
| 🟡    | **Terminé mais à tester**    | La tâche est terminée mais nécessite encore des tests. |
| ⚙️    | **En cours**                 | La tâche est actuellement en cours de réalisation. |
| ⚠️    | **Bug détecté**             | La tâche a été développée, mais des bugs ont été identifiés. |
| 🛑    | **Non commencé**             | La tâche n'a pas encore été commencée. |
| ❌    | **Abandonné**             | La tâche a été abandonné car considéré hors sujet ou plus pertinente. |


## Structure du Projet

L'arborescence du projet est organisée de manière modulaire pour faciliter la maintenance, l'extensibilité et les tests.

### **1. `src/`**
Dossier contenant le code source principal du projet.

- **`main.py`** : Point d'entrée principal du projet. Initialise les modules, les capteurs et démarre les boucles de contrôle.

- **`config/`**

  - ❌`settings.py` : Contient les configurations globales (paramètres des capteurs, chemins de fichiers, etc.).

- **`modules/`**
  - **`navigation/`** : Gestion des fonctionnalités liées au mouvement du robot.
    - ❌`path_planning.py` : Algorithmes de planification de trajectoire (e.g., A*, Dijkstra).
    - ❌`obstacle_avoidance.py` : Évitement des obstacles en temps réel.
    - ❌`localization.py` : Gestion de la localisation via Hector SLAM et les capteurs.
    - ✅`simple_navigation.py` : Navigation simple avec des commandes simples (foward, turn_right, turn_left)
  - **`sensors/`** : Interfaces pour les capteurs.
    - ⚙️`lidar.py` : Gestion des données du RPLIDAR.
    - ✅`kinect.py` : Traitement des images et des profondeurs capturées par la Kinect.
    - ✅`imu.py` : Lecture des données de l'IMU.
  - **`controllers/`** : Gestion des moteurs et des interactions avec le matériel.
    - ✅`maestro_controller.py` : Contrôle des moteurs via le Pololu Maestro.
    - ✅`motor_control.py` : Envoi des commandes de mouvement.
  - **`hector_slam/`** : Modules spécifiques à Hector SLAM.
    - ❌`map_building.py` : Création et mise à jour de la carte.
    - ❌`trajectory_calculation.py` : Calcul des trajectoires basées sur la carte générée.
  - **`api/`** : Interfaces avec les APIs externes.
    - ✅`vision_api.py` : Intégration avec l'API Vision pour interpréter les images.
    - ❌`speech_control.py` : Reconnaissance et traitement des commandes vocales.
    
- **`utils/`**
  - ❌`logger.py` : Gestion centralisée des journaux d'activité.
  - ✅`sensormapper.py` : Mapper les capteurs à leurs emplacements USB

### **2. `tests/`**
Dossier contenant les tests unitaires et fonctionnels pour vérifier le bon fonctionnement de chaque module.
- ❌`test_navigation.py` : Tests pour les fonctionnalités de navigation.
- ❌`test_sensors.py` : Tests pour les capteurs.
- ❌`test_controllers.py` : Tests pour les contrôleurs.
- ❌`test_hector_slam.py` : Tests pour Hector SLAM.
- ❌`test_api.py` : Tests pour l'intégration avec les APIs externes.

### **3. `docs/`**
Dossier pour la documentation du projet.
- `README.md` : Document principal expliquant l'arborescence et les fonctionnalités du projet, avec le lien d'accès au fichier google docs avec l'avancement du projet à chaque séance.
- **`demande_budget`** : Fichier pdf et xls de demande de budget.
- **`photos_avancement`** : Photos du groupe au cours du premier semestre.
- **`ingenierie_systeme`** : TD1 et TD2 d'ingenierie système : architecture matérielle, use-case etc...

### **4. Fichiers Racine**
- `requirements.txt` : Liste des dépendances nécessaires pour le projet.
- `setup.py` : Script d'installation pour configurer le projet comme un package Python.

---


## Quick Start Guide  

### 1. Brancher les batteries  
Suivre les indications des scotch :  
- **12V** → Kinect  
- **12V** (batterie 3S) → Moteurs  
- **19V** → Ordinateur (puis l’allumer et attendre ~1 min)  

### 2. Connexion SSH  
#### Via VS Code  
1. **Ouvrir la palette de commandes** : `Ctrl + Shift + P`  
2. **Ajouter un nouvel hôte SSH** :  
   - Sélectionner : `Remote-SSH: Add new SSH Host...`  
   - Ajouter : `tahlesoufs-desktop.local`  
   - Sélectionner un fichier de configuration SSH (ex: `/home/user/.ssh/config`)  
3. **Se connecter à l'hôte** :  
   - `Ctrl + Shift + P` → `Remote-SSH: Connect to Host...`  
   - Sélectionner : `tahlesoufs-desktop.local`  
4. **Attendre la connexion** et entrer le mot de passe : `vive la rob!`  

### 3. Lancement de la mission  
1. **Activer l’environnement** :  
   ```sh
   source start_venv.sh
   ```
2. **Lancer le programme `src/main.py`**:
    ```sh
    cd src/
    python3 main.py
    ```


## User Manual

### Erreurs possibles
1. Erreurs d'environnement python
- ` ModuleNotFoundError: No module named 'ktb' ` 
- ` ModuleNotFoundError: No module named 'modules' ` 
- ` ModuleNotFoundError: No module named 'pydub' `

  Lancer les programmes avec le bon environnement (sur VS Code choisir l'environnement en bas à droite) ou sinon bien faire source start_venv.sh

2. Erreur kinect
- `[Error] [protocol::CommandTransaction] bulk transfer failed: LIBUSB_ERROR_TIMEOUT Operation timed out
INFO:root:Répertoire de sortie configuré : kinect_images`

Débrancher et rebrancher la batterie de la kinect. Relancer le terminal.






## Instructions pour l'Installation


1. **Clonez ce dépôt :**  
   ```bash
   git clone https://github.com/Quillianne/projet-rob
   ```
   
2. **Installez libfreenect2 :**  
   - Sur les systèmes basés sur Debian/Ubuntu, vous pouvez tenter :
     ```bash
     sudo apt-get update
     sudo apt-get install libfreenect2
     ```
   - Selon votre distribution et votre environnement, vous devrez peut-être compiler libfreenect2 depuis [son dépôt GitHub](https://github.com/OpenKinect/libfreenect2). Consultez la documentation correspondante pour plus de détails. Attention ça peut être un point un peu compliqué

3. **Installez les dépendances Python :**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancez le projet :**  
   ```bash
   python src/main.py
   ```

---


## Objectifs du Projet
Ce projet a pour but de :
1. Naviguer dans un environnement inconnu en utilisant la caméra et ChatGPT
2. Éviter les obstacles en temps réel grâce à l'IMU et d'autres capteurs.
3. Utiliser une caméra Kinect et des algorithmes d'API Vision pour détecter des objets d'intérêt.
4. Expliquer ses choix grâce à des haut-parleurs



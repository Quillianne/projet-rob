# Installation et configuration de libfreenect2 sur Ubuntu 22.04

Ce guide explique comment configurer **libfreenect2** sur Ubuntu 22.04 pour l'utiliser avec un Kinect Xbox One (Kinect v2).

## 1. Prérequis système

Installez les outils de développement requis :

```bash
sudo apt-get update
sudo apt-get install build-essential cmake pkg-config libusb-1.0-0-dev libturbojpeg0-dev libglfw3-dev
```

## 2. Installation de libfreenect2

### Clonez le dépôt Git et construisez-le :

```bash
git clone https://github.com/OpenKinect/libfreenect2.git
cd libfreenect2
```

Si nécessaire, installez les dépendances pour les systèmes plus anciens :

```bash
cd depends
./download_debs_trusty.sh
```

Ensuite, revenez dans le répertoire racine du projet et construisez le projet :

```bash
cd ..
mkdir build && cd build
cmake ..
make
sudo make install
```

## 3.1 Configurer les règles udev pour Kinect

Configurez les règles udev pour permettre l'accès au périphérique Kinect sans avoir besoin de `sudo` :

```bash
sudo cp ../platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Rebranchez votre périphérique Kinect.

## 3.2 Modifier le fichier `.bashrc` pour le chemin des librairies
Ouvrez votre fichier `.bashrc` (ou `.zshrc` si vous utilisez zsh) et ajoutez la ligne suivante pour configurer le chemin des bibliothèques dynamiques :

```bash
nano ~/.bashrc
```

Ajoutez cette ligne à la fin du fichier :

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/home/maxime/libfreenect2/build/lib
```

Enregistrez et fermez l’éditeur (avec `Ctrl+X` pour quitter, puis `Y` pour enregistrer).

Rechargez la configuration de votre shell pour appliquer les modifications :

```bash
source ~/.bashrc
```

(Chaque nouvelle session de terminal nécessitera cette commande, ou utilisez `source ~/.bashrc` après chaque redémarrage du terminal).

## 4. Tester le Kinect avec Protonect

Pour vérifier l'installation et voir si le Kinect est détecté, exécutez le programme `Protonect` depuis le répertoire `build` :

```bash
./bin/Protonect
```

## 5. Dépannage

Si le Kinect n'est pas détecté :

1. Débranchez et rebranchez le périphérique Kinect.
2. Vérifiez que les règles udev sont correctement appliquées en relançant :
   ```bash
   sudo cp ../platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

Une fois cela effectué, essayez de lancer `Protonect` à nouveau.

## Ressources supplémentaires

- [Dépôt GitHub de libfreenect2](https://github.com/OpenKinect/libfreenect2)

# Créer l'exécutable save_rgb

Si problème pour la compilation utiliser la commande : 
```
g++ -std=c++11 -o save_rgb save_rgb.cpp $(pkg-config --cflags --libs opencv4) -I/path/to/libfreenect2/include -L/path/to/libfreenect2/lib -lfreenect2
```

# kinect.py
La fonction photo() permet de prendre une photo et de l'enregistrer sous le nom 'photo.png' dans le dossier courant.

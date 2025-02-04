from rplidar import RPLidar
import time

# Port du LiDAR
PORT_NAME = '/dev/ttyUSB2'

# Initialisation du LiDAR
lidar = RPLidar(PORT_NAME)

# Fichier de sortie
output_file = "data_lidar.dat"

try:
    print("Démarrage du LiDAR")
    lidar.start_motor()
    time.sleep(4)

    print("Collecte de données...")
    for scan in lidar.iter_scans():
        # Créer une liste pour stocker les distances (0° à 360°)
        distances = [0] * 360

        # Placer les distances aux indices correspondants
        for (_, angle, distance) in scan:
            angle = int(angle)  # Convertir l'angle en entier
            if 0 <= angle < 360:  # Vérifier que l'angle est valide
                distances[angle] = int(distance)  # Ajouter la distance

        # Écrire les distances dans le fichier (une ligne par scan)
        with open(output_file, "a") as f:
            f.write(" ".join(map(str, distances)) + "\n")

        print(f"Scan enregistré dans {output_file}")
        break  # Arrêter après un scan pour cet exemple

finally:
    print("Arrêt du LiDAR")
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()

from rplidar import RPLidar, RPLidarException
import numpy as np
import matplotlib.pyplot as plt
import time

# Port du LiDAR
PORT_NAME = '/dev/ttyUSB1'

# Initialisation du LiDAR
lidar = RPLidar(PORT_NAME)
print("Démarrage du LiDAR")
lidar.start_motor()
time.sleep(2)  # Attendre que le moteur démarre correctement

# Collecter toutes les données
scan_data = []

try:
    print("Collecte des données...")
    for i, measurment in enumerate(lidar.iter_measurments()):
        new_scan, quality, angle, distance = measurment  # Décomposition correcte en 4 variables
        if distance > 0:  # Ignorer les distances nulles
            scan_data.append((np.radians(angle), distance))
        
        if i > 5000:  # Limite de mesure (par exemple, 5000 mesures)
            break

except RPLidarException as e:
    print(f"Erreur LiDAR : {e}")

finally:
    print("Arrêt du LiDAR")
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()

# Visualisation des données après collecte
if scan_data:
    angles, distances = zip(*scan_data)

    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection='polar')
    ax.scatter(angles, distances, c='blue', s=5, alpha=0.75)
    ax.set_title("Visualisation complète des données LiDAR")
    ax.set_ylim(0, max(distances) + 100)
    plt.show()
from pyrplidar import PyRPlidar
import time

# Connectez-vous au LiDAR
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200)  # Adaptez le port si nécessaire

# Démarrez le scan
lidar.start_scan()

try:
    print("Récupération des données...")
    for scan in lidar.iter_measurments():  # Méthode correcte pour obtenir les données
        quality, angle, distance = scan
        print(f"Qualité: {quality}, Angle: {angle:.2f}°, Distance: {distance:.2f} mm")
        time.sleep(0.1)  # Pour limiter le débit d'affichage
except KeyboardInterrupt:
    print("Arrêt du scan...")
finally:
    lidar.stop()
    lidar.disconnect()
    print("Déconnecté.")

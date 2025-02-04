from rplidar import RPLidar
import time
# Port du LiDAR (vérifiez le port série, souvent /dev/ttyUSB0 sur Linux)
PORT_NAME = '/dev/ttyUSB1'

lidar = RPLidar(PORT_NAME)

# Lancer la récupération de données (exemple)
print("Démarrage du LiDAR")
lidar.start_motor()
time.sleep(4)
# Effectuer quelques actions ou attendre un certain temps
try:
    print("Collecte de données...")
    for scan in lidar.iter_scans():
        print(f"Nombre de points: {len(scan)}")
        for (_, angle, distance) in scan:
            print(f"Angle: {angle:.2f}, Distance: {distance:.2f}")
        # Si tu veux arrêter après un certain nombre de scans, tu peux mettre une condition ici
        break  # On arrête après un scan pour l'exemple
finally:
    print("Arrêt du LiDAR")
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()

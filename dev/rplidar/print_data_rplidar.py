from rplidar import RPLidar

# Port du LiDAR (vérifiez le port série, souvent /dev/ttyUSB0 sur Linux)
PORT_NAME = '/dev/ttyUSB1'

lidar = RPLidar(PORT_NAME)

try:
    print('Récupération des données...')
    for scan in lidar.iter_scans():
        print(f'Nombre de points : {len(scan)}')
        for (_, angle, distance) in scan:
            print(f'Angle: {angle:.2f}, Distance: {distance:.2f}')
except KeyboardInterrupt:
    print('Arrêt du LiDAR')
finally:
    lidar.stop()
    lidar.disconnect()

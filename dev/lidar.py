from rplidar import RPLidar
import time

class LidarScanner:
    def __init__(self, port='/dev/ttyUSB2', output_file="data_lidar.dat"):
        """
        Initialise le LidarScanner avec le port série et le fichier de sortie.
        
        :param port: Port série du LiDAR (ex. : '/dev/ttyUSB2')
        :param output_file: Nom du fichier pour sauvegarder les données.
        """
        self.port = port
        self.output_file = output_file
        self.lidar = RPLidar(self.port)
        print(f"LiDAR initialisé sur le port {self.port}")

    def start(self):
        """ Démarre le moteur du LiDAR. """
        print("Démarrage du LiDAR...")
        self.lidar.start_motor()
        time.sleep(5)  # Temps d'attente pour que le LiDAR soit prêt

    def stop(self):
        """ Arrête le moteur et déconnecte le LiDAR. """
        print("Arrêt du LiDAR...")
        self.lidar.stop_motor()
        self.lidar.stop()
        self.lidar.disconnect()

    def read(self):
        """ Lit un scan et retourne les données brutes. """
        print("Lecture des données...")
        print("iter_scan:", self.lidar.iter_scans())
        for scan in self.lidar.iter_scans():
            return scan  # Retourne le premier scan trouvé

    def debug(self):
        """ Lit un scan et affiche les données de distance et d'angle. """
        print("Mode Debug : Affichage des données...")
        scan = self.read()
        if scan:
            print(f"Nombre de points : {len(scan)}")
            for (_, angle, distance) in scan:
                print(f"Angle : {angle:.2f}, Distance : {distance:.2f}")
            return scan

    def save(self):
        """ Lit un scan et sauvegarde les distances (0° à 360°) dans un fichier. """
        print("Mode Sauvegarde : Collecte des données et sauvegarde...")
        scan = self.read()
        if scan:
            distances = [0] * 360
            for (_, angle, distance) in scan:
                angle = int(angle)
                if 0 <= angle < 360:
                    distances[angle] = int(distance)
            
            with open(self.output_file, "a") as f:
                f.write(" ".join(map(str, distances)) + "\n")

            print(f"Scan enregistré dans {self.output_file}")
            return scan
        
    def run(self, mode='read'):
        """
        Exécute le LiDAR selon le mode choisi.
        
        :param mode: Mode d'exécution ('debug', 'save', 'read').
        """
        try:
            self.start()
            if mode == 'debug':
                data = self.debug()
            elif mode == 'save':
                data = self.save()
            elif mode == 'read':
                data = self.read()
            else:
                print("Mode inconnu. Utilisez 'debug', 'save' ou 'read'.")
        except KeyboardInterrupt:
            print("Interruption par l'utilisateur.")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            self.stop()


# Exemple d'utilisation
if __name__ == "__main__":
    lidar_scanner = LidarScanner(port="/dev/ttyUSB1", output_file="data_lidar.dat")
    lidar_scanner.start()
    try:  
        lidar_scanner.debug()
    finally:
        lidar_scanner.stop()

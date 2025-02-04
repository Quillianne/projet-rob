import serial.tools.list_ports

class SensorUSBMapper:
    """
    Classe pour mapper les capteurs à leurs emplacements USB en fonction de leur VID et PID.
    """

    def __init__(self, sensor_config):
        """
        Initialise la classe avec une configuration des capteurs.

        :param sensor_config: Dictionnaire avec les noms des capteurs comme clés et leurs VID/PID comme valeurs.
                              Exemple : {"lidar": {"vid": "10c4", "pid": "ea60"}}
        """
        self.sensor_config = sensor_config

    @staticmethod
    def list_usb_devices():
        """
        Retourne une liste des périphériques USB connectés avec leurs informations VID, PID, et chemin /dev.
        """
        devices = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            device_info = {
                "device": port.device,  # Chemin, e.g., /dev/ttyUSB0
                "vid": f"{port.vid:04x}" if port.vid else None,
                "pid": f"{port.pid:04x}" if port.pid else None,
                "serial_number": port.serial_number,
                "description": port.description,
            }
            devices.append(device_info)
        return devices

    def find_device_by_vid_pid(self, vid, pid):
        """
        Recherche un périphérique USB par VID et PID.

        :param vid: VID du périphérique (string, ex: "10c4")
        :param pid: PID du périphérique (string, ex: "ea60")
        :return: Chemin du périphérique, ex: "/dev/ttyUSB0", ou None si non trouvé.
        """
        devices = self.list_usb_devices()
        for device in devices:
            if device["vid"] == vid and device["pid"] == pid:
                return device["device"]
        return None

    def map_sensors(self):
        """
        Mappe chaque capteur à son chemin USB.

        :return: Dictionnaire contenant le mapping des capteurs avec leurs chemins USB.
                 Exemple : {"lidar": "/dev/ttyUSB0", "imu": "/dev/ttyUSB1", "pololu": None}
        """
        result = {}
        for sensor_name, ids in self.sensor_config.items():
            device_path = self.find_device_by_vid_pid(ids["vid"], ids["pid"])
            result[sensor_name] = device_path if device_path else None
        return result


# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration des capteurs avec leurs VID et PID
    sensor_config = {
        "lidar": {"vid": "10c4", "pid": "ea60"},  # Exemple pour le RPLIDAR
        "imu": {"vid": "1a86", "pid": "7523"},    # Exemple pour l'IMU OpenLog
        "pololu": {"vid": "1ffb", "pid": "2300"}  # Exemple pour le Pololu Maestro
    }

    # Instanciation de la classe
    mapper = SensorUSBMapper(sensor_config)

    # Mapping des capteurs
    sensor_mapping = mapper.map_sensors()

    # Affichage des résultats
    print("Sensor Mapping:")
    for sensor, path in sensor_mapping.items():
        print(f"{sensor}: {path if path else 'Not Found'}")

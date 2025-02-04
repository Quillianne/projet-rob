from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from modules.sensors.kinect import KinectSensor
from utils.sensormapper import SensorUSBMapper
import time
import logging


logging.getLogger("MotorControl").setLevel(logging.INFO)
logging.getLogger("IMUSensor").setLevel(logging.INFO)
# logging.getLogger("freenect2").setLevel(logging.WARNING)
# logging.getLogger("ktb").setLevel(logging.WARNING)

if __name__ == "__main__":
    # Initialisation des modules

    # Configuration des capteurs avec leurs VID et PID
    sensor_config = {
        "lidar": {"vid": "10c4", "pid": "ea60"},  # Exemple pour le RPLIDAR 10c4:ea60
        "imu": {"vid": "1a86", "pid": "7523"},    # Exemple pour l'IMU OpenLog 1a86:7523
        "pololu": {"vid": "1ffb", "pid": "008b"}  # Exemple pour le Pololu Maestro 1ffb:008b
    }

    # Instanciation de la classe
    mapper = SensorUSBMapper(sensor_config)

    # Mapping des capteurs
    sensor_mapping = mapper.map_sensors()

    # Affichage des résultats
    print("Sensor Mapping:")
    for sensor, path in sensor_mapping.items():
        print(f"{sensor}: {path if path else 'Not Found'}")

"""
    motors = MotorControl(port='/dev/ttyACM0')
    imu = IMUSensor(port="/dev/ttyUSB2", baudrate=57600)
    kinect = KinectSensor(output_dir="kinect_images")

    try:
        # Connexion à l'IMU
        imu.connect()

        # Capture initiale des données IMU
        imu_data = imu.read_data()
        if imu_data:
            yaw, pitch, roll = imu_data
            logging.info(f"Données IMU initiales - HEADING: {yaw}")

        # Capture et affichage de l'image raw_color depuis Kinect
        frames = kinect.get_raw_color()
        if frames and "raw_color" in frames:
            #kinect.display_frame(frames["raw_color"], window_name="Kinect Raw Color Frame")
            kinect.save_frames(frames)  # Sauvegarde les frames

        # Exemple : faire varier la vitesse des moteurs
        for speed in [-100, 0, 100]:
            logging.info(f"Réglage de la vitesse des moteurs à {speed}")
            motors.set_motor_speed(speed, speed)  # Moteur gauche et droit en synchronisation
            time.sleep(2)

        motors.stop()

        # Capture des données IMU après les mouvements
        imu_data = imu.read_data()
        if imu_data:
            yaw, pitch, roll = imu_data
            logging.info(f"Données IMU après les mouvements - HEADING: {yaw}")

    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")

    finally:
        # Déconnexion des modules et nettoyage
        imu.close()
        motors.disconnect()
        logging.info("Programme terminé proprement.")

"""
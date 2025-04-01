import logging
import time
from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from modules.sensors.kinect import KinectSensor
from utils.sensormapper import SensorUSBMapper
from modules.api.vision_api import VisionAPI
from modules.navigation.simple_navigation import SimpleNavigation

def main():
    # Configuration du logging
    logging.getLogger().setLevel(logging.INFO)
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(logging.INFO)

    # Configuration des capteurs avec leurs VID et PID
    sensor_config = {
        "lidar": {"vid": "10c4", "pid": "ea60"},  # Exemple pour le RPLIDAR 10c4:ea60
        "imu": {"vid": "1a86", "pid": "7523"},     # Exemple pour l'IMU OpenLog 1a86:7523
        "pololu": {"vid": "1ffb", "pid": "008b"}     # Exemple pour le Pololu Maestro 1ffb:008b
    }

    # Instanciation du mapper et mapping des capteurs
    mapper = SensorUSBMapper(sensor_config)
    sensor_mapping = mapper.map_sensors()
    print("LIDAR Path:", sensor_mapping["lidar"])

    # Initialisation des modules en s'appuyant sur le mapping des capteurs
    motors = MotorControl(port=sensor_mapping["pololu"])
    navigator = SimpleNavigation(imu_port=sensor_mapping["imu"], motor_port=sensor_mapping["pololu"])


    try:
        motors.stop()

        ##### Ajouter les tests de navigation ici #####
        
        navigator.turn(90)

        ###############################################

    except Exception as e:
        logging.error(f"Une erreur est survenue pendant le test : {e}")

    finally:
        # Nettoyage et déconnexion des modules
        motors.disconnect()
        logging.info("Programme terminé proprement.")

if __name__ == '__main__':
    main()

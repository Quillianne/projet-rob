from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from utils.sensormapper import SensorUSBMapper
from modules.api.vision_api import VisionAPI
from modules.navigation.simple_navigation import SimpleNavigation

import time
import logging

# Set root logger level
logging.getLogger().setLevel(logging.INFO)

# Iterate through all existing loggers and set their level
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.INFO)


if __name__ == "__main__":
    # Configuration des capteurs avec leurs VID et PID
    sensor_config = {
        "lidar": {"vid": "10c4", "pid": "ea60"},  # Exemple pour le RPLIDAR 10c4:ea60
        "imu": {"vid": "1a86", "pid": "7523"},    # Exemple pour l'IMU OpenLog 1a86:7523
        "pololu": {"vid": "1ffb", "pid": "008b"}  # Exemple pour le Pololu Maestro 1ffb:008b
    }

    # Instanciation de la classe
    mapper = SensorUSBMapper(sensor_config)
    sensor_mapping = mapper.map_sensors()

    motors = MotorControl(port=sensor_mapping["pololu"])
    
    try:

        motors.stop()

    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")

    finally:
        # Déconnexion des modules et nettoyage
        motors.disconnect()
        logging.info("Programme terminé proprement.")
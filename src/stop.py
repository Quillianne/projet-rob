from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from utils.sensormapper import SensorUSBMapper
from modules.api.vision_api import VisionAPI
from modules.navigation.simple_navigation import SimpleNavigation
from config.settings import SENSOR_MAP
import time
import logging

# Set root logger level
logging.getLogger().setLevel(logging.INFO)

# Iterate through all existing loggers and set their level
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.INFO)


if __name__ == "__main__":
    # Configuration des capteurs avec leurs VID et PID
    sensor_config = SENSOR_MAP

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
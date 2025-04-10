from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from utils.sensormapper import SensorUSBMapper
from modules.api.vision_api import VisionAPI
from modules.navigation.simple_navigation import SimpleNavigation

import time
import logging


#logging.getLogger("MotorControl").setLevel(logging.INFO)
#logging.getLogger("IMUSensor").setLevel(logging.INFO)
#logging.getLogger("VisionAPI").setLevel(logging.INFO)


# Set root logger level
logging.getLogger().setLevel(logging.INFO)

# Iterate through all existing loggers and set their level
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.INFO)


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
    print("LIDAR Path: ", sensor_mapping["lidar"])




    motors = MotorControl(port=sensor_mapping["pololu"])
    #imu = IMUSensor(port=sensor_mapping["imu"], baudrate=57600)

    navigator = SimpleNavigation(imu_port=sensor_mapping["imu"], motor_port=sensor_mapping["pololu"])
    api = VisionAPI(api_key="env", prompt="import_txt")
    
    try:
        # Connexion à l'IMU
        #imu.connect()

        # Capture initiale des données IMU
        #imu_data = imu.read_data()
        #if imu_data:
        #    yaw, pitch, roll = imu_data
        #    logging.info(f"Données IMU initiales - HEADING: {yaw}")
        motors.stop()

    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")

    finally:
        # Déconnexion des modules et nettoyage
        #imu.close()
        motors.disconnect()
        logging.info("Programme terminé proprement.")


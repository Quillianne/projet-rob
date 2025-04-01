from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from utils.sensormapper import SensorUSBMapper
from config.settings import SENSOR_MAP

import time
import logging


if __name__ == "__main__":
    sensor_config = {
        "pololu": SENSOR_MAP["pololu"]  # Exemple pour le Pololu Maestro 1ffb:008b
    }
    # Instanciation de la classe
    mapper = SensorUSBMapper(sensor_config)

    # Mapping des capteurs
    sensor_mapping = mapper.map_sensors()
    motors = MotorControl(port=sensor_mapping["pololu"])
    try :
        for speed in [-100, 0, 100, 0]:
            motors.set_motor_speed(speed, speed)  # Moteur gauche et droit en synchronisation
            time.sleep(0.5)

    
    except Exception as e:
        print("Erreur survenue :", e)

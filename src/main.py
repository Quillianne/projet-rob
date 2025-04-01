from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from modules.sensors.kinect import KinectSensor
from utils.sensormapper import SensorUSBMapper
from modules.api.vision_api import VisionAPI
from modules.navigation.simple_navigation import SimpleNavigation
from modules.speech.sound import Sound

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
    # Mapping des capteurs
    mapper = SensorUSBMapper(sensor_config)
    sensor_mapping = mapper.map_sensors()

    motors = MotorControl(port=sensor_mapping["pololu"])
    imu = IMUSensor(port=sensor_mapping["imu"], baudrate=57600)
    for speed in [-100, 0, 100]:
        logging.info(f"Réglage de la vitesse des moteurs à {speed}")
        motors.set_motor_speed(speed, speed)  # Moteur gauche et droit en synchronisation
        time.sleep(0.5)
    motors.stop()

    navigator = SimpleNavigation(imu_port=sensor_mapping["imu"], motor_port=sensor_mapping["pololu"])
    api = VisionAPI(api_key="env", prompt="import_txt")
    kinect = KinectSensor(output_dir="kinect_images")
    son = Sound()
    k = 0 
    try:
        for k in range(10):
            # Capture et affichage de l'image raw_color depuis Kinect
            frames = kinect.get_frames()

            if frames and "raw_depth" in frames:
                kinect.save_frames(frames)  # Sauvegarde les frames
                print("frames saved")
            
            print("Question pour l'api...")
            response = api.send_request(image_path="kinect_images/raw_color.png")
            print("Réponse de l'API:")
            print(response)
            son.text_to_speech(response)
            # Test des 4 derniers charactères
            print(f"Consigne: {response[-4:]}")
            if response[-4:] == "TRUE":
                navigator.forward(2)
            else:
                navigator.turn(45)

            api.clear_history()
            motors.stop()
            time.sleep(1)

    except Exception as e:
        logging.error(f"Une erreur est surveself.kp_turn * abs(error)nue : {e}")

    finally:
        # Déconnexion des modules et nettoyage
        imu.close()
        motors.disconnect()
        logging.info("Programme terminé proprement.")


            

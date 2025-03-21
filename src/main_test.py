from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
from modules.sensors.kinect import KinectSensor
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
    kinect = KinectSensor(output_dir="kinect_images")
    k = 0 
    try:
        for k in range(10):
            # Capture et affichage de l'image raw_color depuis Kinect
            frames = kinect.get_frames()

            if frames and "raw_depth" in frames:
                kinect.save_frames(frames)  # Sauvegarde les frames
                print("frames saved")

            #kinect.display_frame(frames["raw_color"], window_name="Kinect Raw Color Frame")
            
            print("Question pour l'api...")
            response = api.send_request(image_path="kinect_images/raw_color.png")
            print("Réponse de l'API:")
            print(response)
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
        #imu.close()
        motors.disconnect()
        logging.info("Programme terminé proprement.")


            

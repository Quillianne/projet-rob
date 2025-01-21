from modules.controllers.motor_control import MotorControl
from modules.sensors.imu import IMUSensor
import time
import logging



# Réduire le niveau de logging pour les modules spécifiques

#logging.getLogger("MotorControl").setLevel(logging.INFO)
#logging.getLogger("IMUSensor").setLevel(logging.INFO)

if __name__ == "__main__":
    motors = MotorControl(port='/dev/ttyACM0')
    imu = IMUSensor(port="/dev/ttyUSB2", baudrate=57600)

    try:
        imu.connect()
        imu.read_data()
        # Exemple : faire varier la vitesse des moteurs
        for speed in [-100, 0 ,100]:
            motors.set_motor_speed(speed, speed)  # Moteur gauche et droit en opposition
            time.sleep(2)

        motors.stop()
        imu.read_data()
        imu.close()

    finally:
        motors.disconnect()

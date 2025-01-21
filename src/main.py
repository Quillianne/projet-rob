from modules.controllers.motor_control import MotorControl
import time

if __name__ == "__main__":
    motors = MotorControl(port='/dev/ttyACM0')

    try:
        
        # Exemple : faire varier la vitesse des moteurs
        for speed in [-100,-21,-20,-19,0,19,20,21,100]:
            print(f"Réglage des moteurs à la vitesse : {speed}")
            motors.set_motor_speed(speed, speed)  # Moteur gauche et droit en opposition
            time.sleep(2)

        print("Arrêt des moteurs...")
        motors.stop()

    finally:
        motors.disconnect()
        print("Déconnexion.")

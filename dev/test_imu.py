import serial
import pynmea2

# port ACM0 :
# port = "/dev/ttyACM0" # ls /dev/tty*
# baudrate = 9600        

# port USB0 :
port = "/dev/ttyUSB0"
baudrate = 57600

try:
    with serial.Serial(port, baudrate, timeout=2) as ser:
        print(f"Lecture des données sur {port} à {baudrate} bps...")
        while True:
            line = ser.read_until(b'\n').decode('ascii', errors='replace').strip()
            if line:
                #print(f"Données GPS : {line}")
                if line.startswith('#YPR'):
                    ypr_data = line.split("#YPR=")[1]  # récupère la partie après "#YPR="
                    yaw, pitch, roll = map(float, ypr_data.split(',')) 
                    print("yaw =", yaw, "pitch =", pitch, "roll =", roll)
                    
except serial.SerialException as e:
    print(f"Erreur de connexion : {e}")

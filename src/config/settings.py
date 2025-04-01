### This file contains the configuration settings for the application.



#For the sensors, we will use the following VID and PID:

SENSOR_MAP = {
        "lidar": {"vid": "10c4", "pid": "ea60"},  # Exemple pour le RPLIDAR 10c4:ea60
        "imu": {"vid": "1a86", "pid": "7523"},    # Exemple pour l'IMU OpenLog 1a86:7523
        "pololu": {"vid": "1ffb", "pid": "008b"}  # Exemple pour le Pololu Maestro 1ffb:008b
}

### For changing VID and PID, you can find vid and pid of new devices using the command:
# lsusb
### The output will show the VID and PID of all connected USB devices.

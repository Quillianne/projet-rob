# test code taken and adapted from dartv2_tools repo
# move back and forth and get scans when bot stops
import os
import sys
# access to the drivers
sys.path.append(os.path.join(os.path.dirname(__file__))) 
import dartv2_drivers_v3.drivers_v3 as drv
import time
import numpy as np

# save scans in python format (useful for debug on real robot with no graphics)
dosave = False

try:
    spd = int(sys.argv[1])
except:
    spd = 0
try:
    move_duration = float(sys.argv[2])
except:
    move_duration = 0.5
try:
    nloop = int(sys.argv[3])
except:
    nloop = 1
mybot = drv.DartV2DriverV3() #start robot

# graphics allowed in sim mode
if mybot.dart_sim():
    import matplotlib.pyplot as plt
    plt.figure()

# not mandatory but useful to check the lidar status
print (mybot.lidar.info())
print (mybot.lidar.health())

# start the lidar
mybot.lidar.start()
time.sleep(1.0) # wait for the lidar motor to spin up at right speed

# get a first scan (not sure its useful)
v_scan_def = mybot.lidar.get_scan(debug=False)
for il in range(2*nloop):
    sgn=1-2*(il%2)  # alternate forward and backward
    mybot.powerboard.set_speed(sgn*spd,sgn*spd)
    time.sleep(move_duration)
    mybot.powerboard.set_speed(0,0)
    time.sleep(1.0)
    # get a new scan with the robot stopped
    v_scan_def = mybot.lidar.get_scan(debug=False)
    print ("new scan ----------------------------------------------------")
    for iscan in range(len(v_scan_def)):
        scan_t = v_scan_def[iscan]["time"]
        scan = v_scan_def[iscan]["scan"]
        scan = np.array(scan)
    # can only display the scan in simulation mode
    if mybot.dart_sim():
        if il > 0:
            #plt.scatter(old_scan[:,1], old_scan[:,2], c='blue', label='Previous Scan')
            plt.scatter(old_x, old_y, c='blue', label='Previous Scan')
        r = scan[:,2]/1000 # from mm to m
        theta = np.radians(90.0-scan[:,1]) # angles geographic to trigonometric
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        #plt.scatter(scan[:,1], scan[:,2], c='red', label='Current Scan')
        plt.scatter(x, y, c='red', label='Current Scan')
        print(x,y,scan[:,1],scan[:,2])
        plt.xlabel('Angle')
        plt.ylabel('Distance')
        plt.xlabel('Angle')
        plt.ylabel('X')
        plt.title('Y')
        plt.legend()
        plt.draw()
        plt.pause(0.5)
        plt.clf()
    # save old scan for next display
    old_scan = scan
    old_x = x
    old_y = y
    # save the scan in a file in save enabled
    if dosave:
        mybot.lidar.save_scan_py_array(scan)
    time.sleep(1.0)
    
#
mybot.lidar.stop_acquisition()
time.sleep(1.0)

mybot.lidar.fullstop() # clean stop of the RP Lidar
print("front",mybot.sonars.read_front(),"left",mybot.sonars.read_left(),"right",mybot.sonars.read_right(),"back",mybot.sonars.read_rear())
mybot.powerboard.set_speed(-40,40)
time.sleep(2)

mybot.end() # clean end of the robot mission

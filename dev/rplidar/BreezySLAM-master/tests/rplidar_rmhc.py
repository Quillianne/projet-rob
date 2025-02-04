#!/usr/bin/env python3

'''
rpslam.py : BreezySLAM Python with SLAMTECH RP A1 Lidar
                 
Copyright (C) 2018 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = '/dev/ttyUSB1'


# Ideally we could use all 250 or so samples that the RPLidar delivers in one 
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES   = 40

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA2 as LaserModel
from rplidar import RPLidar as Lidar
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    # Connect to Lidar unit
    lidar = Lidar(LIDAR_DEVICE)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display

    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # Create an iterator to collect scan data from the RPLidar
    iterator = lidar.iter_scans()

    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles    = None

    # First scan is crap, so ignore it
    next(iterator)

    cnt=0
    while True:

        # Extract (quality, angle, distance) triples from current scan
        items = [item for item in next(iterator)]

        # Extract distances and angles from triples
        distances = [item[2] for item in items]
        angles    = [item[1] for item in items]
        print(len(distances))
    
        full_angles = np.arange(0, 360, 1)
        full_distances = np.ones(360) * 3000  # On met toutes les distances à 3 mètres par défaut
        for angle, dist in zip(angles, distances):
            full_distances[int(round(angle))] = dist 
        distances = [float(d) for d in full_distances]
        angles = [float(a) for a in full_angles]

        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:
            slam.update(distances, scan_angles_degrees=angles)
            previous_distances = distances.copy()
            previous_angles    = angles.copy()

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances, scan_angles_degrees=previous_angles)

        # Get current robot position
        x, y, theta = slam.getpos()
        print(x,y)

        cnt+=1 

        if cnt == 10:
            print(angles, distances)
            # Get current map bytes as grayscale
            slam.getmap(mapbytes)
            image=Image.frombytes('L',(MAP_SIZE_PIXELS,MAP_SIZE_PIXELS),bytes(mapbytes))
            image.save("images/image_test.png")

            plt.figure(figsize=(6, 6))
            for i in range(len(distances)):
                angle_rad = np.deg2rad(angles[i])
                x_lidar = distances[i] * np.cos(angle_rad)
                y_lidar = distances[i] * np.sin(angle_rad)
                plt.plot(x_lidar, y_lidar, 'ro', markersize=2)  # 'ro' = points rouges

            plt.xlim(-5000, 5000)  # Adapter aux distances réelles du Lidar
            plt.ylim(-5000, 5000)
            plt.title("Points du dernier scan Lidar")
            plt.savefig("images/lidar_points.png")
            plt.close()
            break

    
    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()

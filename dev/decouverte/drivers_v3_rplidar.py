#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import os
import math
import socket
import threading
from queue import Queue
import numpy as np

class RPLidar():
    def __init__(self,exec_robot,vsv=None):
        self.vsv = vsv
        self.__exec_robot = exec_robot
        self.__sim = False
        self.__ros = False
        self.__real = False
        if exec_robot == "Sim V-REP":
            self.__sim = True
        elif exec_robot == "Sim GAZEBO":
            self.__sim = True
        elif exec_robot == "Real":
            self.__real = True
        elif exec_robot == "Real ROS":
            self.__ros = True

        self.hostname = socket.gethostname()
        if self.__sim and not self.hostname.startswith("dart"):
            self.hostname = "dartsim"
        self.scan_cnt = 0
        self.lidar_on = False
        self.lidar_started = False 
        self.rplidar_query_scan_queue = None
        self.rplidar_return_scan_queue = None
        self.thread = None
        self.time_start = time.time()
        
        if self.__real:
            from rplidar import RPLidar as RpLdr
            try:
                self.lidar = RpLdr('/dev/ttyUSB0')
                self.lidar.reset()
                self.lidar_on= True
                print ("RPLidar connected ...")
            except:
                print ("no RPLidar connected !?!")
                self.lidar = None
                self.iterator = None
        elif self.__sim:
            print ("RPLidar simulation init ...")
            import dartv2_simu.lidarsim as lidarsim
            self.lidar = lidarsim.LidarSim()
            print ("... RPLidar simulation ready")
            
    def start_acquisition (self):
        self.rplidar_query_scan_queue = Queue()
        self.max_scan_fifo = 100
        self.rplidar_return_scan_queue = Queue(maxsize=self.max_scan_fifo)
        #self.lidar_iter_measures = self.lidar.iter_measures()
        # self.__thread = threading.Thread(target=rplidar_update_scan, args=(self.__rplidar_query_scan_queue,
        #                                                                         self.__rplidar_return_scan_queue,
        #
        self.thread = threading.Thread(target=self.rplidar_update_scan)
        self.thread.start()
        self.lidar_started= True
        print ("RPLidar acquisition started ...")
        
    def get_array_dimensions(self,arr):
        """Recursively find the size of each dimension in a nested list."""
        if not isinstance(arr, list):  # Base case: not a list
            return []
        return [len(arr)] + self.get_array_dimensions(arr[0]) if arr else [0]
            
    def reset(self):
        self.lidar.reset()
        self.scan_cnt = 0            

    def info(self):
        info = self.lidar.get_info()
        return info

    def health(self):
        health = self.lidar.get_health()
        return health

    def start(self):
        self.lidar.start_motor()  
                    
    def stop_acquisition(self):
        if self.__real:
            self.rplidar_query_scan_queue.put(-1)
            self.thread.join()
        self.lidar_started = False
        
        
    def get_last_scan(self):
        scan = []
        scan_on = False
        if self.lidar_started:
            try:
                for new_scan, quality, angle, distance in self.lidar.iter_measures():
                    if new_scan:
                        if scan_on:
                            break
                        else:
                            scan_on = True
                    if scan_on:
                        scan.append([quality,angle,distance])
            except:
                print ("RPLidar can't access data scan ...")
        else:
            print ("RPLidar acquisition not started ...")
            time.sleep(0.25)
        #print ("get_last scan :",self.get_array_dimensions(scan))
        return scan

    def rplidar_update_scan(self):
        while True:
            scan = self.get_last_scan()
            #print ("update scan :",self.get_array_dimensions(scan),", ",self.rplidar_return_scan_queue.qsize(),"scans in queue")
            if self.rplidar_return_scan_queue.qsize() >= self.max_scan_fifo:
                _ = self.rplidar_return_scan_queue.get()
            scan_def = {"time":time.time()-self.time_start, "scan":scan}
            self.rplidar_return_scan_queue.put(scan_def)
            nquery = self.rplidar_query_scan_queue.qsize()
            if nquery > 0:
                query = self.rplidar_query_scan_queue.get()
                if query==1:
                    print ('empty :',self.rplidar_return_scan_queue.empty(),', # scan stored :',self.rplidar_return_scan_queue.qsize())
                elif query==-1:
                    print ('end acquisition thread ...')
                    break
                else:
                    print ("query",query,"unknown")
                
    def get_scan(self,debug=False):
        v_scan_def = []
        if self.__real:
            #print ("get_scan, lidar status on,started",self.lidar_on, self.lidar_started)
            if not self.lidar_started:
                self.start_acquisition()
            #v_scan = []
            self.rplidar_query_scan_queue.put(1)
            while self.rplidar_return_scan_queue.qsize() == 0:
                time.sleep(0.01)
            while not self.rplidar_return_scan_queue.empty():
                scan_def = self.rplidar_return_scan_queue.get()
                #print ("get_scan",self.get_array_dimensions(scan_def["scan"]))
                v_scan_def.append(scan_def)
        elif self.__sim:
            scan = self.lidar.update_scan(debug=debug)
            scan_def = {"time":time.time()-self.time_start, "scan":scan}
            v_scan_def.append(scan_def)
        return v_scan_def

    def save_scan_py_array(self,scan,file_name=None,file_path="./lidarscans/"):
        # if self.__sim:  # seems that in simulation scan has one more dimension (the scan number
        #     scan = scan[0]
        if file_name is None:
            file_name = "scan_%4.4d_%s.py"%(self.scan_cnt,self.hostname)
            self.scan_cnt += 1
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = file_path + file_name
        st = "scan=["
        for status,angle,distance in scan:
            st = st+"[%.3f,%.3f],"%(angle,distance)
        st = st[0:-1]+"]"
        # print (st)
        print ("save scan in ",file_name)
        fp = open(file_name,"w")
        fp.write(st+"\n")
        fp.close()

    def fullstop(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()
 
if __name__ == "__main__":
    # warning, tests are quite complex in simulation as we need to connect
    # the module to the V-REP simulator...
    pass

import os
import numpy as np
from serial import Serial
from rover_common import aiolcm
from configparser import ConfigParser
from rover_msgs import proximity_sensors
import crcmod.predefined



def main():
    terabee = Terabee()
    terabee.start_sensor()
    terabee.close_range()

    depth_array = []


    while(True):
        depth_array = terabee.get_depth_array()
        obs_msg = Terabee()
        obs_msg.depths = depth_array
        #obs_msg.detected = detect_obstacle(depth_array) #ultrasonic, Sweep
        lcm.publish('proximity_sensors', obs_msg.encode())
        try:
            for i in range(len(depth_array)):
                for j in range(0,7):
                    print(depth_array[i][j])
        except KeyboardInterrupt:
            terabee.stop_sensor()
            break
        


if __name__ == '__main__':
    main()
    

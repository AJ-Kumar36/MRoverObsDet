#import os
import numpy as np
#from rover_common import aiolcm
#from configparser import ConfigParser
#from rover_msgs import proximity_sensors
import serial
import Terabee



def main():
    terabee = Terabee.Terabee()
    terabee.start_sensor()
    terabee.close_range()

    depth_array = []


    while(True):
        depth_array = terabee.get_depth_array()
        #obs_msg = Terabee()
        #obs_msg.depths = depth_array
        #obs_msg.detected = detect_obstacle(depth_array) #ultrasonic, Sweep
        #lcm.publish('proximity_sensors', obs_msg.encode())
        try:        
            print(depth_array)
        except KeyboardInterrupt:
            terabee.stop_sensor()
            break
        


if __name__ == '__main__':
    main()
    

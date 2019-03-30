#import os
import numpy as np
#from rover_common import aiolcm
#from configparser import ConfigParser
#from rover_msgs import proximity_sensors
import serial
import Terabee
import TFmini



def main():
    terabee = Terabee.Terabee()
    terabee.start_sensor()
    terabee.close_range()

    #tfmini = TFmini.TFMini()

    depth_array = []
    #tfmini_dist = 0


    while(True):
        depth_array = terabee.get_depth_array()
        #tfmini_dist = tfmini.get_dist()
        #obs_msg = Terabee()
        #obs_msg.depths = depth_array
        #obs_msg.detected = detect_obstacle(depth_array) #ultrasonic, Sweep
        #lcm.publish('proximity_sensors', obs_msg.encode())
        counter = 0
        try:
            if counter%30==0:
                if terabee.detected():
                    print("Terabee: Detected")
                else:
                    print("None") 
            counter+=1
            #print(tfmini_dist)
        except KeyboardInterrupt:
            terabee.stop_sensor()
            break
        


if __name__ == '__main__':
    main()
    

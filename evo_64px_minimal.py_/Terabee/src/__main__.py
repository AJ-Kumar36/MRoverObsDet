#import os
import numpy as np
#from rover_common import aiolcm
#from configparser import ConfigParser
#from rover_msgs import proximity_sensors
import serial
import Terabee
import TFmini
import Ultrasonics



def main():
    terabee = Terabee.Terabee()
    terabee.start_sensor()
    terabee.close_range()

    #tfmini = TFmini.TFMini()

    depth_array = []
    double_ults = Ultrasonics.Ultrasonics()
    ults1, ults2 = double_ults.get_dist()
    #tfmini_dist = 0

    counter = 0
    while(True):
        depth_array = terabee.get_depth_array()
        #tfmini_dist = tfmini.get_dist()
        #obs_msg = Terabee()
        #obs_msg.depths = depth_array
        #obs_msg.detected = detect_obstacle(depth_array) #ultrasonic, Sweep
        #lcm.publish('proximity_sensors', obs_msg.encode())
        try:
            ults1, ults2 = double_ults.get_dist()
            
            if counter%15==0:
                if double_ults.detected(ults1,ults2) and terabee.detected(): 
                    print("Ults+Bee: Detected")
                elif terabee.detected():
                    print("Terabee: Detected")
                elif double_ults.detected(ults1,ults2):
                    print("Ults: Detected")
                else:
                    print("No objects found") 
                    '''
                if double_ults.detected(ults1, ults2):
                    print("Detected")
                    print(str(ults1) + " " + str(ults2))
                else:
                    print("Not Detected")
                    print(str(ults1) + " " + str(ults2))
                    '''
            counter+=1
            
            
            
            #print(tfmini_dist)
        except KeyboardInterrupt:
            terabee.stop_sensor()
            break
        


if __name__ == '__main__':
    main()
    

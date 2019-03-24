import os
import numpy as np
from serial import Serial
from rover_common import aiolcm
from configparser import ConfigParser
from rover_msgs import Nav_Obstacle
from rover_msgs import Obstacle
import crcmod.predefined



def main():
    terabee = Terabee()

    terabee.port.flushInput()
    terabee.start_sensor()
    terabee.close_range()

    depth_array = []


    while(True):
        depth_array = terabee.get_depth_array()
        obs_msg = Nav_Obstacle()
        obs_msg.depths = depth_array
        obs_msg.detected = detect_obstacle(depth_array) #ultrasonic, Sweep
        lcm.publish('/nav_obs', obs_msg.encode())
        try:
            for i in range(len(depth_array)):
                for j in range(0,7):
                    print(depth_array[i][j])
        except KeyboardInterrupt:
            terabee.stop_sensor()
            break


def detect_obstacle(depth_array): #add ults, sweep
    detected = True #In life, there is always an obstacle in front of you,
    #even if you can't see it

    # ultrasonic


    # terabee


    # Servo Sweep
    # if object is i 70 - 110 deg range


    return detected


class Terabee(object):

    def __init__(self):
        lcm = aiolcm.AsyncLCM()

        settings_path = 'C:/Users/adity/Desktop/AJ/School_18-19/MRover/Obstacle Detection/evo_64px_minimal.py_/config.ini'
        #os.environ['MROVER_CONFIG'] + '/config_obs/config.ini']
        config = ConfigParser()
        config.read(settings_path)

    # Configure the serial connections (the parameters differs on the device you are connecting to)
        self.port = serial.Serial(
            port=config['serial']['port'],
            baudrate=(int)(config['serial']['baudrate']),
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.port.isOpen()
        self.crc32 = crcmod.predefined.mkPredefinedCrcFun('crc-32-mpeg')
        self.crc8 = crcmod.predefined.mkPredefinedCrcFun('crc-8')
        self.serial_lock = threading.Lock()

    def get_depth_array(self):
        '''
        This function reads the data from the serial port and returns it as
        an array of 12 bit values with the shape 8x8
        '''
        got_frame = False
        while not got_frame:
            with self.serial_lock:
                frame = self.port.readline()
            if len(frame) == 269:
                if frame[0] == 0x11 and self.crc_check(frame):  # Check for range frame header and crc
                    dec_out = []
                    for i in range(1, 65):
                        rng = frame[2 * i - 1] << 7
                        rng = rng | (frame[2 * i] & 0x7F)
                        dec_out.append(rng & 0x0FFF)
                    depth_array = [dec_out[i:i + 8] for i in range(0, len(dec_out), 8)]
                    depth_array = np.array(depth_array)
                    got_frame = True
            else:
                print ("Invalid frame length: {}".format(len(frame)))

        depth_array.astype(np.uint16)
        return depth_array

    def crc_check(self, frame):
        index = len(frame) - 9  # Start of CRC
        crc_value = (frame[index] & 0x0F) << 28
        crc_value |= (frame[index + 1] & 0x0F) << 24
        crc_value |= (frame[index + 2] & 0x0F) << 20
        crc_value |= (frame[index + 3] & 0x0F) << 16
        crc_value |= (frame[index + 4] & 0x0F) << 12
        crc_value |= (frame[index + 5] & 0x0F) << 8
        crc_value |= (frame[index + 6] & 0x0F) << 4
        crc_value |= (frame[index + 7] & 0x0F)
        crc_value = crc_value & 0xFFFFFFFF
        crc32 = self.crc32(frame[:index])

        if crc32 == crc_value:
            return True
        else:
            print("Discarding current buffer because of bad checksum")
            return False

    def send_command(self, command):
        with self.serial_lock:# This avoid concurrent writes/reads of serial
            self.port.write(command)
            ack = self.port.read(1)
            # This loop discards buffered frames until an ACK header is reached
            while ord(ack) != 20:
                self.port.readline()
                ack = self.port.read(1)
            else:
                ack += self.port.read(3)
            # Check ACK crc8
            crc8 = self.crc8(ack[:3])
            if crc8 == ack[3]:
                # Check if ACK or NACK
                if ack[2] == 0:
                    return True
                else:
                    print("Command not acknowledged")
                    return False
            else:
                print("Error in ACK checksum")
                return False

    def start_sensor(self):
        if self.send_command(b'\x00\x52\x02\x01\xDF'):
            print("Sensor started successfully")

    def stop_sensor(self):
        if self.send_command(b'\x00\x52\x02\x00\xD8'):
            print("Sensor stopped successfully")
    
    def close_range(self): 
        if self.send_command(b'\x00\x21\x01\xBC'):
            print("Sensor in close range")

    def fast_mode(self):
        if self.send_command(b'\x00\x21\x02\xB5'):
            print("Sensor in fast mode")


class TFMini(object):
    def __init__(self):
        mini_serial = serial.Serial("COM3", 115200)

    def get_dist(self):
        input = self.mini_serial.readline().decode("utf-8")
        return int(input[1])
        


if __name__ == '__main__':
    main()

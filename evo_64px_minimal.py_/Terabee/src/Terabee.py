import numpy as np
import serial
import crcmod.predefined
import threading

class Terabee(object):

    def __init__(self):

        #Update this for when we have a config file maybe
        '''    
        #settings_path = os.environ['MROVER_CONFIG'] + '/config_prox/config.ini']
        config = ConfigParser()
        config.read(settings_path)
        '''


        # Configure the serial connections (the parameters differs on the device you are connecting to)
        self.terabee_port = serial.Serial(
            port="COM4",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.terabee_port.isOpen()
        self.terabee_port.crc32 = crcmod.predefined.mkPredefinedCrcFun('crc-32-mpeg')
        self.terabee_port.crc8 = crcmod.predefined.mkPredefinedCrcFun('crc-8')
        self.terabee_port.serial_lock = threading.Lock()

        self.terabee_port.flushInput()

    def get_depth_array(self):
        '''
        This function reads the data from the serial port and returns it as
        an array of 12 bit values with the shape 8x8
        '''
        got_frame = False
        while not got_frame:
            with self.terabee_port.serial_lock:
                frame = self.terabee_port.readline()
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
        crc32 = self.terabee_port.crc32(frame[:index])

        if crc32 == crc_value:
            return True
        else:
            print("Discarding current buffer because of bad checksum")
            return False

    def send_command(self, command):
        with self.terabee_port.serial_lock:# This avoid concurrent writes/reads of serial
            self.terabee_port.write(command)
            ack = self.terabee_port.read(1)
            # This loop discards buffered frames until an ACK header is reached
            while ord(ack) != 20:
                self.terabee_port.readline()
                ack = self.terabee_port.read(1)
            else:
                ack += self.terabee_port.read(3)
            # Check ACK crc8
            crc8 = self.terabee_port.crc8(ack[:3])
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

    def detected(self):
        array = self.get_depth_array()
        detect_count = 0
        for i in range(0,7):
            for j in range(0,7):
                if array[i][j] < 800 and array[i][j] !=1:
                    detect_count +=1
        if detect_count < 25:
            return False
        return True

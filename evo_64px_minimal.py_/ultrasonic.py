import serial
from time import sleep


def normalize_data(reading):  
    if reading > 3000:
        return "N/D"
    elif reading > 250:
        return "Detected at " + str(reading)
    elif reading > 75:
        return "Warning: " + str(reading)
    return "Emergency: " + str(reading)

ults = serial.Serial("COM3", 9600)
counter = 0
while True:
    counter += 1
    input = ults.readline().decode("utf-8").split(" ")
    left = int(input[1])
    right = int(input[3])
    print(normalize_data(left) + "\t" + normalize_data(right))
    

    #print(str(left) + "   " + str(right))
    if counter == 200:
        break














"""import numpy as np
import serial
import threading

class Ultrasonic(object):

    def __init__(self):
        self.portname = "/dev/tty.usbserial"
        self.baudrate = 9600

        self.port = serial.Serial(
            port = self.portname,
            baudrate = self.baudrate
        )
        self.port.isOpen()
        #self.serial_lock = threading.lock()

    def getData(self):
        print(self.port.readline())

if __name__ == "__main__":
    u = Ultrasonic() 
    for i in range(0,1000):
        u.getData()"""
        

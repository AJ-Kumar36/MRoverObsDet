import numpy as np
from serial import Serial

class TFMini(object):
    def __init__(self):
        mini_serial = serial.Serial("COM3", 115200)

    def get_dist(self):
        input = self.mini_serial.readline().decode("utf-8")
        return int(input[1])
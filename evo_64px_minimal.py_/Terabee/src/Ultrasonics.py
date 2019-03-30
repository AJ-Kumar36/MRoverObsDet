import serial

class Ultrasonics(object):
    def __init__(self):
        self.ultrasonic = serial.Serial("COM3", 9600)

    def get_dist(self):
        input = self.ultrasonic.readline().decode("utf-8").split(" ")
        return int(input[1]), int(input[3])
    
    def detected(self, ults1, ults2):
        if ults1 < 200 or ults2 < 200:
            return True
        
import serial
from time import sleep

#class TFMini(object):
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
    input = ults.readline().decode("utf-8")
    dist = int(input[1])
    print(normalize_data(dist))
    

    #print(str(left) + "   " + str(right))
    if counter == 200:
        break



        

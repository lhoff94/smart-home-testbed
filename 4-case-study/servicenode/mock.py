from tabnanny import check
from serial import Serial, STOPBITS_ONE
import time

port = Serial("/dev/ttyUSB2", baudrate=9600, bytesize=8, timeout=10, stopbits=STOPBITS_ONE)

dummy_ppm = 999
dummy_temp = 25

def calc_return_bytes(ppm, temp):
    command = b'\xff\x86'
    result = ppm.to_bytes(2, 'big') + (temp+40).to_bytes(1,'big')
    temp = command + result + b'\x00\x00\x00'
    return temp + checksum(temp)

def checksum(value):
    '''
    The Method calculates the Checksum accordingly with the official documentation
    for the MH-Z19C Sensor. 
    Link to Documentation: 
    https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19c-pins-type-co2-manual-ver1_0.pdf
    Inspired by https://github.com/overflo23/MH-Z19_MicroPython
    
    '''
    array = bytearray(value)
    cs = 0x00
    for i in array:
        cs += i
    cs %= 256
    cs = 0xff - cs
    #cs += 1
    return cs.to_bytes(1, 'big')

test = (calc_return_bytes(dummy_ppm, dummy_temp))
#test = b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'




with port as ser:
    while True:
        x = ser.read(9)

        if x == b'\xff\x01\x86\x00\x00\x00\x00\x00\x79':
            print("worked")
            print(test)
            ser.write(test)

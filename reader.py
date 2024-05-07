import serial
from config import SERIAL_INTERFACE

# This scripts reads an (unprotected) chip

with open('readout', 'wb') as outfile:
    with serial.Serial(SERIAL_INTERFACE, 115200) as ser:
        ser.write(b'r')
        for i in range(32768):
            response = ser.read(1)
            outfile.write(response)
    print("done")

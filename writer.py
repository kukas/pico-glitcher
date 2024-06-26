import serial
from config import SERIAL_INTERFACE

# This script will write a pre-defined pattern to an unlocked microcontroller

with serial.Serial(SERIAL_INTERFACE, 115200) as ser:
    input("Do you really want to write?")
    ser.write(b'b')
    response = ser.read(4)
    print(response)
    print(f"debug locked: {response[2] & (1<<2)}")
    
    ser.write(b'w')
    response = ser.read(2)
    print(response)

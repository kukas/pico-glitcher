import serial
import time
import signal
import sys
import struct
from config import SERIAL_INTERFACE

# This script will wipe the microcontroller, re-enabling the debug interface

with serial.Serial(SERIAL_INTERFACE, 115200) as ser:
    ser.write(b'b')
    response = ser.read(4)
    print(response)
    print(f"debug locked: {response[3] & (1<<2)}")
    
    sure = input("Are you sure you want to wipe the board? (y/n): ")
    if sure != 'y':
        sys.exit(0)

    ser.write(b'p')
    # send the password (defined in main.cpp)
    ser.write(struct.pack('>Q', 0xAABBCCDDEEFF0102))
    # set the delay after reset (in us)
    ser.write(struct.pack('>Q', 1_000_000))
    response = ser.read(1)
    print(response)
    print(f"debug locked: {response[0] & 0x04}")

import serial
from config import SERIAL_INTERFACE
# This script will set the lock bit, enabling readout protection

with serial.Serial(SERIAL_INTERFACE, 115200) as ser:
    ser.write(b'l')
    response = ser.read(1)
    print(response)
    print(f"debug locked: {response[0] & (1<<2)}")

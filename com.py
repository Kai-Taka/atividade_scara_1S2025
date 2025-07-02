import time
import serial

# Ask user for COM port
port = "COM3"  # Default value, can be changed
with serial.Serial(port, baudrate=9600, timeout=5) as ser:
    for i in range(10):
        count = 0
        line = b''
        while line == b'':
            count += 1
            ser.write(f'Hello, ROBOT! test = {i} count = {count}\n'.encode())
            line = ser.readline()
            print(f"{i} - count = {count} - Received: {line}")
        print(f"{i} - count = {count} - Received {count - 1} lines before getting a response.")


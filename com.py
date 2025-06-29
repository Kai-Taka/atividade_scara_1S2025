import time

import serial

# Ask user for COM port
port = input("Enter COM port (e.g., COM3): ")
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

try:
    while True:
        try:
            q1 = input("Enter value for q1 (or 'exit' to quit): ")
            if q1.lower() == 'exit':
                break
            q2 = input("Enter value for q2: ")
            q3 = input("Enter value for q3: ")
            
            # Prepare and send data
            ser.write(f"1 {q1}\n".encode())
            time.sleep(0.05)
            ser.write(f"2 {q2}\n".encode())
            time.sleep(0.05)
            ser.write(f"3 {q3}\n".encode())
            time.sleep(0.05)
            print(f"Sent: 1 {q1}, 2 {q2}, 3 {q3}")
        except Exception as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    print("Serial port closed.")

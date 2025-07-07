import time
import serial
import numpy as np
from CinematicaInversa import CinematicaInversa

def format_angle(angle):
    # Converts radians to degrees and clamps to [0, 180], then formats as 3-digit string
    deg = int(round(np.degrees(angle)))
    deg = max(0, min(180, deg))
    return f"{deg:03d}"

if __name__ == "__main__":
    port = "COM3"  # Default value, can be changed
    ci = CinematicaInversa(caneta_altura=150)
    # Initial position: q1=0, q2=90, q3=90
    last_q1 = 90
    last_q2 = 90
    last_q3 = 90
    initial_cmd = f"{last_q1:03d}{last_q2:03d}{last_q3:03d}"
    with serial.Serial(port, baudrate=9600, timeout=5) as ser:
        # Send initial position once
        while True:
            ser.write((initial_cmd + '\n').encode())
            line = ser.readline()
            if line != b'':
                print(f"Initial position set, received: {line}")
                break
            else:
                print("Waiting for robot to respond to initial position...")
                time.sleep(0.5)
        while True:
            try:
                x = float(input("Value for X coordinate: "))
                y = float(input("Value for Y coordinate: "))
                z = float(input("Value for Z coordinate: "))
            except Exception:
                print("Invalid input. Try again.")
                continue
            q1, q2, q3 = ci.calcular(x, y, z)
            q1_str = format_angle(q1)
            q2_str = format_angle(q2)
            q3_str = format_angle(q3)
            # Step 1: Move q1 only
            cmd1 = f"{q1_str}{last_q2:03d}{last_q3:03d}"
            while True:
                ser.write((cmd1 + '\n').encode())
                line = ser.readline()
                if line != b'':
                    print(f"Moved q1, received: {line}")
                    break
                else:
                    print("Waiting for robot to respond to q1...")
                    time.sleep(0.5)
            time.sleep(1)
            # Step 2: Move q2
            cmd2 = f"{q1_str}{q2_str}{last_q3:03d}"
            while True:
                ser.write((cmd2 + '\n').encode())
                line = ser.readline()
                if line != b'':
                    print(f"Moved q2, received: {line}")
                    break
                else:
                    print("Waiting for robot to respond to q2...")
                    time.sleep(0.5)
            time.sleep(1)
            # Step 3: Move q3
            cmd3 = f"{q1_str}{q2_str}{q3_str}"
            while True:
                ser.write((cmd3 + '\n').encode())
                line = ser.readline()
                if line != b'':
                    print(f"Moved q3, received: {line}")
                    break
                else:
                    print("Waiting for robot to respond to q3...")
                    time.sleep(0.5)
            # Update last positions
            last_q1 = int(q1_str)
            last_q2 = int(q2_str)
            last_q3 = int(q3_str)
            print(f"Position set: {cmd3}")
            print("---")

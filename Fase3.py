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
    ci = CinematicaInversa()
    # Initial position: q1=0, q2=90, q3=90
    last_q1 = 0
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
            q1_des = np.clip(np.degrees(q1), 0, 180)
            q2_des = np.clip(np.degrees(q2), 0, 180)
            q3_des = np.clip(np.degrees(q3), 0, 180)
            q1_cur = last_q1
            q2_cur = last_q2
            q3_cur = last_q3
            # Calculate steps for each joint
            steps_q1 = abs(int(round(q1_des - q1_cur)))
            steps_q2 = abs(int(round(q2_des - q2_cur)))
            steps_q3 = abs(int(round(q3_des - q3_cur)))
            max_steps = max(steps_q1, steps_q2, steps_q3, 1)
            total_time = 1.0
            interval = total_time / max_steps
            for i in range(1, max_steps + 1):
                q1_step = int(round(q1_cur + (q1_des - q1_cur) * i / max_steps))
                q2_step = int(round(q2_cur + (q2_des - q2_cur) * i / max_steps))
                q3_step = int(round(q3_cur + (q3_des - q3_cur) * i / max_steps))
                cmd = f"{q1_step:03d}{q2_step:03d}{q3_step:03d}"
                while True:
                    ser.write((cmd + '\n').encode())
                    line = ser.readline()
                    if line != b'':
                        break
                    else:
                        time.sleep(0.005)
                time.sleep(interval)
            last_q1 = int(round(q1_des))
            last_q2 = int(round(q2_des))
            last_q3 = int(round(q3_des))
            print(f"Position set: {last_q1:03d}{last_q2:03d}{last_q3:03d}")
            print("---")

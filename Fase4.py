import time
import serial
import numpy as np
from CinematicaInversa import CinematicaInversa

def format_angle(angle):
    # Converts radians to degrees and clamps to [0, 180], then formats as 3-digit string
    deg = int(round(np.degrees(angle)))
    deg = max(0, min(180, deg))
    return f"{deg:03d}"

def transform2polar(x, y, z):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    r_base = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    theta = np.arctan2(z, r_base)
    return r, phi, theta

def discretize_line(initial, final, max_size):
    #initial and final are 3D points (x, y, z)
    # Discretizes the line from (0,0,0) to (x,y,z) into max_size segments
    if max_size <= 0:
        return []
    points = []
    r, phi, theta = transform2polar(final[0] - initial[0], final[1] - initial[1], final[2] - initial[2])
    steps = r//10 + 1 #Round up
    print(f"r: {r}, phi: {phi}, theta: {theta}, steps: {steps}")
    for step in range(int(steps)):
        projecao_xy = max_size * step * np.cos(theta)
        #Pos on next step
        next_x = round(initial[0] + projecao_xy * np.cos(phi))
        next_y = round(initial[1] + projecao_xy * np.sin(phi))
        next_z = round(initial[2] + max_size * step * np.sin(theta))
        
        #Do not overshoot
        x = next_x if abs(next_x - final[0]) > 10 else final[0]
        y = next_y if abs(next_y - final[1]) > 10 else final[1]
        z = next_z if abs(next_z - final[2]) > 10 else final[2]
        points.append([x, y, z])

    return points if points[-1] != points[-2] else points[:-1]  # Remove last point if it's a duplicate

if __name__ == "__main__":
    port = "COM3"  # Default value, can be changed
    ci = CinematicaInversa(caneta_altura=-5, erro_sim_real=30)
    # Initial position: q1=0, q2=90, q3=90
    last_q1 = 90
    last_q2 = 90
    last_q3 = 90
    last_x = 0
    last_y = 80
    last_z = 80
    max_size = 10  # Maximum size of each step
    discret_point_interval = 0.01
    total_time = 1  # Total to move all joints in seconds
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
            discretized_points = discretize_line([last_x, last_y, last_z], [x, y, z], 10)
            print(discretized_points)
            input("Press Enter to start moving the robot...")
            for point in discretized_points:
                q1, q2, q3 = ci.calcular(point[0], point[1], point[2])
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
                time.sleep(discret_point_interval)
            last_x, last_y, last_z = x, y, z

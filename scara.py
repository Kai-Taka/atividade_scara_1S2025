import time
import roboticstoolbox as rtb
from spatialmath import SE3
import numpy as np
import matplotlib.pyplot as plt

# Define the links for the RR robot
L1 = rtb.RevoluteDH(a=100)  # First link with length 100
L2 = rtb.RevoluteDH(a=50)   # Second link with length 50

# Create the robot with the defined links
links = [L1, L2]
robot = rtb.DHRobot(links, name='Robo planar')

# Print the robot's DH parameters
print(robot)

# Define the initial configuration
initialPos = [np.pi/4, -np.pi/4]  # First joint at 45 degrees, second at -45 degrees

# Plot the robot with coordinate frames, joint vectors, base frame and end-effector
robot.teach(initialPos)
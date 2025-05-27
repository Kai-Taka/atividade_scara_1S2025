import sympy as sp
import numpy as np

# Define symbolic variables
theta3, theta4 = sp.symbols('theta3 theta4')  # For revolute joints
d1, d5 = sp.symbols('d1 d5')  # For prismatic joints

# Helper function to create the transformation matrix
def create_transformation_matrix(theta, alpha, a, d):
    ct, st = sp.cos(theta), sp.sin(theta)
    ca, sa = sp.cos(alpha), sp.sin(alpha)
    
    return sp.Matrix([
        [ct,    -st * ca,    st * sa,    a * ct],
        [st,     ct * ca,   -ct * sa,    a * st],
        [0,         sa,        ca,         d  ],
        [0,          0,         0,         1  ]
    ])

# Create transformation matrices for each link
# L0: Prismatic (α = π/2, d = 0 fixed)
T0 = create_transformation_matrix(0, sp.pi/2, 0, 0)

# L1: Prismatic (α = -π/2)
T1 = create_transformation_matrix(0, -sp.pi/2, 0, d1)

# L2: Prismatic (d = 27.5 fixed)
T2 = create_transformation_matrix(0, 0, 0, 27.5)

# L3: Revolute (a = 17)
T3 = create_transformation_matrix(theta3, 0, 17, 0)

# L4: Revolute (α = π, a = 11)
T4 = create_transformation_matrix(theta4, sp.pi, 11, 0)

# L5: Prismatic
T5 = create_transformation_matrix(0, 0, 0, d5)

# Initialize pretty printing
sp.init_printing(use_unicode=True)

# Calculate the complete transformation matrix
print("Individual transformation matrices:")
print("\nT0 (Base to Link 0):")
sp.pprint(T0)
print("\nT1 (Link 0 to Link 1):")
sp.pprint(T1)
print("\nT2 (Link 1 to Link 2):")
sp.pprint(T2)
print("\nT3 (Link 2 to Link 3):")
sp.pprint(T3)
print("\nT4 (Link 3 to Link 4):")
sp.pprint(T4)
print("\nT5 (Link 4 to End Effector):")
sp.pprint(T5)

print("\nT5 (Link 0 to End Effector):")

T_total = T0 * T1 * T2 * T3 * T4 * T5
sp.pprint(T_total)

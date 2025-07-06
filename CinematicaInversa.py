import math 
import sympy as sp
import numpy as np
import roboticstoolbox as rtb


#Reduzindo o problema com coordenadas polares
#Resonvendo caso 2D determinando theta e r

x = float(input("Value for X coordinate: "))
y = float(input("Value for Y coordinate: "))
z = float(input("Value for Z coordinate: "))
#Define barras
a1, a2 = sp.symbols('a1 a2')
 
#Define coordenadas polares
r = math.sqrt(x**2 + y**2 + z**2)
r_base = math.sqrt(x**2 + y**2)
phi = math.atan2(y, x)  # Ângulo polar XY
theta = math.atan2(z, r_base)  # Ângulo polar do plano XY para o eixo Z
print(f"Polar coordinates: r = {r:.2f}, phi = {math.degrees(phi):.2f}°, theta = {math.degrees(theta):.2f}°")
#Regra dos cossenos para encontrar os ângulos de um triângulo
def regra_dos_cossenos(a, b, c):
    """
    a, b, c são os comprimentos dos lados do triângulo
    Retorna os ângulos em graus
    """
    alpha_local = sp.acos((b**2 + c**2 - a**2) / (2 * b * c))
    beta_local = sp.acos((a**2 + c**2 - b**2) / (2 * a * c))
    gama_local = sp.acos((a**2 + b**2 - c**2) / (2 * a * b))
    return alpha_local, beta_local, gama_local

alpha, beta, gama = regra_dos_cossenos(a2, a1, r)

#SIMULA ROBO RR
# Calcula valores dos angulos e seta valores do DH
alpha = float(alpha.subs({a1: 8, a2: 8}).evalf())
beta = float(beta.subs({a1: 8, a2: 8}).evalf())
gama = float(gama.subs({a1: 8, a2: 8}).evalf())
print(f"Angles: alpha = {math.degrees(alpha):.2f}°, beta = {math.degrees(beta):.2f}°, gama = {math.degrees(gama):.2f}°")
a1 = 8
a2 = 8

L1 = rtb.RevoluteDH(alpha = np.pi/2)
L2 = rtb.RevoluteDH(a = a1)
L3 = rtb.RevoluteDH(a = a2, offset=np.pi)

links = [L1,L2,L3]
robot = rtb.DHRobot(links, name='Robo articulado')
print(robot)

#Expressões para q1 e q2
q1 = phi
q2 = alpha + theta
q3 = gama

initialPos = [q1, q2, q3]
robot.teach(initialPos)

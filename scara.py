import numpy as np
import roboticstoolbox as rtb

# Define os parâmetros DH para o robô SCARA
L0 = rtb.PrismaticDH(theta = -np.pi/2, alpha = -np.pi/2, qlim=[0, 0]) #Devido ao comportamento da biblioteca será precisao definir um word frame. Uso de DH diferente
L1 = rtb.PrismaticDH(alpha = +np.pi/2, qlim=[0, 30])  # Junta prismática vertical com curso de 0 a 30cm
L2 = rtb.PrismaticDH(theta = np.pi/2, qlim=[27.5, 27.5])# Primeiro elo prismático (0 a 30cm)
L3 = rtb.RevoluteDH(a = 17)    # Primeira junta de rotação do braço com comprimento de 17cm
L4 = rtb.RevoluteDH(alpha = np.pi, a = 11)  # Segunda junta de rotação do braço com comprimento de 11cm
L5 = rtb.PrismaticDH(qlim=[0, 27.5])  # Junta prismática do efetuador final com curso de 0 a 27.5cm

# Cria o robô SCARA com os elos definidos
links = [L0, L1, L2, L3, L4, L5]
robot = rtb.DHRobot(links, name='Robo SCARA')

# Exibe os parâmetros DH do robô
print(robot)

# Define a configuração inicial das juntas do robô
initialPos = [0, 0, 27.5, 0, 0, 0]  # Posição inicial com segunda junta rotacional a 45 graus

# Plota o robô com sistemas de coordenadas, vetores das juntas, base e efetuador final
robot.teach(initialPos)

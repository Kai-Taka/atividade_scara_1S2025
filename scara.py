import numpy as np
import roboticstoolbox as rtb

# Define os elos para o robô RR
L0 = rtb.PrismaticDH(alpha = np.pi/2, qlim=[0, 0]) #Devido ao comportamento da biblioteca será precisao definir um word frame. Uso de DH diferente
L1 = rtb.PrismaticDH(alpha = -np.pi/2, qlim=[0, 30])
L2 = rtb.PrismaticDH(qlim=[27.5, 27.5])# Primeiro elo prismático (0 a 30cm)
L3 = rtb.RevoluteDH(a = 17)    # Segundo elo de rotação
L4 = rtb.RevoluteDH(alpha = np.pi, a = 11)  # Terceiro elo de rotação
L5 = rtb.PrismaticDH(qlim=[0, 20])  # Quarto elo prismático (0 a 20cm)

# Cria o robô com os elos definidos
links = [L0, L1, L2, L3, L4, L5]  # Removido L2, L3 e L4 temporariamente
robot = rtb.DHRobot(links, name='Robo planar')

# Imprime os parâmetros DH do robô
print(robot)

# Define a configuração inicial
initialPos = [0, 0, 27.5, np.pi/4, 0, 0]  # Configuração inicial: junta em 0

# Plota o robô com sistemas de coordenadas, vetores das juntas, base e efetuador final
robot.teach(initialPos)  # frame=True mostra os sistemas de coordenadas de cada elo

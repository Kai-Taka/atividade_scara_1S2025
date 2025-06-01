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


def Cinematica_direta():
    initialPos = [0, 0, 27.5, 0, 0, 0]
    robot.teach(initialPos)


def Cinematica_inversa():
    
        # Define a posição do efetuador final
    x = float(input("Digite a coordenada x do efetuador final: "))
    y = float(input("Digite a coordenada y do efetuador final: "))
    z = float(input("Digite a coordenada z do efetuador final: "))

    #Se posição se encontra dentro do raio do robo
    if (np.sqrt(x**2+y**2) < 28):
        d1 = 0
    else: 
        d1 = x - np.sqrt(28**2-y**2)

    Theta2 = np.arccos(((x-d1)**2 + y**2 - 17**2 - 11**2)/(2*17*11) )  # Calcula o ângulo da segunda junta


    Theta1 = np.arctan2(y, x - d1) - np.arctan2(11 * np.sin(Theta2), 17 + 11 * np.cos(Theta2)) # Calcula o ângulo da primeira junta

    d2 = 27.5 - z  # Calcula a distância da terceira junta prismática ao efetuador final
    # Calcula a posição das juntas do robô

    print("Posição das juntas do robô:")
    print(f"Junta 1 (d1): {d1} cm") 
    print(f"Junta 2 (Theta1): {np.degrees(Theta1)} graus")
    print(f"Junta 3 (Theta2): {np.degrees(Theta2)} graus")
    print(f"Junta 4 (d2): {d2} cm") 

    # Importa a biblioteca necessária para o robô SCARA

    # Define a configuração inicial das juntas do robô
    initialPos = [0, d1, 27.5, Theta1, Theta2, d2]  # Posição inicial com segunda junta rotacional a 45 graus

    # Plota o robô com sistemas de coordenadas, vetores das juntas, base e efetuador final
    robot.teach(initialPos)

if input("Pressione 'i' para calcular a Cinemática Inversa do robô SCARA...") == "i":
    Cinematica_inversa()
else:
    Cinematica_direta()

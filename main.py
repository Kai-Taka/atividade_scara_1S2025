import numpy as np
import roboticstoolbox as rtb

 # Define os parâmetros DH para o robô SCARA
L1 = rtb.RevoluteDH(a = 0, d = 15.93 , alpha=np.pi/2)    
L2 = rtb.RevoluteDH(d = 52.3, a=80)  
L3 = rtb.RevoluteDH(d=-22, a=80, offset=np.pi)  # Junta prismática do efetuador final com curso de 0 a 27.5cm

""" L1 = rtb.RevoluteDH( d= 15.93 , alpha=np.pi/2)    # Primeira junta de rotação do braço com comprimento de 17cm
L2 = rtb.RevoluteDH( a=80)  # Segunda junta de rotação do braço com comprimento de 11cm
L3 = rtb.RevoluteDH( a=80)  # Junta prismática do efetuador final com curso de 0 a 27.5cm """



links = [L1,L2,L3]
robot = rtb.DHRobot(links, name='Robo articulado')

# Exibe os parâmetros DH do robô
print(robot)


def Cinematica_direta():
    initialPos = [0.13255153229667402, 1.5301586728222558, 1.1724175158799934]
    robot.teach(initialPos)

print(robot.jacob0([0, 0, 0]))

Cinematica_direta() 


""" def Cinematica_inversa():
    
        # Define a posição do efetuador final
    x = float(input("Digite a coordenada x do efetuador final: "))
    y = float(input("Digite a coordenada y do efetuador final: "))
    z = float(input("Digite a coordenada z do efetuador final: "))

    if (28>np.sqrt(x**2+y**2)):
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
    #initialPos = [0, 0, 27.5, 0, 0, 0] 

    # Plota o robô com sistemas de coordenadas, vetores das juntas, base e efetuador final
    robot.teach(initialPos)

if(input("Pressione i para calcular a Cinemática Inversa do robô SCARA...") == "i"):
    Cinematica_inversa() 
else:
    Cinematica_direta() """
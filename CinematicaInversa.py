"""
Cinematica Inversa para um robo articulado com
mecanismo de barra paralela
"""
import numpy as np
import roboticstoolbox as rtb

class CinematicaInversa:
    """
    Classe para calcular a cinemática inversa de um robô articulado com
    Recebe erros para compensar posição do EE
    """
    def __init__(self, link_1=80, link_2=80, erro_sim_real=30, caneta_altura=0):
        self.link_1 = link_1
        self.link_2 = link_2
        self.erro_sim_real = erro_sim_real
        self.caneta_altura = caneta_altura
        L1 = rtb.RevoluteDH(alpha = np.pi/2)
        L2 = rtb.RevoluteDH(a = self.link_1)
        L3 = rtb.RevoluteDH(a = self.link_2, offset=np.pi)
        self.links = [L1, L2, L3]
        self.robot = rtb.DHRobot(self.links, name='Robo articulado')
        
        

    def regra_dos_cossenos(self, a, b, c):
        """
        Calcula os ângulos de um triângulo usando a regra dos cossenos.
        a = link_2
        b = link_1
        c = r (distância do ponto ao centro do robô)
        """
        alpha_local = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
        beta_local = np.arccos((a**2 + c**2 - b**2) / (2 * a * c))
        gama_local = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))
        return alpha_local, beta_local, gama_local

    def calcular(self, x, y, z):
        """        
        Calcula a cinemática inversa do robô para as coordenadas (x, y, z).
        """
        y = y + self.caneta_altura
        r = np.sqrt(x**2 + y**2 + z**2)
        r_base = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        theta = np.arctan2(z, r_base)
        print(f"Polar coordinates: r = {r:.2f}, phi = {np.degrees(phi):.2f}°, theta = {np.degrees(theta):.2f}°")
        alpha, beta, gama = self.regra_dos_cossenos(self.link_2, self.link_1, r)
        print(f"Angles: alpha = {np.degrees(alpha):.2f}°, beta = {np.degrees(beta):.2f}°, gama = {np.degrees(gama):.2f}°")
        
        q1 = phi + (np.arctan2(self.erro_sim_real, r_base)) #Trig para compensar erro do EE
        q2 = alpha + theta
        q3 = gama
        print("q1:", np.degrees(q1), "q2:", np.degrees(q2), "q3:", np.degrees(q3))
        return [q1, q2, q3]

if __name__ == "__main__":
    x = float(input("Value for X coordinate: "))
    y = float(input("Value for Y coordinate: "))
    z = float(input("Value for Z coordinate: "))
    ci = CinematicaInversa()
    result = ci.calcular(x, y, z)
    ci.robot.teach(result)


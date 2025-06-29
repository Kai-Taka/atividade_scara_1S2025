import sympy as sp

# Inicializa o 'pretty printing' para uma visualização matemática mais agradável no console
sp.init_printing(use_unicode=True)


q1, q2, q3 = sp.symbols('q1 q2 q3')


# Elo 1: theta é a variável q1
dh_params_1 = (q1, 15.93, 0, sp.pi/2)
# Elo 2: theta é a variável q2
dh_params_2 = (q2, 52.3, 80, 0)
# Elo 3: theta é a variável q3
dh_params_3 = (q3, -22, 80, 0)


def dh_transformation_matrix(theta, d, a, alpha):

    A = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)*sp.cos(alpha),  sp.sin(theta)*sp.sin(alpha), a*sp.cos(theta)],
        [sp.sin(theta),  sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha), a*sp.sin(theta)],
        [0,             sp.sin(alpha),               sp.cos(alpha),              d              ],
        [0,             0,                           0,                          1              ]
    ])
    return A


A1 = dh_transformation_matrix(*dh_params_1)
A2 = dh_transformation_matrix(*dh_params_2)
A3 = dh_transformation_matrix(*dh_params_3)

# Transformações da base (0) até cada junta (i)
T01 = A1
T02 = T01 * A2
T03 = T02 * A3  # Esta é a matriz de cinemática direta do efetuador final

print("="*50)
print("Matriz de Cinemática Direta (T03):")
sp.pprint(T03)
print("="*50)


# Vetores de posição (p) e eixos z de cada sistema de coordenadas
p0 = sp.Matrix([0, 0, 0])
p1 = T01[:3, 3]
p2 = T02[:3, 3]
pn = T03[:3, 3] # Posição do efetuador final

z0 = sp.Matrix([0, 0, 1])
z1 = T01[:3, 2]
z2 = T02[:3, 2]


Jv1 = z0.cross(pn - p0)
Jw1 = z0
J1 = Jv1.col_join(Jw1)

# Coluna para a junta 2
Jv2 = z1.cross(pn - p1)
Jw2 = z1
J2 = Jv2.col_join(Jw2)

# Coluna para a junta 3
Jv3 = z2.cross(pn - p2)
Jw3 = z2
J3 = Jv3.col_join(Jw3)

# Monta a matriz Jacobiana J
J = sp.Matrix.hstack(J1, J2, J3)

# Simplificar as expressões trigonométricas para um resultado mais limpo
J_simplified = sp.simplify(J)

print("\n" + "="*50)
print("Matriz Jacobiana Simbólica (J):")
sp.pprint(J_simplified)
print("="*50)


# SymPy pode converter essas expressões diretamente para código C,


# from sympy.utilities.codegen import codegen
# from sympy.printing import ccode

# print("\n" + "="*50)
# print("Código C para os elementos da Matriz Jacobiana:")
# for i in range(J_simplified.rows):
#     for j in range(J_simplified.cols):
#         # Imprime no formato 'J[i][j] = ...;'
#         print(f"J[{i}][{j}] = {ccode(J_simplified[i,j])};")
# print("="*50)
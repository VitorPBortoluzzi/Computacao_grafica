import numpy as np
import matplotlib.pyplot as plt
# Função para calcular a translação dos pontos
def translacao(pontos, Tx, Ty):
  pontos_transladados = []
  for ponto in pontos:
    x_u = ponto[0] + Tx
    y_u = ponto[1] + Ty
    pontos_transladados.append((x_u, y_u))
  return pontos_transladados


# -------------------------
def escalar(pontos,k):
  pontos_escalados = []
  for ponto in pontos:
    x_u = ponto[0] * k
    y_u = ponto[1] * k
    pontos_escalados.append((x_u, y_u))
  return pontos_escalados
# ________________________

def rotacao(pontos, angulo):
  pontos_rotacionados = []
  angulo_rad = np.radians(angulo)
  for ponto in pontos:
    x0, y0 = ponto # Obtém as coordenadas do ponto
    # Calcular as coordenadas após a rotação
    xu = round(x0 * np.cos(angulo_rad) - y0 * np.sin(angulo_rad), 2)
    yu = round(x0 * np.sin(angulo_rad) + y0 * np.cos(angulo_rad), 2)
    pontos_rotacionados.append((xu, yu)) # Adiciona o ponto rotacionado à lista
  return pontos_rotacionados



# Pontos originais - Translação
p1 = (6, 8)
p2 = (4, 5)
p3 = (8, 5)
# Vetor de translação
Tx = 3
Ty = -4

# Calcular a translação dos pontos
pontos_transladados = translacao([p1, p2, p3], Tx, Ty)
# Plotar os pontos originais e os pontos transladados
plt.plot ( [p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], 'ro-', label='Pontos originais') 
# Plotar os pontos transladados da mesma forma
# Pegando o X do primeiro [0][0] e o X do segundo [1][0]
lista_x = [ pontos_transladados[0][0], pontos_transladados[1][0], pontos_transladados[2][0], pontos_transladados[0][0] ]
# Pegando o Y do primeiro [0][1] e o Y do segundo [1][1]
lista_y = [ pontos_transladados[0][1], pontos_transladados[1][1], pontos_transladados[2][1], pontos_transladados[0][1] ]
plt.plot(lista_x, lista_y, 'ro-', label='Pontos transladados')

#------------------
# Pontos originais - Escalação
e_p1 = (1, 1)
e_p2 = (1, 3)
e_p3 = (3, 3)
e_p4 = (3, 1)

# Valor do escalar:

k = 5
# Calcular o escalar dos pontos
pontos_escalados = escalar([e_p1, e_p2, e_p3, e_p4],k)
# Plotar os pontos originais e os pontos Escalados
plt.plot ( [e_p1[0], e_p2[0], e_p3[0], e_p4[0], e_p1[0]], [e_p1[1], e_p2[1], e_p3[1],e_p4[1], e_p1[1]], 'go-', label='Pontos originais') 

lista_ex = [ pontos_escalados[0][0], pontos_escalados[1][0],pontos_escalados[2][0],pontos_escalados[3][0], pontos_escalados[0][0] ]
lista_ey = [ pontos_escalados[0][1], pontos_escalados[1][1],pontos_escalados[2][1],pontos_escalados[3][1], pontos_escalados[0][1] ]
plt.plot(lista_ex, lista_ey, 'go-', label='Pontos escalados')

# ------------------

# Pontos Originais Rotação:
r_p1 = (10, 10)
r_p2 = (12,12)

#Angulo da rotação em Graus
angulo = 90

# Calcular a rotação dos pontos
pontos_rotacionados = rotacao([r_p1, r_p2], angulo)
# Plotar os pontos
plt.plot( [r_p1[0],r_p2[1]],[r_p1[1],r_p2[1]],'bo-', label='Pontos originais')
plt.plot([p[0] for p in pontos_rotacionados], [p[1] for p in pontos_rotacionados], 'yo-', label='Pontos rotacionados') # Plota os pontos rotacionados em vermelho


plt.xlim(-15, 30) # Define o limite do eixo X de 0 a 10
plt.ylim(-15, 30) # Define o limite do eixo Y de 0 a 10
# Configurações do gráfico
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Translação & Escalação de pontos no plano cartesiano')
plt.grid(True)
plt.legend()
# Mostrar o gráfico
plt.show()
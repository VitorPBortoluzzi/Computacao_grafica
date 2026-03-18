#Biliotecas
import matplotlib.pyplot as plt
# Coordenadas dos pontos P1 e P2
P1x = 2
P1y = 1
P2x = 7
P2y = 3
# Inicialização das listas para armazenar os pontos da reta
points_x = []
points_y = []
#reta vertical
if P1x == P2x:
    print("Reta vertical")
    y = P1y
    while y<=P2y:
        #imprime os pontos na tela
        #print(P1x,",",y)
        #adiciona os pontos na lista para gerar o gráfico
        points_x.append(P1x)
        points_y.append(y)
        y+=1
else:
    # Cálculo do coeficiente angular (m) e coeficiente linear (b)
    m = (P2y - P1y)/(P2x - P1x)
    b = P1y - m*P1x
    #reta mais deitada
if m <= 1: #angulo <= 45º
    print("Reta mais deitada")
    x = P1x
    while x <= P2x:
        #equacao reduzida da reta
        y = round(m*x + b)
        #imprime os pontos na tela
        #print(x,",",y)
        #adiciona os pontos na lista para gerar o gráfico
        points_x.append(x)
        points_y.append(y)
        x+=1
        #reta mais de pé
elif m > 1: #angulo > 45º
    print("Reta mais de pé")
    y = P1y
    while y <= P2y:
        x = round((y-b)/m)
        #imprime os pontos na tela
        #print(x,",",y)
        #adiciona os pontos na lista para gerar o gráfico
        points_x.append(x)
        points_y.append(y)
        y+=1

# Imprimir os pontos da reta
print("\n Pontos da reta:")
for i in range(len(points_x)):
    print(points_x[i], ",", points_y[i])
    
# Gerar o gráfico
plt.plot(points_x, points_y, marker='o',
linestyle='-', color='b')
plt.title('Rasterização de Linha')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(True)
plt.show()
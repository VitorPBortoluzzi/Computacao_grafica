#Matriz * escalar
import numpy as np
Matriz = np.array([[2,3,8],[6,0,4],[1,5,7]])

linhas = Matriz.shape[0]
colunas= Matriz.shape[1]

resultado = np.zeros((linhas,colunas))

escalar = 3

if linhas != colunas:
  print("Operação inválida")
else: 
  for i in range(linhas):
    for j in range(colunas):
      resultado[i][j] = Matriz[i][j] * escalar

print(resultado)
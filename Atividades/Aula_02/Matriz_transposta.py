#Matriz Transposta
import numpy as np
Matriz = np.array([[2,3,8],[6,0,4],[1,5,7]])

linhas = Matriz.shape[0]
colunas= Matriz.shape[1]

Matriz_T = np.zeros((linhas,colunas))

if linhas != colunas:
  print("Operação inválida")
else: 
  for i in range(linhas):
    for j in range(colunas):
      Matriz_T[j][i] = Matriz[i][j]


print("Matriz\n",Matriz)
print("\nMatriz Transposta\n",Matriz_T)
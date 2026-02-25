# Matriz identidade: 
import numpy as np
Matriz = np.array([[1,0,0],[0,1,0],[0,0,1]])

linhas = Matriz.shape[0]
colunas= Matriz.shape[1]

eh_identidade = True

if linhas != colunas:
  print("Operação inválida")
else: 
  for i in range(linhas):
    for j in range(colunas):
      if (i == j and Matriz[i][j] != 1) or (i != j and Matriz[i][j] != 0):
        eh_identidade = False


print("É Identidade:",eh_identidade)
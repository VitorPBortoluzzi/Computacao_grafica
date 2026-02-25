# Matriz Diagonal
import numpy as np
Matriz = np.array([[2,0,0],[0,1,0],[0,0,7]])

linhas = Matriz.shape[0]
colunas= Matriz.shape[1]

eh_diagonal = True

if linhas != colunas:
  print("Operação inválida")
else: 
  for i in range(linhas):
    for j in range(colunas):
      if i != j and Matriz[i][j] != 0:
        eh_diagonal = False

print("É diagonal:",eh_diagonal)
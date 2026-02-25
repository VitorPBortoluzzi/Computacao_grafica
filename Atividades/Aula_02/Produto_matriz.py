# #Produto de 2 Matrizes

# mA = [
#     [1,3,2],
#     [4,7,6]
#     ]
# mB = [
#     [2,8],
#     [3,1],
#     [5,7]
#     ]

# def multiplicador(mA,mB):
#   resultado = []

#   for i in range(len(mA)):
#     linha = []
#     for j in range(len(mB[0])):
#       soma = 0
#       for k in range(len(mB)):
#         soma += mA[i][k] * mB[k][j]
#       linha.append(soma)
#     resultado.append(linha)
    
#   return resultado


# print(multiplicador(mA,mB))



import numpy as np

#Define a matriz A:
A = np.array([[1,3,2],[4,7,6]])
B = np.array([[2,8],[3,1],[5,7]])

print("Matriz A:")
print(A)
print("\nMatriz B:")
print(B)

linhas_A = A.shape[0]
colunas_A = A.shape[1]
linhas_B = B.shape[0]
colunas_B = B.shape[1]
resultado = []

resultado = np.zeros((linhas_A, colunas_B))

if colunas_A != linhas_B:
  print("Operação inválida")
else: 
  for i in range(linhas_A):
    for j in range (colunas_B):
      soma = 0
      for k in range(colunas_A):
        soma += A[i][k] * B[k][j]
      resultado[i][j] = soma


  print("\nResultado: ")
  print(resultado)


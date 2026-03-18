import numpy as np

# 1. Definir o Ponto P (-2, 4, 1, 1)
# Em computação gráfica, usamos vetores coluna para multiplicação de matrizes
P = np.array([[-2],
              [ 4],
              [ 1],
              [ 1]])

# 2. Definir os fatores de translação
tx, ty, tz = 5, 2, 3

# 3. Montar a Matriz de Translação 4x4 (Mt)
# Iniciamos com uma matriz identidade e preenchemos a quarta coluna
Mt = np.array([[1, 0, 0, tx],
               [0, 1, 0, ty],
               [0, 0, 1, tz],
               [0, 0, 0,  1]])

# 4. Realizar o cálculo: P' = Mt * P
P_linha = np.dot(Mt, P)

# pegar linha e coluna
linhas, colunas = P_linha.shape

# --- Exibição dos resultados no terminal ---
print("Matriz de Translação (Mt):")
print(Mt)
print("\nPonto Original (P):")
print(P)
print("\nCálculo: Mt multiplicado por P...")
print("\nNovo Ponto Transladado (P'):")
print(P_linha)

print("IMPRIMINDO ELEMENTO POR ELEMENTO DA MATRIZ RESULTADO:")
for i in range(linhas):
    for j in range(colunas):
        elemento = P_linha[i, j]
        print(f"Linha {i}, Coluna {j} -> Valor: {elemento}")
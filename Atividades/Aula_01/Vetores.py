import math

def calcularTamanho(x,y,z):
  tam = math.sqrt(x*x + y*y + z*z)
  return tam

print("Exercicio 01 - Computação gráfica")
print("\n Digite os valores do vetor")
x = float(input("Digite o valor de x"))
y = float(input("Digite o valor de y"))
z = float(input("Digite o valor de z"))

def menu():
    print("\n--- MENU ---")
    print("1. Calcular o tamanho do vetor")
    print("2. Normalizar o vetor")
    print("3. Adicionar outro vetor")
    print("4. Subtrair outro vetor")
    print("5. Multiplicar por escalar")
    print("6. Dividir por escalar")
    print("7. Produto escalar")
    print("8. Terminar")

while True:
  menu()
  op = input("Escolha a operação: ")

  if op == '1':
    print("\n Calcular o tamanho do Vetor")
    print("Tamanho do vetor: ", calcularTamanho(x,y,z))

  elif op == '2':
    tamanho = calcularTamanho(x,y,z)
    if tamanho == 0:
      print("Não é possivel normalizar um vetor nulo")
    else:
      nx = x / tamanho
      ny = y / tamanho
      nz = z / tamanho
      print ("Vetor normalizado:( ",nx,",",ny,",",nz,")" )

  elif op == '3':
    print("\n DIGITE OS VALORES DO VETOR 02")
    x2 = float(input("Digite o valor de x2"))
    y2 = float(input("Digite o valor de y2"))
    z2 = float(input("Digite o valor de z2"))
    print("A soma dos vetores é = ",x+x2, ",",y+y2,",",z+z2)
    print("----------------------------\n")

  elif op == '4' :
    print("\n DIGITE OS VALORES DO VETOR 02")
    x2 = float(input("Digite o valor de x2"))
    y2 = float(input("Digite o valor de y2"))
    z2 = float(input("Digite o valor de z2"))
    print("A soma dos vetores é = ",x-x2, ",",y-y2,",",z-z2)
    print("----------------------------\n")

  elif op == '5':
    escalar = float(input("Digite o escalar"))
    print("\n a multiplicação por escalar é: ", x*escalar, ",", y*escalar,",",z*escalar)

  elif op == '6':
    escalar = float(input("Digite o escalar"))
    print("\n a Divisão por escalar é: ", round(x/escalar,2), ",", round(y/escalar,2),",",round(z/escalar,2))

  elif op == '7':
    print("\n DIGITE OS VALORES DO VETOR 02")
    x2 = float(input("Digite o valor de x2"))
    y2 = float(input("Digite o valor de y2"))
    z2 = float(input("Digite o valor de z2"))
    produtoEscalar =  x * x2 + y * y2 + z * z2
    print("Produto escalar: ",produtoEscalar)

  elif op == '8':
    break

  else:
    print("Opção inválida")
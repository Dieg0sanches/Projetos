#Exercicio 5 - Listas

#Faça uma rotina que leia um vetor de 10 números reais e mostre-os na ordem inversa.

numeros = []

for i in range(10):
    num = float(input(f"Digite o {i+1}º número: "))
    numeros.append(num)

print("Números na ordem inversa:")
for num in reversed(numeros):
    print(num)
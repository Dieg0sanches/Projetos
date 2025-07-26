# Exercicio 8 - Strings

# Faça um programa que permita ao usuário digitar o seu nome e em seguida mostre o nome do usuário de trás para frente
# utilizando somente letras maiúsculas. 

nome = input("Digite seu nome: ")
nome_invertido = nome[::-1].upper()
print(f"Seu nome de trás para frente em maiúsculas é: {nome_invertido}")
# Além disso, informe quantas letras tem o nome (desconsiderando espaços).
quantidade_letras = len(nome.replace(" ", ""))
print(f"Seu nome tem {quantidade_letras} letras (desconsiderando espaços).")

# Exercicio 2 - Condicional

# Faça um programa que lê as duas notas parciais obtidas por um aluno numa disciplina ao longo de um semestre, e calcule a sua média. A atribuição de conceitos obedece à tabela abaixo:

# Média de Aproveitamento
# *   A - Entre 9.0 e 10.0        
# *   B - Entre 7.5 e 9.0
# *   C - Entre 6.0 e 7.5
# *   D - Entre 4.0 e 6.0
# *   E - Entre 4.0 e zero

media = float(input("Digite a média do aluno: "))
if 9 <= media <= 10:
    print("A")
elif 7 <= media < 9:
    print("B")
elif 5 <= media < 7:
    print("C")
elif 3 <= media < 5:
    print("D")
elif 0 <= media < 3:
    print("E")
else:
    print("F")
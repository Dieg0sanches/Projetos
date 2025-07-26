
#Exercicio 1 - Entrada de dados e atribuições

#Faça um script que pergunte quanto você ganha por hora e o número de horas trabalhadas no mês. Calcule e mostre o total do seu salário no referido mês, sabendo-se que são descontados 11% para o Imposto de Renda, 8% para o INSS e 5% para o sindicato, faça um programa que nos dê:
#salário bruto.
#quanto pagou ao INSS.
#quanto pagou ao sindicato.
#o salário líquido.
#calcule os descontos e o salário líquido, conforme a tabela abaixo:
#+ Salário Bruto : RS
#- IR (11%) : RS
#- INSS (8%) : RS
#- Sindicato (5%) : RS
#= Salário Liquido : RS

#Obs.: Salário Bruto - Descontos = Salário Líquido.!

salario_bruto = 2800.00
imposto_de_renda = salario_bruto * 0.11
desconto_inss = salario_bruto * 0.08
desconto_sindicato = salario_bruto * 0.05
salario_liquido = salario_bruto - (imposto_de_renda + desconto_inss + desconto_sindicato)
salario_bruto = 2800.00
imposto_de_renda = salario_bruto * 0.11
desconto_inss = salario_bruto * 0.08
desconto_sindicato = salario_bruto * 0.05
salario_liquido = salario_bruto - (imposto_de_renda + desconto_inss + desconto_sindicato)

print(f"Salário bruto: R$ {salario_bruto:.2f}")
print(f"Imposto de renda (11%): R$ {imposto_de_renda:.2f}")
print(f"Desconto INSS (8%): R$ {desconto_inss:.2f}")
print(f"Desconto sindicato (5%): R$ {desconto_sindicato:.2f}")
print(f"Salário líquido: R$ {salario_liquido:.2f}")


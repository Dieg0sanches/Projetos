# Exercicio 7 - Funções

# Faça um programa com uma função chamada somaImposto. A função possui dois parâmetros de entrada: taxaImpostoVendas, que é a quantia de imposto sobre vendas expressa em porcentagem e custo, 
# que é o custo de um item antes do imposto. A função retorna o valor de custo incluindo o imposto sobre vendas.

def somaImposto(taxaImpostoVendas, custo):
    return custo + (custo * taxaImpostoVendas / 100)

# Execução interativa:

taxa = float(input("Digite a taxa de imposto sobre vendas (%): "))
custo = float(input("Digite o custo do item: "))
valor_final = somaImposto(taxa, custo)
print(f"Valor final com imposto: {valor_final}")


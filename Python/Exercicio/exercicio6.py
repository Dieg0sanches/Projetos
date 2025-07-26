# Exercicio 6 - Listas

# Faça uma rotina que leia os dados de um cliente até que o usuário digite "fim" e os imprima na tela
# cliente = ["Fernanda", "Montenegro", 1929, "Central do Brasil", 1998, "Atriz", "Rio de Janeiro, RJ"]
# cliente.append("Brasil")

cliente = ["Fernanda", "Montenegro", 1929, "Central do Brasil", 1998, "Atriz", "Rio de Janeiro, RJ"]
while True:
    dado = input("Digite um dado do cliente (ou 'fim' para encerrar): ")
    if dado.lower() == "fim":
        break
    cliente.append(dado)
print("Dados do cliente:")
for item in cliente:
    print(item)

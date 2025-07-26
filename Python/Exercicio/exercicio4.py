# Exercicio 4 - Loop While

# Faça uma rotina que leia um nome de usuário e a sua senha e não aceite a senha igual ao nome do usuário, mostrando uma mensagem de erro e voltando a pedir as informações.

usuario = input("Digite o nome de usuário: ")
senha = input("Digite a senha: ")

while senha == usuario:
    print("Erro: a senha não pode ser igual ao nome de usuário. Tente novamente.")
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

print("Usuário e senha cadastrados com sucesso!")

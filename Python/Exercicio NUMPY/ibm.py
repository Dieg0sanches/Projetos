

# Complete the 'getUniqueCharacter' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def getUniqueCharacter(s):
    # Retorna o índice do primeiro caractere único, ou -1 se não houver
    from collections import Counter
    count = Counter(s)
    return next((idx for idx, char in enumerate(s) if count[char] == 1), -1)

if __name__ == '__main__':
    # Exemplo de uso
    s = input('Digite uma string: ')
    idx = getUniqueCharacter(s)
    print(f'O índice do primeiro caractere único é: {idx}')
    nome_jogo = input('Digite o nome do jogo: ')
    print(f'Você escolheu o jogo: {nome_jogo}')
    
    


#as part of a firewall log analysis. a team needs a list of all the client´s mac adress, whihch was active and has traffic (its clients.id) existis in the traffic table
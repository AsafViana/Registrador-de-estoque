def criptografar(mensagem = str):
    chave = 3
    # tamanho tabela ASCII
    n = 128

    cifrada = list(mensagem)
    i = 0
    # você pode usar a string 'mensagem' ou a lista 'cifrada' no FOR
    for letra in mensagem:
        # achar no alfabeto a letra que esteja chave posições a frente
        indice = ord(letra)
        # substituir na mensagem a letra pela nova_letra
        cifrada[i] = chr((indice + chave) % n)
        i = i + 1

    # converte a lista em string novamente
    cifrada = "".join(cifrada)
    return cifrada


def descriptografar(mensagem):
    chave = -3
    # tamanho tabela ASCII
    n = 128

    cifrada = list(mensagem)
    i = 0
    # você pode usar a string 'mensagem' ou a lista 'cifrada' no FOR
    for letra in mensagem:
        # achar no alfabeto a letra que esteja chave posições a frente
        indice = ord(letra)
        # substituir na mensagem a letra pela nova_letra
        cifrada[i] = chr((indice + chave) % n)
        i = i + 1

    # converte a lista em string novamente
    cifrada = "".join(cifrada)
    return cifrada[:-1]


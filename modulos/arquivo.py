def arquivo_existe(nome):
    try:
        a = open(nome, 'rt')
    except FileNotFoundError:
        return False
    else:
        return True


def pasta_existe(dir=str):
    try:
        a = open(dir.nome)
    except:
        return False
    else:
        return True


def criar_arquivo(nome):
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('\033[31mFalha na criação do arquivo!\033[m')
    else:
        print(f'\033[32mArquivo {nome} criado com sucesso!\033[m')


def ler_arquivo(nome):
    try:
        a = open(nome, 'rt')

    except:
        print('\033[32mErro ao ler o arquivo!\033[m')
    finally:
        a.close()

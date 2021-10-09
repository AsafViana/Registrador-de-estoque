from os import *
from time import *
from getpass import getpass
from sqlite3 import *
from modulos.arquivo import *
#==========================================================

arquivo = arquivo_existe('tela de login.db')
print('Conectando a o servidor...')
sleep(1)
system('cls')
banco = connect('tela de login.db')
cursor = banco.cursor()

if arquivo == False:
    try:
        if arquivo == False:
            # criando a tabela login_senha
            cursor.execute('CREATE TABLE Login_senha (usuario text,senha text)')
            print(colored("Banco de dados criado com sucesso!!!", 'green'))
    except:
        fonte_cor_texto('isometric2', 'red', 'ERRO')
        print(colored('NÃO FOI POSSIVEL CRIAR E/OU INICIAR O BANCO DE DADOS', 'red'))

cursor.execute("SELECT * FROM login_senha")
bd = cursor.fetchall()
#==========================================================

def erros_user(parametro1, parametro2, mensagem_erro, mensagem_opção):
    while parametro1 not in parametro2:
        system('cls')
        print(colored(mensagem_erro, 'red'))
        opc = input(mensagem_opção + ''' [s/n]
>''')
        while opc not in 'sn':
            system('cls')
            print(colored('Opção invalida.', 'red'))
            erros_user(parametro1, parametro2, mensagem_erro, mensagem_opção)

    return opc

def login():
    system('cls')
    cabeçalho('ENTRAR')
    usuario = input(colored('Usuario: ', 'yellow'))
    senha = getpass(colored('Senha: ', 'yellow'))
    gabarito = usuario, senha


    while gabarito not in bd:
        system('cls')
        print(colored('Login ou senha incorreta', 'red'))
        opc = input('''Deseja sair? [s/n]
>''')
        while opc not in 'sn':
            system('cls')
            print(colored('Digite um opção valida.', 'red'))
            opc = input('''Deseja sair? [s/n]
>''')
        if opc == 's':
            system('cls')
            sistema()
        else:
            system('cls')
            login()
    system('cls')
    print('Entrou')
    fonte_cor_texto('starwars', 'yellow', '''STAR
WARS''')

    input('')

def cadastro():
    cabeçalho('CADASTRAR')
    usuario = input(colored('Usuario: ', 'yellow'))
    senha1 = getpass(colored('Senha: ', 'yellow'))
    senha2 = getpass(colored('Confirme a senha: ', 'yellow'))
    while senha1 != senha2:
        system('cls')
        print(colored('Senhas incorretas.', 'red'))
        cadastro()
    else:
        try:
            cursor.execute("INSERT INTO login_senha VALUES('"+usuario+"', '"+senha1+"')")
            banco.commit()
        except:
            system('cls')
            fonte_cor_texto('isometric2', 'red', 'ERRO')
            print('Não foi possivel registrar.')
    system('cls')
    print(colored('REGISTRADO', 'green'))
    sistema()

def sistema():
    menu1 = menu('LOGIN', ['Entrar', 'Cadastrar', 'Sair'])

    #corrigindo possiveis erros do usuario
    while menu1 not in '123':
        system('cls')
        print(colored('Alternativa incorreta.', 'red'))
        sistema()
    #seleção das opçoes
    if menu1 == '1':
        login()
    elif menu1 == '2':
        system('cls')
        cadastro()
    else:
        print('Desligando...')
        sleep(2)
        exit()

# ===========================================================


sistema()
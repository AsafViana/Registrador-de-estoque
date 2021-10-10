from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
import os

dir = os.path.dirname(os.path.realpath(__file__))
tirar = dir.find('configurações')
dir = dir[:tirar]
cred = credentials.Certificate(dir + r"s\credenciais\registro-de-estoque.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://registro-de-estoque-default-rtdb.firebaseio.com/'})


refstoque = db.reference('estoque')
refusuario = db.reference('usuarios')


def adicionar(lista=list, loja: str = '', produto: str = 'Nada'):
    loja = refstoque.child(loja)
    produto = loja.child(produto)
    produto.update(lista)


def atualizar_nome(nome_antigo=str,novo_nome=str, loja=str, backup=dict):

    item_antigo = refstoque.child(loja + '/' + nome_antigo)
    item_antigo.delete()
    adicionar(loja=loja, produto=novo_nome, lista=backup)


def atualizar(loja=str, novos_dados=dict, linha=int):
    produtos = list(refstoque.child(loja).get())

    backup = refstoque.child(loja + '/' + produtos[linha]).get()
    backup['nome'] = produtos[linha]

    tag_dados = ['nome', 'categoria', 'codigo', 'preço']
    relação = {}

    for c in range(0, len(tag_dados)):
        if backup[tag_dados[c]] == novos_dados[tag_dados[c]]:
            relação[tag_dados[c]] = True
        else:
            relação[tag_dados[c]] = False
    print(relação)

    if relação['nome'] == False:
        backup.pop('nome')
        atualizar_nome(produtos[linha],novos_dados['nome'], loja, backup)
        atualizar(loja, novos_dados, linha)

    else:
        nome_do_produto = novos_dados['nome']
        relação, backup, novos_dados.pop('nome')
        tag_dados.remove('nome')
        for x in range(0, len(tag_dados)):
            if relação[tag_dados[x]] == False:
                mais = refstoque.child(loja+'/'+nome_do_produto)
                mais.update({tag_dados[x]: novos_dados[tag_dados[x]]})
            else:
                pass

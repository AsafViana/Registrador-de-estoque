from modulos.fire import *
from pyautogui import alert, confirm
from PyQt5 import uic, QtWidgets, QtGui
from os import system

dire = os.path.dirname(os.path.realpath(__file__))
tirar = dire.find('modulos')
dire = dire[:tirar]


# =======================================================

def guardar_loja(loja):
    url = dire + 'modulos\credenciais\loja.txt'
    system('NUL> ' + url)
    with open(url, 'w') as arquivo:
        arquivo.write(loja)


def receber_loja():
    url = dire + 'modulos\credenciais\loja.txt'
    with open(url, 'r') as arquivo:
        loja = arquivo.read()
    print(loja)
    return loja


def enviarCripto(dados):
    tags = ['usuario', 'senha']
    novos_dados = dados
    # print(novos_dados)
    with open('modulos\credenciais\conta_salva.txt', 'w') as arquivo:
        for c in range(0, 2):
            # print(dados[tags[c]])
            if dados_local != dados:
                arquivo.write(novos_dados[tags[c]] + '\n')
            else:
                pass


def recebercripto():
    tag = ['usuario', 'senha']
    credenciais = {}
    with open(dire + 'modulos\credenciais\conta_salva.txt', 'r') as arquivo:
        c = 0
        for x in arquivo:
            credenciais[tag[c]] = x
            c += 1
    return credenciais
# ======================================================

usuarios = refusuario.get()
dados_local = recebercripto()


def logar():
    usuario = login.usuario.text()
    senha_tela = login.senha.text()
    usuarios_lista = list(usuarios.keys())
    usuarios_lista.append(usuario)

    if usuario in usuarios_lista:
        dados_banco = usuarios[usuario]
        senha_banco = dados_banco['senha']
        loja = dados_banco['loja']
        if senha_banco != senha_tela:
            alert('Senha incorreta')

        else:  # cadastro deu certo
            alert(f'Bem vindo de volta, {usuario[0].upper() + usuario[1:].lower()}')
            enviarCripto({'usuario': usuario, 'senha': senha_banco})

            if loja not in list(refstoque.get()):
                resposta = confirm('Vi que sua loja não foi registrada. Deseja regidtrar sua loja?',
                                   title='Loja não encontrada', buttons=['SIM', 'NÃO'])
                if resposta == 'SIM':
                    alert('Preencha o formulario a seguir:')
                    cadastrar_tela()

        enviarCripto({'usuario': usuario, 'senha': senha_banco, })
        formulario_tela.show()
        guardar_loja(loja)
        chama_segunda_tela()
        login.close()

    else:
        alert('Usuario incorreto')


def cadastrar_produto():
    item = {'codigo': int(formulario.codigo.text()), 'preço': float(formulario.preco.text()), 'categoria': ''}
    produto = formulario.produto.text()

    if formulario.eletronicos.isChecked():
        # print("Categoria Eletronicos selecionada")
        item['categoria'] = "Informatica"

    elif formulario.alimentos.isChecked():
        # print("Categoria Alimentos selecionada")
        item['categoria'] = "Alimentos"

    else:
        # print("Categoria Eletronicos selecionada")
        item['categoria'] = "Eletronicos"

    try:
        nome_loja = loja_mercadoria_e_parametros_endereço()[0]
        adicionar(
            lista=item,
            loja=nome_loja,
            produto=produto
        )

    except:
        alert('Algo deu errado!!!')
    else:
        alert('Produto cadastrado com sucesso')
    formulario.codigo.setText("")
    formulario.produto.setText("")
    formulario.preco.setText("")


def chama_segunda_tela():
    # definindo o tamanho das colunas
    formulario_tela.tabela.setColumnWidth(2, 150)
    formulario_tela.tabela.setColumnWidth(0, 167)
    formulario_tela.tabela.setColumnWidth(3, 130)
    formulario_tela.tabela.setColumnWidth(1, 170)
    formulario.close()
    formulario_tela.show()
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    endereço = loja_mercadoria_e_parametros_endereço()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endereço()[2]

    formulario_tela.tabela.setRowCount(len(mercadoria_lista))

    try:
        for x in range(0, len(mercadoria_lista[1])):
            formulario_tela.tabela.setItem(x, 0, QtWidgets.QTableWidgetItem(mercadoria_lista[x]))
            i = endereço.child(mercadoria_lista[x])
            informações_produtos = i.get()
            informações_produtos_lista = list(informações_produtos.keys())

            for c in range(0, 3):
                if parametros_nomes[0] == informações_produtos_lista[c]:  # categoria
                    formulario_tela.tabela.setItem(x, 1, QtWidgets.QTableWidgetItem(informações_produtos['categoria']))

                elif informações_produtos_lista[c] == parametros_nomes[1]:  # codigo
                    formulario_tela.tabela.setItem(x, 2,
                                                   QtWidgets.QTableWidgetItem(str(informações_produtos['codigo'])))

                elif informações_produtos_lista[c] == parametros_nomes[2]:  # preço
                    formulario_tela.tabela.setItem(x, 3, QtWidgets.QTableWidgetItem(str(informações_produtos['preço'])))

    except:
        alert('Algo deu errado.')


def inicial():
    formulario_tela.close()
    formulario.show()


def excluir():
    # pegando a posição da linha
    linha = formulario_tela.tabela.currentRow()

    # apagando as linhas no banco e na interface
    endereço = loja_mercadoria_e_parametros_endereço()[3]
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    formulario_tela.tabela.removeRow(linha)
    endereço.child(mercadoria_lista[linha]).delete()


def pdf():
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    estoque_nome = list(mercadoria_lista.get())
    dados_lidos = []

    for c in range(0, len(estoque_nome)):
        tudo = {'nome': estoque_nome[c]}
        parametros = mercadoria_lista.child(estoque_nome[c]).get()

        for informações in parametros:
            tudo[informações] = parametros[informações]
        dados_lidos.append(list(tudo.values()))
    # print(dados_lidos)
    alert("PDF FOI GERADO COM SUCESSO!")


def abrir_editar():
    tela_editar.show()
    formulario_tela.close()


def editar_dados():
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    endereço = loja_mercadoria_e_parametros_endereço()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endereço()[2]
    abrir_editar()

    linha = formulario_tela.tabela.currentRow()

    produto = mercadoria_lista[linha]
    estoque = endereço.get()

    tela_editar.codigo.setText(str(estoque[produto][parametros_nomes[1]]))
    tela_editar.produto.setText(produto)
    tela_editar.preco.setText(str(estoque[produto][parametros_nomes[2]]))
    tela_editar.categoria.setText(str(estoque[produto][parametros_nomes[0]]))


def salvar_valor_editado():
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    endereço = loja_mercadoria_e_parametros_endereço()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endereço()[2]
    loja = loja_mercadoria_e_parametros_endereço()[0]
    linha = formulario_tela.tabela.currentRow()

    # ler dados do lineEdit
    codigo = tela_editar.codigo.text()
    produto = tela_editar.produto.text()
    preço = tela_editar.preco.text()
    tipo = tela_editar.categoria.text()
    dados_recebidos = {
        'nome': produto,
        'categoria': tipo,
        'codigo': int(codigo),
        'preço': float(preço)
    }

    # atualizar os dados no banco
    atualizar(loja, dados_recebidos, linha)

    # atualizar as janelas
    tela_editar.close()
    formulario_tela.show()


enviarCripto(usuarios['asaf'])


def cadastrar_tela():
    cadastrar.show()
    login.close()


def cadastro():
    senha1 = cadastrar.senha.text()
    senha2 = cadastrar.confirmar_senha.text()
    while senha1 != senha2:
        alert('Senhas diferentes')
        cadastrar.confirmar_senha.setText('')
        cadastrar.senha.setText('')
    dados = {
        'email': cadastrar.email.text(),
        'loja': cadastrar.loja.text(),
        'senha': senha2,
        'usuario': cadastrar.usuario.text().lower()
    }

    enviarCripto(dados)

    try:
        banco = refusuario.child(dados['usuario'])
        banco.update(dados)
    except:
        alert('Erro ao cadastrar')
    else:
        alert('Cadastro feito com sucesso!!!')

    login.show()
    cadastrar.close()


dados_local = recebercripto()
# ============================================

def loja_mercadoria_e_parametros_endereço():
    loja = receber_loja()
    try:
        endereço = refstoque.child(loja)
        mercadoria = list(endereço.get())
        parametros_nomes = ['categoria', 'codigo', 'preço']
        return loja, mercadoria, parametros_nomes, endereço

    except:
        pass
# ======================================================

app = QtWidgets.QApplication([])
formulario = uic.loadUi("telas/formulario.ui")
formulario_tela = uic.loadUi("telas/listar_dados.ui")
tela_editar = uic.loadUi("telas/menu_editar.ui")
login = uic.loadUi("telas/login.ui")
cadastrar = uic.loadUi("telas/cadastrar_login.ui")

formulario_tela.setWindowIcon(QtGui.QIcon(r'modulos\icon\registro.png'))
formulario.setWindowIcon(QtGui.QIcon(r'modulos\icon\registro.png'))
tela_editar.setWindowIcon(QtGui.QIcon(r'modulos\icon\registro.png'))
login.setWindowIcon(QtGui.QIcon(r'modulos\icon\registro.png'))
cadastrar.setWindowIcon(QtGui.QIcon(r'modulos\icon\registro.png'))

from modulos.fire import *
from pyautogui import alert, confirm
from PyQt5 import uic, QtWidgets, QtGui
from os import system
from modulos.criptografia import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
from modulos.arquivo import *

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
    return loja


def enviarCripto(dados):
    tags = ['usuario', 'senha']
    novos_dados = dados
    arquivo = dire + 'modulos\credenciais\conta_salva.txt'
    result = arquivo_existe(arquivo)
    if result == False: criar_arquivo(arquivo)

    with open(arquivo, 'w') as arquivo:
        for c in range(0, 2):
            # print(dados[tags[c]])
            if dados_local != dados:
                arquivo.write(criptografar(novos_dados[tags[c]]) + '\n')
            else:
                pass


def recebercripto():
    tag = ['usuario', 'senha']
    arquivo = dire + 'modulos\credenciais\conta_salva.txt'
    result = arquivo_existe(arquivo)
    if result == False: criar_arquivo(arquivo)

    credenciais = {}
    with open(arquivo, 'r') as arquivo:
        c = 0
        for x in arquivo:
            credenciais[tag[c]] = descriptografar(x)
            c += 1
    return credenciais


# ======================================================

usuarios = refusuario.get()
dados_local = recebercripto()


def logar():
    usuario = login.usuario.text()
    senha_tela = login.senha.text()
    usuarios_lista = list(usuarios.keys())

    if usuario in usuarios_lista:
        dados_banco = usuarios[usuario]
        senha_banco = dados_banco['senha']
        loja = dados_banco['loja']
        if senha_banco != senha_tela:
            alert('Senha incorreta')

        else:  # cadastro deu certo
            alert(f'Bem vindo de volta, {usuario[0].upper() + usuario[1:].lower()}')

            if loja not in list(refstoque.get()):
                enviarCripto({'usuario': usuario, 'senha': senha_banco, })
                formulario.show()
                guardar_loja(loja)
                login.close()

            else:
                enviarCripto({'usuario': usuario, 'senha': senha_banco, })
                formulario_tela.show()
                guardar_loja(loja)
                chama_segunda_tela()
                login.close()

    else:
        alert('Usuario incorreto')


def cadastrar_produto():
    formulario.quantidade.setPrefix('UNI: ')
    item = {'codigo': int(formulario.codigo.value()), 'pre??o': float(formulario.preco.value()), 'categoria': '',
            'quantidade': formulario.quantidade.value()}
    produto = formulario.produto.text()
    print(produto, item)

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
        nome_loja = receber_loja()
        adicionar(
            lista=item,
            loja=nome_loja,
            produto_nome=produto
        )

    except:
        alert('Algo deu errado!!!')
    else:
        alert('Produto cadastrado com sucesso')
    formulario.codigo.setValue(0)
    formulario.produto.setText("")
    formulario.preco.setValue(0)
    formulario.quantidade.setValue(0)


def chama_segunda_tela():
    # definindo o tamanho das colunas
    formulario_tela.tabela.setColumnWidth(2, 120)
    formulario_tela.tabela.setColumnWidth(0, 167)
    formulario_tela.tabela.setColumnWidth(3, 100)
    formulario_tela.tabela.setColumnWidth(1, 170)
    formulario_tela.tabela.setColumnWidth(4, 150)
    formulario.close()
    formulario_tela.show()

    try:
        endere??o = loja_mercadoria_e_parametros_endere??o()[3]
        mercadoria_lista = loja_mercadoria_e_parametros_endere??o()[1]
        parametros_nomes = loja_mercadoria_e_parametros_endere??o()[2]

        formulario_tela.tabela.setRowCount(len(mercadoria_lista))
        try:
            for x in range(0, len(mercadoria_lista)):
                formulario_tela.tabela.setItem(x, 0, QtWidgets.QTableWidgetItem(mercadoria_lista[x]))
                i = endere??o.child(mercadoria_lista[x])
                informa????es_produtos = i.get()
                informa????es_produtos_lista = list(informa????es_produtos.keys())

                for y in range(0, 4):
                    if parametros_nomes[0] == informa????es_produtos_lista[y]:  # categoria
                        formulario_tela.tabela.setItem(x, 1,
                                                       QtWidgets.QTableWidgetItem(informa????es_produtos['categoria']))

                    elif informa????es_produtos_lista[y] == parametros_nomes[1]:  # codigo
                        formulario_tela.tabela.setItem(x, 2,
                                                       QtWidgets.QTableWidgetItem(str(informa????es_produtos['codigo'])))

                    elif informa????es_produtos_lista[y] == parametros_nomes[2]:  # pre??o
                        formulario_tela.tabela.setItem(x, 3,
                                                       QtWidgets.QTableWidgetItem(str(informa????es_produtos['pre??o'])))

                    elif informa????es_produtos_lista[y] == parametros_nomes[3]:  # Quantidade
                        formulario_tela.tabela.setItem(x, 4,
                                                       QtWidgets.QTableWidgetItem(
                                                           str(informa????es_produtos['quantidade'])))

        except:
            alert('Algo deu errado.')
    except:
        alert('Seu estoque est?? vazio.')


def inicial():
    formulario_tela.close()
    formulario.show()


def excluir():
    # pegando a posi????o da linha
    linha = formulario_tela.tabela.currentRow()

    # apagando as linhas no banco e na interface
    endere??o = loja_mercadoria_e_parametros_endere??o()[3]
    mercadoria_lista = loja_mercadoria_e_parametros_endere??o()[1]
    formulario_tela.tabela.removeRow(linha)
    endere??o.child(mercadoria_lista[linha]).delete()

    # recarregar telas
    itens = endere??o.get()
    print(itens)

    if itens == None:
        alert('N??o h?? nada no seu estoque.')


def pdf():
    pasta = str(QtWidgets.QFileDialog.getExistingDirectory(formulario_tela, "Select Directory"))
    if pasta == '':
        pass
    else:
        loja = receber_loja()
        endere??o = refstoque.child(loja)
        dados_lidos = endere??o.get()
        produtos = list(dados_lidos)

        y = 0
        pdf = canvas.Canvas(pasta + f"/Relat??rio do estoque de {loja} ({date.today()}).pdf", pagesize=A4)
        pdf.setFont("Times-Bold", 25)
        pdf.drawString(200, 800, "Produtos cadastrados:")
        pdf.setFont("Times-Bold", 18)

        pdf.drawString(20, 750, "PRODUTO")
        pdf.drawString(130, 750, "CATEGORIA")
        pdf.drawString(260, 750, "CODIGO")
        pdf.drawString(354, 750, "PRE??O")
        pdf.drawString(440, 750, "QUANTIDADE")
        y = y + 50

        for h in range(0, len(dados_lidos.keys())):
            y = y + 50
            pdf.drawString(20, 750 - y, produtos[h])
            pdf.drawString(130, 750 - y, str(dados_lidos[produtos[h]]['categoria']))
            pdf.drawString(260, 750 - y, str(dados_lidos[produtos[h]]['codigo']))
            pdf.drawString(354, 750 - y, str(dados_lidos[produtos[h]]['pre??o']))
            pdf.drawString(450, 750 - y, str(dados_lidos[produtos[h]]['quantidade']))

        pdf.save()
        alert("PDF FOI GERADO COM SUCESSO!")


def abrir_editar():
    tela_editar.show()
    formulario_tela.close()


def editar_dados():
    mercadoria_lista = loja_mercadoria_e_parametros_endere??o()[1]
    endere??o = loja_mercadoria_e_parametros_endere??o()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endere??o()[2]
    abrir_editar()

    linha = formulario_tela.tabela.currentRow()

    produto = mercadoria_lista[linha]
    estoque = endere??o.get()

    tela_editar.codigo.setText(str(estoque[produto][parametros_nomes[1]]))
    tela_editar.produto.setText(produto)
    tela_editar.preco.setText(str(estoque[produto][parametros_nomes[2]]))
    tela_editar.categoria.setText(str(estoque[produto][parametros_nomes[0]]))


def salvar_valor_editado():
    mercadoria_lista = loja_mercadoria_e_parametros_endere??o()[1]
    endere??o = loja_mercadoria_e_parametros_endere??o()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endere??o()[2]
    loja = loja_mercadoria_e_parametros_endere??o()[0]
    linha = formulario_tela.tabela.currentRow()

    # ler dados do lineEdit
    codigo = tela_editar.codigo.text()
    produto = tela_editar.produto.text()
    pre??o = tela_editar.preco.text()
    tipo = tela_editar.categoria.text()
    dados_recebidos = {
        'nome': produto,
        'categoria': tipo,
        'codigo': int(codigo),
        'pre??o': float(pre??o)
    }

    # atualizar os dados no banco
    atualizar(loja, dados_recebidos, linha)

    # atualizar as janelas
    tela_editar.close()
    chama_segunda_tela()


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


def voltar():
    login.show()
    cadastrar.close()


def recarregar():
    formulario_tela.close()
    chama_segunda_tela()


def mais():
    loja, mercadoria, parametros_tag, endere??o = loja_mercadoria_e_parametros_endere??o()
    linha = formulario_tela.tabela.currentRow()
    endere??o = refstoque.child(loja)
    item = endere??o.child(mercadoria[linha])
    informa????es = item.get()

    soma = informa????es['quantidade'] + 1
    print()
    adicionar(
        lista={'quantidade': soma},
        loja=loja,
        produto_nome=mercadoria[linha]
    )

    formulario_tela.tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(soma)))


def menos():
    loja, mercadoria, parametros_tag, endere??o = loja_mercadoria_e_parametros_endere??o()
    linha = formulario_tela.tabela.currentRow()
    endere??o = refstoque.child(loja)
    item = endere??o.child(mercadoria[linha])
    informa????es = item.get()

    subtra????o = informa????es['quantidade'] - 1
    print()
    adicionar(
        lista={'quantidade': subtra????o},
        loja=loja,
        produto_nome=mercadoria[linha]
    )

    formulario_tela.tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(subtra????o)))


# ============================================

def loja_mercadoria_e_parametros_endere??o():
    loja = receber_loja()
    try:
        endere??o = refstoque.child(loja)
        mercadoria = list(endere??o.get())
        parametros_nomes = ['categoria', 'codigo', 'pre??o', 'quantidade']
        return loja, mercadoria, parametros_nomes, endere??o

    except:
        pass


# ======================================================

app = QtWidgets.QApplication([])
formulario = uic.loadUi(dire + r"modulos/telas/formulario.ui")
formulario_tela = uic.loadUi(dire + r"modulos/telas/listar_dados.ui")
tela_editar = uic.loadUi(dire + r"modulos/telas/menu_editar.ui")
login = uic.loadUi(dire + r"modulos/telas/login.ui")
cadastrar = uic.loadUi(dire + r"modulos/telas/cadastrar_login.ui")

formulario_tela.setWindowIcon(QtGui.QIcon(dire + r'modulos\icon\registro.png'))
formulario.setWindowIcon(QtGui.QIcon(dire + r'modulos\icon\registro.png'))
tela_editar.setWindowIcon(QtGui.QIcon(dire + r'modulos\icon\registro.png'))
login.setWindowIcon(QtGui.QIcon(dire + r'modulos\icon\registro.png'))
cadastrar.setWindowIcon(QtGui.QIcon(dire + r'modulos\icon\registro.png'))

formulario.quantidade.setPrefix('UNI: ')
formulario.preco.setPrefix('R$ ')
formulario.preco.setMaximum(999999999)
formulario.quantidade.setMaximum(999999999)
formulario.codigo.setMaximum(999999999)

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
    item = {'codigo': int(formulario.codigo.value()), 'preço': float(formulario.preco.value()), 'categoria': '',
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
    mercadoria_lista = loja_mercadoria_e_parametros_endereço()[1]
    endereço = loja_mercadoria_e_parametros_endereço()[3]
    parametros_nomes = loja_mercadoria_e_parametros_endereço()[2]

    formulario_tela.tabela.setRowCount(len(mercadoria_lista))
    try:
        for x in range(0, len(mercadoria_lista)):
            formulario_tela.tabela.setItem(x, 0, QtWidgets.QTableWidgetItem(mercadoria_lista[x]))
            i = endereço.child(mercadoria_lista[x])
            informações_produtos = i.get()
            informações_produtos_lista = list(informações_produtos.keys())

            for y in range(0, 4):
                if parametros_nomes[0] == informações_produtos_lista[y]:  # categoria
                    formulario_tela.tabela.setItem(x, 1, QtWidgets.QTableWidgetItem(informações_produtos['categoria']))

                elif informações_produtos_lista[y] == parametros_nomes[1]:  # codigo
                    formulario_tela.tabela.setItem(x, 2,
                                                   QtWidgets.QTableWidgetItem(str(informações_produtos['codigo'])))

                elif informações_produtos_lista[y] == parametros_nomes[2]:  # preço
                    formulario_tela.tabela.setItem(x, 3, QtWidgets.QTableWidgetItem(str(informações_produtos['preço'])))

                elif informações_produtos_lista[y] == parametros_nomes[3]:  # Quantidade
                    formulario_tela.tabela.setItem(x, 4,
                                                   QtWidgets.QTableWidgetItem(str(informações_produtos['quantidade'])))

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
    pasta = str(QtWidgets.QFileDialog.getExistingDirectory(formulario_tela, "Select Directory"))
    if pasta == '':
        pass
    else:
        loja = receber_loja()
        endereço = refstoque.child(loja)
        dados_lidos = endereço.get()
        produtos = list(dados_lidos)

        y = 0
        pdf = canvas.Canvas(pasta + f"/Relatório do estoque de {loja} ({date.today()}).pdf", pagesize=A4)
        pdf.setFont("Times-Bold", 25)
        pdf.drawString(200, 800, "Produtos cadastrados:")
        pdf.setFont("Times-Bold", 18)

        pdf.drawString(20, 750, "PRODUTO")
        pdf.drawString(130, 750, "CATEGORIA")
        pdf.drawString(260, 750, "CODIGO")
        pdf.drawString(354, 750, "PREÇO")
        pdf.drawString(440, 750, "QUANTIDADE")
        y = y + 50

        for h in range(0, len(dados_lidos.keys())):
            y = y + 50
            pdf.drawString(20, 750 - y, produtos[h])
            pdf.drawString(130, 750 - y, str(dados_lidos[produtos[h]]['categoria']))
            pdf.drawString(260, 750 - y, str(dados_lidos[produtos[h]]['codigo']))
            pdf.drawString(354, 750 - y, str(dados_lidos[produtos[h]]['preço']))
            pdf.drawString(450, 750 - y, str(dados_lidos[produtos[h]]['quantidade']))

        pdf.save()
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
    pass


def recarregar():
    formulario_tela.close()
    chama_segunda_tela()


def mais():
    loja, mercadoria, parametros_tag, endereço = loja_mercadoria_e_parametros_endereço()
    linha = formulario_tela.tabela.currentRow()
    endereço = refstoque.child(loja)
    item = endereço.child(mercadoria[linha])
    informações = item.get()

    soma = informações['quantidade'] + 1
    print()
    adicionar(
        lista={'quantidade': soma},
        loja=loja,
        produto_nome=mercadoria[linha]
    )

    formulario_tela.tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(soma)))


def menos():
    loja, mercadoria, parametros_tag, endereço = loja_mercadoria_e_parametros_endereço()
    linha = formulario_tela.tabela.currentRow()
    endereço = refstoque.child(loja)
    item = endereço.child(mercadoria[linha])
    informações = item.get()

    subtração = informações['quantidade'] - 1
    print()
    adicionar(
        lista={'quantidade': subtração},
        loja=loja,
        produto_nome=mercadoria[linha]
    )

    formulario_tela.tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(subtração)))


# ============================================

def loja_mercadoria_e_parametros_endereço():
    loja = receber_loja()
    try:
        endereço = refstoque.child(loja)
        mercadoria = list(endereço.get())
        parametros_nomes = ['categoria', 'codigo', 'preço', 'quantidade']
        return loja, mercadoria, parametros_nomes, endereço

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

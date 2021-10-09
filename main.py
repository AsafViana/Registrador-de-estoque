from reportlab.pdfgen import canvas
from modulos.fire import *
from modulos.arquivo import arquivo_existe, criar_arquivo
from modulos.criptografia import criptografar, descriptografar
import os
from pyautogui import alert, confirm
from PyQt5 import uic, QtWidgets, QtGui


usuarios = refusuario.get()

dir = os.path.dirname(os.path.realpath(__file__))
tirar = dir.find('modulo')
dir = dir[:tirar]

conta = dir + r'2\modulos\login\credenciais\conta_salva.txt'
arquivo = arquivo_existe(conta)
if arquivo == False: criar_arquivo(conta)
# =================================================================

try:
    endereço = refstoque.child(loja)
    mercadoria_lista = list(endereço.get())
    parametros_nomes = ['categoria', 'codigo', 'preço']

except:
    pass


loja = ''
def recebercripto():
    tag = ['usuario', 'senha']
    credenciais = {}
    with open(conta, 'r') as arquivo:
        c = 0
        for x in arquivo:
            credenciais[tag[c]] = x
            c += 1
    return credenciais


def logar():
    usuario = login.usuario.text()
    senha_tela = login.senha.text()
    usuarios_lista = list(usuarios.keys())
    usuarios_lista.append(usuario)
    print(usuario in usuarios_lista)

    if usuario in list(usuarios.keys()):
        dados_banco = usuarios[usuario]
        senha_banco = dados_banco['senha']
        print(dados_banco, senha_banco)
        loja = dados_banco['loja']
        if senha_banco != senha_tela:
            alert('Senha incorreta')

        else:  # cadastro deu certo
            alert(f'Bem vindo de volta, {usuario[0].upper() + usuario[1:].lower()}')
            informações = usuarios[usuario]
            enviarCripto({'usuario': usuario, 'senha': senha_banco})

            if loja not in list(refstoque.get()):
                resposta = confirm('Vi que sua loja não foi registrada. Deseja regidtrar sua loja?',
                                   title='Loja não encontrada', buttons=['SIM', 'NÃO'])
                if resposta == 'SIM':
                    alert('Preencha o formulario a seguir:')
                    cadastrar_tela()

            enviarCripto({'usuario': usuario, 'senha': senha_banco,})
            formulario_tela.show()
            chama_segunda_tela()
            login.close()



    else:
        alert('Usuario incorreto')


def cadastrar_produto():
    item = {'codigo': int(formulario.codigo.text()), 'preço': float(formulario.preco.text()), 'categoria': ''}
    produto = formulario.produto.text()

    if formulario.eletronicos.isChecked():
        #print("Categoria Eletronicos selecionada")
        item['categoria'] = "Informatica"

    elif formulario.alimentos.isChecked():
        #print("Categoria Alimentos selecionada")
        item['categoria'] = "Alimentos"

    else:
        #print("Categoria Eletronicos selecionada")
        item['categoria'] = "Eletronicos"

    try:
        adicionar(
            lista=item,
            loja=loja,
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


    formulario_tela.tabela.setRowCount(len(mercadoria_lista))

    try:
        for x in range(0, len(mercadoria_lista)):
            formulario_tela.tabela.setItem(x, 0, QtWidgets.QTableWidgetItem(mercadoria_lista[x]))
            i = endereço.child(mercadoria_lista[x])
            informações_produtos = i.get()
            informações_produtos_lista = list(informações_produtos.keys())
            #print(informações_produtos, informações_produtos_lista)

            for c in range(0, 3):
                if parametros_nomes[0] == informações_produtos_lista[c]:  # categoria
                    formulario_tela.tabela.setItem(x, 1, QtWidgets.QTableWidgetItem(informações_produtos['categoria']))
                    #print(informações_produtos['categoria'])

                elif informações_produtos_lista[c] == parametros_nomes[1]:  # codigo
                    formulario_tela.tabela.setItem(x, 2,
                                                   QtWidgets.QTableWidgetItem(str(informações_produtos['codigo'])))
                    #print(str(informações_produtos['codigo']))

                elif informações_produtos_lista[c] == parametros_nomes[2]:  # preço
                    formulario_tela.tabela.setItem(x, 3, QtWidgets.QTableWidgetItem(str(informações_produtos['preço'])))
                    #print(str(informações_produtos['preço']))

    except:
        alert('Algo deu errado.')


def inicial():
    formulario_tela.close()
    formulario.show()


def excluir():
    # pegando a posição da linha
    linha = formulario_tela.tabela.currentRow()

    # apagando as linhas no banco e na interface
    formulario_tela.tabela.removeRow(linha)
    endereço.child(mercadoria_lista[linha]).delete()


def pdf():
    estoque_nome = list(mercadoria_lista.get())
    dados_lidos = []

    for c in range(0, len(estoque_nome)):
        tudo = {'nome': estoque_nome[c]}
        parametros = mercadoria_lista.child(estoque_nome[c]).get()

        for informações in parametros:
            tudo[informações] = parametros[informações]
        dados_lidos.append(list(tudo.values()))
    #print(dados_lidos)
    alert("PDF FOI GERADO COM SUCESSO!")


def abrir_editar():
    tela_editar.show()
    formulario_tela.close()


def editar_dados():
    abrir_editar()

    linha = formulario_tela.tabela.currentRow()

    produto = mercadoria_lista[linha]
    estoque = endereço.get()

    tela_editar.codigo.setText(str(estoque[produto][parametros_nomes[1]]))
    tela_editar.produto.setText(produto)
    tela_editar.preco.setText(str(estoque[produto][parametros_nomes[2]]))
    tela_editar.categoria.setText(str(estoque[produto][parametros_nomes[0]]))


def salvar_valor_editado():
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


dados_local = recebercripto()
#print(dados_local)

def enviarCripto(dados):
    tags = ['usuario', 'senha']
    novos_dados = dados
    #print(novos_dados)
    with open('modulos\login\credenciais\conta_salva.txt', 'w') as arquivo:
        for c in range(0, 2):
            #print(dados[tags[c]])
            if dados_local != dados:
                arquivo.write(novos_dados[tags[c]] + '\n')
            else:
                pass


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
# ==================================================================================


app = QtWidgets.QApplication([])
formulario = uic.loadUi("telas/formulario.ui")
formulario_tela = uic.loadUi("telas/listar_dados.ui")
tela_editar = uic.loadUi("telas/menu_editar.ui")
login = uic.loadUi("telas/login.ui")
cadastrar = uic.loadUi("telas/cadastrar_login.ui")


dados = recebercripto()
try:
    login.usuario.setText(dados['usuario'])
    login.senha.setText(dados['senha'])
except AttributeError:
    pass

formulario.enviar.clicked.connect(cadastrar_produto)
formulario.listar.clicked.connect(chama_segunda_tela)
formulario_tela.add.clicked.connect(inicial)
formulario_tela.excluir.clicked.connect(excluir)
formulario_tela.pdf.clicked.connect(pdf)
formulario_tela.editar.clicked.connect(editar_dados)
tela_editar.salvar.clicked.connect(salvar_valor_editado)
login.entrar.clicked.connect(logar)
login.cadastrar.clicked.connect(cadastrar_tela)
cadastrar.cadastrar.clicked.connect(cadastro)





formulario_tela.show()
chama_segunda_tela()
app.exec()

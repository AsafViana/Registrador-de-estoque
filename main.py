from modulos.telas_funções import *


usuarios = refusuario.get()
# =================================================================

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

from modulos.telas_funções import *


try:
    usuarios = refusuario.get()
    dados = recebercripto()
    login.usuario.setText(dados['usuario'][:-1])
    login.senha.setText(dados['senha'][:-1])
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
# ======================================================

login.show()
app.exec()
exit()

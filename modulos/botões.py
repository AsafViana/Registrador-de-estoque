from modulos.telas_funções import *


try:
    usuarios = refusuario.get()
    dados = recebercripto()
    login.usuario.setText(dados['usuario'][:-1])
    login.senha.setText(dados['senha'][:-1])
except AttributeError:
    pass
except KeyError:
    pass

formulario.enviar.clicked.connect(cadastrar_produto)
formulario.listar.clicked.connect(chama_segunda_tela)
formulario_tela.mais.clicked.connect(mais)
formulario_tela.menos.clicked.connect(menos)
formulario_tela.add.clicked.connect(inicial)
formulario_tela.recarregar.clicked.connect(recarregar)
formulario_tela.excluir.clicked.connect(excluir)
formulario_tela.pdf.clicked.connect(pdf)
formulario_tela.editar.clicked.connect(editar_dados)
tela_editar.salvar.clicked.connect(salvar_valor_editado)
login.entrar.clicked.connect(logar)
login.cadastrar.clicked.connect(cadastrar_tela)
cadastrar.cadastrar.clicked.connect(cadastro)
cadastrar.voltar.clicked.connect(voltar)
feedback_tela.enviar.clicked.connect(feedback)
feedback_tela2.enviar.clicked.connect(feedback_inicio)
login.actionFeedback.triggered.connect(feedback_abrir2)
cadastrar.actionFeedback.triggered.connect(feedback_abrir)
formulario.actionFeedback.triggered.connect(feedback_abrir)
formulario_tela.actionFeedback.triggered.connect(feedback_abrir)
tela_editar.actionFeedback.triggered.connect(feedback_abrir)



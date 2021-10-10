import os
from modulos.arquivo import arquivo_existe, criar_arquivo

dire = os.path.dirname(os.path.realpath(__file__))
tirar = dire.find('modulos')
dire = dire[:tirar]

conta = dire + r'2\modulos\login\credenciais\conta_salva.txt'
arquivo = arquivo_existe(conta)
if arquivo == False: criar_arquivo(conta)

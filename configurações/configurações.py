import firebase_admin
from firebase_admin import credentials
import os

dir = os.path.dirname(os.path.realpath(__file__))
tirar = dir.find('configurações')
dir = dir[:tirar]
cred = credentials.Certificate(dir + r"modulos\login\credenciais\registro-de-estoque.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://registro-de-estoque-default-rtdb.firebaseio.com/'})



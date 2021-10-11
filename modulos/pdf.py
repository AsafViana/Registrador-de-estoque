from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
from pyautogui import alert
from fire import refstoque
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog



diretorio = os.path.dirname(os.path.realpath(__file__))
tirar = diretorio.find('modulos')
diretorio = diretorio[:tirar]


url = diretorio + 'modulos\credenciais\loja.txt'
def receber_loja():
    url = diretorio + 'modulos\credenciais\loja.txt'
    with open(url, 'r') as arquivo:
        loja = arquivo.read()
    return loja




pdf()
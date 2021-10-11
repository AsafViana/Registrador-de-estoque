from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
from pyautogui import alert
from fire import refstoque
from tkinter.filedialog import askdirectory


diretorio = os.path.dirname(os.path.realpath(__file__))
tirar = diretorio.find('modulos')
diretorio = diretorio[:tirar]


def criar_pdf():
    cnv = canvas.Canvas(diretorio + r'\teste.pdf', pagesize=A4)
    cnv.save()
criar_pdf()

url = diretorio + 'modulos\credenciais\loja.txt'
def receber_loja():
    url = diretorio + 'modulos\credenciais\loja.txt'
    with open(url, 'r') as arquivo:
        loja = arquivo.read()
    return loja


def pdf():
    pasta = askdirectory()
    loja = receber_loja()
    endereço = refstoque.child(loja)
    dados_lidos = endereço.get()
    produtos = list(dados_lidos)

    y = 0
    pdf = canvas.Canvas(pasta + f"/cadastro_produtos ({date.today()}).pdf", pagesize=A4)
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


print(askdirectory())
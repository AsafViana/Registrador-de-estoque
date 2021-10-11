from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
from pyautogui import alert
from fire import refstoque


diretorio = os.path.dirname(os.path.realpath(__file__))
tirar = diretorio.find('modulos')
diretorio = diretorio[:tirar]
print(date.today())

def criar_pdf():
    cnv = canvas.Canvas(diretorio + r'\teste.pdf', pagesize=A4)
    cnv.save()
criar_pdf()

url = diretorio + 'modulos\credenciais\loja.txt'
print(url)
def receber_loja():
    url = diretorio + 'modulos\credenciais\loja.txt'
    print(url)
    with open(url, 'r') as arquivo:
        loja = arquivo.read()
    return loja


def pdf():
    loja = receber_loja()
    endereço = refstoque.child(loja)
    dados_lidos = endereço.get()
    print(dados_lidos)
    y = 0
    pdf = canvas.Canvas(diretorio + "cadastro_produtos.pdf", pagesize=A4)
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(20, 750, "PRODUTO")
    pdf.drawString(130, 750, "CATEGORIA")
    pdf.drawString(260, 750, "CODIGO")
    pdf.drawString(354, 750, "PREÇO")
    pdf.drawString(440, 750, "QUANTIDADE")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(20, 750 - y, dados_lidos[i]['produto'])
        pdf.drawString(130, 750 - y, dados_lidos[i]['categoria'])
        pdf.drawString(260, 750 - y, dados_lidos[i]['codigo'])
        pdf.drawString(354, 750 - y, dados_lidos[i]['preco'])
        pdf.drawString(440, 750 - y, dados_lidos[i]['quantidade'])

    pdf.save()
    alert("PDF FOI GERADO COM SUCESSO!")
pdf()
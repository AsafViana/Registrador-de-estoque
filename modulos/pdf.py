from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
from pyautogui import alert
from modulos.telas_funções import loja_mercadoria_e_parametros_endereço
from fire import refstoque


diretorio = os.path.dirname(os.path.realpath(__file__))
tirar = diretorio.find('modulos')
diretorio = diretorio[:tirar]
print(date.today())

def criar_pdf():
    cnv = canvas.Canvas(diretorio + r'\teste.pdf', pagesize=A4)
    cnv.save()
criar_pdf()

def pdf():
    loja, mercadoria, parametros, endereço = loja_mercadoria_e_parametros_endereço()
    dados_lidos = refstoque.child(loja)
    print(dados_lidos)
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "PRODUTO")
    pdf.drawString(110, 750, "CATEGORIA")
    pdf.drawString(210, 750, "CODIGO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "QUANTIDADE")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i]['produto']))
        pdf.drawString(110, 750 - y, str(dados_lidos[i]['categoria']))
        pdf.drawString(210, 750 - y, str(dados_lidos[i]['codigo']))
        pdf.drawString(310, 750 - y, str(dados_lidos[i]['preco']))
        pdf.drawString(410, 750 - y, str(dados_lidos[i]['quantidade']))

    pdf.save()
    alert("PDF FOI GERADO COM SUCESSO!")
pdf()
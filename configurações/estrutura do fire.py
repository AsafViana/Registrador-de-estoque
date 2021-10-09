import firebase_admin
from firebase_admin import credentials, db
import os
import configurações


estoque = db.reference('estoque')

es = estoque.child('loja 2')

mercadoria_lista = list(es.get())
parametros_part1 = es.get()

print(list(parametros_part1.keys()))

for item1 in range(0, len(mercadoria_lista)):
    for c in range(0, 4):
        i = estoque.child(mercadoria_lista[item1])
        informações_produtos = i.get()

        info = {}
        info['nome'] = mercadoria_lista[item1]

        c = 0
        while True:
            if lista3[c] in lista4:
                print('tem ', lista3[c])
            else:
                print('não tem ', lista3[c])
                break
            c += 1
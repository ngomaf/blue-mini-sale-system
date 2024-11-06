# -*- coding: utf-8 -*-
'''
    Sistema de venda
    O presente sistema foi desenvolvido com esforço
    no sentido de criar um soffware de vendan que revolucione
    as interfaces actuais implemento principicios de design modernos.

    Descrição
    O software dispõe das seguintes secções: 
    (1) Login, (2) Vender, (3) Vendas, (4) Produtos,
    (5) Clientes fidelizados, (6) Stok, (5) Relatorios e (6) Definições

    Tecnologias
    Linguagem: Python 3 | Interface: Tkinter 8.6 e Tkinter.ttk | Banco de dados: SQLite3

    Versão: 0.2 | Criação: 00.00.0000 | Actualização: 05.01.2022

    Créditos:
    Flaticon e eucalyp: www.flaticon.com/br/autores/eucalyp

    Por: Ngoma Manuel Fortuna
    Homenagem: Zany A. Manuel Fortuna (minha querida irmã)
'''
from components.app import App


if __name__ == '__main__':
    app = App()
    app.run()

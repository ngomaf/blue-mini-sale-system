from tkinter import PhotoImage, LEFT, RIGHT, HORIZONTAL
from tkinter import BOTH, VERTICAL, NO, X, Y, W, E
from tkinter import Entry as tkEntry
from tkinter import LabelFrame as tkLabelFrame
from tkinter.ttk import Frame, Label, Button, Combobox, Separator
from tkinter.ttk import Treeview, Scrollbar

from datetime import datetime

from models.modelsqlitesequence import ModelSQLiteSequence
from models.modelbuy import ModelBuy
from components.notdecimal import NotDecimal


class ViewSale:

	def __init__(self, mother, main, model, mdsale):
		self._main = main
		self._mother = mother
		self._model = model
		self._mdsale = mdsale
		self._mdbuy = ModelBuy()
		self._decimal = NotDecimal()
		self._lite_sequence = ModelSQLiteSequence()
		self._sale = Frame(mother)
		self._sale.pack(fill=X, padx=20)

		# --- inicializacao ---------
		self._iam = self._main.get_user_logd()
		self._sel_product = []
		self._count_lancado = 0
		self._total_sale = 0
		self.show_widgets()

	def select_product(self):
		if len(self._tv_products.selection()) != 0:

			item = self._tv_products.selection()
			datas = self._tv_products.item(item)['values']
			
			datas[0] = item[0]
			datas[2] = int(self._et_qtdade.get())
			datas[3] = float(self._decimal.mspp_reverse(datas[3])) * float(self._decimal.mspp_reverse(datas[2]))
			self._sel_product.append(datas)
		else:
			print('seleccione um produto.')

	def search_products(self):
		self._tv_products.delete(*self._tv_products.get_children())
		products = self._model.get_products('')

		for prod in products:
			if int(prod[6]):
				self._tv_products.insert(parent='', index=prod[0], iid=prod[0], text='', values=(prod[0],prod[2],int(prod[3]),self._decimal.mspp(prod[4])))

	def lancar_venda(self):

		if self._et_client.get() != '':
			self._lf_client['fg'] = '#909090'
			if self._et_qtdade.get() != '':
				self._lf_qtdade['fg'] = '#909090'
				self._tv_products_lanc.delete(*self._tv_products_lanc.get_children())
				self._total_sale = 0
				self._count_lancado += 1

				self.select_product()
				for index, item in enumerate(self._sel_product):
					self._tv_products_lanc.insert(parent='', index=index, iid=index, text='', values=(item[0], item[1], item[2], self._decimal.mspp(item[3])))
					self._total_sale += item[3]
				self._lb_total_value['text'] = self._decimal.mspp(self._total_sale)
				self.search_products()
				self._et_qtdade.delete(0, 'end')
				self._et_qtdade.focus_force()

			else:
				self._lf_qtdade['fg'] = '#e0002c'
				self._et_qtdade.focus_force()
		else:
			self._lf_client['fg'] = '#e0002c'
			self._et_client.focus_force()

	def reduzir_venda(self):
		if len(self._tv_products_lanc.selection()) != 0:
			item = int(self._tv_products_lanc.selection()[0])
			self._sel_product.pop(item)

			self._total_sale = 0
			self._tv_products_lanc.delete(*self._tv_products_lanc.get_children())
			for index, item in enumerate(self._sel_product):
				self._tv_products_lanc.insert(parent='', index=index, iid=index, text='', values=(item[0], item[1], item[2], item[3]))
				self._total_sale += item[3]
			self._lb_total_value['text'] = f'{self._total_sale:.2f}'
			self._et_pagou.focus_force()

	def vender(self):
		if self._et_pagou.get() != '':
			self._lf_pagou['fg'] = '#909090'
			total = self._decimal.mspp_reverse(self._lb_total_value['text'])
			if (float(self._et_pagou.get()) - float(total)) >= 0:
				user = self._iam[0][0]
				id_sale = int(self._lite_sequence.get_datas()[3][1]) + 1

				client = self._et_client.get()
				buy = self.cod_generate() # recibo ou codigo da venda
				total = f'{self._total_sale:.2f}'
				date = datetime.now()
				date = date.strftime('%d.%m.%Y %H:%M')

				msg = self._mdsale.set_sale(user, client, buy, total, date)
				print(msg)

				# compra
				for item in self._sel_product:
					msg = self._model.less_product(item[2], item[0])

				for item in self._sel_product:
					self._mdbuy.set_buy(id_sale, item[0], item[2])

				self.set_cod()
				self.search_products()
				self._et_client.delete(0, 'end')
				self._et_qtdade.delete(0, 'end')
				self._et_client.focus_force()

				self._et_pagou.delete(0, 'end')
				self._lb_total_value['text'] = '0,00'
				self._lb_debito['text'] = '0,00'

				self._total_sale = 0
				self._sel_product = []
				self._tv_products_lanc.delete(*self._tv_products_lanc.get_children())
		else:
			self._lf_pagou['fg'] = '#e0002c'
			self._et_pagou.focus_force()

	# metodo debito
	def on_debito(self):
		if self._et_pagou.get() == '': self._et_pagou.insert(0, 0)
		value = self._decimal.mspp_reverse(self._lb_total_value['text'])
		debito = float(self._et_pagou.get()) - float(value)
		self._lb_debito['text'] = self._decimal.mspp(debito)

	def set_cod(self):
		self._et_cod['state'] = 'normal'
		self._et_cod.delete(0, 'end')
		self._et_cod.insert(0, self.cod_generate())
		self._et_cod['state'] = 'readonly'

	def cod_generate(self):
		cod = int(self._lite_sequence.get_datas()[3][1]) + 1

		return str(cod).zfill(5)

	# metodo voltar
	def back(self):
		self._sale.pack_forget()
		self._main.back_main()

	def show_widgets(self):

		mpgraph = ('Montserrat', 12, 'bold')
		pgraph = ('Montserrat', 10)
		pgraph_small = ('Montserrat', 8)

		top = Frame(self._sale)
		top.pack(fill=X, expand=True, pady=(20, 5))

		icon_sale = PhotoImage(file=r"components/icons/main_vender.png")
		lb_sale = Label(top, text='  Vender', style='IconFrame.TLabel', image=icon_sale, 
			compound=LEFT)
		lb_sale.image = icon_sale
		lb_sale.pack(side=LEFT)

		icon_sale = PhotoImage(file=r"components/icons/logo_small.png")
		lb_sale = Label(top, text='', style='IconFrame.TLabel', image=icon_sale)
		lb_sale.image = icon_sale
		lb_sale.pack(side=LEFT, fill=Y, expand=True)

		user = Frame(top)
		user.pack(side=RIGHT)

		icon_user = PhotoImage(file=r"components/icons/main_user2.png")
		lb_user = Label(user, text='', image=icon_user)
		lb_user.image = icon_user
		lb_user.pack(side=LEFT)

		Button(user, text=self._iam[0][3], width=0, cursor='hand1', style='UserMain.TButton').pack(side=LEFT, anchor=W)
		Button(user, text='[« Voltar]', width=0, cursor='hand1', command=self.back,
			style='Out.TButton').pack(side=LEFT, anchor=W)

		Separator(self._sale, orient=HORIZONTAL).pack(fill=X)

		body = Frame(self._sale)
		body.pack(fill=BOTH, expand=True, pady=10)

		# left
		left = Frame(body, style='Side.TFrame', padding=10)
		left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

		top_left = Frame(left)
		top_left.pack(fill=X)

		self._lf_cod = tkLabelFrame(top_left, font=pgraph_small, text='Código', fg='#909090', 
			width=5, bg='#f1f1f1', relief='ridge')
		self._lf_cod.pack(side=LEFT)

		self._et_cod = tkEntry(self._lf_cod, font=pgraph, fg='#666', relief='flat', takefocus=False, 
			width=5, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_cod.pack(padx=5, pady=(0, 3))

		self.set_cod()

		client_qtidade = Frame(top_left)
		client_qtidade.pack(side=RIGHT)

		self._lf_client = tkLabelFrame(client_qtidade, font=pgraph_small, text='Cliente', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_client.pack(side=LEFT, anchor=E, padx=5)

		self._et_client = tkEntry(self._lf_client, font=pgraph, fg='#333', relief='flat', 
			width=12, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_client.focus_force()
		self._et_client.pack(side=LEFT, padx=5, pady=(0, 3))

		self._lf_qtdade = tkLabelFrame(client_qtidade, font=pgraph_small, text='Quantidade', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_qtdade.pack(side=LEFT, anchor=E)

		self._et_qtdade = tkEntry(self._lf_qtdade, font=pgraph, fg='#333', relief='flat', 
			width=5, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_qtdade.pack(side=LEFT, padx=5, pady=(0, 3))

		# treeview
		treeview = Frame(left)
		treeview.pack(fill=BOTH, expand=True, anchor=E, pady=(10, 20))

		self._tv_products = Treeview(treeview, selectmode="extended", height=13)
		self._tv_products['columns']=('#' ,'Product', 'Quantify', 'Prace')
		self._tv_products.column('#0', width=0, stretch=NO)
		self._tv_products.column('#', anchor=W, width=45)
		self._tv_products.column('Product', anchor=W, width=180)
		self._tv_products.column('Quantify', anchor=W, width=80)
		self._tv_products.column('Prace', anchor=W, width=80)

		self._tv_products.heading('#0', text='', anchor=W)
		self._tv_products.heading('#', text='#', anchor=W)
		self._tv_products.heading('Product', text='Produto', anchor=W)
		self._tv_products.heading('Quantify', text='Qtidade', anchor=W)
		self._tv_products.heading('Prace', text='Preço', anchor=W)
		self._tv_products.pack(side=LEFT, fill=BOTH, expand=True)

		self._sc_products = Scrollbar(treeview, orient=VERTICAL)
		self._sc_products.pack(side=LEFT, fill=Y, padx=(5, 0))
		
		self._tv_products.config(yscrollcommand=self._sc_products.set)
		self._sc_products.config(command=self._tv_products.yview)

		# 
		self.search_products()

		Button(left, text='Lançar venda +', cursor='hand1', style='Lancar.TButton', 
			command=self.lancar_venda).pack(fill=X, expand=True)

		# direita
		right = Frame(body, style='Side.TFrame', padding=10)
		right.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

		# treeview
		treeview_r = Frame(right)
		treeview_r.pack(fill=BOTH, expand=True)

		self._tv_products_lanc = Treeview(treeview_r, selectmode="extended", height=8)
		self._tv_products_lanc['columns']=('#' ,'Product', 'Qtdd', 'Total')
		self._tv_products_lanc.column('#0', width=0, stretch=NO)
		self._tv_products_lanc.column('#', anchor=W, width=25)
		self._tv_products_lanc.column('Product', anchor=W, width=130)
		self._tv_products_lanc.column('Qtdd', anchor=W, width=50)
		# self._tv_products_lanc.column('Prace', anchor=W, width=55)
		self._tv_products_lanc.column('Total', anchor=W, width=65)

		self._tv_products_lanc.heading('#0', text='', anchor=W)
		self._tv_products_lanc.heading('#', text='#', anchor=W)
		self._tv_products_lanc.heading('Product', text='Produto', anchor=W)
		self._tv_products_lanc.heading('Qtdd', text='Qtdd', anchor=W)
		# self._tv_products_lanc.heading('Prace', text='Preço', anchor=W)
		self._tv_products_lanc.heading('Total', text='Total', anchor=W)
		self._tv_products_lanc.pack(side=LEFT, fill=BOTH, expand=True)

		self._sc_products_lanc = Scrollbar(treeview_r, orient=VERTICAL)
		self._sc_products_lanc.pack(side=LEFT, fill=Y, padx=(5, 0))

		self._tv_products_lanc.config(yscrollcommand=self._sc_products_lanc.set)
		self._sc_products_lanc.config(command=self._tv_products_lanc.yview)

		remover_pagou = Frame(right)
		remover_pagou.pack(fill=X, pady=10)

		Button(remover_pagou, text='Remover -', command=self.reduzir_venda, cursor='hand1', style='Remove.TButton').pack(side=LEFT, anchor=W)

		value_frame = Frame(remover_pagou)
		value_frame.pack(side=RIGHT, anchor=E)
		Label(value_frame, text='valor pago', style='Legend.TLabel').pack(anchor=E)
		self._lb_total_value = Label(value_frame, text='0,00', style='Data2.TLabel')
		self._lb_total_value.pack()

		self._lf_pagou = tkLabelFrame(right, font=pgraph, text='Pagou', fg='#909090', 
			bg='#f1f1f1', labelanchor='ne', relief='ridge')
		self._lf_pagou.pack(anchor=E)

		self._et_pagou = tkEntry(self._lf_pagou, font=mpgraph,
			relief='flat', fg='#333', width=15, bg='#f1f1f1', justify=RIGHT,
			highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_pagou.focus_force()
		self._et_pagou.bind("<KeyRelease>", lambda e: self.on_debito())
		self._et_pagou.pack(side=LEFT, padx=5, pady=(0, 3))

		less_frame = Frame(right)
		less_frame.pack(anchor=E, pady=10)
		Label(less_frame, text='Débito', style='Legend.TLabel').pack(anchor=E)
		self._lb_debito = Label(less_frame, text='0,00', style='Data2.TLabel')
		self._lb_debito.pack()

		Button(right, text='Vender', command=self.vender, cursor='hand1', style='Sale.TButton').pack(fill=X, expand=True)

from tkinter import PhotoImage, messagebox, LEFT, RIGHT, CENTER, HORIZONTAL
from tkinter import BOTH, VERTICAL, NO, BOTH, X, Y, W, E
from tkinter import Entry as tkEntry
from tkinter import LabelFrame as tkLabelFrame
from tkinter.ttk import Frame, Label, Button, Combobox, Separator
from tkinter.ttk import Treeview, Scrollbar

from models.modelsqlitesequence import ModelSQLiteSequence
from components.notdecimal import NotDecimal


class ViewProducts:

	def __init__(self, mother, main, model):
		self._main = main
		self._model = model
		self._lite_sequence = ModelSQLiteSequence()
		self._decimal = NotDecimal()
		self._sales = Frame(mother)
		self._sales.pack(fill=X, padx=20)

		self._save_state = 0

		# --- inicializacao -----------------
		self._iam = self._main.get_user_logd()
		self.show_widgets()

	# seleccionar id na treeview
	def select_product(self):
		return self._tv_products.selection()

	# editar produtos
	def edit(self):
		if len(self.select_product()) != 0:
			self._id = self.select_product()[0]

			product = self._model.get_product(self._id)

			self.clear()
			self._save_state = 1

			self._et_cod['state'] = 'normal'
			self._et_cod.delete(0, 'end')
			self._et_cod.insert(0, product[0][1])
			self._et_cod['state'] = 'readonly'

			self._et_n_produto.insert(0, product[0][2])
			self._et_description.insert(0, product[0][5])
			self._et_prace.insert(0, f'{self._decimal.mspp(product[0][4])}')
			self._et_quantidade.insert(0, int(product[0][3]))
		else:
			self._lb_msg.configure(style='MsgError.TLabel')
			self._lb_msg['text'] = '<== Selecione um produto na tabela.'					
			self._tv_products.after(3000, self.empty_entry)

	# eliminar produto
	def delete(self):

		self._lb_msg.configure(style='MsgError.TLabel')

		if len(self.select_product()) != 0:

			action = messagebox.askokcancel('Cuidado!', 'Deseja realmente eliminar definitivamente o produto?')
			
			if action == True:
				msg = self._model.delete(self.select_product()[0])
				self._lb_msg['text'] = msg['content']
				self.search()
				self.clear()

				self._tv_products.after(3000, self.empty_entry)
		else:
			self._lb_msg['text'] = '<== Selecione um utilizador na tabela.'					
			self._tv_products.after(3000, self.empty_entry)

	# metodo 
	def search(self):
		self.search_products('')

	def search_entry(self):
		self.search_products(self._et_search.get())

	def search_products(self, filter):
		self._total = 0
		products = self._model.get_products(filter)
		self._tv_products.delete(*self._tv_products.get_children())

		for n, prod in enumerate(products):
			state = prod[6]
			if state == 1: state = 'on'
			else: state = 'off'
			self._tv_products.insert(parent='', index=prod[0], iid=prod[0], text='', values=(n+1,prod[2],int(prod[3]),self._decimal.mspp(prod[4]),state))
			self._total += 1
		self._lb_total['text'] = 'Total: ' + str(self._total)

	# salvar usuario
	def save_product(self):
		cod = self._et_cod.get().strip()
		product = self._et_n_produto.get().strip()
		description = self._et_description.get().strip()
		prace = self._decimal.mspp_reverse(self._et_prace.get().strip())

		qtdade = int(self._et_quantidade.get().strip())

		state = 0

		if self._save_state == 0:
			if product != '':
				self._lf_n_produto['fg'] = '#909090'
				if prace != '':
					self._lf_prace['fg'] = '#909090'
					if qtdade != '':
						self._lf_quantidade['fg'] = '#909090'
						
						if int(qtdade) > 1: state = 1
						msg = self._model.set_product(cod, product, qtdade, prace, description, state)
						self._et_n_produto.focus_force()

						if 'Sucesso!' in msg['title']:
							self._lb_msg.configure(style='MsgSucess.TLabel')
							self.search()
							self.clear()
						else:
							self._lb_msg.configure(style='MsgError.TLabel')

						self._lb_msg['text'] = msg['content']						
						self._tv_products.after(3000, self.empty_entry)
						
					else:
						self._lf_quantidade['fg'] = '#e0002c'
						self._et_quantidade.focus_force()		
				else:
					self._lf_prace['fg'] = '#e0002c'
					self._et_prace.focus_force()
			else:
				self._lf_n_produto['fg'] = '#e0002c'
				self._et_n_produto.focus_force()
		else:
			id = self._id

			if int(qtdade) > 1: state = 1
			msg = self._model.update(product, qtdade, prace, description, state, id)

			self._et_n_produto.focus_force()

			if 'Sucesso!' in msg['title']:
				self._lb_msg.configure(style='MsgSucess.TLabel')
				self.search()
				self.clear()
			else:
				self._lb_msg.configure(style='MsgError.TLabel')

			self._lb_msg['text'] = msg['content']						
			self._tv_products.after(3000, self.empty_entry)

	def empty_entry(self):
		self._lb_msg['text'] = ' '

	def clear(self):

		self._save_state = 0

		self._et_cod['state'] = 'normal'
		self._et_cod.delete(0, 'end')
		self._et_cod.insert(0, self.cod_generate())
		self._et_cod['state'] = 'readonly'

		self._et_n_produto.delete(0, 'end')
		self._et_description.delete(0, 'end')
		self._et_prace.delete(0, 'end')
		self._et_quantidade.delete(0, 'end')

		self._lf_n_produto['fg'] = '#909090'
		self._lf_prace['fg'] = '#909090'
		self._lf_quantidade['fg'] = '#909090'

		self._et_n_produto.focus_force()

	def cod_generate(self):
		cod = self._lite_sequence.get_datas()[2][1] + 1
		if cod < 10:
			cod = '0000' + str(cod)
		elif cod < 100:
			cod = '000' + str(cod)
		elif cod < 1000:
			cod = '00' + str(cod)
		elif cod < 10000:
			cod = '0' + str(cod)
		elif cod < 100000:
			cod = cod

		return cod

	def back(self):
		self._sales.pack_forget()
		self._main.back_main()

	def show_widgets(self):

		pgraph = ('Montserrat', 10)
		pgraph_small = ('Montserrat', 8)

		top = Frame(self._sales)
		top.pack(fill=X, expand=True, pady=(20, 5))

		icon_products = PhotoImage(file=r"components/icons/main_produtos.png")
		lb_products = Label(top, text='  Produtos', style='IconFrame.TLabel', image=icon_products, 
			compound=LEFT)
		lb_products.image = icon_products
		lb_products.pack(side=LEFT)

		icon_sales = PhotoImage(file=r"components/icons/logo_small.png")
		lb_sales = Label(top, text='', style='IconFrame.TLabel', image=icon_sales)
		lb_sales.image = icon_sales
		lb_sales.pack(side=LEFT, fill=Y, expand=True)

		user = Frame(top)
		user.pack(side=RIGHT)

		icon_user = PhotoImage(file=r"components/icons/main_user2.png")
		lb_user = Label(user, text='', image=icon_user)
		lb_user.image = icon_user
		lb_user.pack(side=LEFT)

		Button(user, text=self._iam[0][3], width=0, cursor='hand1', style='UserMain.TButton').pack(side=LEFT, anchor=W)
		Button(user, text='[« Voltar]', width=0, cursor='hand1', command=self.back, 
			style='Out.TButton').pack(side=LEFT, anchor=W)

		Separator(self._sales, orient=HORIZONTAL).pack(fill=X)

		body = Frame(self._sales)
		body.pack(fill=BOTH, expand=True, pady=10)

		# left
		left = Frame(body, style='Side.TFrame', padding=10)
		left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

		top_left = Frame(left)
		top_left.pack(fill=X)

		edit_del = Frame(top_left)
		edit_del.pack(side=LEFT)

		img_edit = PhotoImage(file=r"components/icons/products_edit.png")
		bt_edit = Button(edit_del, text='', width=0, cursor='hand1', style='Out.TButton', image=img_edit)
		bt_edit.image = img_edit
		bt_edit['command'] = self.edit
		bt_edit.pack(side=LEFT)

		img_del = PhotoImage(file=r"components/icons/products_del.png")
		bt_del = Button(edit_del, text='', width=0, cursor='hand1', style='Out.TButton', image=img_del)
		bt_del.image = img_del
		bt_del['command'] = self.delete
		bt_del.pack(side=LEFT)

		cod_search = Frame(top_left)
		cod_search.pack(side=RIGHT)

		self._lf_cod = tkLabelFrame(cod_search, font=pgraph_small, text='Código', fg='#909090', 
			bg='#f1f1f1', relief='flat')
		self._lf_cod.pack(side=LEFT, pady=(2, 0))

		cod = ['Nome', 'Data', 'valor']
		self._cb_cod = Combobox(self._lf_cod, values=cod, justify=CENTER, width=10)
		self._cb_cod.current(0)
		self._cb_cod['state'] = 'readonly'
		self._cb_cod.pack(padx=5, pady=3)

		self._lf_search = tkLabelFrame(cod_search, font=pgraph_small, text='Pesquisar', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_search.pack(side=RIGHT)

		self._et_search = tkEntry(self._lf_search, font=pgraph, fg='#333', relief='flat', 
			width=15, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_search.focus_force()
		self._et_search.bind("<KeyRelease>", lambda e: self.search_entry())
		self._et_search.pack(side=LEFT, padx=5, pady=(0, 3))

		self._icon_glass = PhotoImage(file=r"components/icons/sales_glass.png")
		self._lb_glass = Label(self._lf_search, text='', image=self._icon_glass)
		self._lb_glass.image = self._icon_glass
		self._lb_glass.pack(side=LEFT, padx=5, pady=5)

		# treeview
		treeview = Frame(left)
		treeview.pack(fill=BOTH, expand=True, pady=(10, 0))

		self._tv_products = Treeview(treeview, selectmode="extended", height=13)
		self._tv_products['columns']=('#' ,'product', 'quantify', 'prace', 'state')
		self._tv_products.column('#0', width=0, stretch=NO)
		self._tv_products.column('#', anchor=W, width=45)
		self._tv_products.column('product', anchor=W, width=170)
		# self._tv_products.column('description', anchor=W, width=120)
		self._tv_products.column('quantify', anchor=W, width=80)
		self._tv_products.column('prace', anchor=W, width=80)
		self._tv_products.column('state', anchor=W, width=50)

		self._tv_products.heading('#0', text='', anchor=W)
		self._tv_products.heading('#', text='#', anchor=W)
		self._tv_products.heading('product', text='Produto', anchor=W)
		# self._tv_products.heading('description', text='Descrição', anchor=W)
		self._tv_products.heading('quantify', text='Qtidade', anchor=W)
		self._tv_products.heading('prace', text='Preço', anchor=W)
		self._tv_products.heading('state', text='Stdo', anchor=W)

		self._tv_products.pack(side=LEFT, fill=BOTH, expand=True)

		self._sc_products = Scrollbar(treeview, orient=VERTICAL)
		self._sc_products.pack(side=LEFT, fill=Y, padx=(5, 0))
		
		self._tv_products.config(yscrollcommand=self._sc_products.set)
		self._sc_products.config(command=self._tv_products.yview)
		
		self._lb_total = Label(left, text='', style='Legend.TLabel')
		self._lb_total.pack(anchor=E)

		self.search()

		# direita
		right = Frame(body, style='Side.TFrame', padding=(10, 5))
		right.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

		self._lf_cod = tkLabelFrame(right, font=pgraph_small, text='Código', fg='#909090', 
			width=5, bg='#f1f1f1', relief='ridge')
		self._lf_cod.pack(anchor=W, pady=(0, 15))

		self._et_cod = tkEntry(self._lf_cod, font=pgraph, fg='#666', relief='flat', takefocus=False, 
			width=5, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_cod.insert(0, self.cod_generate())
		self._et_cod['state'] = 'readonly'
		self._et_cod.pack(padx=5, pady=(0, 3))

		self._lb_msg = Label(right, text=' ') #, style='MsgError.TLabel'
		self._lb_msg.pack()

		self._lf_n_produto = tkLabelFrame(right, font=pgraph, text='Nome do Produto', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_n_produto.pack(fill=X, pady=(15, 0))

		self._et_n_produto = tkEntry(self._lf_n_produto, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_n_produto.focus_force()
		self._et_n_produto.pack(fill=X, padx=5, pady=(0, 3))

		self._lf_description = tkLabelFrame(right, font=pgraph, text='Descrição', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_description.pack(fill=X, pady=10)

		self._et_description = tkEntry(self._lf_description, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_description.focus_force()
		self._et_description.pack(fill=X, padx=5, pady=(0, 3))

		quatidade_preco = Frame(right)
		quatidade_preco.pack(fill=X)

		self._lf_prace = tkLabelFrame(quatidade_preco, font=pgraph, text='Preço unitário', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_prace.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

		self._et_prace = tkEntry(self._lf_prace, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_prace.focus_force()
		self._et_prace.pack(fill=X, padx=5, pady=(0, 3))

		self._lf_quantidade = tkLabelFrame(quatidade_preco, font=pgraph, text='Quantidade', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_quantidade.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

		self._et_quantidade = tkEntry(self._lf_quantidade, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_quantidade.focus_force()
		self._et_quantidade.pack(fill=X, padx=5, pady=(0, 3))

		Button(right, text='Salvar', command=self.save_product, cursor='hand1', style='Sale.TButton').pack(fill=X, pady=(40, 5))
		Button(right, text='Limpar', command=self.clear, cursor='hand1', style='Clear.TButton').pack(fill=X)

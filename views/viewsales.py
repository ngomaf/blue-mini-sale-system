from tkinter import PhotoImage, LEFT, RIGHT, CENTER, HORIZONTAL
from tkinter import BOTH, VERTICAL, NO, BOTH, X, Y, W, E
from tkinter import Entry as tkEntry
from tkinter import LabelFrame as tkLabelFrame
from tkinter.ttk import Frame, Label, Button, Combobox, Separator
from tkinter.ttk import Treeview, Scrollbar

from models.modelbuy import ModelBuy
from models.modelproducts import ModelProducts
from models.modelsettuser import ModelSettUser
from components.notdecimal import NotDecimal


class ViewSales:

	def __init__(self, mother, main, model):
		self._main = main
		self._model = model
		self._mdbuy = ModelBuy()
		self._mdproducts = ModelProducts()
		self._mduser = ModelSettUser()
		self._decimal = NotDecimal()
		self._sales = Frame(mother)
		self._sales.pack(fill=X, padx=20)

		# --- inicializacao --------------------
		self._iam = self._main.get_user_logd()
		self.show_widgets()

	def select_sale(self):
		item = []
		if len(self._tv_clients.selection()) != 0:
			id = self._tv_clients.selection()[0]
			item = self._model.get_sale(id)[0]

		return item

	def show_selectd_item(self):
		item = self.select_sale()

		if len(item) != 0:
			self._tv_saled.delete(*self._tv_saled.get_children())
			self._lb_sale_by['text'] = self._mduser.get_user(item[1])[0][3]
			self._lb_cod['text'] = item[3]
			self._lb_client['text'] = item[2]
			self._lb_date['text'] = item[5]
			self._lb_total_sale['text'] = f'{self._decimal.mspp(item[4])} AKZ'

			buys = self._mdbuy.get_buys(item[0])

			for line, prod in enumerate(buys):
				product = self._mdproducts.get_product(prod[2])
				# print(f'{line} {product[0][2]} {prod[3]} {product[0][4]} {float(prod[3]) * float(product[0][4])}')
				self._tv_saled.insert(parent='', index=prod[0], iid=prod[0], text='', values=(line,product[0][2], prod[3],self._decimal.mspp(product[0][4]),self._decimal.mspp(float(prod[3]) * float(product[0][4]))))



	def search(self):
		self.search_sales('')

	def search_entry(self):
		self.search_sales(self._et_search.get())

	def search_sales(self, filter):
		self._total = 0
		self._tv_clients.delete(*self._tv_clients.get_children())
		sales = self._model.get_sales(filter)

		for count, item in enumerate(sales):
			self._tv_clients.insert(parent='', index=item[0], iid=item[0], text='', values=(count,item[2],self._decimal.mspp(item[4]),item[5][:10]))
			self._total += 1
		self._lb_total['text'] = f'Total: {self._total}'			

	def back(self):
		self._sales.pack_forget()
		self._main.back_main()

	# metodo debito
	def search_client(self):
		print(f'Procurar pelo: {self._et_search.get()}')

	def show_widgets(self):

		pgraph = ('Montserrat', 10)
		pgraph_small = ('Montserrat', 8)

		top = Frame(self._sales)
		top.pack(fill=X, expand=True, pady=(20, 5))

		icon_sales = PhotoImage(file=r"components/icons/main_vendas.png")
		lb_sales = Label(top, text='  Vendas', style='IconFrame.TLabel', image=icon_sales, 
			compound=LEFT)
		lb_sales.image = icon_sales
		lb_sales.pack(side=LEFT)

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

		self._lf_cod = tkLabelFrame(top_left, font=pgraph_small, text='Código', fg='#909090', 
			bg='#f1f1f1', relief='flat')
		self._lf_cod.pack(side=LEFT)

		cod = ['Nome', 'Data', 'valor']
		self._cb_cod = Combobox(self._lf_cod, values=cod, justify=CENTER, width=10)
		self._cb_cod.current(0)
		self._cb_cod['state'] = 'readonly'
		self._cb_cod.pack(padx=5, pady=(8, 3))

		self._lf_search = tkLabelFrame(top_left, font=pgraph_small, text='Pesquisar', fg='#909090', 
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

		self._tv_clients = Treeview(treeview, selectmode="extended", height=13)
		self._tv_clients['columns']=('#' ,'name', 'value', 'date')
		self._tv_clients.column('#0', width=0, stretch=NO)
		self._tv_clients.column('#', anchor=W, width=45)
		self._tv_clients.column('name', anchor=W, width=120)
		self._tv_clients.column('value', anchor=W, width=90)
		self._tv_clients.column('date', anchor=W, width=80)

		self._tv_clients.heading('#0', text='', anchor=W)
		self._tv_clients.heading('#', text='#', anchor=W)
		self._tv_clients.heading('name', text='Nome', anchor=W)
		self._tv_clients.heading('value', text='Valor', anchor=W)
		self._tv_clients.heading('date', text='Data', anchor=W)
		self._tv_clients.bind('<Button-1>', lambda x : self.show_selectd_item())

		self._tv_clients.pack(side=LEFT, fill=BOTH, expand=True)


		self._sc_clients = Scrollbar(treeview, orient=VERTICAL)
		self._sc_clients.pack(side=LEFT, fill=Y, padx=(5, 0))
		
		self._tv_clients.config(yscrollcommand=self._sc_clients.set)
		self._sc_clients.config(command=self._tv_clients.yview)

		self._lb_total = Label(left, text='255/2550', style='Legend.TLabel')
		self._lb_total.pack(anchor=E)

		self.search()

		# direita
		right = Frame(body, style='Side.TFrame', padding=10)
		right.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

		top_rigth = Frame(right)
		top_rigth.pack(fill=X, expand=True)

		cod_frame = Frame(top_rigth)
		cod_frame.pack(side=LEFT)
		Label(cod_frame, text='cod', style='Legend.TLabel').pack(anchor=W)
		self._lb_cod = Label(cod_frame, text='0000', style='Legend.TLabel')
		self._lb_cod.pack()

		client_frame = Frame(top_rigth)
		client_frame.pack(side=RIGHT)
		Label(client_frame, text='nome do cliente', style='Legend.TLabel').pack(anchor=E)
		self._lb_client = Label(client_frame, text='---', style='Data.TLabel')
		self._lb_client.pack(anchor='e')

		data_frame = Frame(right)
		data_frame.pack(anchor=E, pady=(10, 5))
		Label(data_frame, text='data', style='Legend.TLabel').pack(anchor=E)
		self._lb_date = Label(data_frame, text='00.00.0000 00:00')
		self._lb_date.pack()

		# treeview
		treeview_r = Frame(right)
		treeview_r.pack(fill=BOTH, expand=True)

		self._tv_saled = Treeview(treeview_r, selectmode="extended", height=8)
		self._tv_saled['columns']=('#' ,'Product', 'Qtdd', 'Prace', 'Total')
		self._tv_saled.column('#0', width=0, stretch=NO)
		self._tv_saled.column('#', anchor=W, width=25)
		self._tv_saled.column('Product', anchor=W, width=130)
		self._tv_saled.column('Qtdd', anchor=W, width=50)
		self._tv_saled.column('Prace', anchor=W, width=55)
		self._tv_saled.column('Total', anchor=W, width=65)

		self._tv_saled.heading('#0', text='', anchor=W)
		self._tv_saled.heading('#', text='#', anchor=W)
		self._tv_saled.heading('Product', text='Produto', anchor=W)
		self._tv_saled.heading('Qtdd', text='Qtdd', anchor=W)
		self._tv_saled.heading('Prace', text='Preço', anchor=W)
		self._tv_saled.heading('Total', text='Total', anchor=W)
		self._tv_saled.pack(side=LEFT, fill=BOTH, expand=True)

		self._sc_saled = Scrollbar(treeview_r, orient=VERTICAL)
		self._sc_saled.pack(side=LEFT, fill=Y, padx=(5, 0))

		self._tv_saled.config(yscrollcommand=self._sc_saled.set)
		self._sc_saled.config(command=self._tv_saled.yview)

		value_salebay = Frame(right)
		value_salebay.pack(fill='x', pady=(15, 20))

		saleby_frame = Frame(value_salebay)
		saleby_frame.pack(side='left', anchor='w')

		Label(saleby_frame, text='atendido por', style='Legend.TLabel').pack(anchor=W)
		self._lb_sale_by = Label(saleby_frame, text='---', style='Legend.TLabel')
		self._lb_sale_by.pack(anchor='w')

		value_frame = Frame(value_salebay)
		value_frame.pack(side='right', anchor='e')

		Label(value_frame, text='valor pago', style='Legend.TLabel').pack(anchor=E)
		self._lb_total_sale = Label(value_frame, text='0,00 AKZ', style='Data2.TLabel')
		self._lb_total_sale.pack()

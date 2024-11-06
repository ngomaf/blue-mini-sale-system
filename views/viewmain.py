from tkinter import PhotoImage, LEFT, RIGHT, TOP, VERTICAL, X, Y, W
from tkinter.ttk import Frame, Label, Button, Separator


class ViewMain:

	def __init__(self, mother, windows, frames):
		self._mother = mother

		self._main = Frame(self._mother)
		self._main.pack(fill=X, expand=True, padx=70)

		self._windows = windows

		self._frames = frames

		# -- inicializacao --
		self.show_widgets()
		self._user = []
	
	#  -- metodos --
	def set_user_logd(self, user):
		self._user = user

	def get_user_logd(self):
		return self._user

	# vender
	def show_sale(self):
		self.set_user_logd(self._windows[0].get_user())
		
		self._main.pack_forget()
		self._frames[0](self._mother, self)
	
	#  vendas
	def show_sales(self):
		self.set_user_logd(self._windows[0].get_user())
		
		self._main.pack_forget()
		self._frames[1](self._mother, self)
	
	#  produtos
	def show_products(self):
		self.set_user_logd(self._windows[0].get_user())
		
		self._main.pack_forget()
		self._frames[2](self._mother, self)
	
	#  definicoes de usuario
	def show_setting_user(self):
		self.set_user_logd(self._windows[0].get_user())
		
		self._main.pack_forget()
		self._frames[3](self._mother, self)

	def back_main(self):
		self._main.pack(fill=X, expand=True, padx=70)

	def out(self):
		# mostrar a janela login
		self._windows[0].get_win().iconify()
		self._windows[0].get_win().deiconify()

		# ocultar janela principal
		self._mother.withdraw()

	def set_user(self, user, type):
		self._bt_user_logd['text'] = user

		if type == 0: type = 'admin'
		elif type == 1: type = 'stok'
		elif type == 2: type = 'caixa'
		self._lb_type_user_logd['text'] = type

	def show_widgets(self):

		container = Frame(self._main)
		container.pack()

		# topo --------
		topo = Frame(container)
		topo.pack(fill=X, expand=True, pady=(0,15))

		img_logo = PhotoImage(file=r"components/icons/logo.png")
		lb_logo = Label(topo, text='', image=img_logo)
		lb_logo.image = img_logo
		lb_logo.pack(side=LEFT)

		img_out = PhotoImage(file=r"components/icons/main_sair.png")
		bt_out = Button(topo, text='Sair', width=3, cursor='hand1', style='Out.TButton', 
			image=img_out, compound=LEFT)
		bt_out.image = img_out
		bt_out['command'] = self.out
		bt_out.pack(side=RIGHT)

		# corpo --------------------------------
		body = Frame(container)
		body.pack(pady=(0,50))

		# esquerda
		left = Frame(body)
		left.pack(side=LEFT)

		# linha 1
		line1 = Frame(left)
		line1.pack(pady=(15))

		img_sale = PhotoImage(file=r"components/icons/main_vender.png")
		bt_sale = Button(line1, text='Vender', width=9, cursor='hand1', 
			style='Services.TButton', image=img_sale, compound=TOP)
		bt_sale.image = img_sale
		bt_sale['command'] = self.show_sale # remover () depois dos testes
		bt_sale.pack(side=LEFT)

		img_sales = PhotoImage(file=r"components/icons/main_vendas.png")
		bt_sales = Button(line1, text='Vendas', width=9, cursor='hand1', 
			style='Services.TButton', image=img_sales, compound=TOP)
		bt_sales.image = img_sales
		bt_sales['command'] = self.show_sales
		bt_sales.pack(side=LEFT, padx=15)

		img_products = PhotoImage(file=r"components/icons/main_produtos.png")
		bt_products = Button(line1, text='Produtos', width=9, cursor='hand1', 
			style='Services.TButton', image=img_products, compound=TOP)
		bt_products.image = img_products
		bt_products['command'] = self.show_products
		bt_products.pack(side=LEFT)

		# linha 2
		line2 = Frame(left)
		line2.pack(pady=(0, 15))

		img_clients = PhotoImage(file=r"components/icons/main_clientes_null.png")
		bt_clients = Button(line2, text='Clientes', width=9, cursor='hand1', 
			style='ServicesNull.TButton', takefocus=False, image=img_clients, compound=TOP)
		bt_clients.image = img_clients
		bt_clients.pack(side=LEFT)

		img_stok = PhotoImage(file=r"components/icons/main_stok_null.png")
		bt_stok = Button(line2, text='Stok', width=9, cursor='hand1', 
			style='ServicesNull.TButton', takefocus=False, image=img_stok, compound=TOP)
		bt_stok.image = img_stok
		bt_stok.pack(side=LEFT, padx=15)

		img_relat = PhotoImage(file=r"components/icons/main_relatorios_null.png")
		bt_relat = Button(line2, text='Relatórios', width=9, cursor='hand1', 
			style='ServicesNull.TButton', takefocus=False, image=img_relat, compound=TOP)
		bt_relat.image = img_relat
		bt_relat.pack(side=LEFT)

		# separador vertical
		Separator(body, orient=VERTICAL).pack(side=LEFT, fill=Y ,padx=55)

		# direita
		right = Frame(body)
		right.pack(side=LEFT)

		user = Frame(right)
		user.pack(pady=(5,40))

		img_logo = PhotoImage(file=r"components/icons/main_user.png")
		lb_logo = Label(user, text='', image=img_logo)
		lb_logo.image = img_logo
		lb_logo.pack(side=LEFT)

		user_type = Frame(user)
		user_type.pack(side=LEFT)
		self._bt_user_logd = Button(user_type, text='Utilizador', cursor='hand1', 
			style='UserMain.TButton')
		self._bt_user_logd.pack(anchor=W)
		self._lb_type_user_logd = Label(user_type, text='Tipo', style='User.TLabel')
		self._lb_type_user_logd.pack(anchor=W, padx=8)

		icon_fidelity = PhotoImage(file=r"components/icons/main_fidelizar_null.png")
		bt_fidelity = Button(right, text='  Fidelizar cliente', cursor='hand1', 
			style='OutNull.TButton', takefocus=False, image=icon_fidelity, compound=LEFT)
		bt_fidelity.image = icon_fidelity
		bt_fidelity.pack(anchor=W)

		icon_gstok = PhotoImage(file=r"components/icons/main_gstok_null.png")
		bt_gstok = Button(right, text='  Gestão de stok', cursor='hand1', 
			style='OutNull.TButton', takefocus=False, image=icon_gstok, compound=LEFT)
		bt_gstok.image = icon_gstok
		bt_gstok.pack(anchor=W, pady=5)

		icon_setting = PhotoImage(file=r"components/icons/main_definicoes.png")
		bt_setting = Button(right, text='  Definições dos\n  sistema', cursor='hand1', 
			style='Actions.TButton', image=icon_setting, compound=LEFT)
		bt_setting.image = icon_setting
		bt_setting['command'] = self.show_setting_user
		bt_setting.pack(anchor=W)

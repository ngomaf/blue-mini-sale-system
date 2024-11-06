from tkinter import PhotoImage, BooleanVar, messagebox
from tkinter import LEFT, RIGHT, CENTER, HORIZONTAL
from tkinter import BOTH, VERTICAL, NO, BOTH, X, Y, W, E
from tkinter import Entry as tkEntry
from tkinter import LabelFrame as tkLabelFrame
from tkinter.ttk import Frame, Label, Button, Combobox, Separator
from tkinter.ttk import Treeview, Scrollbar, Checkbutton

from models.modelsqlitesequence import ModelSQLiteSequence


class ViewSettUser:

	def __init__(self, mother, main, model):
		self._mother = mother
		self._main = main
		self._model = model
		self._lite_sequence = ModelSQLiteSequence()
		self._setting_user = Frame(mother)
		self._setting_user.pack(fill=X, padx=20)

		# não apagar (importante)
		# print(self._lite_sequence.get_datas())
		# print(self._lite_sequence.get_datas()[2][1])

		# --- inicializacao --------------------
		self._iam = self._main.get_user_logd()
		self._save_state = 0
		self.show_widgets()

	# metodo selecina um user
	def select_user(self):
		return self._tv_users.selection()

	def edit(self):
		if len(self.select_user()) != 0:
			self._id = self.select_user()[0]
			user = self._model.get_user(self._id)

			self.clear()
			self._save_state = 1
			self._et_user.focus_force()

			self._varstate.set(user[0][7])
			self.state_checkbox()
			self._cb_type.current(user[0][6])

			self._et_user.insert(0, user[0][1])
			# self._et_pass.insert(0, user[0][2])
			self._pass = user[0][2]
			self._et_fullname.insert(0, user[0][3])
			self._et_phone.insert(0, user[0][4])
			self._et_mail.insert(0, str(user[0][5]))
		else:
			self._lb_msg.configure(style='MsgError.TLabel')
			self._lb_msg['text'] = '<== Selecione um utilizador na tabela.'					
			self._tv_users.after(3000, self.empty_entry)

	def delete(self):
		
		self._lb_msg.configure(style='MsgError.TLabel')

		if len(self.select_user()) != 0:

			user = self._model.get_user(self.select_user()[0])

			#print(user[0][6])

			if user[0][6] != 0:

				action = messagebox.askokcancel('Cuidado!', 'Deseja realmente eliminar definitivamente o utilizador?')
				
				'''title = 'Cuidado!'
				content = 'Deseja realmente eliminar\ndefinitivamente o utilizador?'
				popup = self._main._windows[-1](self._mother, title, content)'''

				if action == True:
					id = self.select_user()[0]
					
					msg = self._model.delete(id)
					self._lb_msg['text'] = msg['content']
					self.search()
					self.clear()

					self._tv_users.after(3000, self.empty_entry)
			else:
				self._lb_msg['text'] = 'Não é permitio eliminar o administrador.'
				self._tv_users.after(3000, self.empty_entry)	
		else:
			self._lb_msg['text'] = '<== Selecione um utilizador na tabela.'					
			self._tv_users.after(3000, self.empty_entry)

	# metodo search
	def search(self):
		self.search_users('')

	def search_entry(self):
		self.search_users(self._et_search.get())

	def search_users(self, filter):
		self._total = 0
		list_users = self._model.get_users(filter)

		self._tv_users.delete(*self._tv_users.get_children())

		for n, user in enumerate(list_users):
			type = user[6]
			if type == 0: type = 'admin'
			elif type == 1: type = 'stok'
			elif type == 2: type = 'caixa'

			state = int(user[7])
			if state == 1: state = 'on'
			else: state = 'off'
			self._tv_users.insert(parent='', index=user[0], iid=user[0], text='', values=(n+1,user[1],user[4],type,state))
			self._total += 1

		self._lb_total['text'] = 'Total: ' + str(self._total)

	# metodo salvar utilizador
	def save_user(self):
		state = self._varstate.get()
		type = self._cb_type.current()

		user = self._et_user.get().strip()
		pswd = self._et_pass.get().strip()
		fullname = self._et_fullname.get().strip()
		phone = self._et_phone.get().strip()
		mail = self._et_mail.get().strip()

		if self._save_state == 0:
			if user != '':
				self._lf_user['fg'] = '#909090'
				if pswd != '':
					self._lf_pass['fg'] = '#909090'
					if fullname != '':
						self._lf_fullname['fg'] = '#909090'
						if phone != '':
							self._lf_phone['fg'] = '#909090'

							msg = self._model.set_user(user, pswd, fullname, phone, mail, type, state)

							if 'Sucesso!' in msg['title']:
								self._lb_msg.configure(style='MsgSucess.TLabel')
								self.search()
								self.clear()
							else:
								self._lb_msg.configure(style='MsgError.TLabel')

							self._lb_msg['text'] = msg['content']						
							self._tv_users.after(3000, self.empty_entry)

						else:
							self._lf_phone['fg'] = '#e0002c'
							self._et_phone.focus_force()
					else:
						self._lf_fullname['fg'] = '#e0002c'
						self._et_fullname.focus_force()
				else:
					self._lf_pass['fg'] = '#e0002c'
					self._et_pass.focus_force()
			else:
				self._lf_user['fg'] = '#e0002c'
				self._et_user.focus_force()
		else:
			id = self._id
			if pswd == '':
				pswd = self._pass
			
			msg = self._model.update(user, pswd, fullname, phone, mail, type, state, id)
			
			if 'Sucesso!' in msg['title']:
				self._lb_msg.configure(style='MsgSucess.TLabel')
				self.search()
				self.clear()
			else:
				self._lb_msg.configure(style='MsgError.TLabel')

			self._lb_msg['text'] = msg['content']						
			self._tv_users.after(3000, self.empty_entry)

	def empty_entry(self):
		self._lb_msg['text'] = ' '

	def clear(self):
		self._et_search.delete(0, 'end')
		self.search()
		self._save_state = 0
		self._et_user.focus_force()

		self._varstate.set(0)
		self.state_checkbox()
		self._cb_type.current(2)

		self._et_user.delete(0, 'end')
		self._et_pass.delete(0, 'end')
		self._et_fullname.delete(0, 'end')
		self._et_phone.delete(0, 'end')
		self._et_mail.delete(0, 'end')

		self._lf_user['fg'] = '#909090'
		self._lf_pass['fg'] = '#909090'
		self._lf_fullname['fg'] = '#909090'
		self._lf_phone['fg'] = '#909090'

	def back(self):
		self._setting_user.pack_forget()
		self._main.back_main()

	def state_checkbox(self):
		if self._cbu_state.instate(['!disabled', 'selected']):
			self._cbu_state['image'] = self._on_image
		else:
			self._cbu_state['image'] = self._off_image

	def show_widgets(self):

		pgraph = ('Montserrat', 10)
		pgraph_small = ('Montserrat', 8)

		top = Frame(self._setting_user)
		top.pack(fill=X, expand=True, pady=(20, 5))

		icon_setting_user = PhotoImage(file=r"components/icons/icon-settings_user.png")
		lb_setting_user = Label(top, text=' ', style='IconFrame.TLabel', image=icon_setting_user, 
			compound=LEFT)
		lb_setting_user.image = icon_setting_user
		lb_setting_user.pack(side=LEFT)

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

		Separator(self._setting_user, orient=HORIZONTAL).pack(fill=X)

		body = Frame(self._setting_user)
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
		self._lf_cod.pack(side=LEFT, pady=(5, 0))

		cod = ['Nome', 'Telefone', 'Email']
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

		self._tv_users = Treeview(treeview, selectmode="extended", height=13)
		self._tv_users['columns']=('#' ,'user', 'telephone', 'type', 'estate')
		self._tv_users.column('#0', width=0, stretch=NO)
		self._tv_users.column('#', anchor=W, width=25)
		self._tv_users.column('user', anchor=W, width=130)
		self._tv_users.column('telephone', anchor=W, width=140)
		self._tv_users.column('type', anchor=W, width=60)
		self._tv_users.column('estate', anchor=W, width=50)

		self._tv_users.heading('#0', text='', anchor=W)
		self._tv_users.heading('#', text='#', anchor=W)
		self._tv_users.heading('user', text='Utilizador', anchor=W)
		self._tv_users.heading('telephone', text='Telefone', anchor=W)
		self._tv_users.heading('type', text='Tipo', anchor=W)
		self._tv_users.heading('estate', text='Etdo', anchor=W)

		self._tv_users.pack(side=LEFT, fill=BOTH, expand=True)

		self._sc_users = Scrollbar(treeview, orient=VERTICAL)
		self._sc_users.pack(side=LEFT, fill=Y, padx=(5, 0))
		
		self._tv_users.config(yscrollcommand=self._sc_users.set)
		self._sc_users.config(command=self._tv_users.yview)

		self._lb_total = Label(left, text='', style='Legend.TLabel')
		self._lb_total.pack(anchor=E)

		self.search()

		# direita
		right = Frame(body, style='Side.TFrame', padding=(10, 5))
		right.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

		right_top = Frame(right)
		right_top.pack(fill=X)

		lf_cod = tkLabelFrame(right_top, font=pgraph_small, text='Código', fg='#909090', 
			width=5, bg='#f1f1f1', relief='ridge')
		lf_cod.pack(side=LEFT, anchor=W)

		self._et_cod = tkEntry(lf_cod, font=pgraph, fg='#333', relief='flat', takefocus=False, 
			width=5, bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_cod.insert(0, '00001')
		self._et_cod['state'] = 'readonly'
		self._et_cod.pack(padx=5, pady=(0, 3))

		state_type = Frame(right_top)
		state_type.pack(side=RIGHT, pady=(0, 10))

		lf_state = tkLabelFrame(state_type, text='Estado', labelanchor='e', font=pgraph_small, fg='#909090', 
			bg='#f1f1f1', relief='flat')
		lf_state.pack(side=LEFT, anchor=E, padx=5, pady=(15, 0))

		self._on_image = PhotoImage(file=r"components/icons/checkbox_checked.png")
		self._off_image = PhotoImage(file=r"components/icons/button_basic.png")
		self._varstate = BooleanVar(value=0)

		self._cbu_state = Checkbutton(lf_state, text='estado', image=self._off_image, variable=self._varstate, onvalue=1, 
			offvalue=0, command=self.state_checkbox, style='State.TCheckbutton', cursor='hand1')
		self._cbu_state.pack(side='left', anchor=E, padx=5)

		lf_type = tkLabelFrame(state_type, text='Tipo', font=pgraph_small, fg='#909090', 
			bg='#f1f1f1', relief='flat')
		lf_type.pack(side=LEFT, anchor=E, pady=(5, 0))

		type_itens = ['admin', 'stok', 'caixa']
		self._cb_type = Combobox(lf_type, values=type_itens, justify=CENTER, width=10)
		self._cb_type.current(2)
		self._cb_type['state'] = 'readonly'
		self._cb_type.pack(padx=5, pady=3)

		self._lb_msg = Label(right, text=' ') #, style='MsgError.TLabel'
		self._lb_msg.pack()

		self._lf_user = tkLabelFrame(right, font=pgraph, text='Utilizador*', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_user.pack(fill=X, pady=(5, 0))

		self._et_user = tkEntry(self._lf_user, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_user.focus_force()
		self._et_user.pack(fill=X, padx=5, pady=(0, 3))

		Label(right, text='Exemplo: zany.fortuna', style='LegendUsblity.TLabel').pack(anchor=E)

		self._lf_pass = tkLabelFrame(right, font=pgraph, text='Senha*', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_pass.pack(fill=X)

		self._et_pass = tkEntry(self._lf_pass, font=pgraph, fg='#333', relief='flat', 
			show='*', bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_pass.focus_force()
		self._et_pass.pack(fill=X, padx=5, pady=(0, 3))

		Label(right, text='Exemplo: ZanyforT19!', style='LegendUsblity.TLabel').pack(anchor=E)

		self._lf_fullname = tkLabelFrame(right, font=pgraph, text='Nome completo*', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_fullname.pack(fill=X)

		self._et_fullname = tkEntry(self._lf_fullname, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_fullname.focus_force()
		self._et_fullname.pack(fill=X, padx=5, pady=(0, 3))

		phone_mail = Frame(right)
		phone_mail.pack(fill=X, pady=(10, 0))

		self._lf_phone = tkLabelFrame(phone_mail, font=pgraph, text='Telefone*', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_phone.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

		self._et_phone = tkEntry(self._lf_phone, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_phone.focus_force()
		self._et_phone.pack(fill=X, padx=5, pady=(0, 3))

		self._lf_mail = tkLabelFrame(phone_mail, font=pgraph, text='E-mail', fg='#909090', 
			bg='#f1f1f1', relief='ridge')
		self._lf_mail.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

		self._et_mail = tkEntry(self._lf_mail, font=pgraph, fg='#333', relief='flat', 
			bg='#f1f1f1', highlightbackground='#f1f1f1', highlightcolor='#f1f1f1')
		self._et_mail.focus_force()
		self._et_mail.pack(fill=X, padx=5, pady=(0, 3))

		Button(right, text='Salvar', command=self.save_user, cursor='hand1', style='Sale.TButton').pack(fill=X, pady=(15, 5))
		Button(right, text='Limpar', command=self.clear, cursor='hand1', style='Clear.TButton').pack(fill=X, pady=(0, 5))

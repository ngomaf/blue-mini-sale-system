from tkinter import Tk, Frame, LabelFrame, PhotoImage, BOTH, LEFT, X, Toplevel
from tkinter import INSERT
from tkinter import Entry as tkEntry
from tkinter.constants import CENTER, LEFT
from tkinter.ttk import Entry, Label, Button


class ViewWinLogin:

    def __init__(self, mother, model, app):
        self._mother = mother
        self._model = model
        self._app = app
        self._win = Toplevel(self._mother)

        self._win.title('Entrar')
        self._win.geometry('500x460+100+50')
        self._win.configure(bg='white')

        self._win.resizable(False, False)
        self._win.iconphoto(False, PhotoImage(file='components/icons/svicon.png'))
        self._win.focus_force()
        # self._win.grab_set()

        self._corpo = Frame(self._win, bg='white')
        self._corpo.pack()

        # inicializacao
        self._user = []
        self._timer = 0
        self._timer2 = 0

        # exibir widgets
        self.show_widgets()

        self._win.protocol("WM_DELETE_WINDOW", self.on_closing)


    def show_root(self):

    	if (self._et_user.get() != '' and self._timer == 0) or self._timer2 == 1: # trovar par != depois dos testes
    		
            user = self._et_user.get()
            pswd = self._et_pass.get()

            user_db = self._model.login(user)
            
            # verificar se o retoron é uma lista e se a mesma é > 0
            if type(user_db) is list and len(user_db) > 0:
                
                if user == user_db[0][1] and pswd == user_db[0][2]:

                    if  int(user_db[0][7]) == 1: # verificar estado

                        self._et_user.delete(0, 'end')
                        self._et_pass.delete(0, 'end')
                        self._et_user.focus_force()

                        # set usr
                        self.set_user(user_db)
                        self._app.set_user(user_db[0][3], user_db[0][6])

                        # tornar a root vizivel
                        self._mother.iconify()
                        self._mother.deiconify()

                        # Ocultar janela login
                        self._win.withdraw()
                    else:
                        self._timer2 = 1
                        self._lb_msg_error['text'] = 'Por favor, contacte o admintrador.'
                        self._win.after(2000, self.empty_entry)
                else:
                    self._timer2 = 1
                    self._lb_msg_error['text'] = '[Erro!] Utilizador ou senha incorrecta.'
                    self._win.after(2000, self.empty_entry)
            else:
                self._timer2 = 1
                self._lb_msg_error['text'] = '[Erro!] Utilizador ou senha incorrecta.'
                self._win.after(2000, self.empty_entry)
    	else:
            self._timer = 1
            self._lb_msg_error['text'] = '[Erro!] Campo vázio.'
            self._win.after(3000, self.empty_entry)

    def empty_entry(self):
        self._lb_msg_error['text'] = ' '
        self._timer = 0
        self._et_user.focus_force()

    def on_closing(self):
        self._mother.destroy()

    def get_win(self):
        return self._win

    def get_user(self):
        return self._user

    def set_user(self, user):
        self._user = user

    def show_widgets(self):
        pgraph = ('Montserrat', 12)
        pgraph_small = ('Montserrat', 10)

        self._img_logo = PhotoImage(file=r"components/icons/logo.png")
        self._lb_logo = Label(self._corpo, text='', image=self._img_logo, 
        	style='Login.TLabel')
        self._lb_logo.image = self._img_logo
        self._lb_logo.pack(pady=(50,0))

        Label(self._corpo, text='Entra com as suas crecenciais aqui.', 
        	style='Login.TLabel').pack(pady=(10,20))

        # utilizador
        self._lf_user = LabelFrame(self._corpo, font=pgraph_small, text='Utilizador', fg='#909090', 
            width=5, bg='white', relief='ridge')
        self._lf_user.pack(pady=5)

        self._et_user = tkEntry(self._lf_user, font=pgraph, fg='#666', relief='flat', 
            width=25, highlightbackground='white', highlightcolor='white')
        self._et_user.focus_force()
        self._et_user.insert(0, 'zany.fortuna')
        self._et_user.pack(side=LEFT, padx=5)

        self._icon_person = PhotoImage(file=r"components/icons/login_person.png")
        self._lb_person = Label(self._lf_user, text='', style='Login.TLabel', 
        	image=self._icon_person)
        self._lb_person.image = self._icon_person
        self._lb_person.pack(side=LEFT, padx=5, pady=5)

        # senha
        self._lf_pass = LabelFrame(self._corpo, font=pgraph_small, text='Senha', fg='#909090', 
            bg='white', relief='ridge')
        self._lf_pass.pack(pady=(0, 8))

        self._et_pass = tkEntry(self._lf_pass, font=pgraph, fg='#666', relief='flat', 
            width=25, show='*', highlightbackground='white', highlightcolor='white')
        self._et_pass.insert(0, 'Mt13')
        self._et_pass.pack(side=LEFT, padx=5)

        self._icon_key = PhotoImage(file=r"components/icons/login_key.png")
        self._lb_pass = Label(self._lf_pass, text='', style='Login.TLabel', 
            image=self._icon_key)
        self._lb_pass.image = self._icon_key
        self._lb_pass.pack(side=LEFT, padx=5, pady=5)

        self._lb_msg_error = Label(self._corpo, text=' ', style='MsgErrorLogin.TLabel')
        self._lb_msg_error.pack()

        # botao entrar
        Button(self._corpo, text='Entrar »', style='Login.TButton', cursor='hand1', 
        command=self.show_root).pack(fill=X, expand=True, pady=(8, 25)) # remover () depois dos testes

        text_login = '''Se não lembras as tuas credencias não êxite em nos\ncontactar pelo terminal +244 926 043 182.'''
        Label(self._corpo, text=text_login, style='LoginSmal.TLabel').pack()

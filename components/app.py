from tkinter import Tk, PhotoImage, CENTER, FLAT, RIDGE
from tkinter.ttk import Style

from controllers.ctrlwinlogin import CtrlWinLogin
from controllers.ctrlwinpopupask import CtrlWinPopupAsk

from controllers.ctrlmain import CtrlMain
from controllers.ctrlsale import CtrlSale
from controllers.ctrlsales import CtrlSales
from controllers.ctrlproducts import CtrlProducts

from controllers.ctrlsettuser import CtrlSettUser


class App:

    # __slots__ = ['']

    def __init__(self):
        self._root = Tk()

        # ocultar main
        self._root.withdraw()

        # controllers em accao -----------
        # janelas 
        self._win_login = CtrlWinLogin(self._root, self)

        # alocacao de janelas e frames para a main
        windows = [self._win_login, CtrlWinPopupAsk]
        frames = [CtrlSale, CtrlSales, CtrlProducts, CtrlSettUser]
        self._main = CtrlMain(self._root, windows, frames)


        # fontes
        pfonte=('Montserrat', 8)
        pbfonte=('Montserrat', 8, 'bold')
        psfonte=('Montserrat', 10)
        psbfonte=('Montserrat', 10, 'bold')
        pmfonte=('Montserrat', 12)
        pmbfonte=('Montserrat', 12, 'bold')
        TPfonte = ('Montserrat', 18, 'bold')

        # estilo
        style = Style()
        style.theme_use('default') # clam
        
        style.configure('TFrame', background='#f1f1f1')
        style.configure('TLabel', font=psfonte, background='#f1f1f1')
        style.configure('User.TLabel', font=psfonte, foreground='#909090', background='#f1f1f1')
        style.configure('Out.TButton', font=psbfonte, foreground='#e0002c', background='#f1f1f1')
        style.configure('OutNull.TButton', font=psbfonte, foreground='#ccc', background='#f1f1f1')
        style.configure('Services.TButton', font=psbfonte, foreground='#909090', padding=10, relief=FLAT, background='#f1f1f1', borderwidth=2)
        style.configure('ServicesNull.TButton', font=psbfonte, foreground='#ccc', background='#f1f1f1', padding=10, relief=FLAT, borderwidth=2, highlightbackground='#ccc', highlightcolor='#f1f1f1')
        style.configure('UserMain.TButton', font=psbfonte, foreground='#188fdd', background='#f1f1f1', relief=FLAT)
        style.configure('Actions.TButton', font=psfonte, foreground='#909090', background='#f1f1f1')

        # map
        style.map('Out.TButton',
             foreground=[('pressed', 'orange'), ('active', '#FF3059')],
             background=[('pressed', '!focus', '#375777'), ('active', '#f1f1f1')],
             highlightcolor=[('focus', 'green'), ('!focus', 'red')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        style.map('OutNull.TButton',
             foreground=[('pressed', '#ccc'), ('active', '#ccc')],
             background=[('pressed', '!focus', '#f1f1f1'), ('active', '#f1f1f1')],
             # highlightcolor=[('focus', 'green'), ('!focus', 'red')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        style.map('Services.TButton',
            foreground=[('pressed', 'orange'), ('active', '#188fdd')],
            background=[('pressed', '!focus', '#375777'), ('active', 'white')],
            highlightcolor=[('focus', 'green'), ('!focus', 'red')],
            relief=[('pressed', 'flat'), ('!pressed', 'ridge')])

        style.map('ServicesNull.TButton',
            foreground=[('pressed', '#ccc'), ('active', '#ccc')],
            background=[('pressed', '!focus', '#f1f1f1'), ('active', '#f1f1f1')],
            #highlightcolor=[('focus', 'green'), ('!focus', 'red')],
            relief=[('pressed', 'ridge'), ('!pressed', 'ridge')])

        style.map('UserMain.TButton',
             foreground=[('pressed', 'orange'), ('active', '#26AAFF')],
             background=[('pressed', '!focus', '#375777'), ('active', '#f1f1f1')],
             highlightcolor=[('focus', 'green'), ('!focus', 'red')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        style.map('Actions.TButton',
             foreground=[('pressed', 'orange'), ('active', '#ff652b')],
             background=[('pressed', '!focus', '#375777'), ('active', '#f1f1f1')],
             highlightcolor=[('focus', 'green'), ('!focus', 'red')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        # frame vendas
        style.configure('IconFrame.TLabel', font=psbfonte, foreground='#188fdd', background='#f1f1f1')
        style.configure('HTree.TLabel', padding=5, font=psbfonte, foreground='#333', background='#E6E3E3', relief=FLAT)
        style.configure('Side.TFrame', relief=RIDGE, borderwidth=2)
        style.configure('TCombobox', background='#f1f1f1', font=psfonte, padding=(0, 5), borderwidth=0)
        style.configure('Legend.TLabel', font=psfonte, foreground='#909090', background='#f1f1f1', relief=FLAT)
        style.configure('LegendUsblity.TLabel', font=pfonte, foreground='#909090', background='#f1f1f1', relief=FLAT)
        style.configure('Data.TLabel', font=pmfonte, foreground='#333', background='#f1f1f1', relief=FLAT)
        style.configure('Data2.TLabel', font=pmbfonte, foreground='#333', background='#f1f1f1', relief=FLAT)
        style.configure('Treeview', font=psfonte, borderwidth=0, background='#E6E6E6')
        style.configure('Heading', font=psbfonte, padding=(4, 8), borderwidth=0, relief=RIDGE, background='#D8D8D8')
        style.configure('Vertical.TScrollbar', width=4, borderwidth=0, arrowsize=4, arrowcolor='#188fdd', background='#188fdd', troughtcolor='#E6E6E6', relief='ridge')

        style.map('Treeview',
            background=[('selected', '#188fdd')])

        style.map('Vertical.TScrollbar',
             arrowcolor=[('pressed', '#188fdd'), ('active', '#26AAFF')],
             background=[('pressed', '!focus', '#188fdd'), ('active', '#26AAFF')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        # frame vender
        style.configure('Lancar.TButton', font=psbfonte, foreground='white', background='#ff652b', padding=10, borderwidth=0)
        style.configure('Sale.TButton', font=psbfonte, foreground='white', background='#14bb14', padding=10, borderwidth=0)
        style.configure('Clear.TButton', font=psbfonte, foreground='white', background='#e0002c', padding=10, borderwidth=0)
        style.configure('Remove.TButton', font=psbfonte, foreground='white', background='#c5c5c5', padding=6, borderwidth=0)

        # map
        style.map('Lancar.TButton',
             foreground=[('pressed', 'orange'), ('active', '#fff')],
             background=[('pressed', '!focus', '#375777'), ('active', '#FF7744')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        style.map('Sale.TButton',
             foreground=[('pressed', 'orange'), ('active', '#fff')],
             background=[('pressed', '!focus', '#375777'), ('active', '#16EA16')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        style.map('Clear.TButton',
             foreground=[('pressed', 'orange'), ('active', '#fff')],
             background=[('pressed', '!focus', '#375777'), ('active', '#FF3059')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        style.map('Remove.TButton',
             foreground=[('pressed', 'orange'), ('active', '#fff')],
             background=[('pressed', '!focus', '#375777'), ('active', 'gray')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        # frame settings
        # user
        style.configure('State.TCheckbutton', background='#f1f1f1', font=psfonte, padding=(0, 5), borderwidth=0)
        
        style.layout('State.TCheckbutton',
         [('Checkbutton.padding', {'sticky': 'nswe', 'children': [
             ('Checkbutton.focus', {'side': 'left', 'sticky': 'w',
                                    'children':
                                    [('Checkbutton.label', {'sticky': 'nswe'})]})]})]
         )

        # janela login
        style.configure('Login.TLabel', font=psfonte, foreground='#909090', 
            background='white')
        style.configure('LoginSmal.TLabel', font=pfonte, justify=CENTER, foreground='#909090', 
            background='white')
        style.configure('MsgErrorLogin.TLabel', font=psfonte, foreground='#e0002c', background='white')
        style.configure('MsgError.TLabel', font=psfonte, padding=(3, 0), foreground='#e0002c', background='#f1f1f1')
        style.configure('MsgSucess.TLabel', font=psfonte, padding=(3, 0), foreground='#14bb14', background='#f1f1f1')
        style.configure('Login.TButton', font=psbfonte, padding=(10, 15), foreground='white', background='#188fdd')

        # map
        style.map('Login.TButton',
             foreground=[('pressed', 'orange'), ('active', '#fff')],
             background=[('pressed', '!focus', '#375777'), ('active', '#26AAFF')],
             relief=[('pressed', 'groove'), ('!pressed', 'flat')])

        # janelas popup
        style.configure('TitlePop.TLabel', font=TPfonte, foreground='#188fdd', background='white')
        style.configure('ContentPop.TLabel', font=pmfonte, justify='center', foreground='#188fdd', background='white')
        style.configure('Popup.TButton', font=psbfonte, foreground='white', background='#188fdd', padding=10,
                        borderwidth=0)
        style.map('Popup.TButton',
                  foreground=[('pressed', 'orange'), ('active', '#fff')],
                  background=[('pressed', '!focus', '#375777'), ('active', '#26AAFF')],
                  relief=[('pressed', 'groove'), ('!pressed', 'flat')])

    def set_user(self, user, type):
        self._main.set_user(user, type)

    def run(self):
        self._root.title('Sistema de vendas')
        self._root.geometry('800x530+100+100')
        self._root.minsize(800, 500)
        self._root.configure(bg='#f1f1f1')
        self._root.iconphoto(False, PhotoImage(file='components/icons/svicon.png'))
        # self._root.resizable(False, False)
        self._root.mainloop()

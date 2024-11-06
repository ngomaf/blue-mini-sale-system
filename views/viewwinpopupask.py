from tkinter import Tk, PhotoImage, Toplevel
from tkinter.ttk import Frame, Label, Button


class ViewWinPopupAsk:

    def __init__(self, mother, title, content):
        self._mother = mother
        self._win = Toplevel(self._mother)

        self._win.title(title)
        self._win.geometry('400x280')
        self._win.configure(bg='white')

        self._win.resizable(False, False)
        self._win.iconphoto(False, PhotoImage(file='components/icons/svicon.png'))
        self._win.focus_force()
        # self._win.grab_set()

        icon_pop = PhotoImage(file=r'components/icons/popup_question.png')
        lb_icon = Label(self._win, text='', image = icon_pop)
        lb_icon.image = icon_pop
        lb_icon.pack(pady=(30, 10))

        Label(self._win, text=title, style='TitlePop.TLabel').pack(pady=(0, 10))

        Label(self._win, text=content, style='ContentPop.TLabel').pack(pady=(0, 25))

        buttons = Frame(self._win)
        buttons.pack(side='bottom', anchor='s', fill='x', expand=True)

        Button(buttons, text='Sim', command=self.yes, style='Popup.TButton'
               ).pack(side='left', fill='x', expand=True, padx=(0, 1))
        Button(buttons, text='Não', command=self._win.destroy, style='Popup.TButton').pack(side='left', fill='x', expand=True)

    def yes(self):
        print(True)
        self._win.destroy()
        return True
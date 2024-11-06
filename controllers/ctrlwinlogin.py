from views.viewwinlogin import ViewWinLogin
from models.modelsettuser import ModelSettUser

class CtrlWinLogin:

    def __init__(self, mother, app):
        self._model = ModelSettUser()
        self._view = ViewWinLogin(mother, self._model, app)

    def get_win(self):
        return self._view.get_win()

    def get_user(self):
        return self._view.get_user()
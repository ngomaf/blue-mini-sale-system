from models.modelsettuser import ModelSettUser
from views.viewsettuser import ViewSettUser



class CtrlSettUser:

	def __init__(self, mother, main_win):
		self._model = ModelSettUser()
		self._view = ViewSettUser(mother, main_win, self._model)


from views.viewproducts import ViewProducts
from models.modelproducts import ModelProducts


class CtrlProducts:
	
	def __init__(self, mother, main_win):
		self._model = ModelProducts()
		self._view = ViewProducts(mother, main_win, self._model)

from models.modelproducts import ModelProducts
from models.modelsale import ModelSale
from views.viewsale import ViewSale


class CtrlSale:
	
	def __init__(self, mother, main_win):
		self._model = ModelProducts()
		self._mdsale = ModelSale()
		self._view = ViewSale(mother, main_win, self._model, self._mdsale)

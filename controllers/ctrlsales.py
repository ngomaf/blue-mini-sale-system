
from models.modelsale import ModelSale
from views.viewsales import ViewSales


class CtrlSales:
	
	def __init__(self, mother, main_win):
		self._model = ModelSale()
		self._view = ViewSales(mother, main_win, self._model)

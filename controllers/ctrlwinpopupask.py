
from views.viewwinpopupask import ViewWinPopupAsk


class CtrlWinPopupAsk:
	
	def __init__(self, mother, title, content):
		self._view = ViewWinPopupAsk(mother, title, content)
from views.viewmain import ViewMain


class CtrlMain:

	def __init__(self, mother, windows, frames):
		self._view = ViewMain(mother, windows, frames)

	def set_user(self, user, type):
		self._view.set_user(user, type)

import sqlite3



class DB:

	__slots__ = ['_connection', '_cursor', '_table']
	
	def __init__(self, tb_name):
		self._connection = sqlite3.connect('components/database/svenda_bd.sqlite')
		self._cursor = self._connection.cursor()
		self._table = tb_name

	def get_table(self):
		return self._table
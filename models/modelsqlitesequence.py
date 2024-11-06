from components.db import DB


class ModelSQLiteSequence:

	def __init__(self):
		self._db = DB('sqlite_sequence')

	def get_datas(self):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()}'
			self._db._cursor.execute(sql_query)
			datas = self._db._cursor.fetchall()

			return datas
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelProducts->get_products(): {ex}')
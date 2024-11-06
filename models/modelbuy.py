from components.db import DB


class ModelBuy:

	def __init__(self):
		self._db = DB('sv_buys')

	def get_buys(self, sale):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE sale={sale}'
			self._db._cursor.execute(sql_query)
			buy = self._db._cursor.fetchall()

			return buy
		except Exception as ex:
			print(f'Error in ModelBuy->get_buys(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def set_buy(self, sale, product, qtidade):
		try:
			sql_query = f'INSERT INTO {self._db.get_table()} (sale, product, qtidade) VALUES (?,?,?)'
			sql_args = [sale, product, qtidade]
			self._db._cursor.execute(sql_query, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Compra efectuada com sucesso.'}
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelBuy->set_buy(): {ex}')

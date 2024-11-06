from components.db import DB


class ModelSale:

	def __init__(self):
		self._db = DB('sv_sales')

	def get_sales(self, filter):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE client LIKE "{filter}%" ORDER BY id DESC'
			self._db._cursor.execute(sql_query)
			sales = self._db._cursor.fetchall()

			return sales
		except Exception as ex:
			print(f'Error in ModelSales->get_sales(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def get_sale(self, id):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE id={id}'
			self._db._cursor.execute(sql_query)
			sale = self._db._cursor.fetchall()

			return sale
		except Exception as ex:
			print(f'Error in ModelSales->get_sale(): {ex}')
			return {'title': 'Erro', 'content': f'{ex}'}

	def set_sale(self, user, client, buy, total_many, date):
		try:
			sql_query = f'INSERT INTO {self._db.get_table()} (user, client, buy, total_many, date) VALUES (?,?,?,?,?)'
			sql_args = [user, client, buy, total_many, date]
			self._db._cursor.execute(sql_query, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Venda efectuada com sucesso.'}
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelSale->set_sale(): {ex}')

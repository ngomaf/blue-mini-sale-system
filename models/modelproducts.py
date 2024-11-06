from components.db import DB


class ModelProducts:

	def __init__(self):
		self._db = DB('sv_products')

	def get_products(self, filter):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE product LIKE "{filter}%" ORDER BY product'
			self._db._cursor.execute(sql_query)
			products = self._db._cursor.fetchall()

			return products
		except Exception as ex:
			print(f'Error in ModelProducts->get_products(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def get_product(self, id):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE id={id}'
			self._db._cursor.execute(sql_query)
			product = self._db._cursor.fetchall()

			return product
		except Exception as ex:
			print(f'Error in ModelProducts->get_product(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def set_product(self, cod, product, qtdade, praceunit, description, state):
		try:
			sql_query = f'INSERT INTO {self._db.get_table()} (cod, product, qtdade, praceunit, description, state) VALUES (?,?,?,?,?,?)'
			sql_args = [cod, product, qtdade, praceunit, description, state]
			self._db._cursor.execute(sql_query, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Produto cadastrado com sucesso.'}			
		except Exception as ex:
			print(f'Error in ModelProducts->set_set(): {ex}')
			return {'title': 'Erro', 'content': f'{ex}'}

	def update(self, product, qtdade, prace, description, state, id):
		try:
			sql_query = f'UPDATE {self._db.get_table()} SET product=?, qtdade=?, praceunit=?, description=?, state=? WHERE id=?'
			sql_args = [product, qtdade, prace, description, state, id]
			self._db._cursor.execute(sql_query, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Produto actualizado com sucesso.'}
		except Exception as ex:
			print(f'Error in ModelProducts->update(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def less_product(self, value, id):
		try:
			sql_query = f'UPDATE {self._db.get_table()} SET qtdade = qtdade - {value} WHERE id={id}'
			self._db._cursor.execute(sql_query)
			self._db._connection.commit()

			total = self.get_product(id)
			if int(total[0][3]) < 1:
				sql_query2 = f'UPDATE {self._db.get_table()} SET state={0} WHERE id={id}'
				self._db._cursor.execute(sql_query2)
				self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Diminuição executada com sucesso.'}
		except Exception as ex:
			print(f'Error in ModelProducts->less_product(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

	def delete(self, id):
		try:
			sql_query = f'DELETE FROM {self._db.get_table()} WHERE id={id}'
			self._db._cursor.execute(sql_query)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Produto eliminado.'}
		except Exception as ex:
			print(f'Error in ModelProducts->update(): {ex}')
			return {'title': 'Erro!', 'content': f'{ex}'}

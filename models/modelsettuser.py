from components.db import DB


class ModelSettUser:

	def __init__(self):
		self._db = DB('sv_users')

	# entrar
	def login(self, login_name):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE user="{login_name}"'
			self._db._cursor.execute(sql_query)
			user = self._db._cursor.fetchall()

			return user
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->get_users(): {ex}')

	# buscar lista usuarios por nome de utilizador
	def get_users(self, filter):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE user LIKE "{filter}%" ORDER BY user'
			self._db._cursor.execute(sql_query)
			list_users = self._db._cursor.fetchall()

			return list_users
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->get_users(): {ex}')

	# buscar user por id
	def get_user(self, id):
		try:
			sql_query = f'SELECT * FROM {self._db.get_table()} WHERE id={id}'
			self._db._cursor.execute(sql_query)
			user = self._db._cursor.fetchall()

			return user
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->get_user(): {ex}')

	# cadastrar utilizador
	def set_user(self, user, pswd, fullname, phone, mail, type, state):
		try:
			sql_user = (f'INSERT INTO {self._db.get_table()} (user, pass, fullname, phone, mail, type, state) VALUES (?,?,?,?,?,?,?)')
			sql_args = [user, pswd, fullname, phone, mail, type, state]
			self._db._cursor.execute(sql_user, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Utilizador cadastrado com sucesso.'}
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->set_user(): {ex}')

	# actualizar utilizador
	def update(self, user, pswd, fullname, phone, mail, type, state, id):
		try:
			sql_query = f'UPDATE {self._db.get_table()} SET user=?, pass=?, fullname=?, phone=?, mail=?, type=?, state=? WHERE id=?'
			sql_args = ([user, pswd, fullname, phone, mail, type, state, id])
			self._db._cursor.execute(sql_query, sql_args)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Utilizador actualizado com sucesso.'}
		except Exception as ex:
			return {'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->update(): {ex}')

	def delete(self, id):
		try:
			sql_query = f'DELETE FROM {self._db.get_table()} WHERE id = {id}'
			self._db._cursor.execute(sql_query)
			self._db._connection.commit()

			return {'title': 'Sucesso!', 'content': 'Utilizador eliminado.'}
		except Exception as ex:
			return {f'title': 'Erro!', 'content': f'{ex}'}
			print(f'Error in ModelUser->delete: {ex}')

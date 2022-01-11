class User:

	# using _id isntead of id, as id is a python keyword
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password
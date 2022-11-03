from description_indexer.dao_plugins import DaoSystem

class MySystem(DaoSystem):
	dao_system_name = "example"

	def __init__(self):
		print (f"Setup {self.dao_system_name} dao system for reading digital object data.")

		# Set up any prerequisites or checks here

	def read_data(dao):
		print ("reading data from " + dao.href + "?format=json")
		
		# Add or override dao here
		# dao.metadata = {}

		return dao

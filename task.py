class Task():
	'''A class containing information for a task'''
	def __init__(self,name,completed=False):
		self.name = name
		self.completed = completed
	

	def get_task(self):
		return [self.name,self.completed]

	def set_completed(self):
		self.completed = True


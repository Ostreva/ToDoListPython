import json
from task import Task


def get_stored_users(file_name='usernames.json'):
	'''Get stored username if available'''
	user_names = []
	try:
		with open(file_name) as file_object:
			user_names = json.load(file_object)
	except FileNotFoundError:
		pass
	return user_names

def set_new_username(user_names, user_name,file_name='usernames.json'):
	'''Prompt for new username'''
	
	response = input("Could not find user name. Would you like me to set '" + 
					user_name +"' as your user name Y/N? ")
	if(response.upper() == "Y"):
		with open(file_name, 'w') as file_object:
			user_names.append(user_name.lower())
			json.dump(user_names,file_object)
		return True
	return False

def check_username():
	'''Find user or ask if set new user'''
	user_name = input("What is your user name? ")
	user_names = []
	user_names = get_stored_users()
	if(user_names and user_name in user_names):
		print("hello " + user_name)
	else:
		if(set_new_username(user_names, user_name)):
			print("hello new user: " + user_name)
		else:
			print("Did not set new user. Quitting application :(")
			user_name = None
	return user_name

def set_task(users_tasks,new_tasks,a_task):
	'''append new task to current and new task lists'''
	users_tasks.append(a_task.get_task())
	new_tasks.append(a_task.get_task())


def print_all_current_tasks(users_tasks,start_id=0):
	'''print all tasks that need to be completed'''
	print("All tasks that need to be completed:")
	print("\tID\tTask")
	for i in range(0,len(users_tasks)):
		if not users_tasks[i][1]:
			print('\t' + str(i+start_id) +'\t'+ users_tasks[i][0])

def set_complete(task_id, users_tasks,new_tasks):
	'''set task to completed'''
	length = len(users_tasks)
	if(task_id >= length or task_id < 0):
		print("Could not find task id")
	else:
		users_tasks[task_id][1] = True
		new_length = len(new_tasks)
		new_id = task_id - (length - new_length)
		print(new_id)
		if( new_id < new_length and new_id >= 0):
			new_tasks[new_id][1] = True

def print_all_completed_tasks(users_tasks):
	'''print all tasks that have been completed'''
	print("All tasks that have been completed:")
	print("\tID\tTask")
	for i in range(0,len(users_tasks)):
		if users_tasks[i][1]:
			print('\t' + str(i) +'\t'+ users_tasks[i][0])

def print_all(users_tasks):
	print("All tasks:")
	print("\tID\tTask\tCompletion")
	for i in range(0,len(users_tasks)):
		print('\t' + str(i) +
			'\t' + users_tasks[i][0] + 
			'\t' + str(users_tasks[i][1]))

def print_new_tasks(new_tasks,start_id):
	'''print all new tasks 
	that need to be completed'''
	print("For new tasks")
	print_all_current_tasks(new_tasks,start_id)

def get_help():
	'''print commands and descriptions'''
	main_menu = {
				'add':'add a new task',
				'current':'show task id and tasks that are not completed', 
				'completed': 'show completed tasks and task id', 
				'mark':'check task as complete, need task ID', 
				'all': 'Show task ID, task info, and completion',
				'new':'Show task id and new tasks added this session that are not completed'
			}
	print('Here are the commands to run\n')
	for key, val in main_menu.items():
		print(key, ' : ', val)
	print()

def mark_task(users_tasks, new_tasks):
	'''gets user input for task id'''
	task_id = input('What is the task id you want to mark as completed? ')
	try:
		val = int(task_id)
		set_complete(val, users_tasks,new_tasks)
	except ValueError:
		print('That is not an int!')

def get_users_tasks(user_name):
	'''Get the stored tasks for this user'''
	users_tasks = get_all_tasks()
	if(user_name in users_tasks):
		return users_tasks[user_name]
	return []

def get_all_tasks():
	'''Get all tasks for all users'''
	user_names = {}
	file_name = 'userstasks.json'
	try:
		with open(file_name) as file_object:
			user_names = json.load(file_object)
	except FileNotFoundError:
		pass
	return user_names

def save_users_tasks(user_name,user_tasks):
	'''add tasks to task file for this user'''
	file_name = 'userstasks.json'
	users = get_all_tasks()
	users[user_name] = user_tasks
	with open(file_name, 'w') as file_object:
		json.dump(users,file_object)
		

def run_tasks(user_name):
	'''Main loop for to do list'''
	users_tasks = get_users_tasks(user_name)
	response = ''
	start_id = len(users_tasks)
	new_tasks = []
	while(response.lower() != 'q'):
		response = input('What would you like to do?'+
					'(Push "q" to quit or "h" for help) ').lower()
		if(response == 'h'):
			get_help()
		elif(response == 'add'):
			my_task = Task(input('Please enter a new task: '))
			set_task(users_tasks,new_tasks,my_task)
		elif(response == 'current'):
			print_all_current_tasks(users_tasks)
		elif(response == 'completed'):
			print_all_completed_tasks(users_tasks)
		elif(response == 'mark'):
			mark_task(users_tasks, new_tasks)
		elif(response == 'all'):
			print_all(users_tasks)
		elif(response == 'new'):
			print_new_tasks(new_tasks,start_id)
		elif(response != 'q'):
			print('Command not recognized')
	save_users_tasks(user_name, users_tasks)

if __name__ == '__main__':
	user_name = check_username()
	if(user_name):
		run_tasks(user_name)





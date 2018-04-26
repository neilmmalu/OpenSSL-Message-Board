from datetime import datetime
import json

OUTFILE = 'board.json'

def create_message_wrapper(user_name, group, message):
	return {'user': user_name, 'group': group, 'message': message, 'time': datetime.now().strftime("%A, %d. %B %Y %I:%M%p")}
	message

def get_messages(group):
	data = json.load(open(OUTFILE))
	try:
		if data.has_key(group):
			messages = data[group]
			return messages
	except:
		print 'Exception when GETing message'
	return []

def post_message(user_name, group, message_text):
	try:
		message = create_message_wrapper(user_name, group, message_text)
		data = json.load(open(OUTFILE))
		if data.has_key(group):
			data[group].append(message)
		else:
			data[group] = [message]
		with open(OUTFILE, 'w') as json_file:
			json.dump(data, json_file)
	except:
		print 'Exception when POSTing message'
		return False


if __name__ == '__main__':
	user_name = 'Joe'
	group = 'Penn State'
	message = 'I hate everything :('
	print post_message(user_name, group, message)
	# print get_messages('Rutgers')


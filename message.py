'''
	This module contains all functions pertaining to message objects including creation and fetching.
'''
from datetime import datetime
import json

OUTFILE = 'board.json'

def create_message_wrapper(user_name, group, message):
	''' This function is used to wrap variables in a message dictionary '''
	return {'user': user_name, 'group': group, 'message': message, 'time': datetime.now().strftime("%A, %d. %B %Y %I:%M%p")}
	message

def get_messages(group):
	'''
		Should be used by GET request.
		Gets all messages belonging to a group, gives empty array, [], if no group exists

		Arguments: group (string)
	'''
	data = json.load(open(OUTFILE))
	try:
		if data.has_key(group):
			messages = data[group]
			return messages
	except:
		print 'Exception when GETing message'
	return []

def message_to_string(message):
	''' Use this as a toString for a single message. Stringifies the message in a desired format '''
	return "\n%s - %s\n%s\n" % (message['user'], message['time'], message['message'])

def post_message(user_name, group, message_text):
	'''
		Should be used by POST request.
		Gets messages in json.
			If the group exists it appends the new message to the group.
			If the group doesn't exist it creates a new group with the new message.
		Returns True if message saved successfully.
		Returns False if there was an error and message failed to save.

		Arguments: user_name (string), group (string), message_text (string)
	'''
	try:
		message = create_message_wrapper(user_name, group, message_text)
		data = json.load(open(OUTFILE))
		if data.has_key(group):
			data[group].append(message)
		else:
			data[group] = [message]
		with open(OUTFILE, 'w') as json_file:
			json.dump(data, json_file)
		return True
	except:
		print 'Exception when POSTing message'
		return False


if __name__ == '__main__':
	# user_name = 'Joe'
	# group = 'Penn State'
	# message = 'I hate everything :('
	# print post_message(user_name, group, message)
	messages = get_messages('Rutgers')
	for message in messages:
		print message_to_string(message)


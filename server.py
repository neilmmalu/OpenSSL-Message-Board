import socket
import thread
import ssl
from hashlib import sha256
from message import *

HOST = 'localhost'
PORT = 8080

def main():

	# create and get the socket to listen to clients
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(10)

	# wrap socket in the cert
	ssl_s = ssl.wrap_socket(s, certfile = 'domain.crt', keyfile = 'domain.key', server_side = True)
	while True:
		client_socket, client_address = ssl_s.accept()
		print "Received connection from ", client_address

		try:
			print "Server running"
			# spin a new thread for a new client
			thread.start_new_thread(handle, (client_socket,))
		except ssl.SSLError as e:
			print(e)


def handle(conn):
    conn.send('ACK')
    response = conn.recv(1024).decode()
    print(response)
    #Confirmed connection and Synced
    username = conn.recv(1024).decode()
    password = conn.recv(1024).decode()

    success = verify(username, password)

    # verify if the username password combination is right
    if success == 1:
    	conn.send('SUCCESS')
    	# Do stuff with queries here
    	info = queries(conn, username)
    else:
    	conn.send('FAILURE')

    handle(conn)


def verify(username, password):
	file = open('passwords.txt', 'r')
	line = file.readline()
	# line number
	i = 1;
	while line:
		# even lines are passwords 
		if i % 2 == 0:
			line = file.readline()
			i += 1
		else:
			user = line.strip('\n')
			# check if the line has the user 
			if user == username:
				hashed = file.readline().strip('\n')

				# check if passwords match
				if(sha256(password).hexdigest() == hashed):
					# print "Success. Welcome " + username + '\n'
					return 1
				else:
					# print "Wrong password. Please try again\n"
					return 0
			else:
				line = file.readline()
				i += 1

	file.close()

	# create a new user if the username does not exist
	file = open('passwords.txt', 'w')
	new_hash = sha256(password).hexdigest()
	file.write(username+'\n'+new_hash+'\n')
	file.close()
	print "New user added\n"
	return 1

def queries(conn, username):
	conn.send("ACK queries".encode())
	info = conn.recv(1024).decode()

	# info can be END, GET or POST
	while info != 'END':
		info = conn.recv(1024).decode()
		if info == 'END':
			# Logout user but keep the connection
			print "Logging out\n"
			conn.send('END'.encode())
		
		elif info == 'GET':
			conn.send('GET'.encode())
			group = conn.recv(1024).decode()
			# get messages from the JSON file and add them to a buffer
			messages = get_messages(group)
			buff = ""

			if len(messages) == 0:
				buff = "Message board does not exist. Please try again!\n"

			else:
				for i in range(len(messages)):
					buff += message_to_string(messages[i])
			conn.send(buff.encode())

		elif info == 'POST':
			conn.send('POST'.encode())
			group = conn.recv(1024).decode()
			message = conn.recv(4096).decode()

			# post the message to the JSON file 
			post_message(username, group, message)

		else:
			conn.send('ACK'.encode())

	conn.send('END')


if __name__ == '__main__':
	main()

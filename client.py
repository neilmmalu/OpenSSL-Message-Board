import socket
import ssl

HOST = 'localhost'
PORT = 8080

def main():
	s = socket.socket(socket.AF_INET)
	conn = ssl.wrap_socket(s, ca_certs = 'domain.crt')

	try:
		conn.connect((HOST, PORT))
		login(conn)
	finally:
		conn.close()

def login(conn):
	conn.send('SYN'.encode())
	response = conn.recv(1024).decode()

	username = raw_input("Enter username: ")
	password = raw_input("Enter password: ")
	conn.send(username.encode())
	conn.send(password.encode())

	result = conn.recv(1024).decode()
	if result == 'SUCCESS':
		#Success
		info = queries(conn)
	else:
		print "Invalid Login"

	login(conn)

def queries(conn):
	info = conn.recv(1024).decode()
	conn.send('SYN'.encode())

	while info != 'END':
		query = raw_input("Enter a GET, POST or END query:\n")
		conn.send(query)
		info = conn.recv(1024).decode()
		if query == 'END':
			return 'END'
		elif query == 'POST':
			group = raw_input("Name of message board. A new board will be created if it does not exist: ")
			message = raw_input("Enter your message: ")
			conn.send(group.encode())
			conn.send(message.encode())
		elif query == 'GET':
			group = raw_input("What message board would you like to view?: ")
			conn.send(group.encode())
			buff = conn.recv(65536).decode()
			print buff
		else:
			print "Invalid query. Try again\n"

	return 'END'

if __name__ == '__main__':
	main()
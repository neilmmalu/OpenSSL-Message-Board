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
	response = conn.recv(2048).decode()

	username = raw_input("Enter username: ")
	password = raw_input("Enter password: ")
	conn.send(username.encode())
	conn.send(password.encode())

	result = conn.recv(1024).decode()
	if result == 1:
		#Success
		info = 'GET/POST/END'
	else:
		print "Invalid Login"
	if info == 'END':
		conn.close()
		return

	login(conn)

if __name__ == '__main__':
	main()
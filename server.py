import socket
import thread
import ssl

HOST = 'localhost'
PORT = 8080

def main():
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(10)

	while True:
		client_socket, client_address = s.accept()
		print "Received connection from ", client_address

		try:
			conn = ssl.wrap_socket(s, certfile = 'domain.crt', keyfile = 'domain.key', server_side = True)
			print "Server running"
		except ssl.SSLError as e:
			print(e)

if __name__ == '__main__':
	main()
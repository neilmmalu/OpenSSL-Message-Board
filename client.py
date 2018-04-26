import socket
import ssl

HOST = 'localhost'
PORT = 8080

def main():
	s = socket.socket(socket.AF_INET)
	conn = ssl.wrap_socket(s, ca_certs = 'domain.crt')

	try:
		conn.connect((HOST, PORT))
	finally:
		conn.close()

if __name__ == '__main__':
	main()
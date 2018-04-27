import socket
import thread
import ssl
from hashlib import sha256

HOST = 'localhost'
PORT = 8080

def main():
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(10)

	ssl_s = ssl.wrap_socket(s, certfile = 'domain.crt', keyfile = 'domain.key', server_side = True)
	while True:
		client_socket, client_address = ssl_s.accept()
		print "Received connection from ", client_address

		try:
			print "Server running"
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
    if success == 1:
    	conn.send('SUCCESS')
    	# Do stuff with queries here
    else:
    	conn.send('FAILURE')

    if data == 'QUIT':
    	return
    else:
    	handle(conn)


def verify(username, password):
	file = open('passwords.txt', 'r')
	line = file.readline()
	i = 1;
	while line:
		if i % 2 == 0:
			line = file.readline()
			i += 1
		else:
			user = line.strip('\n')
			if user == username:
				hashed = file.readline().strip('\n')
				if(sha256(password).hexdigest() == hashed):
					print "Success" + username
					return 1
				else:
					print "Wrong password. Please try again"
					return 0
			else:
				line = file.readline()
				i += 1

	file.close()
	file = open('passwords.txt', 'w')
	new_hash = sha256(password).hexdigest()
	file.write(username+'\n'+new_hash+'\n')
	file.close()
	print "New user added"
	return 1



if __name__ == '__main__':
	main()

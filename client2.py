# Import socket module
import socket
import ssl


def Main():
    # local host IP '127.0.0.1'
    host = 'localhost'

    # Define the port on which you want to connect
    port = 3001

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Wrapping socket in ssl
    ssl_sock = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED, ca_certs='domain.crt')

    # connect to server on local computer
    ssl_sock.connect((host,port))

    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:

        # message sent to server
        ssl_sock.send(message.encode('ascii'))

        # messaga received from server
        data = ssl_sock.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = raw_input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()

if __name__ == '__main__':
    Main()

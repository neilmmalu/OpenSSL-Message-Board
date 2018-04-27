# import socket programming library
import socket

# import thread module
from thread import *
import threading
import ssl

print_lock = threading.Lock()

# thread fuction
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]
        print "Received %s" % str(data.decode('ascii'))

        # send back reversed string to client
        c.send(data)

    # connection closed
    c.close()


def Main():
    host = "localhost"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 3001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    # s_ssl = s
    s_ssl = ssl.wrap_socket(s, keyfile='domain.key', certfile='domain.crt', server_side=True)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s_ssl.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])


        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()

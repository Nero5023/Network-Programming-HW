import socket

HOST = "127.0.0.1"
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = raw_input()
    s.sendto(message, (HOST, PORT))
    print(s.recv(1024))

s.close()
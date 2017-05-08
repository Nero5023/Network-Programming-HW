#coding:utf-8

import socket
HOST = 'localhost'
PORT = 8080

while True:
    temp = raw_input("input> ")
    if temp == 'exit':
        break
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(temp)
    data = s.recv(1024)
    print "Got from server: '%s'" % (data,)
    s.close()

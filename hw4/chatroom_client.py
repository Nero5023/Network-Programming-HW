#coding:utf-8

import socket
import select

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

userName = raw_input("Please enter your name: ")
sock.connect((HOST, PORT))
while True:
    
    data = raw_input("> ")
    data = userName + ": " + data
    sock.send(data)


    
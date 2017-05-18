#coding:utf-8

import socket
import select
import sys

HOST = 'localhost'
PORT = 8080

inputFS = [sys.stdin]
s = None
while True:
    infs, outfs, excs = select.select(inputFS, [], [])
    for x in infs:
        if x is sys.stdin:
            data = sys.stdin.readline()
            if data[-1] == '\n':
                data = data[:len(data)-1]
            s = socket.socket()
            s.connect((HOST, PORT))
            s.send(data)
            inputFS.append(s)
        if x is s:
            s.recv(1024)
            print "Got from server: '%s'" % (data,)
            s.close()
            inputFS.remove(s)
            s = None




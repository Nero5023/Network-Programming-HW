#coding:utf-8

import socket
import time
import select

PORT = 8080

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
sock.listen(5)

inputSockets = [sock]

while True:
    rlist, _, _ = select.select(inputSockets, [], [])

    for s in rlist:
        if s == sock:
            conn, addr = s.accept()
            print "Got connecting from ", addr
            inputSockets.append(conn)
        else:
            try:
                data = s.recv(1024)
                disconnected = not data
            except socket.error:
                disconnected = True
            if disconnected:
                print s.getpeername(), 'disconnected'
                inputSockets.remove(s)
            else:
                print 'receive %s from %s' %(data, s.getpeername())

    # print "Waiting for connecting..."
    # thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # try:
    #     conn, addr = sock.accept()
    #     buf = conn.recv(1024)
    #     if not buf:
    #         print "None"
    #         break
    #     print thistime + ' receive from %s:' %(str(addr)) + buf
    #     conn.send(thistime + ' you [%s] say:'%(str(addr)) + buf)
    # except socket.error:
    #     print "time out!"
    # conn.close()





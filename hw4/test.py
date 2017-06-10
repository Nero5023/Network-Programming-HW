import select
import sys
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print sys.stdin
while True:
    ins, outs, excs = select.select([sys.stdin], [], [])
    # print ins
    for x in ins:
        print x
        print type(x)
        print sock
        print type(sock)
        data = sys.stdin.readline()
        print data
        if x is sys.stdin:
            print "Yeah"
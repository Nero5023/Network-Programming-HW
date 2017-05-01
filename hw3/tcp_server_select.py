import socket
import select

HOST = ''
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

inSocks  = [sock]
outSocks = []

data = {}
adrs = {}

try:
    while True:
        ins, outs, excs = select.select(inSocks, outSocks, [])
        for x in ins:
            if x is sock:
                newSocket, addr = sock.accept()
                print "Got connecting from ", addr
                inSocks.append(newSocket)
                adrs[newSocket] = addr
            else:
                newdata = x.recv(1024)
                if newdata:
                    print "%d bytes from %s" % (len(newdata), adrs[x])
                    data[x] = data.get(x, "") + newdata
                    if x not in outSocks:
                        outSocks.append(x)
                else:
                    print "disconnected from", adrs[x]
                    del adrs[x]
                    try:
                        outSocks.remove(x)
                    except ValueError:
                        pass
                    x.close()

        for x in outs:
            tosend = data.get(x)
            if tosend:
                nsent = x.send(tosend)
                print "%d bytes to %s" % (nsent, adrs[x])
                tosend = tosend[nsent:]
            if tosend:
                print "%d bytes remain for %s" % (len(tosend), adrs[x])
                data[x] = tosend
            else:
                try:
                    del data[x]
                except KeyError:
                    pass
                outSocks.remove(x)
                print "No data currently remain for", adrs[x]
finally:
    sock.close()
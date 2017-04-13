import socket
from Parser import Parser

HOST = "127.0.0.1"
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print("Start server")
receivedStr = ""
while True:
    data, addr = s.recvfrom(1024)
    print("Receive from %s:%s" % (addr, data))
    if data == "wc":
        p = Parser()
        wcRes = p.parse(receivedStr)
        s.sendto(str(wcRes), addr)
    else:
        receivedStr += " "
        receivedStr += data
        s.sendto("Hello, %s, you send %s" % (addr, data), addr)

s.close()
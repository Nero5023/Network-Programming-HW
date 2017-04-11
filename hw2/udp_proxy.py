import socket

BIND_ADDR = ("127.0.0.1", 8000)
DST_ADDR  = ("127.0.0.1", 8080)

sockRev  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockRev.bind(BIND_ADDR)

print("Start proxy server")
while True:
    # get data from client
    data, addr = sockRev.recvfrom(1024)
    print("Proxy receive from %s" % (addr, ))
    # send data to server
    sockSend.sendto(data, DST_ADDR)
    print("Proxy send data to server: %s" % (DST_ADDR,))
    # get data from server
    backdata, _ =  sockSend.recvfrom(1024)
    print("Proxy get data from server")
    # send back to client
    sockRev.sendto(backdata, addr)
    print("Proxy send the data received from server to client")
    print("--------------------------")


sockRev.close()
sockSend.close()
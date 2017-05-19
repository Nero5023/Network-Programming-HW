#coding:utf-8

import socket
import select
import json
HOST = ''
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

inSocks  = [sock]
outSocks = []
registerSocks = set()

data = {}
adrs = {}


userInfos = {}

aliveUsers = {}

# return Bool
def saveRegisterInfo(username, password):
    if userInfos.get(username) is not None:
        return False
    userInfos[username] = password
    return True


def register(sock, registerSocks, recvData):
    try:
        jdata = json.loads(recvData)
    except ValueError:
        reponse = json.dumps({'res':0})
        sock.sendall(reponse)
    else:
        username = jdata.get('username')
        password = jdata.get('password')
        reponse = ""
        if username is None or password is None:
            reponse = json.dumps({'res':0})
        else:
            res = saveRegisterInfo(username, password)
            reponse = json.dumps({'res': res})
            if res == True:
                registerSocks.remove(sock)
                aliveUsers[sock] = username
                print "User: %s register successed" % (username, )
        sock.sendall(reponse)


print "Start Select Server..."
try:
    while True:
        ins, outs, excs = select.select(inSocks, outSocks, [])
        for x in ins:

            if x is sock:   # 有新的连接
                newSocket, addr = sock.accept()
                print "Got connecting from ", addr
                inSocks.append(newSocket)
                registerSocks.add(newSocket)
                adrs[newSocket] = addr
            else:          # 有新的数据到来
                newdata = x.recv(1024)
                if x in registerSocks:
                    register(x, registerSocks, newdata)
                    continue
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
                    inSocks.remove(x)
        # 进行写操作
        for x in outs:  
            # tosend = data.get(x)
            # if tosend:
            #     nsent = x.send(tosend)
            #     print "%d bytes to %s" % (nsent, adrs[x])
            #     tosend = tosend[nsent:]
            # if tosend:
            #     print "%d bytes remain for %s" % (len(tosend), adrs[x])
            #     data[x] = tosend
            # else:
            #     try:
            #         del data[x]
            #     except KeyError:
            #         pass
            #     outSocks.remove(x)
            #     print "No data currently remain for", adrs[x]
            if tosend:
                dic = {
                    "username": aliveUsers.get(x),
                    "data"    : tosend}
                dataToSend = json.dumps(dic)
                x.sendall(dataToSend)
finally:
    sock.close()
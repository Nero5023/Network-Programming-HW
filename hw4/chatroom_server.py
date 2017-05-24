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

sockToUserName = {}

# return Bool
def saveRegisterInfo(username, password):
    if userInfos.get(username) is not None:
        return False
    userInfos[username] = password
    return True

def sendDataToSockExcept(data, exSock, allInSocks):
    for s in allInSocks:
        if s is not exSock and s is not sock:
            s.sendall(data)

def login(username, password):
    if userInfos[username] == password:
        return True
    return False

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
            res = False
            if username in userInfos and username not in aliveUsers:
                res = login(username, password)
                if res == True:
                    aliveUsers[username] = sock
                    sockToUserName[sock] = username
                    print "User: %s login successed" % (username, )
            if username not in userInfos:
                res = saveRegisterInfo(username, password)
                if res == True:
                    registerSocks.remove(sock)
                    aliveUsers[username] = sock
                    sockToUserName[sock] = username
                    print "User: %s register successed" % (username, )
            reponse = json.dumps({'res': res})
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
                    print "%d bytes forrom %s" % (len(newdata), adrs[x])
                    data[x] = data.get(x, "") + newdata
                    if x not in outSocks:
                        outSocks.append(x)
                else:
                    print "disconnected from", adrs[x]
                    del adrs[x]
                    del aliveUsers[sockToUserName[x]]
                    del sockToUserName[x]
                    try:
                        outSocks.remove(x)
                    except ValueError:
                        pass
                    x.close()
                    inSocks.remove(x)
        # 进行写操作
        for x in outs:  
            tosend = data.get(x)
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
                    "username": sockToUserName.get(x),
                    "data"    : tosend}
                dataToSend = json.dumps(dic)
                # x.sendall(dataToSend)
                sendDataToSockExcept(dataToSend, x, inSocks)
                data[x] = None
            else:
                try:
                    del data[x]
                except KeyError:
                    pass
                outSocks.remove(x)
finally:
    sock.close()